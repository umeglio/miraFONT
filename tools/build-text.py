#!/usr/bin/env python3
"""
miraFONT Text - taglio da lettura generato dalla stessa matrice 5x9 di miraFONT
Autore: Umberto Meglio - Supporto alla creazione: Claude di Anthropic

Differenze rispetto a Dots/Linear/Spline:
  * passo verticale piu' alto di quello orizzontale (proporzioni da testo)
  * larghezze proporzionali (i, l, 1, punteggiatura occupano solo le colonne usate)
  * tratto monolineare uniforme (come Linear) con terminali arrotondati
Uso (dalla radice del repository):
  pip install fonttools skia-pathops
  python3 tools/build-text.py esp32/esp-idf/main/mirafont.c fonts/Text
Richiede: fonttools, skia-pathops (solo per generare i file, non per usarli).
"""
import math, re, sys, os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
import pathops

SRC, OUT = sys.argv[1], sys.argv[2]
UPM = 1000
DX, DY = 92, 120            # passo orizzontale / verticale (rapporto 1:1.30)
BASE_ROW = 6                # la riga 6 poggia sulla linea di base
SB = 56                     # spaziatura laterale
SPACE = 300

# ---------- lettura della matrice dal sorgente C ----------
c = open(SRC, encoding='utf-8').read()
glyphs = {}
for m in re.finditer(r"/\* 0x([0-9A-F]{2}) .*?\*/\s*\{([^}]*)\}", c):
    glyphs[int(m.group(1), 16)] = [int(x, 16) for x in m.group(2).split(',')]
acc_cp = [int(x, 16) for x in re.search(r"MIRA_ACCENT_CP\[[^\]]*\]\s*=\s*\{([^}]*)\}", c).group(1).split(',')]
acc_rows = re.findall(r"/\* U\+[0-9A-F]{4} .*?\*/\s*\{([^}]*)\}", c)
for cp, rows in zip(acc_cp, acc_rows):
    glyphs[cp] = [int(x, 16) for x in rows.split(',')]

def B(*rows):
    """bitmap da stringhe di 5 caratteri ('#' = nodo acceso), righe 0..8"""
    rows = list(rows) + ['.....'] * (9 - len(rows))
    return [int(r.replace('#', '1').replace('.', '0'), 2) for r in rows]

