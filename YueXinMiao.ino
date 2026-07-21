/*
 * YueXinMiao — 月薪喵 OLED 动画
 * ESP32-S3 + SH1106 I2C OLED (128x64)
 *
 * 接线: VDD→3.3V  GND→GND  SCK→GPIO20  SDA→GPIO21
 * 零依赖: 不需要 U8g2 / Adafruit 等任何库
 */

#include <Arduino.h>
#include <Wire.h>
#include "frames/gif_frames.h"

#define SDA_PIN  21
#define SCL_PIN  20

// ── SH1106 I2C 驱动 ──

static void cmd(uint8_t c) {
  Wire.beginTransmission(0x3C);
  Wire.write(0x00);
  Wire.write(c);
  Wire.endTransmission();
}

static void init_oled() {
  cmd(0xAE); cmd(0x02); cmd(0x10); cmd(0x40); cmd(0xB0);
  cmd(0x81); cmd(0xFF); cmd(0xA1); cmd(0xA6);
  cmd(0xA8); cmd(0x3F); cmd(0xC8); cmd(0xD3); cmd(0x00);
  cmd(0xD5); cmd(0x80); cmd(0xD8); cmd(0x05);
  cmd(0xD9); cmd(0xF1); cmd(0xDA); cmd(0x12);
  cmd(0xDB); cmd(0x30); cmd(0x8D); cmd(0x14); cmd(0xAF);
}

static void draw_frame(int n) {
  for (int page = 0; page < 8; page++) {
    Wire.beginTransmission(0x3C);
    Wire.write(0x00);
    Wire.write(0xB0 | page);
    Wire.write(0x02);
    Wire.write(0x10);
    Wire.endTransmission();

    Wire.beginTransmission(0x3C);
    Wire.write(0x40);
    Wire.write(all_frames + n * FRAME_SIZE + page * 128, 128);
    Wire.endTransmission();
  }
}

int frame = 0;
unsigned long last = 0;

void setup() {
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(400000);
  init_oled();
}

void loop() {
  unsigned long now = millis();
  if (now - last < 100) return;
  last = now;
  draw_frame(frame);
  frame++;
  if (frame >= FRAME_COUNT) frame = 0;
}
