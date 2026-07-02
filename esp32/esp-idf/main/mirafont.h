/* ============================================================
   miraFONT — Digital Runtime typeface for miraNET
   5x9 dot-matrix bitmap font, portable ANSI C (C89/C99).
   Target: SSD1306 128x64 OLED (e.g. ELEGOO 0.96" blue/yellow)
   over I2C on ESP32-S3. No dependencies.
   Generated from the miraNET type project — do not hand-edit data.
   ============================================================ */
#ifndef MIRAFONT_H
#define MIRAFONT_H

#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif

#if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
#include <stdint.h>
#else
typedef unsigned char  uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int   uint32_t;
#endif

#define MIRA_COLS         5
#define MIRA_ROWS         9      /* rows 0..6 = cap band, 7..8 = descenders */
#define MIRA_ASCII_FIRST  32
#define MIRA_ASCII_COUNT  95     /* 0x20..0x7E */
#define MIRA_ACCENT_COUNT 8

/* SSD1306 128x64 monochrome framebuffer, page format (1 bit = 1 pixel). */
#define MIRA_FB_W    128
#define MIRA_FB_H    64
#define MIRA_FB_SIZE (MIRA_FB_W * MIRA_FB_H / 8)  /* 1024 bytes */

/* On the blue/yellow panel the top 16 px are yellow, the rest blue. */
#define MIRA_YELLOW_H 16

typedef enum {
  MIRA_DOTS  = 0,  /* dot-matrix nodes (the family's "Dots" cut)   */
  MIRA_SOLID = 1   /* filled cells -> connected "Linear/Spline" look */
} mira_style_t;

/* Glyph tables (each glyph = MIRA_ROWS bytes; low 5 bits, bit4 = left col). */
extern const uint8_t  MIRA_GLYPHS[MIRA_ASCII_COUNT][MIRA_ROWS];
extern const uint16_t MIRA_ACCENT_CP[MIRA_ACCENT_COUNT];
extern const uint8_t  MIRA_ACCENT_GLYPHS[MIRA_ACCENT_COUNT][MIRA_ROWS];

/* Fox+M logo, 32x32, row-major, MSB-first, 4 bytes/row. */
#define MIRA_FOX_W 32
#define MIRA_FOX_H 32
extern const uint8_t MIRA_FOX32[MIRA_FOX_W * MIRA_FOX_H / 8];

/* --- framebuffer primitives --- */
void mira_fb_clear(uint8_t *fb);
void mira_fb_pixel(uint8_t *fb, int x, int y, int on);

/* --- glyph lookup / metrics --- */
const uint8_t *mira_glyph(uint32_t codepoint);   /* NULL if unknown */
int  mira_char_width(int scale);                 /* advance in px = 6*scale */
int  mira_text_width(const char *ascii, int scale);

/* --- drawing (return advance in px) --- */
int mira_draw_glyph(uint8_t *fb, int x, int y, const uint8_t rows[MIRA_ROWS], mira_style_t style, int scale);
int mira_draw_char (uint8_t *fb, int x, int y, char c, mira_style_t style, int scale);
int mira_draw_text (uint8_t *fb, int x, int y, const char *ascii, mira_style_t style, int scale);
int mira_draw_utf8 (uint8_t *fb, int x, int y, const char *utf8, mira_style_t style, int scale); /* handles à è é ì ò ù À È */

/* --- bitmap blit (row-major, MSB-first) --- */
void mira_draw_bitmap(uint8_t *fb, int x, int y, const uint8_t *bmp, int w, int h);

#ifdef __cplusplus
}
#endif
#endif /* MIRAFONT_H */
