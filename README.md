# YueXinMiao

> 月薪喵 — ESP32-S3 + SH1106 I2C OLED 动画小玩具

让一只猫在 1.3 寸单色 OLED 上蹦跶。GIF 转帧 → 单片机循环播放，零依赖、纯手写驱动。

## 它能干什么

把一张 GIF 动图丢进 Python 脚本，吐出一帧一帧的 C 数组，ESP32-S3 读到后逐帧推到 SH1106 OLED 上。猫就在屏幕上跑起来了。

## 硬件

| 东西 | 型号 |
|------|------|
| 主控 | ESP32-S3 N16R8 (淘宝通用开发板) |
| 屏幕 | 中景园 1.3 寸蓝色 OLED (SH1106 驱动, I2C, 128×64) |

## 接线

| 屏幕针脚 | 接 ESP32-S3 |
|----------|-------------|
| VDD | 3.3V |
| GND | GND |
| SCK | GPIO 20 |
| SDA | GPIO 21 |

> 这块屏幕的引脚标的是 SCK/SDA，其实就是 I2C 的 SCL/SDA。

## 怎么跑

1. Arduino IDE 打开 `YueXinMiao.ino`
2. 开发板选 **ESP32S3 Dev Module**，PSRAM 设 **OPI PSRAM**，**USB CDC On Boot** 开
3. 编译，上传
4. 猫开始跳

> 不需要装任何 Arduino 库。驱动是翻中景园 C51 例程照着写的，裸 Wire I2C，不依赖 U8g2 也不依赖 Adafruit。

## 换动画

```bash
pip install Pillow
python tools/convert.py 你的猫.gif frames/gif_frames.h
```

然后重新编译。

## 文件说明

```
YueXinMiao/
├── YueXinMiao.ino        # 主程序：SH1106 初始化 + 帧循环
├── frames/
│   └── gif_frames.h      # 自动生成的帧数据（SH1106 page-column 格式）
├── tools/
│   └── convert.py        # GIF → 帧数据转换脚本
└── README.md
```

## 技术细节

- **数据格式**: SH1106 page-column 原生布局，每字节对应一列 8 个纵向像素。这和常见 XBM 格式互为转置，所以不能直接用 U8g2 的 `drawXBM`
- **驱动**: 纯 `Wire` 手写，初始化序列照自中景园 C51 参考代码
- **帧率**: 约 10 FPS，I2C 跑 400kHz
- **I2C 地址**: `0x3C`

## 类似的猫

- [YueXinCat](https://github.com/EatFans/YueXinCat) — ESP32 Arduino 版，使用 Adafruit 库
- [MonthSalaryCat](https://github.com/ddexerdong/MonthSalaryCat) — STM32 HAL 版，结构最完整
- [ESP32yuexinmiao](https://github.com/MYKNBSHK11/ESP32yuexinmiao) — ESP32-S3 SPI 彩屏版，LVGL 驱动

## License

MIT
