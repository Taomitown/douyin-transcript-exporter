#!/usr/bin/env python3
"""合并多源热点条目 → 去重、按领域关键词过滤、热度排序，输出 candidates.json。

输入：一个 JSON 数组，元素字段：title, source, heat, url, desc, raw_date
输出：candidates.json（去重 + 领域命中优先 + 热度降序，截取 top_n）
用法：
  python3 normalize_hot.py raw_hot.json --config assets/config.json --top 10 --output candidates.json
"""
import argparse
import json
import re
import sys


def normalize(items):
    """按归一化标题去重，保留热度更高者。"""
    seen = {}
    for it in items:
        title = (it.get("title") or "").strip()
        if not title:
            continue
        key = re.sub(r"[\s#【】\[\]（）()！!？?]", "", title).lower()
        if key in seen:
            if (it.get("heat") or 0) > (seen[key].get("heat") or 0):
                seen[key] = it
            continue
        seen[key] = it
    return list(seen.values())


def hits_keywords(item, keywords):
    text = (item.get("title") or "") + " " + (item.get("desc") or "")
    return [k for k in keywords if k.lower() in text.lower()]


def main():
    ap = argparse.ArgumentParser(description="Normalize multi-source hot items")
    ap.add_argument("input", help="raw hot items JSON file (list of dicts)")
    ap.add_argument("--config", default=None, help="config.json path (keywords/domains/top_n)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--output", default="candidates.json")
    args = ap.parse_args()

    config = {}
    if args.config:
        with open(args.config, encoding="utf-8") as f:
            config = json.load(f)
    keywords = config.get("keywords", []) or []
    domains = config.get("domains", []) or []
    top = args.top or config.get("top_n") or 10

    with open(args.input, encoding="utf-8") as f:
        items = json.load(f)

    items = normalize(items)
    for it in items:
        it["matched"] = hits_keywords(it, keywords + domains)

    # 领域命中优先，其次热度
    items.sort(key=lambda x: (bool(x["matched"]), x.get("heat") or 0), reverse=True)
    out = items[:top]

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[normalize_hot] 去重后 {len(items)} 条，输出 Top {len(out)} → {args.output}")
    for it in out:
        tag = ",".join(it["matched"]) if it["matched"] else "-"
        print(f"  [{it.get('source', '?')}] 热度={it.get('heat', '-')} 领域={tag} {it['title'][:34]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
