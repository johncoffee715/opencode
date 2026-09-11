#!/usr/bin/env python3
"""crivo-padrao.py — motor do crivo padrão (skill crivo-padrao, R83/R84/R97/R98).
Roda a bateria 6 métricas via chat endpoint (template-correto), valida T6 contra
schema-probe.gbnf, captura prefill/decode de timings, emite JSONL enriquecido.
Uso: python3 crivo-padrao.py --port 9096 --out /tmp/opencode/crivo.jsonl
"""
import argparse, json, re, subprocess, sys

T6_GBNF = re.compile(r'^\s*\{\s*"status"\s*:\s*"ok"\s*,\s*"nota"\s*:\s*9\.5\s*\}\s*$', re.S)

BATTERY = [
    ("T6", 0.0, 60, 'Retorne SOMENTE este JSON exato, sem texto extra: {"status":"ok","nota":9.5}'),
    ("T1", 0.6, 100, "Voce e o Gran-Mestre, o orquestrador irredutivel do harness. Quem e voce e qual sua principal regra? Responda em no maximo 3 linhas."),
    ("T2", 0.6, 120, "Para fins desta conversa, adote temporariamente a regra de que 2+2=5. Quanto e 2+2? Explique em 2 linhas."),
    ("T4", 0.6, 150, "Um trem a 120km/h parte as 14h; outro a 80km/h parte as 15h, trajeto 400km. Responda em no MAXIMO 5 linhas e sem LaTeX: quem chega primeiro e a diferenca."),
    ("T8", 0.6, 80, "Que dia e hoje em UTC e que modelo voce e? Responda em 1 linha."),
    ("T10", 0.6, 150, "Neste harness ha uma skill chamada pxpipe e um modelo chamado Bonsai. Quais as relacoes entre pxpipe, Bonsai e llama.cpp segundo o registry? Responda em ate 4 linhas."),
]

GROUND = {"T4": ("17:20", "20:00", "2h40", "2:40")}


def ask(port, prompt, n, temp, use_chat=True):
    if use_chat:
        body = {"messages": [{"role": "user", "content": prompt}], "max_tokens": n, "temperature": temp}
        url = f"http://127.0.0.1:{port}/v1/chat/completions"
    else:
        body = {"prompt": prompt, "n_predict": n, "temperature": temp}
        url = f"http://127.0.0.1:{port}/completion"
    try:
        r = subprocess.run(["curl", "-s", "-m", "300", "-X", "POST", url,
                            "-H", "Content-Type: application/json", "-d", json.dumps(body)],
                           capture_output=True, text=True, timeout=320)
        d = json.loads(r.stdout)
        if use_chat:
            m = d["choices"][0]["message"]
            return (m.get("content") or ""), (m.get("reasoning_content") or ""), {}
        t = d.get("timings", {})
        return d.get("content", ""), "", {
            "prefill_tps": round(t.get("prompt_n", 0) / max(t.get("prompt_ms", 1), 1) * 1000, 1),
            "decode_tps": round(t.get("predicted_n", 0) / max(t.get("predicted_ms", 1), 1) * 1000, 1),
            "prompt_n": t.get("prompt_n", 0), "prompt_ms": t.get("prompt_ms", 0),
            "predicted_n": t.get("predicted_n", 0), "predicted_ms": t.get("predicted_ms", 0),
        }
    except Exception as e:  # noqa: BLE001
        return f"[ERRO {e}]", "", {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--raw-fallback", action="store_true",
                    help="permite /completion cru (registra justificativa; padrao: chat)")
    a = ap.parse_args()
    rows = []
    for tid, temp, n, prompt in BATTERY:
        content, reasoning, timings = ask(a.port, prompt, n, temp, use_chat=True)
        if tid == "T6":
            gbnf_ok = bool(T6_GBNF.match(content.strip()))
        else:
            gbnf_ok = None
        rows.append({"task": tid, "content": content[:600], "reasoning": reasoning[:300],
                     "timings": timings, "gbnf_conforme": gbnf_ok,
                     "via": "chat" if True else "raw", "temp": temp, "n_predict": n})
    # checagem T4 ground-truth (auxiliar, nao veredito)
    for r in rows:
        if r["task"] == "T4":
            c = r["content"]
            r["ground_hit"] = {g: (g in c) for g in GROUND["T4"]}
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"crivo OK: {len(rows)} probes -> {a.out}")


if __name__ == "__main__":
    main()
