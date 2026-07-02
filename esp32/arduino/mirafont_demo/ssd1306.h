/* Minimal SSD1306 128x64 I2C driver (transport-agnostic ANSI C).
   You implement mira_i2c_write() for your platform (ESP-IDF / Arduino). */
#ifndef SSD1306_H
#define SSD1306_H
#include "mirafont.h"
#ifdef __cplusplus
extern "C" {
#endif

/* Provide this on your platform. Return 0 on success.
   'data' already includes the SSD1306 control byte (0x00 cmd / 0x40 data). */
int  mira_i2c_write(uint8_t addr, const uint8_t *data, size_t len);

void ssd1306_init(uint8_t addr);              /* addr is usually 0x3C */
void ssd1306_flush(const uint8_t *fb);        /* push 1024-byte framebuffer */
void ssd1306_contrast(uint8_t value);
void ssd1306_invert(int on);

#ifdef __cplusplus
}
#endif
#endif
