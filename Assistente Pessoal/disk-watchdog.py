#!/usr/bin/env python3
"""Disk Watchdog - Sistema de Monitoramento de Disco e Limpeza Automática (Versão sem dependências externas)"""

import os
import sys
import json
import time
import shutil
import subprocess
import logging
import threading
import signal
import fcntl
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/disk-watchdog.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DiskWatchdog')

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disk-watchdog.json')
ALERT_FILE = '/tmp/disk-alerts.json'
PID_FILE = '/tmp/disk-watchdog.pid'

class DiskWatchdogConfig:
    def __init__(self, config_path=CONFIG_FILE):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        default_config = {
            "watchdog": {"check_interval_seconds": 300},
            "disk_monitoring": {
                "warning_threshold_percent": 75,
                "critical_threshold_percent": 85,
                "emergency_threshold_percent": 95
            },
            "snapshot_policies": {"max_snapshots_per_dir": 2, "cleanup_on_violation": True},
            "database_policies": {"max_sqlite_size_mb": 1024, "vacuum_threshold_mb": 512},
            "git_policies": {"auto_gc_days": 7, "gc_aggressive": False, "prune_now": True},
            "alerts": {"enabled": True, "methods": ["log", "file"]}
        }
        if not os.path.exists(self.config_path):
            self.save_config(default_config)
            return default_config
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return default_config

    def save_config(self, config):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except:
            return default

