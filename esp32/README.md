# miraFONT for ESP32-S3 + SSD1306 OLED (ANSI C)

Bring **miraFONT** — the miraNET Digital Runtime typeface — to a real
**ELEGOO 0.96" blue/yellow OLED (SSD1306, 128×64, I2C)** driven by an
**ESP32-S3**. Pure ANSI C, no dependencies, portable to any MCU.

```
     ┌──────────────────────────────┐  ← rows 0..15  = YELLOW
     │  🦊  miraNET                  │
     │      S3 . 128x64              │  ← rows 16..63 = BLUE
     │      i2c 0x3C                 │
     │  > boot runtime               │
     │  miracache .. ok              │
     │  data speaks c_               │
     └──────────────────────────────┘
```

The panel is a single **monochrome** SSD1306. The top 16 px glow **yellow**
and the rest **blue** — a physical color filter, not addressable. Draw as
usual and put your title in rows `0..15` (see `MIRA_YELLOW_H`) to land it in
the yellow band.

---

## Files

| File | What it is |
|------|------------|
| `mirafont.h` / `mirafont.c` | The font: 5×9 dot-matrix glyphs (ASCII 0x20–0x7E + Italian accents) generated 1:1 from the miraNET type project, plus a framebuffer renderer and the 32×32 fox+M logo bitmap. |
| `ssd1306.h` / `ssd1306.c` | Minimal SSD1306 128×64 I2C driver. Transport-agnostic: you provide `mira_i2c_write()`. |
| `arduino/mirafont_demo/` | Ready Arduino sketch (uses `Wire`). |
| `esp-idf/` | Ready ESP-IDF v5.x project (uses the new `i2c_master` driver). |

---

## Wiring

| OLED | ESP32-S3 |
|------|----------|
| VCC  | 3V3 |
| GND  | GND |
| SDA  | GPIO 8  *(edit `PIN_SDA`)* |
| SCL  | GPIO 9  *(edit `PIN_SCL`)* |

I2C address is usually `0x3C` (some panels `0x3D`). ESP32-S3 has no fixed
default I2C pins — set `PIN_SDA` / `PIN_SCL` to whatever your board exposes.

---

## Build — Arduino IDE

1. Install the **esp32** board package (Boards Manager) and select your
   ESP32-S3 board.
2. Open `arduino/mirafont_demo/mirafont_demo.ino` (the `.c/.h` files next to
   it compile automatically).
3. Set `PIN_SDA`, `PIN_SCL`, `OLED_ADDR` at the top of the sketch.
4. Upload.

## Build — ESP-IDF (v5.x)

```sh
idf.py -C esp-idf set-target esp32s3
idf.py -C esp-idf build flash monitor
```

Edit pins/address at the top of `esp-idf/main/main.c`.

---

## API (ANSI C)

```c
uint8_t fb[MIRA_FB_SIZE];          /* 1024-byte SSD1306 framebuffer */

mira_fb_clear(fb);

/* text — returns advance in px. style: MIRA_DOTS or MIRA_SOLID; scale >= 1 */
mira_draw_text(fb, x, y, "miraNET", MIRA_SOLID, 1);
mira_draw_text(fb, x, y, "runtime", MIRA_DOTS,  2);   /* 2x = big nodes */

/* Italian accents (UTF-8 in, à è é ì ò ù À È supported) */
mira_draw_utf8(fb, x, y, "città è pronta", MIRA_DOTS, 1);

/* the fox+M logo */
mira_draw_bitmap(fb, 0, 0, MIRA_FOX32, MIRA_FOX_W, MIRA_FOX_H);

/* single pixel / metrics */
mira_fb_pixel(fb, x, y, 1);
int w = mira_text_width("hello", 1);

ssd1306_flush(fb);                 /* push to the panel */
```

### Two cuts, one font
- `MIRA_DOTS` — the dot-matrix nodes (miraFONT **Dots**). At `scale >= 2`
  each node gets a 1-px gap so the matrix reads.
- `MIRA_SOLID` — filled cells that fuse into strokes (miraFONT
  **Linear/Spline**). Best for the wordmark and small sizes.

### Metrics
5 cols × 9 rows per glyph; rows 0–6 are the cap band, 7–8 hold descenders.
Advance is `6 * scale` px (monospace). At `scale 1`: ~21 chars/line, 5–6 lines.

---

## Porting to another MCU / display

Only one function is platform-specific — implement it and you're done:

```c
int mira_i2c_write(uint8_t addr, const uint8_t *data, size_t len);
/* send `len` bytes to I2C device `addr`; return 0 on success.
   `data` already carries the SSD1306 control byte (0x00 cmd / 0x40 data). */
```

`ssd1306_flush()` sends the buffer in 16-byte chunks, so it is safe even on
stacks with a 32-byte I2C buffer (e.g. classic Arduino `Wire`).

For a non-SSD1306 display, keep `mirafont.c` (pure framebuffer drawing) and
replace `ssd1306.c` with your panel's init + flush.
