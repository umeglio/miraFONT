/* ============================================================
   miraFONT demo — ESP32-S3 + SSD1306 128x64 OLED
   (ELEGOO 0.96" blue/yellow, I2C) — ESP-IDF v5.x.

   Uses the new I2C master driver (driver/i2c_master.h).
   Wiring: VCC->3V3  GND->GND  SDA->GPIO8  SCL->GPIO9  (adjust).
   ============================================================ */
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c_master.h"
#include "esp_log.h"
#include "mirafont.h"
#include "ssd1306.h"

#define I2C_PORT   I2C_NUM_0
#define PIN_SDA    8       /* <-- set to your ESP32-S3 SDA pin */
#define PIN_SCL    9       /* <-- set to your ESP32-S3 SCL pin */
#define OLED_ADDR  0x3C    /* some panels are 0x3D            */

static const char *TAG = "miraFONT";
static i2c_master_bus_handle_t s_bus;
static i2c_master_dev_handle_t s_dev;
static uint8_t fb[MIRA_FB_SIZE];

/* SSD1306 transport required by ssd1306.c */
int mira_i2c_write(uint8_t addr, const uint8_t *data, size_t len) {
  (void)addr;
  return i2c_master_transmit(s_dev, data, len, 100) == ESP_OK ? 0 : -1;
}

static void i2c_setup(void) {
  i2c_master_bus_config_t bus_cfg;
  i2c_device_config_t dev_cfg;
  memset(&bus_cfg, 0, sizeof(bus_cfg));
  memset(&dev_cfg, 0, sizeof(dev_cfg));

  bus_cfg.clk_source = I2C_CLK_SRC_DEFAULT;
  bus_cfg.i2c_port = I2C_PORT;
  bus_cfg.sda_io_num = PIN_SDA;
  bus_cfg.scl_io_num = PIN_SCL;
  bus_cfg.glitch_ignore_cnt = 7;
  bus_cfg.flags.enable_internal_pullup = true;
  ESP_ERROR_CHECK(i2c_new_master_bus(&bus_cfg, &s_bus));

  dev_cfg.dev_addr_length = I2C_ADDR_BIT_LEN_7;
  dev_cfg.device_address = OLED_ADDR;
  dev_cfg.scl_speed_hz = 400000;
  ESP_ERROR_CHECK(i2c_master_bus_add_device(s_bus, &dev_cfg, &s_dev));
}

void app_main(void) {
  int frame = 0;
  i2c_setup();
  ssd1306_init(OLED_ADDR);
  ESP_LOGI(TAG, "miraFONT ready on SSD1306 0x%02X", OLED_ADDR);

  for (;;) {
    int aw, w, i;
    mira_fb_clear(fb);

    /* logo + wordmark (fox ears land in the yellow band) */
    mira_draw_bitmap(fb, 0, 0, MIRA_FOX32, MIRA_FOX_W, MIRA_FOX_H);
    mira_draw_text(fb, 38,  2, "miraNET",        MIRA_SOLID, 1);
    mira_draw_text(fb, 38, 12, "S3 . 128x64",    MIRA_DOTS,  1);
    mira_draw_text(fb, 38, 22, "i2c 0x3C",       MIRA_DOTS,  1);

    /* runtime log (blue zone) */
    mira_draw_text(fb, 2, 36, "> boot runtime",  MIRA_DOTS,  1);
    mira_draw_text(fb, 2, 46, "miracache .. ok", MIRA_DOTS,  1);
    aw = mira_draw_text(fb, 2, 55, "data speaks c", MIRA_SOLID, 1);

    if (frame & 1) mira_draw_char(fb, 2 + aw, 55, '_', MIRA_SOLID, 1);

    w = (frame % 63) * 2;
    for (i = 0; i < w && i < 124; i++) mira_fb_pixel(fb, 2 + i, 63, 1);

    ssd1306_flush(fb);
    frame++;
    vTaskDelay(pdMS_TO_TICKS(120));
  }
}
