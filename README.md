# CatAnimation

ESP32-S3 + 1.3" SH1106 OLED (I2C) GIF animation player.

Converts GIFs to OLED frame data and loops playback on a 128x64 monochrome display.

## Hardware

| Part | Model |
|------|-------|
| MCU | ESP32-S3 (N16R8) |
| OLED | 中景园电子 1.3" Blue OLED (SH1106, I2C, 128x64) |

## Wiring

| OLED Pin | ESP32-S3 GPIO |
|----------|---------------|
| VDD | 3.3V |
| GND | GND |
| SCK | GPIO 20 (SCL) |
| SDA | GPIO 21 (SDA) |

## Quick Start

### 1. Requirements

Only the ESP32 Arduino core is needed — **no third-party libraries required**. The project uses a hand-written SH1106 I2C driver based on the manufacturer's C51 reference code.

### 2. Upload

1. Open `CatAnimation.ino` in Arduino IDE
2. Board: **ESP32S3 Dev Module**
3. PSRAM: **OPI PSRAM**
4. USB CDC On Boot: **Enabled**
5. Compile & upload

### 3. Use your own GIF

```bash
pip install Pillow
python convert.py "your-file.gif" "gif_frames.h"
```

Then recompile and upload.

## Files

| File | Purpose |
|------|---------|
| `CatAnimation.ino` | Main sketch: SH1106 driver + animation loop |
| `gif_frames.h` | Frame data in SH1106 page-column native format |
| `convert.py` | GIF → frame data conversion tool |

## Technical Details

- **Data format**: SH1106 page-column native (8 pages x 128 bytes, each byte = 8 vertical pixels)
- **Driver**: Raw Wire I2C, following manufacturer's C51 reference code
- **Framerate**: ~10 FPS (100ms/frame)
- **I2C**: Address 0x3C, 400kHz

## License

MIT
