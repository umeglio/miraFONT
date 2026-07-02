/* SSD1306 128x64 I2C driver. */
#include "ssd1306.h"

static uint8_t s_addr = 0x3C;

static void ssd_cmd(uint8_t c){ uint8_t b[2]; b[0] = 0x00; b[1] = c; mira_i2c_write(s_addr, b, 2); }

void ssd1306_init(uint8_t addr){
  static const uint8_t seq[] = {
    0xAE, 0xD5,0x80, 0xA8,0x3F, 0xD3,0x00, 0x40,
    0x8D,0x14, 0x20,0x00, 0xA1, 0xC8, 0xDA,0x12,
    0x81,0x8F, 0xD9,0xF1, 0xDB,0x40, 0xA4, 0xA6,
    0x2E, 0xAF
  };
  unsigned i;
  s_addr = addr;
  for (i = 0; i < sizeof(seq); i++) ssd_cmd(seq[i]);
}

void ssd1306_contrast(uint8_t v){ ssd_cmd(0x81); ssd_cmd(v); }
void ssd1306_invert(int on){ ssd_cmd(on ? 0xA7 : 0xA6); }

void ssd1306_flush(const uint8_t *fb){
  uint8_t chunk[17]; int i, j;
  ssd_cmd(0x21); ssd_cmd(0); ssd_cmd(127);   /* column range 0..127 */
  ssd_cmd(0x22); ssd_cmd(0); ssd_cmd(7);     /* page range 0..7     */
  for (i = 0; i < MIRA_FB_SIZE; i += 16){
    chunk[0] = 0x40;                          /* data control byte  */
    for (j = 0; j < 16; j++) chunk[1 + j] = fb[i + j];
    mira_i2c_write(s_addr, chunk, 17);        /* 16B/chunk: Wire-safe */
  }
}
