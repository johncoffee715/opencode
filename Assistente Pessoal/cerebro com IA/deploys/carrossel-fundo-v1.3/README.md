# Carrossel Fundo v1.3.0 — pacote plug-n-play

Background em carrossel animado + reativo para Obsidian, a partir de uma pasta
de imagens do vault. Canonizado 2026-09-10 (IMAGENS APARECEM + shuffle ok +
letterbox, verificado pelo usuário).

## Conteúdo

- `plugins/carrossel-fundo/manifest.json` + `main.js` — motor (JS puro, sem build):
  rotaciona por intervalo (20s), ao abrir nota, ao criar pasta/nota; reindexa em
  delete/rename; status `🖼 n/m` clicável; 4 comandos; aba de ajustes; autodiagnóstico.
- `snippets/fundo.css` — tinta battle-tested: custom-background do AnuPpuccin
  (AnubisNekhet, **AGPLv3** — crédito e licença no cabeçalho do arquivo).
  Pinta no `.app-container` + véu por `backdrop-filter`. REQUERIDO.
- `snippets/carrossel-fundo.css` — preferência: `contain` (inteira, sem distorção,
  centralizada, barras na cor do tema). Opcional; sem ele = crop (`cover`).

## Instalação (3 passos, 2 min)

1. Copie `plugins/carrossel-fundo/` para `<seu-vault>/.obsidian/plugins/` e
   `snippets/*.css` para `<seu-vault>/.obsidian/snippets/`.
2. No Obsidian: Plugins da comunidade → ativar **Carrossel Fundo** (desative o
   modo seguro antes, se pedido); Aparência → Snippets → ativar **fundo**
   (+ **carrossel-fundo** para letterbox).
3. `Ctrl+R`. Coloque suas imagens numa pasta `ImagensFundo/` (ou ajuste o nome
   na aba de ajustes do plugin). Pronto: status `🖼 1/N` na barra inferior.

## Notas

- Imagens NÃO incluídas (use as suas; ~12 MB p/ 8 PNGs 1080p é confortável).
- Graph view: sem cobertura (limitação herdada do referencial).
- Mobile: funciona; PNGs pesados custam bateria — prefira JPG ≤1920px.
- Licenças: motor próprio (livre); `fundo.css` AGPLv3 (AnubisNekhet).