# glifi mancanti o vuoti nella matrice originale, disegnati sulla stessa griglia
EXTRA = {
    0x24: B('..#..', '.####', '#.#..', '.###.', '..#.#', '####.', '..#..'),          # $
    0xC9: B('...#.', '#####', '#....', '####.', '#....', '#....', '#####'),          # É
    0xCC: B('.#...', '.###.', '..#..', '..#..', '..#..', '..#..', '.###.'),          # Ì
    0xEC: B('.#...', '..#..', '.....', '.##..', '..#..', '..#..', '.###.'),          # ì (accento staccato dall'asta)
    0xD2: B('.#...', '.###.', '#...#', '#...#', '#...#', '#...#', '.###.'),          # Ò
    0xD9: B('.#...', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'),          # Ù
    0xE1: B('...#.', '..#..', '.###.', '....#', '.####', '#...#', '.####'),          # á
    0xED: B('...#.', '..#..', '.....', '.##..', '..#..', '..#..', '.###.'),          # í
    0xF3: B('...#.', '..#..', '.###.', '#...#', '#...#', '#...#', '.###.'),          # ó
    0xFA: B('...#.', '..#..', '#...#', '#...#', '#...#', '#..##', '.##.#'),          # ú
    0xE7: B('.....', '.....', '.####', '#....', '#....', '#....', '.####', '..#..', '.##..'),  # ç
    0xF1: B('.##.#', '#.##.', '####.', '#...#', '#...#', '#...#', '#...#'),          # ñ
    0xFC: B('.#.#.', '.....', '#...#', '#...#', '#...#', '#..##', '.##.#'),          # ü
    0xF6: B('.#.#.', '.....', '.###.', '#...#', '#...#', '#...#', '.###.'),          # ö
    0xE4: B('.#.#.', '.....', '.###.', '....#', '.####', '#...#', '.####'),          # ä
    0x2018: B('..#..', '.#...', '.#...'),                                             # ‘
    0x2019: B('..#..', '..#..', '.#...'),                                             # ’
    0x201C: B('.#.#.', '#.#..', '#.#..'),                                             # “
    0x201D: B('.#.#.', '.#.#.', '#.#..'),                                             # ”
    0xAB: B('.....', '.....', '..#.#', '.#.#.', '#.#..', '.#.#.', '..#.#'),          # «
    0xBB: B('.....', '.....', '#.#..', '.#.#.', '..#.#', '.#.#.', '#.#..'),          # »
    0x2013: B('.....', '.....', '.....', '.....', '####.'),                          # –
    0x2014: B('.....', '.....', '.....', '.....', '#####'),                          # —
    0x2026: B('.....', '.....', '.....', '.....', '.....', '.....', '#.#.#'),        # …
    0x20AC: B('..###', '.#...', '####.', '.#...', '####.', '.#...', '..###'),        # €
    0xB0: B('.##..', '#..#.', '.##..'),                                               # °
    0xB7: B('.....', '.....', '.....', '..#..'),                                      # ·
    0xD7: B('.....', '.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#'),          # ×
    0x2022: B('.....', '.....', '.###.', '.###.', '.###.'),                          # •
    0xA0: B(),                                                                        # spazio non separabile
}
OVERRIDE = {0xEC}   # glifi della matrice originale ridisegnati per la leggibilita'
for cp, rows in EXTRA.items():
    if cp in OVERRIDE or cp not in glyphs or not any(glyphs.get(cp, [])):
        glyphs[cp] = rows

# ---------- costruzione del contorno ----------
def on(rows, r, col):
    return 0 <= r < 9 and 0 <= col < 5 and bool(rows[r] >> (4 - col) & 1)

def capsule(p, a, b, w):
    """segmento con terminali arrotondati (approssimazione poligonale fine)"""
    (x1, y1), (x2, y2) = a, b
    ang = math.atan2(y2 - y1, x2 - x1)
    r = w / 2
    pts = []
    for i in range(0, 13):                      # semicerchio attorno a b
        t = ang - math.pi / 2 + math.pi * i / 12
        pts.append((x2 + r * math.cos(t), y2 + r * math.sin(t)))
    for i in range(0, 13):                      # semicerchio attorno a a
        t = ang + math.pi / 2 + math.pi * i / 12
        pts.append((x1 + r * math.cos(t), y1 + r * math.sin(t)))
    p.moveTo(pts[0])
    for q in pts[1:]:
        p.lineTo(q)
    p.closePath()

def dot(p, c0, w):
    x, y = c0; r = w / 2
    pts = [(x + r * math.cos(2 * math.pi * i / 24), y + r * math.sin(2 * math.pi * i / 24)) for i in range(24)]
    p.moveTo(pts[0])
    for q in pts[1:]:
        p.lineTo(q)
    p.closePath()

def glyph_path(rows, w, minc):
    path = pathops.Path()
    pen = path.getPen()
    pos = lambda r, col: (SB + w / 2 + (col - minc) * DX, (BASE_ROW - r) * DY)
    used = False
    for r in range(9):
        for col in range(5):
            if not on(rows, r, col):
                continue
            used = True
            linked = False
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                r2, c2 = r + dr, col + dc
                if not on(rows, r2, c2):
                    continue
                if dr and dc and (on(rows, r, c2) or on(rows, r2, col)):
                    continue  # diagonale gia' coperta da due tratti ortogonali
                capsule(pen, pos(r, col), pos(r2, c2), w)
                linked = True
            # nodo isolato (o raggiunto solo dall'alto/sinistra): disegna il punto
            if not linked:
                dot(pen, pos(r, col), w * 1.08)
    if not used:
        return None
    path.simplify(fix_winding=True, keep_starting_points=False)
    return path

def build(style, weight_name, stroke, italic):
    order = ['.notdef', 'space']
    cmap = {0x20: 'space'}
    shapes, advances = {}, {'.notdef': 500, 'space': SPACE}
    for cp in sorted(glyphs):
        if cp == 0x20:
            continue
        rows = glyphs[cp]
        name = 'uni%04X' % cp
        cols = [col for col in range(5) if any(on(rows, r, col) for r in range(9))]
        if cp == 0xA0:
            order.append(name); cmap[cp] = name; advances[name] = SPACE; shapes[name] = None
            continue
        if not cols:
            continue
        minc, maxc = min(cols), max(cols)
        path = glyph_path(rows, stroke, minc)
        adv = int(round(2 * SB + stroke + (maxc - minc) * DX))
        order.append(name); cmap[cp] = name
        shapes[name] = path; advances[name] = adv
    skew = math.tan(math.radians(9)) if italic else 0

    def draw(name, pen):
        path = shapes.get(name)
        if path is None:
            return
        tp = TransformPen(pen, (1, 0, skew, 1, -skew * 300, 0)) if skew else pen
        path.draw(tp)

    family = 'miraFONT Text'
    sub = style
    out = {}
    for flavor in ('ttf', 'otf'):
        fb = FontBuilder(UPM, isTTF=(flavor == 'ttf'))
        fb.setupGlyphOrder(order)
        fb.setupCharacterMap(cmap)
        if flavor == 'ttf':
            gl = {}
            for n in order:
                p = TTGlyphPen(None)
                draw(n, Cu2QuPen(p, 1.0, reverse_direction=False))
                gl[n] = p.glyph()
            fb.setupGlyf(gl)
        else:
            cs = {}
            for n in order:
                p = T2CharStringPen(advances[n], None)
                draw(n, p)
                cs[n] = p.getCharString()
            fb.setupCFF(family.replace(' ', '') + '-' + sub.replace(' ', ''), {'FullName': f'{family} {sub}'}, cs, {})
        metrics = {}
        for n in order:
            xmin = 0
            if flavor == 'ttf':
                g = fb.font['glyf'][n]
                xmin = getattr(g, 'xMin', 0) if g.numberOfContours else 0
            metrics[n] = (advances[n], xmin)
        fb.setupHorizontalMetrics(metrics)
        asc, desc = 900, -280
        fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=0)
        fb.setupNameTable({
            'familyName': family, 'styleName': sub,
            'uniqueFontIdentifier': f'miraNET:{family}-{sub}:2026',
            'fullName': f'{family} {sub}', 'psName': family.replace(' ', '') + '-' + sub.replace(' ', ''),
            'version': 'Version 1.000', 'manufacturer': 'miraNET / Umberto Meglio', 'designer': 'Umberto Meglio',
            'description': 'Reading cut of miraFONT: same 5x9 node matrix, text proportions. Built with the support of Claude by Anthropic.',
            'licenseDescription': 'CC0 1.0 Universal - public domain dedication',
            'licenseInfoURL': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'vendorURL': 'https://umeglio.github.io/miraFONT/',
        })
        wclass = 700 if 'Bold' in sub else 400
        fsSel = (0x01 if italic else 0) | (0x20 if 'Bold' in sub else 0) | (0x40 if sub == 'Regular' else 0)
        fb.setupOS2(sTypoAscender=asc, sTypoDescender=desc, sTypoLineGap=200, usWinAscent=asc + 60, usWinDescent=-desc + 60,
                    sxHeight=4 * DY + stroke // 2, sCapHeight=6 * DY + stroke // 2, usWeightClass=wclass, fsSelection=fsSel,
                    achVendID='MIRA', fsType=0)
        fb.setupPost(isFixedPitch=0, italicAngle=-9 if italic else 0)
        fb.setupHead(unitsPerEm=UPM, macStyle=(1 if 'Bold' in sub else 0) | (2 if italic else 0))
        out[flavor] = fb.font
    return out

os.makedirs(OUT, exist_ok=True)
for sub, stroke, italic in (('Regular', 72, False), ('Bold', 108, False), ('Italic', 72, True), ('Bold Italic', 108, True)):
    fonts = build(sub, sub, stroke, italic)
    base = os.path.join(OUT, 'miraFONT-' + sub.replace(' ', '') + '-Text')
    fonts['ttf'].save(base + '.ttf')
    fonts['otf'].save(base + '.otf')
    fonts['ttf'].flavor = 'woff'
    fonts['ttf'].save(base + '.woff')
    print('ok', base, len(fonts['ttf'].getGlyphOrder()), 'glifi')
