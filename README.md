<div align="center">

# miraFONT

**Digital typography for a Digital Runtime**

*Built from a 5×7 node matrix — no third-party outlines. Free for everyone, forever.*

[![License: CC0 1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Formats](https://img.shields.io/badge/formats-OTF%20·%20TTF%20·%20WOFF-blue.svg)](fonts/)
[![Cuts](https://img.shields.io/badge/cuts-21-orange.svg)](fonts/)
[![ESP32 ready](https://img.shields.io/badge/ESP32-SSD1306%20OLED-green.svg)](esp32/)
[![miraNET DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19402571.svg)](https://doi.org/10.5281/zenodo.19402571)

**🌐 [Live specimen & OLED simulator → umeglio.github.io/miraFONT](https://umeglio.github.io/miraFONT/)**

*The site itself is set 100% in miraFONT — every heading, label and paragraph. / Il sito stesso è composto al 100% in miraFONT — ogni titolo, etichetta e paragrafo.*

[English](#-english) · [Italiano](#-italiano)

</div>

---

## 🇬🇧 English

### What is miraFONT?

miraFONT is an original typeface designed for the **miraNET Digital Runtime**: every glyph is generated from a **5×7 node matrix**, with no third-party outlines. The same DNA that drives a 0.96" OLED display also produces a complete desktop and web font family.

It is released under **[CC0 1.0 Universal](LICENSE)** (public domain dedication): you can use it, modify it, embed it and redistribute it **for any purpose, including commercial, with no attribution required**. It belongs to everyone.

> ▶ **Coming up** — the **[miraNET Digital Runtime](https://doi.org/10.5281/zenodo.19402571)** is built on miraFONT: this is its native typeface. DOI: [10.5281/zenodo.19402571](https://doi.org/10.5281/zenodo.19402571)

### The family — 21 cuts × 3 formats

Three **textures**, each rendering the node matrix in a different way:

| Texture | Character |
|---|---|
| **Dots** | the raw node matrix — pure display/terminal feel |
| **Linear** | nodes merged into a continuous stroke |
| **Spline** | smooth monoline interpolation |

Available **weights**: Light, Regular, Bold, Black — plus **styles**: Italic, Compressed, Narrow, Double Strike. Every cut ships as `.otf`, `.ttf` and `.woff` (optional `.woff2`: see [MAKE-WOFF2.txt](MAKE-WOFF2.txt)).

### Install

| Platform | How |
|---|---|
| **Windows** | double-click a `.ttf` / `.otf` → *Install* |
| **macOS** | double-click → *Install Font* (Font Book) |
| **Linux** | copy to `~/.local/share/fonts/` then run `fc-cache -f` |
| **Web** | `<link rel="stylesheet" href="fonts/miraFONT.css">` — every cut is already wired |

```css
/* Example */
body { font-family: 'miraFONT', monospace; }          /* Dots, 300/400/700/900 + italic */
h1   { font-family: 'miraFONT Spline'; }              /* smooth monoline */
code { font-family: 'miraFONT Linear'; }              /* merged stroke   */
```

### ESP32 / embedded

The [`esp32/`](esp32/) folder contains the font as **ANSI C**, an **SSD1306 OLED driver** and demos for **Arduino** and **ESP-IDF** (tested on ELEGOO 0.96" displays). The [live specimen](https://umeglio.github.io/miraFONT/) includes an interactive OLED simulator that works offline.

### Repository map

```
fonts/                  21 cuts × 3 formats in Dots/ Linear/ Spline/ + miraFONT.css
esp32/                  ANSI C font + SSD1306 driver + Arduino & ESP-IDF demos
miraFONT-specimen.html  full interactive specimen + live OLED simulator (offline OK)
index.html              presentation site (GitHub Pages)
MAKE-WOFF2.txt          one command to generate optional .woff2 files
LICENSE                 CC0 1.0 Universal
```

### License

**CC0 1.0 Universal** — dedicated to the public domain. No permission needed, no attribution required (though a mention of *miraNET / Umberto Meglio* is always appreciated). See [LICENSE](LICENSE).

---

## 🇮🇹 Italiano

### Cos'è miraFONT?

miraFONT è un carattere tipografico originale nato per il **miraNET Digital Runtime**: ogni glifo è generato da una **matrice di nodi 5×7**, senza outline di terze parti. Lo stesso DNA che pilota un display OLED da 0,96" produce anche una famiglia completa di font per desktop e web.

È rilasciato con licenza **[CC0 1.0 Universal](LICENSE)** (dedica al pubblico dominio): puoi usarlo, modificarlo, incorporarlo e ridistribuirlo **per qualsiasi scopo, anche commerciale, senza obbligo di attribuzione**. È di tutti.

> ▶ **In arrivo** — il **[miraNET Digital Runtime](https://doi.org/10.5281/zenodo.19402571)** è interamente basato su miraFONT: questa è la sua tipografia nativa. DOI: [10.5281/zenodo.19402571](https://doi.org/10.5281/zenodo.19402571)

### La famiglia — 21 tagli × 3 formati

Tre **texture**, ognuna interpreta la matrice di nodi in modo diverso:

| Texture | Carattere |
|---|---|
| **Dots** | la matrice di nodi allo stato puro — feeling display/terminale |
| **Linear** | nodi fusi in un tratto continuo |
| **Spline** | interpolazione monolinea morbida |

**Pesi** disponibili: Light, Regular, Bold, Black — più gli **stili**: Italic, Compressed, Narrow, Double Strike. Ogni taglio è fornito in `.otf`, `.ttf` e `.woff` (`.woff2` opzionale: vedi [MAKE-WOFF2.txt](MAKE-WOFF2.txt)).

### Installazione

| Piattaforma | Come |
|---|---|
| **Windows** | doppio clic su un `.ttf` / `.otf` → *Installa* |
| **macOS** | doppio clic → *Installa font* (Libro Font) |
| **Linux** | copia in `~/.local/share/fonts/` poi esegui `fc-cache -f` |
| **Web** | `<link rel="stylesheet" href="fonts/miraFONT.css">` — tutti i tagli già pronti |

```css
/* Esempio */
body { font-family: 'miraFONT', monospace; }          /* Dots, 300/400/700/900 + italic */
h1   { font-family: 'miraFONT Spline'; }              /* monolinea morbida */
code { font-family: 'miraFONT Linear'; }              /* tratto continuo   */
```

### ESP32 / embedded

La cartella [`esp32/`](esp32/) contiene il font in **C ANSI**, un **driver OLED SSD1306** e demo per **Arduino** ed **ESP-IDF** (testato su display ELEGOO 0,96"). Lo [specimen online](https://umeglio.github.io/miraFONT/) include un simulatore OLED interattivo che funziona anche offline.

### Mappa del repository

```
fonts/                  21 tagli × 3 formati in Dots/ Linear/ Spline/ + miraFONT.css
esp32/                  font in C ANSI + driver SSD1306 + demo Arduino ed ESP-IDF
miraFONT-specimen.html  specimen interattivo completo + simulatore OLED (anche offline)
index.html              sito di presentazione (GitHub Pages)
MAKE-WOFF2.txt          un comando per generare i .woff2 opzionali
LICENSE                 CC0 1.0 Universal
```

### Licenza

**CC0 1.0 Universal** — dedicato al pubblico dominio. Nessun permesso necessario, nessuna attribuzione richiesta (una menzione a *miraNET / Umberto Meglio* è comunque sempre gradita). Vedi [LICENSE](LICENSE).

---

<div align="center">

*where data speaks C.* — **miraNET / Umberto Meglio, 2026**

</div>
