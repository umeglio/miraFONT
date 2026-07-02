/* ============================================================
   miraFONT demo — ESP32-S3 + SSD1306 128x64 OLED
   (ELEGOO 0.96" blue/yellow, I2C driver) — Arduino core.

   The panel is a single monochrome SSD1306; the top 16 px show
   as YELLOW, the rest BLUE. Draw normally and place your title
   in rows 0..15 to land in the yellow band.

   Wiring (adjust pins to your board):
     OLED VCC -> 3V3     OLED GND -> GND
     OLED SDA -> GPIO 8  OLED SCL -> GPIO 9
   ============================================================ */
#include <Wire.h>
extern "C" {
  #include "mirafont.h"
  #include "ssd1306.h"
}

#define PIN_SDA    8      /* <-- set to your ESP32-S3 SDA pin */
#define PIN_SCL    9      /* <-- set to your ESP32-S3 SCL pin */
#define OLED_ADDR  0x3C   /* some panels are 0x3D            */

/* SSD1306 transport required by ssd1306.c (C linkage). */
extern "C" int mira_i2c_write(uint8_t addr, const uint8_t *data, size_t len) {
  Wire.beginTransmission(addr);
  Wire.write(data, len);
  return Wire.endTransmission();
}

static uint8_t fb[MIRA_FB_SIZE];
static int frame = 0;

void setup() {
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  ssd1306_init(OLED_ADDR);
}

void loop() {
  mira_fb_clear(fb);

  /* ---- logo + wordmark (fox ears sit in the yellow band) ---- */
  mira_draw_bitmap(fb, 0, 0, MIRA_FOX32, MIRA_FOX_W, MIRA_FOX_H);
  mira_draw_text(fb, 38,  2, "miraNET",       MIRA_SOLID, 1);  /* linear cut */
  mira_draw_text(fb, 38, 12, "S3 . 128x64",   MIRA_DOTS,  1);  /* dot cut    */
  mira_draw_text(fb, 38, 22, "i2c 0x3C",      MIRA_DOTS,  1);

  /* ---- runtime log (blue zone) ---- */
  mira_draw_text(fb, 2, 36, "> boot runtime", MIRA_DOTS,  1);
  mira_draw_text(fb, 2, 46, "miracache .. ok", MIRA_DOTS, 1);
  int aw = mira_draw_text(fb, 2, 55, "data speaks c", MIRA_SOLID, 1);

  /* blinking cursor */
  if (frame & 1) mira_draw_char(fb, 2 + aw, 55, '_', MIRA_SOLID, 1);

  /* looping progress bar along the bottom */
  int w = (frame % 63) * 2;
  for (int i = 0; i < w && i < 124; i++) mira_fb_pixel(fb, 2 + i, 63, 1);

  ssd1306_flush(fb);
  frame++;
  delay(120);
}
