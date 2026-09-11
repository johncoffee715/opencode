// carrossel-fundo v1.2 — forja cloud-direct (R93) + via autoral AnuPpuccin (Hefesto).
// Instalacao: esta pasta ja esta em <vault>/.obsidian/plugins/carrossel-fundo/.
// No Obsidian: Configuracoes → Plugins da comunidade → ativar "Carrossel Fundo".
// Requer "Plugins da comunidade" desbloqueado. Sem build: JS puro, API estavel do Obsidian.
// Compativel com o snippet legado fundo.css: alimenta --fundo-aleatorio-atual + --carrossel-bg.
const { Plugin, PluginSettingTab, Setting, Notice } = require("obsidian");

const DEFAULTS = {
  pastaImagens: "ImagensFundo",
  intervaloSeg: 20,
  avancarAoAbrirNota: true,
  reagirACriacao: true,
  opacidadeVeu: 0.55,
};
const EXT_IMG = /\.(png|jpe?g|gif|webp|avif|bmp|svg)$/i;
// Via autoral (v1.2, Hefesto): a tinta mora no fundo.css (custom-background do
// AnuPpuccin, AnubisNekhet). O plugin so pilota as variaveis dele + a classe.
const VAR_BG_AUTOR = "--anp-background-image";
const VAR_BRILHO_AUTOR = "--anp-custom-bg-brightness";
const CLASSE_TOGGLE_AUTOR = "anp-background-image-toggle";

