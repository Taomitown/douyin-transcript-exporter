# 多源热点抓取要点

本文件说明各热点源的抓取方式。**首选浏览器自动化**（`mac_computer_use_tool`，`plane="bu"`，`import seed_browser_use as bu`），用 `bu.navigate()` → `bu.read_all()` / `bu.get_page_text()` 提取 Top 列表；备选用通用搜索或舆情追踪能力。

通用流程：
1. 打开热榜页 → 观察 → 用 `bu.read_all()` 抽取「标题 + 热度」条目，`limit` 取 Top 15~30。
2. 记录每条：`title, source, heat, url, raw_date`。
3. 遇到登录/验证码 → 调 `interaction.request_action`（`type="browserControl"`），完成后重新观察。
4. 各源结果合并后交 `scripts/normalize_hot.py` 去重过滤。

## 源清单

| 源 key | 名称 | 入口 | 是否需要登录 |
|--------|------|------|--------------|
| `weibo` | 微博热搜 | `https://s.weibo.com/top/summary`（或 `weibo.com/hot`） | 看榜单通常无需登录 |
| `zhihu` | 知乎热榜 | `https://www.zhihu.com/hot` | 看榜单无需；展开正文可能需登录 |
| `baidu` | 百度热搜 | `https://top.baidu.com/board?tab=realtime` | 无需 |
| `douyin` | 抖音热点 | `https://www.douyin.com/hot` | 常需登录/验证，按需降级 |
| `xhs` | 小红书热榜/发现 | `https://www.xiaohongshu.com/explore` 或创作者中心 | 通常需登录 |

## 各源抓取要点

- **weibo**：榜单条目含「标题 + 热度值（如"新"或数字）」；热度字段缺失时标 `null`，不编造。
- **zhihu**：热榜每项含标题 + 热度（"xxx 万热度"）；可解析热度数字，缺失标 `null`。
- **baidu**：`top.baidu.com` 实时榜含标题 + 搜索指数（如"xxx 万"）。
- **douyin**：热点榜含标题 + 热度标签（"热/新/爆"）；若被登录墙拦截，按登录 handoff 处理或跳过并说明。
- **xhs**：无公开独立热榜页时，抓「发现页」热门笔记标题/话题，或按领域关键词搜热门笔记；记录为站内热度信号。

## 抓取后处理

- 合并各源原始条目到一个 JSON（`title, source, heat, url, desc, raw_date`）。
- 运行 `scripts/normalize_hot.py raw_hot.json --config assets/config.json`。
- 输出 `candidates.json`：按「领域命中优先 → 热度降序」排序，取 Top N。

## 配置字段（assets/config.json）

```json
{
  "sources": ["weibo", "zhihu", "baidu"],
  "top_n": 10,
  "domains": ["科技", "生活"],
  "keywords": ["科技", "AI", "数码", "效率", "工具", "生活", "技巧", "避坑", "好物"],
  "content_type_preference": ["image", "video", "dynamic"],
  "account": "小红书账号名",
  "schedule": "daily"
}
```

- `sources`：启用哪些源；`top_n`：最终候选数量；`domains`/`keywords`：领域过滤用词；`content_type_preference`：形态偏好顺序；`account`：发布前核对的账号名；`schedule`：定时频率备注。
