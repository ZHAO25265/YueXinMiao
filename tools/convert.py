#!/usr/bin/env python3
"""
GIF -> SH1106 OLED frame data (page-column format)
SH1106 RAM: 8 pages x 128 columns, each byte = 8 vertical pixels
"""

from PIL import Image
import os, sys

def gif_to_frames(gif_path, width=128, height=64):
    img = Image.open(gif_path)
    frames = []

    try:
        while True:
            frame = img.convert('L')
            orig_w, orig_h = frame.size
            scale = min(width / orig_w, height / orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            frame = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)

            canvas = Image.new('L', (width, height), 0)
            offset_x = (width - new_w) // 2
            offset_y = (height - new_h) // 2
            canvas.paste(frame, (offset_x, offset_y))
            canvas = canvas.point(lambda x: 255 if x > 127 else 0, '1')

            # SH1106 page-column format:
            # 8 pages (0-7), each page = 128 bytes (columns 0-127)
            # Each byte: bit0=top pixel, bit7=bottom pixel of column
            frame_bytes = []
            for page in range(height // 8):
                for col in range(width):
                    byte = 0
                    for row in range(8):
                        y = page * 8 + row
                        if canvas.getpixel((col, y)):
                            byte |= (1 << row)
                    frame_bytes.append(byte)
            frames.append(frame_bytes)
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return frames


def write_header(frames, output_path):
    count = len(frames)
    size = len(frames[0])
    total = count * size

    lines = []
    lines.append("// Auto-generated SH1106 page-column format")
    lines.append(f"// Frames: {count}, Resolution: 128x64")
    lines.append(f"// Format: 8 pages x 128 bytes, each byte = 8 vertical pixels")
    lines.append(f"// Total: {total} bytes")
    lines.append("")
    lines.append("#ifndef GIF_FRAMES_H")
    lines.append("#define GIF_FRAMES_H")
    lines.append("")
    lines.append("#include <Arduino.h>")
    lines.append("")
    lines.append(f"#define FRAME_COUNT {count}")
    lines.append(f"#define FRAME_WIDTH 128")
    lines.append(f"#define FRAME_HEIGHT 64")
    lines.append(f"#define FRAME_SIZE {size}")
    lines.append("")
    lines.append(f"// flat array: frame[n] at all_frames[n * FRAME_SIZE]")
    lines.append(f"const unsigned char all_frames[{total}] PROGMEM = {{")

    for fi, frame in enumerate(frames):
        lines.append(f"  // Frame {fi}")
        for j in range(0, len(frame), 16):
            chunk = frame[j:j+16]
            hexes = ", ".join(f"0x{b:02X}" for b in chunk)
            if j + 16 < len(frame) or fi < count - 1:
                lines.append(f"  {hexes},")
            else:
                lines.append(f"  {hexes}")

    lines.append("};")
    lines.append("")
    lines.append("#endif // GIF_FRAMES_H")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

    print(f"Done: {count} frames, {total} bytes -> {output_path}")


if __name__ == "__main__":
    gif_path = sys.argv[1] if len(sys.argv) > 1 else r"D:\TUPIAN\jumping.gif"
    output = sys.argv[2] if len(sys.argv) > 2 else "gif_frames.h"

    if not os.path.exists(gif_path):
        print(f"ERROR: file not found: {gif_path}")
        sys.exit(1)

    print(f"Converting: {gif_path} -> {output}")
    frames = gif_to_frames(gif_path)
    write_header(frames, output)
