#!/usr/bin/env python3
"""校验待发布笔记 JSON：字段完整性、字数、媒体文件存在性。

用法：
  python3 validate_note.py note.json --base-dir <媒体相对路径基准>
校验通过返回 0；否则返回 1 并列出问题。
"""
import argparse
import json
import os
import sys

TYPE_IMAGE = "image"
TYPE_VIDEO = "video"
TYPE_DYNAMIC = "dynamic"
VALID_TYPES = (TYPE_IMAGE, TYPE_VIDEO, TYPE_DYNAMIC)


def check(note, base_dir):
    errors = []
    title = note.get("title", "")
    body = note.get("body", "")
    topics = note.get("topics", []) or []
    ntype = note.get("type", "")
    media = note.get("media", []) or []

    if not title:
        errors.append("title 为空")
    elif len(title) > 20:
        errors.append(f"title 超过 20 字（当前 {len(title)} 字）")
    if not body:
        errors.append("body 为空")
    elif len(body) < 50:
        errors.append(f"body 过短（当前 {len(body)} 字，建议 ≥50）")
    if ntype not in VALID_TYPES:
        errors.append(f"type 非法：{ntype}（应为 {VALID_TYPES}）")
    if not topics:
        errors.append("topics 为空（建议 3~8 个话题标签）")
    elif len(topics) > 8:
        errors.append(f"topics 过多（当前 {len(topics)} 个，建议 ≤8）")
    if ntype == TYPE_IMAGE and len(media) < 1:
        errors.append("图文（image）至少需要 1 张图")
    if ntype == TYPE_VIDEO and len(media) < 1:
        errors.append("视频（video）需要视频文件")
    for m in media:
        p = m if os.path.isabs(m) else os.path.join(base_dir, m)
        if not os.path.exists(p):
            errors.append(f"媒体文件不存在：{m}")

    return errors


def main():
    ap = argparse.ArgumentParser(description="Validate a note JSON before publishing")
    ap.add_argument("input", help="note JSON path")
    ap.add_argument("--base-dir", default=".", help="relative media base dir")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        note = json.load(f)

    errors = check(note, args.base_dir)
    if errors:
        print("[validate_note] FAIL")
        for e in errors:
            print("  -", e)
        return 1

    print("[validate_note] OK  "
          f"title={len(note.get('title', ''))}字 body={len(note.get('body', ''))}字 "
          f"topics={len(note.get('topics', []))} media={len(note.get('media', []))} type={note.get('type')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
