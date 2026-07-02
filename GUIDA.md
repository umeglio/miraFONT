# 📖 miraFONT — Guida completa
### Tutte le indicazioni per usare, pubblicare e diffondere la tua font

*miraNET / Umberto Meglio, 2026 — "where data speaks C."*
Licenza: **CC0 1.0 Universal (pubblico dominio)** · DOI miraNET: [10.5281/zenodo.19402571](https://doi.org/10.5281/zenodo.19402571)

---

## 1. I link ufficiali

| Cosa | Link |
|---|---|
| 🌐 Sito pubblico (specimen + simulatore OLED) | https://umeglio.github.io/miraFONT/ |
| 📦 Repository GitHub (sorgenti e download) | https://github.com/umeglio/miraFONT |
| 📜 Licenza CC0 | https://github.com/umeglio/miraFONT/blob/main/LICENSE |
| 🔬 DOI miraNET (Zenodo) | https://doi.org/10.5281/zenodo.19402571 |
| 🎨 CSS "tutto in uno" per il web | https://umeglio.github.io/miraFONT/fonts/miraFONT.css |

---

## 2. Cos'è miraFONT (testo di presentazione pronto)

**IT** — miraFONT è un carattere tipografico originale nato da una matrice di nodi 5×7,
senza outline di terze parti. 21 tagli in 3 texture (Dots, Linear, Spline), dal desktop
al web fino ai display OLED su ESP32. Rilasciato in CC0 — pubblico dominio: usalo,
modificalo e ridistribuiscilo liberamente, anche per scopi commerciali, senza attribuzione.
È di tutti.

**EN** — miraFONT is an original typeface built from a 5×7 node matrix, no third-party
outlines. 21 cuts in 3 textures, from desktop to ESP32 OLED displays. Released under
CC0 — public domain: free for everyone, any use, no attribution required.

> ▶ **In arrivo / Coming up** — il **miraNET Digital Runtime** è interamente basato su
> miraFONT: questa è la sua tipografia nativa. / The miraNET Digital Runtime is built on
> miraFONT — this is its native typeface.

---

## 3. La famiglia: 21 tagli × 3 formati

**Le tre texture** (stessa matrice 5×7, tre interpretazioni):

| Texture | Carattere | Uso consigliato |
|---|---|---|
| **Dots** | matrice di nodi allo stato puro | look display/terminale, codice |
| **Linear** | nodi fusi in tratto continuo | testo corrente, massima leggibilità |
| **Spline** | monolinea morbida interpolata | titoli e intestazioni |

**Gli stili**: Light · Regular · Bold · Black · Italic · Compressed · Narrow · Double Strike
(Light/Bold/Black esistono in Dots e Spline; Linear ha Regular + Italic + le varianti).

**I formati**: ogni taglio è fornito in `.otf`, `.ttf` e `.woff`.
Il `.woff2` opzionale si genera con un comando (vedi `MAKE-WOFF2.txt` nel repository).

---

## 4. Installazione desktop

| Sistema | Procedura |
|---|---|
| **Windows** | doppio clic su un file `.ttf` o `.otf` → pulsante **Installa** |
| **macOS** | doppio clic → **Installa font** (si apre Libro Font) |
| **Linux** | copia i file in `~/.local/share/fonts/` poi esegui `fc-cache -f` |

Scarichi i file dal repository (cartella `fonts/`) o con i link diretti della sezione 6.

---

## 5. Uso sul web — metodo semplice (consigliato)

Una sola riga nell'`<head>` della pagina:

```html
<link rel="stylesheet" href="https://umeglio.github.io/miraFONT/fonts/miraFONT.css">
```

Poi nel CSS usi questi nomi di famiglia:

| `font-family` | Texture / stile | Pesi |
|---|---|---|
| `'miraFONT'` | Dots | 300 · 400 · 700 · 900 + *italic* |
| `'miraFONT Compressed'` | Dots compresso | 400 |
| `'miraFONT Narrow'` | Dots stretto | 400 |
| `'miraFONT Double Strike'` | Dots doppio tratto | 400 |
| `'miraFONT Linear'` | Linear | 400 + *italic* |
| `'miraFONT Compressed Linear'` | Linear compresso | 400 |
| `'miraFONT Narrow Linear'` | Linear stretto | 400 |
| `'miraFONT Double Strike Linear'` | Linear doppio tratto | 400 |
| `'miraFONT Spline'` | Spline | 300 · 400 · 700 · 900 + *italic* |
| `'miraFONT Compressed Spline'` | Spline compresso | 400 |
| `'miraFONT Narrow Spline'` | Spline stretto | 400 |
| `'miraFONT Double Strike Spline'` | Spline doppio tratto | 400 |

Esempio completo:

```css
body { font-family: 'miraFONT Linear', monospace; }                    /* testo corrente  */
h1   { font-family: 'miraFONT Spline', monospace; font-weight: 700; } /* titoli          */
code { font-family: 'miraFONT', monospace; }                           /* stile terminale */
```

---

## 6. Uso sul web — link diretti ai singoli file

Schema URL (63 file totali):

```
https://umeglio.github.io/miraFONT/fonts/<Texture>/miraFONT-<Stile>-<Texture>.<estensione>
```

- `<Texture>` = `Dots` · `Linear` · `Spline`
- `<Stile>`   = `Light` · `Regular` · `Bold` · `Black` · `Italic` · `Compressed` · `Narrow` · `DoubleStrike`
- `<estensione>` = `woff` (web) · `ttf` · `otf` (desktop)

I file `.woff` (per il web):

**Dots**
```
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Light-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Regular-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Bold-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Black-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Italic-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Compressed-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-Narrow-Dots.woff
https://umeglio.github.io/miraFONT/fonts/Dots/miraFONT-DoubleStrike-Dots.woff
```

**Linear**
```
https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-Regular-Linear.woff
https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-Italic-Linear.woff
https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-Compressed-Linear.woff
https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-Narrow-Linear.woff
https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-DoubleStrike-Linear.woff
```

**Spline**
```
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Light-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Regular-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Bold-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Black-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Italic-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Compressed-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Narrow-Spline.woff
https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-DoubleStrike-Spline.woff
```

Esempio di `@font-face` manuale:

```css
@font-face{
  font-family:'miraFONT Linear';
  font-style:normal; font-weight:400;
  src:url('https://umeglio.github.io/miraFONT/fonts/Linear/miraFONT-Regular-Linear.woff') format('woff');
}
@font-face{
  font-family:'miraFONT Spline';
  font-style:normal; font-weight:700;
  src:url('https://umeglio.github.io/miraFONT/fonts/Spline/miraFONT-Bold-Spline.woff') format('woff');
}
```

---

## 7. ESP32 / display OLED

Nella cartella [`esp32/`](https://github.com/umeglio/miraFONT/tree/main/esp32) del repository:

- il font in **C ANSI** (stessa matrice 5×7 dei file desktop)
- il **driver SSD1306** per display OLED I²C
- demo pronte per **Arduino** e **ESP-IDF** (testate su ELEGOO 0,96")

Il [sito pubblico](https://umeglio.github.io/miraFONT/) include un **simulatore OLED
interattivo** che mostra pixel-per-pixel cosa disegna la demo ESP32-S3.

---

## 8. Il sito pubblico: com'è fatto e come si aggiorna

**Struttura**
- `index.html` = lo specimen interattivo con intro bilingue IT/EN, badge "100% miraFONT",
  badge DOI miraNET e note d'installazione. **Ogni testo della pagina è reso in miraFONT**
  (i font UI originali sono rimappati ai tagli reali via `@font-face`).
- `miraFONT-specimen.html` = lo specimen originale, intatto.
- `FoxLogo.dc.html` = il componente della volpe miraNET (sezione FOX MARK), con effetto
  hover: si illumina e si anima.

**Pubblicazione automatica**
Il sito è servito da GitHub Pages dal branch `gh-pages`. Il workflow
`.github/workflows/deploy-pages.yml` sincronizza `main → gh-pages` ad ogni push:
**basta fare push su `main` e il sito si aggiorna da solo** in 1–2 minuti.
Se una build di Pages fallisse con errore transitorio, si rilancia con un commit
(anche vuoto) su `gh-pages`, o da GitHub → Actions → Re-run.

---

## 9. Usare miraFONT su un altro sito

I font sono serviti pubblicamente da `umeglio.github.io/miraFONT/` con licenza CC0:
qualsiasi sito può caricarli direttamente con la riga `<link>` della sezione 5 o con
gli `@font-face` della sezione 6, **senza copiare alcun file**.

Badge DOI da riusare ovunque (Markdown):

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19402571.svg)](https://doi.org/10.5281/zenodo.19402571)
```

---

## 10. Licenza e citazione

**CC0 1.0 Universal** — dedica al pubblico dominio: chiunque può usare, modificare,
incorporare, vendere e ridistribuire miraFONT, per qualsiasi scopo, senza chiedere
permesso e senza attribuzione. Una menzione è gradita ma mai dovuta:

> miraFONT — miraNET / Umberto Meglio, 2026 · DOI: 10.5281/zenodo.19402571

---

*Tutti i link di questa guida sono verificati funzionanti sul sito pubblico.*