module.exports = class CarrosselFundo extends Plugin {
  async onload() {
    this.settings = Object.assign({}, DEFAULTS, await this.loadData());
    this.imagens = [];
    this.indice = -1;
    this.timer = null;
    this.pausado = false;

    // try cobre TODO o init (GAP-4/Hefesto): falha vira Notice + log, nunca silencio.
    try {
    this.injetarEstilo();
    this.statusEl = this.addStatusBarItem();
    this.statusEl.classList.add("carrossel-fundo-status");
    this.statusEl.setAttribute("title", "Carrossel fundo — clique para a proxima imagem");
    this.statusEl.addEventListener("click", () => this.proxima(true));

    // (protegido pelo try aberto acima.)
    this.aplicarBrilho();
    await this.reindexar(false);
    this.mostrar(this.imagens.length > 0 ? 0 : -1);
    this.iniciarTimer();

    this.registerEvent(this.app.vault.on("create", (f) => this.aoCriar(f)));
    this.registerEvent(this.app.vault.on("delete", () => this.reindexar(true)));
    this.registerEvent(this.app.vault.on("rename", () => this.reindexar(true)));
    this.registerEvent(this.app.workspace.on("file-open", (f) => this.aoAbrir(f)));

    this.addCommand({ id: "proxima", name: "Carrossel fundo: proxima imagem", callback: () => this.proxima(true) });
    this.addCommand({ id: "anterior", name: "Carrossel fundo: imagem anterior", callback: () => this.anterior() });
    this.addCommand({ id: "pausar-retomar", name: "Carrossel fundo: pausar/retomar", callback: () => this.alternarPausa() });
    this.addCommand({ id: "reembaralhar", name: "Carrossel fundo: reembaralhar", callback: () => this.reembaralhar() });

    this.addSettingTab(new CarrosselTab(this.app, this));
    console.log("[carrossel-fundo] ativo: " + this.imagens.length + " imagem(ns) em '" + this.settings.pastaImagens + "'");
    } catch (e) {
      console.error("[carrossel-fundo] falha no onload:", e);
      new Notice("Carrossel fundo: falha ao iniciar (" + (e && e.message ? e.message : e) + "). Abra o console (Ctrl+Shift+I).");
    }
  }

  onunload() {
    if (this.timer) window.clearInterval(this.timer);
    const st = document.body.style;
    st.removeProperty(VAR_BG_AUTOR);
    st.removeProperty(VAR_BRILHO_AUTOR);
    st.removeProperty("--carrossel-bg");
    st.removeProperty("--fundo-aleatorio-atual");
    document.body.classList.remove(CLASSE_TOGGLE_AUTOR);
  }

  // —— indice ——
  async reindexar(manterPosicao) {
    const pasta = (this.settings.pastaImagens || "ImagensFundo").replace(/\/+$/, "");
    const atual = this.imagens[this.indice] ? this.imagens[this.indice].path : null;
    this.imagens = this.app.vault
      .getFiles()
      .filter((f) => f.path === pasta || f.path.startsWith(pasta + "/"))
      .filter((f) => EXT_IMG.test(f.name))
      .sort((a, b) => a.path.localeCompare(b.path));
    if (this.imagens.length === 0) { this.mostrar(-1); return; }
    if (manterPosicao && atual) {
      const i = this.imagens.findIndex((f) => f.path === atual);
      this.mostrar(i >= 0 ? i : 0);
    } else if (this.indice < 0 || this.indice >= this.imagens.length) {
      this.mostrar(0);
    } else {
      this.atualizarStatus();
    }
  }

  mostrar(i) {
    const st = document.body.style;
    if (this.imagens.length === 0 || i < 0) {
      this.indice = -1;
      st.removeProperty(VAR_BG_AUTOR);
      st.removeProperty("--carrossel-bg");
      st.removeProperty("--fundo-aleatorio-atual");
      if (this.statusEl) this.statusEl.setText("🖼 sem imagens");
      return;
    }
    this.indice = ((i % this.imagens.length) + this.imagens.length) % this.imagens.length;
    const url = this.app.vault.getResourcePath(this.imagens[this.indice]);
    const cssUrl = 'url("' + url + '")';
    st.setProperty(VAR_BG_AUTOR, cssUrl); // pinta via fundo.css (mecanismo AnuPpuccin)
    st.setProperty("--carrossel-bg", cssUrl); // compat
    st.setProperty("--fundo-aleatorio-atual", cssUrl); // compat snippet legado
    this.verificarImagem(url);
    this.atualizarStatus();
  }

  injetarEstilo() {
    // Garante o caminho de tinta autoral: classe no body (o CSS do fundo.css faz o resto).
    document.body.classList.add(CLASSE_TOGGLE_AUTOR);
    console.log("[carrossel-fundo] via autoral ativa (.app-container pinta).");
  }

  verificarImagem(url) {
    // Autodiagnostico (v1.1): se a URL nao carregar, o proprio plugin avisa em tela.
    try {
      const img = new Image();
      img.onload = () => console.log("[carrossel-fundo] imagem ok.");
      img.onerror = () => {
        console.error("[carrossel-fundo] imagem NAO carregou: " + url);
        new Notice("Carrossel fundo: a imagem não carregou (console tem o detalhe). Gradiente mantido.");
      };
      img.src = url;
    } catch (e) { console.error("[carrossel-fundo] preload indisponivel:", e); }
  }

  atualizarStatus() {
    if (this.statusEl) {
      this.statusEl.setText(this.indice < 0 ? "🖼 —" : "🖼 " + (this.indice + 1) + "/" + this.imagens.length + (this.pausado ? " ⏸" : ""));
    }
  }

  proxima(manual) { if (!this.imagens.length) return; if (manual && this.pausado) { this.mostrar(this.indice + 1); return; } this.mostrar(this.indice + 1); }
  anterior() { if (this.imagens.length) this.mostrar(this.indice - 1); }
  aleatoria() {
    if (!this.imagens.length) return;
    if (this.imagens.length === 1) { this.mostrar(0); return; }
    let n = this.indice;
    while (n === this.indice) n = Math.floor(Math.random() * this.imagens.length);
    this.mostrar(n);
  }
  reembaralhar() {
    for (let i = this.imagens.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = this.imagens[i]; this.imagens[i] = this.imagens[j]; this.imagens[j] = t;
    }
    this.mostrar(0);
  }
  alternarPausa() { this.pausado = !this.pausado; this.atualizarStatus(); }

  iniciarTimer() {
    if (this.timer) window.clearInterval(this.timer);
    const seg = Math.max(5, Number(this.settings.intervaloSeg) || 20);
    this.timer = window.setInterval(() => { if (!this.pausado) this.mostrar(this.indice + 1); }, seg * 1000);
    this.registerInterval(this.timer);
  }

  aplicarBrilho() {
    // Veu (0..0.9) vira brilho autoral (1..0.1): 0.55 -> 0.45 (~padrao 0.5 do autor).
    const b = Math.round((1 - Number(this.settings.opacidadeVeu)) * 100) / 100;
    document.body.style.setProperty(VAR_BRILHO_AUTOR, String(b));
  }

  ehPasta(f) { return !!f && f.children !== undefined; }
  dentroDaPasta(f) {
    const pasta = (this.settings.pastaImagens || "ImagensFundo").replace(/\/+$/, "");
    return f && (f.path === pasta || f.path.startsWith(pasta + "/"));
  }

  // —— reatividade (o pedido: clicar em outra path, criar pasta, criar anotacao) ——
  aoAbrir(f) {
    if (!f || f.extension !== "md") return;
    if (this.settings.avancarAoAbrirNota && !this.pausado) this.proxima(false);
  }

  aoCriar(f) {
    if (!f) return;
    if (this.ehPasta(f)) {
      // Nova pasta (qualquer lugar): reembaralha o carrossel.
      if (this.settings.reagirACriacao) this.reembaralhar();
      else this.reindexar(true);
      return;
    }
    if (f.extension === "md" && this.settings.reagirACriacao) {
      // Nova anotacao: salto aleatorio.
      this.aleatoria();
      return;
    }
    if (EXT_IMG.test(f.name || "") && this.dentroDaPasta(f)) {
      // Nova imagem na pasta: entra na rotacao e exibe.
      this.reindexar(false);
      const i = this.imagens.findIndex((x) => x.path === f.path);
      this.mostrar(i >= 0 ? i : 0);
      return;
    }
    this.reindexar(true);
  }
};