class DiskSpaceMonitor:
    def __init__(self, config):
        self.config = config
        self.alerts = []
        self.running = True
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        logger.info("Received shutdown signal")
        self.running = False

    def get_disk_usage(self, path='/'):
        try:
            stat = shutil.disk_usage(path)
            total = stat.total / (1024**3)
            used = stat.used / (1024**3)
            percent = (stat.used / stat.total) * 100
            return {
                'path': path,
                'total_gb': round(total, 2),
                'used_gb': round(used, 2),
                'free_gb': round(stat.free / (1024**3), 2),
                'percent': round(percent, 1)
            }
        except Exception as e:
            logger.error(f"Error getting disk usage for {path}: {e}")
            return None

    def check_disk_thresholds(self, disk_info):
        if not disk_info:
            return
        thresholds = self.config.get('disk_monitoring', {})
        warning = thresholds.get('warning_threshold_percent', 75)
        critical = thresholds.get('critical_threshold_percent', 85)
        emergency = thresholds.get('emergency_threshold_percent', 95)
        percent = disk_info['percent']

        if percent >= emergency:
            self.trigger_alert('EMERGENCY', f"Disk at {percent}% - Immediate action required!")
            self.emergency_cleanup()
        elif percent >= critical:
            self.trigger_alert('CRITICAL', f"Disk at {percent}% - Critical level reached")
            self.perform_cleanup()
        elif percent >= warning:
            self.trigger_alert('WARNING', f"Disk at {percent}% - Warning threshold exceeded")

    def trigger_alert(self, level, message):
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'disk_info': self.get_disk_usage('/mnt/dados')
        }
        self.alerts.append(alert)
        logger.log(
            logging.CRITICAL if level == 'EMERGENCY' else
            logging.ERROR if level == 'CRITICAL' else
            logging.WARNING,
            f"[{level}] {message}"
        )
        self.save_alerts()

    def save_alerts(self):
        try:
            with open(ALERT_FILE, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save alerts: {e}")

    def emergency_cleanup(self):
        logger.critical("EMERGENCY CLEANUP INITIATED")
        paths = [
            "/mnt/dados/Assistente Pessoal/opencode/data/opencode/snapshot",
            "/mnt/dados/Assistente Pessoal/opencode/cache",
            "/mnt/dados/Assistente Pessoal/opencode/data/opencode/tool-output"
        ]
        for path in paths:
            if os.path.exists(path):
                self.clean_directory(path)

    def perform_cleanup(self):
        logger.warning("PERFORMING CLEANUP")
        self.cleanup_snapshots()
        self.cleanup_cache()
        self.cleanup_temp_files()
        self.cleanup_git()
        self.check_sqlite_dbs()

    def cleanup_snapshots(self):
        snapshot_dirs = self.config.get('snapshot_policies', {}).get(
            'snapshot_dirs',
            ['/mnt/dados/Assistente Pessoal/opencode/data/opencode/snapshot']
        )
        max_snapshots = self.config.get('snapshot_policies', {}).get('max_snapshots_per_dir', 2)
        cleanup_on_violation = self.config.get('snapshot_policies', {}).get('cleanup_on_violation', True)

        for snap_dir in snapshot_dirs:
            if not os.path.exists(snap_dir):
                continue
            snapshots = sorted(Path(snap_dir).iterdir(), key=os.path.getmtime, reverse=True)
            if len(snapshots) > max_snapshots:
                to_remove = snapshots[max_snapshots:]
                logger.info(f"Removing {len(to_remove)} snapshots from {snap_dir}")
                for snap in to_remove:
                    snap_path = str(snap)
                    size = self.get_dir_size(snap_path)
                    if os.path.isdir(snap_path):
                        shutil.rmtree(snap_path)
                    else:
                        os.remove(snap_path)
                    logger.info(f"Removed {snap_path} ({self.bytes_to_human(size)})")
                    self.trigger_alert('SNAPSHOT_REMOVED', f"Removed {snap_path} ({self.bytes_to_human(size)})")

    def cleanup_cache(self):
        cache_dirs = self.config.get('cache_policies', {}).get(
            'cache_dirs',
            ['/mnt/dados/Assistente Pessoal/opencode/cache']
        )
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                self.clean_directory(cache_dir)
                logger.info(f"Cleaned cache directory: {cache_dir}")

    def clean_directory(self, dir_path):
        try:
            for item in Path(dir_path).iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(str(item))
                    else:
                        item.unlink()
                    logger.debug(f"Removed {item}")
                except Exception as e:
                    logger.error(f"Failed to remove {item}: {e}")
        except Exception as e:
            logger.error(f"Failed to clean directory {dir_path}: {e}")

    def cleanup_temp_files(self):
        logger.info("Cleaning temporary files")
        try:
            pack_dir = Path("/mnt/dados/.git/objects/pack")
            if pack_dir.exists():
                import time as _time
                now = _time.time()
                for f in pack_dir.glob("tmp_pack_*"):
                    try:
                        # R92-fix: NAO apagar tmp_pack de pack-objects vivo (idade < 30min)
                        if now - f.stat().st_mtime < 1800:
                            continue
                        if f.is_dir():
                            shutil.rmtree(str(f))
                        else:
                            f.unlink()
                    except:
                        pass
            tmp_dir = Path("/tmp")
            if tmp_dir.exists():
                for f in tmp_dir.glob("*.tmp"):
                    try:
                        f.unlink()
                    except:
                        pass
                for f in tmp_dir.glob("*~"):
                    try:
                        f.unlink()
                    except:
                        pass
        except Exception as e:
            logger.error(f"Error in cleanup_temp_files: {e}")

    def cleanup_git(self):
        if not self.config.get('git_policies', {}).get('enabled', True):
            logger.info("Git gc disabled via config (git_policies.enabled=false)")
            return
        git_dirs = self.config.get('git_policies', {}).get(
            'git_dirs',
            ['/mnt/dados/.git', '/mnt/dados/Assistente Pessoal/opencode']
        )
        prune_now = self.config.get('git_policies', {}).get('prune_now', True)

        for git_dir in git_dirs:
            if not os.path.exists(git_dir):
                continue
            logger.info(f"Running git gc on {git_dir}")
            try:
                cmd = ['git', '-C', git_dir, 'gc', '--prune=now']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    logger.info(f"Git gc successful for {git_dir}")
                else:
                    logger.error(f"Git gc failed for {git_dir}: {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.error(f"Git gc timed out for {git_dir}")
            except Exception as e:
                logger.error(f"Failed to run git gc on {git_dir}: {e}")

    def check_sqlite_dbs(self):
        db_paths = self.config.get('database_policies', {}).get('db_paths', [])
        max_size_mb = self.config.get('database_policies', {}).get('max_sqlite_size_mb', 1024)
        vacuum_threshold_mb = self.config.get('database_policies', {}).get('vacuum_threshold_mb', 512)

        for db_path in db_paths:
            if not os.path.exists(db_path):
                continue
            size_mb = os.path.getsize(db_path) / (1024**2)
            if size_mb > max_size_mb:
                logger.warning(f"Database {db_path} is {size_mb:.0f}MB, exceeding {max_size_mb}MB limit")
                self.vacuum_sqlite(db_path)
            elif size_mb > vacuum_threshold_mb:
                logger.info(f"Database {db_path} at {size_mb:.0f}MB, scheduling vacuum")

    def vacuum_sqlite(self, db_path):
        logger.info(f"VACUUM on {db_path}")
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("VACUUM")
            conn.close()
            new_size = os.path.getsize(db_path) / (1024**2)
            logger.info(f"Database vacuumed: {new_size:.0f}MB")
        except Exception as e:
            logger.error(f"Failed to vacuum {db_path}: {e}")

    def get_dir_size(self, path):
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total += os.path.getsize(fp)
        except:
            pass
        return total

    def bytes_to_human(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} PB"

    def run_full_check(self):
        logger.info("=" * 50)
        logger.info("FULL DISK CHECK INITIATED")
        logger.info("=" * 50)
        disk_info = self.get_disk_usage('/mnt/dados')
        if disk_info:
            logger.info(f"Disk usage: {disk_info['percent']}% ({disk_info['used_gb']}GB used of {disk_info['total_gb']}GB)")
            self.check_disk_thresholds(disk_info)
        else:
            logger.error("Failed to get disk usage")

        self.cleanup_snapshots()
        self.cleanup_cache()
        self.check_sqlite_dbs()
        self.cleanup_git()
        self.cleanup_temp_files()
        logger.info("FULL DISK CHECK COMPLETE")

    def run_daemon(self):
        # Write PID file
        try:
            with open(PID_FILE, 'w') as f:
                f.write(str(os.getpid()))
            fcntl.flock(PID_FILE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            logger.warning("Could not acquire lock on PID file")

        interval = self.config.get('watchdog.check_interval_seconds', 300)
        logger.info(f"Starting watchdog daemon (check interval: {interval}s)")

        self.run_full_check()

        while self.running:
            try:
                time.sleep(interval)
                if self.running:
                    self.run_full_check()
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)

        # Cleanup
        try:
            os.remove(PID_FILE)
        except:
            pass
        logger.info("Watchdog stopped")

def main():
    # Check if already running
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Check if process exists
            logger.error(f"Watchdog already running (PID: {pid})")
            sys.exit(1)
        except:
            pass  # Stale PID file

    watchdog = DiskSpaceMonitor(DiskWatchdogConfig())
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        watchdog.run_daemon()
    else:
        watchdog.run_full_check()

if __name__ == '__main__':
    main()