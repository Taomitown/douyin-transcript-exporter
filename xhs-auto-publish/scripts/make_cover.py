#!/usr/bin/env python3
"""生成文字排版封面（竖版 3:4，1080×1440），适合图文笔记的确定性封面。

依赖 Pillow；若不可用则明确报错并提示改用图片生成能力。
用法：
  python3 make_cover.py --title "3个AI提效小工具" --subtitle "科技生活 | 实测好用" --output cover.png
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="Generate a text-based XHS cover (1080x1440)")
    ap.add_argument("--title", required=True, help="cover main title")
    ap.add_argument("--subtitle", default="", help="cover subtitle")
    ap.add_argument("--output", default="cover.png")
    ap.add_argument("--bg", default="#FFFFFF", help="background color")
    ap.add_argument("--fg", default="#111111", help="text color")
    args = ap.parse_args()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as e:
        print(f"[make_cover] 不可用：Pillow 未安装（{e}）。请改用图片生成能力按封面规范生成。")
        return 2

    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), args.bg)
    d = ImageDraw.Draw(img)

    font = None
    for fp in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 88)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    # 简单自动换行（按画布宽度）
    lines, cur = [], ""
    for ch in args.title:
        if d.textlength(cur + ch, font=font) > W - 160:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    lines = lines[:6]

    y = 420
    for ln in lines:
        w = d.textlength(ln, font=font)
        d.text(((W - w) / 2, y), ln, fill=args.fg, font=font)
        y += 130

    if args.subtitle:
        sub_font = font if font is None else font
        w = d.textlength(args.subtitle, font=sub_font)
        d.text(((W - w) / 2, y + 30), args.subtitle, fill=args.fg, font=sub_font)

    img.save(args.output)
    print(f"[make_cover] 已生成 {args.output} ({W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
