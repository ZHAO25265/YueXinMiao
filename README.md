# 月薪喵 — ESP32-S3 + SH1106 I2C OLED 动画

## 硬件

| 东西 | 型号 |
| -- | -------------- |
| 主控 | ESP32-S3 N16R8 |
| 屏幕 | 1.3寸 OLED |

## 接线

| 屏幕针脚 | 接 ESP32-S3 |
| ---- | ---------- |
| VDD  | 3.3V       |
| GND  | GND        |
| SCK  | GPIO 20    |
| SDA  | GPIO 21    |

> 如这块屏幕的引脚标的是 SCK/SDA，其实就是 I2C 的 SCL/SDA。

## 跑

1. Arduino IDE 打开 `YueXinMiao.ino`
2. 开发板选 **ESP32S3 Dev Module**，PSRAM 设 **OPI PSRAM**，**USB CDC On Boot** 开
3. 编译，上传
4. 猫开始跳

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
- **帧率**: 约 10 FPS，I2C 跑 400kHz
- **I2C 地址**: `0x3C`

## License

MIT