class CarrosselTab extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }
  display() {
    const { containerEl } = this;
    const p = this.plugin;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Carrossel Fundo" });
    new Setting(containerEl)
      .setName("Pasta das imagens")
      .setDesc("Caminho da pasta dentro do vault (ex.: ImagensFundo).")
      .addText((t) => t.setValue(p.settings.pastaImagens)
        .onChange(async (v) => { p.settings.pastaImagens = v.trim() || "ImagensFundo"; await p.saveData(); await p.reindexar(false); }));
    new Setting(containerEl)
      .setName("Intervalo do carrossel (segundos)")
      .setDesc("Troca automatica. Minimo 5.")
      .addText((t) => t.setValue(String(p.settings.intervaloSeg))
        .onChange(async (v) => { p.settings.intervaloSeg = Math.max(5, Number(v) || 20); await p.saveData(); p.iniciarTimer(); }));
    new Setting(containerEl)
      .setName("Avancar ao abrir nota")
      .setDesc("Clicar em outra nota/pasta com markdown troca o fundo.")
      .addToggle((t) => t.setValue(p.settings.avancarAoAbrirNota)
        .onChange(async (v) => { p.settings.avancarAoAbrirNota = v; await p.saveData(); }));
    new Setting(containerEl)
      .setName("Reagir a criacoes")
      .setDesc("Nova pasta embaralha; nova anotacao salta p/ imagem aleatoria.")
      .addToggle((t) => t.setValue(p.settings.reagirACriacao)
        .onChange(async (v) => { p.settings.reagirACriacao = v; await p.saveData(); }));
    // (pan removido na v1.2: a tinta e autoral; o "animado" e a rotacao por tempo/eventos.)
    new Setting(containerEl)
      .setName("Veu de leitura")
      .setDesc("Escurece o fundo p/ legibilidade (0 = claro, 0.9 = bem escuro). Vira brilho no mecanismo autoral.")
      .addSlider((s) => s.setLimits(0, 0.9, 0.05).setValue(p.settings.opacidadeVeu).setDynamicTooltip()
        .onChange(async (v) => { p.settings.opacidadeVeu = v; await p.saveData(); p.aplicarBrilho(); }));
  }
}
