---
name: xhs-auto-publish
description: "小红书「热点→发布」自动化流水线：抓取多源热点（微博热搜/知乎热榜/百度热搜/抖音/小红书热榜，可配置，默认 2~3 源）→ 按小红书图文/视频/动态格式做原创改写并生成封面 → 通过浏览器自动化登录小红书发布。适用于「自动发布小红书笔记」「追热点写笔记」「抓热点做种草文」「定时发小红书」「热点改成小红书格式」等需求；默认领域科技/生活。触发词：小红书、红书、笔记、热榜、热点、自动发布、种草、图文/视频/动态发布。"
---

# 小红书热点自动发布

一键完成「热点收集 → 选题改写 → 素材制作 → 发布验证」全流程。默认领域：**科技 / 生活**。

## 流程总览

按顺序推进，每阶段产物作为下一阶段输入：

1. **收集热点（Collect）** → 候选列表
2. **选题 & 小红书化改写（Rewrite）** → 笔记 JSON
3. **制作素材（Media）** → 封面/配图/视频
4. **发布 & 验证（Publish）** → 笔记链接

## 0. 前置：读配置与合规红线

- 先读 `assets/config.json`：热点源、数量、领域、形态偏好、发布账号。多源可配置，默认微博/知乎/百度 3 源。
- 合规红线（必须遵守，任一命中即停该条）：只做**原创改写**，不照搬他人图文/视频/文案；不虚假宣传、不夸大收益、不用绝对化用语；不站外导流、不诱导关注交易。

## 1. 收集热点（Collect）

按 `assets/config.json` 中 `sources` 逐个采集（默认 2~3 源）：

- **首选路径：浏览器自动化**。用 `mac_computer_use_tool`（`plane="bu"`，`import seed_browser_use as bu`）打开热榜页抓取，各源 URL 与抓取要点见 `references/hot-sources.md`。遇到登录/验证码时，**下一步立即**调 `interaction.request_action`（`type="browserControl"`），用户完成后重新观察、拿新 ref。
- **备选路径**：通用搜索或舆情追踪能力抓取各源 Top 列表。
- 把各源原始条目合并写入一个 JSON（字段：`title, source, heat, url, desc, raw_date`）。
- 运行 `scripts/normalize_hot.py` 去重、按领域关键词过滤、热度排序，输出 `candidates.json`。

输出：候选热点卡片（标题 / 来源 / 热度 / 是否命中领域），向用户展示 Top 5 并确认选题。

## 2. 选题 & 小红书化改写（Rewrite）

1. 从候选里选 1 个最贴近「科技 / 生活」且能产出原创干货的热点；优先选用户有真实体验/观点/数据的方向。
2. 按 `references/xhs-style.md` 改写为小红书格式，产出字段：
   - `title`：爆款标题（≤20 字）
   - `body`：正文（钩子开头 → 干货主体 → 互动结尾；适度 emoji、分段）
   - `topics`：话题标签（3~8 个，含 1~2 个领域标签）
   - `type`：`image`（图文）/ `video`（视频）/ `dynamic`（动态）
   - `media`：封面/配图/视频文件列表
   - `cover_prompt`：封面生成提示词（图文形态）
3. 组装成笔记 JSON，运行 `scripts/validate_note.py` 校验字段、字数与媒体文件。

## 3. 制作素材（Media）

- **图文**：封面用图片生成能力按 `cover_prompt` 生成（竖版 3:4，1080×1440），配图 2~5 张与正文呼应；也可用 `scripts/make_cover.py` 生成文字排版封面（需 Pillow）。
- **视频**：用视频生成/剪辑能力或用户素材准备视频文件，封面帧按封面规范生成。
- **动态**：通常纯文字 + 可选 1 图，无需复杂封面。
- 所有素材保存到工作目录，媒体文件必须真实存在（`validate_note.py` 会检查）。

## 4. 发布 & 验证（Publish）

1. 打开小红书发布入口（创作者中心或网页版发布页），见 `references/publish-guide.md`。
2. 首次登录/会话过期：调 `interaction.request_action`（`type="browserControl"`）让用户扫码/登录。
3. 按形态填表：图文（传图、标题、正文、话题）；视频（上传视频、封面、标题、正文、话题）；动态（短正文）。
4. **发布前**：调 `interaction.request_action`（`type="browserControl"`）让用户核对账号、内容与可见范围；用户批准后才点发布。
5. 发布后重新观察页面：抓到**已发布状态/笔记链接**才算成功；否则报告未完成，不得宣称成功。

## 配置说明

- 热点源与数量：编辑 `assets/config.json` 的 `sources` / `top_n`。
- 领域与关键词：编辑 `domains` / `keywords`（默认科技、生活）。
- 定时触发：可用定时任务按 cron 调度本流水线（建议每天 1 次）。

## 资源索引

| 用途 | 文件 |
|------|------|
| 多源热点抓取要点 | `references/hot-sources.md` |
| 小红书图文/视频/动态内容规范 | `references/xhs-style.md` |
| 浏览器发布流程 | `references/publish-guide.md` |
| 热点合并/去重/过滤脚本 | `scripts/normalize_hot.py` |
| 笔记字段校验脚本 | `scripts/validate_note.py` |
| 文字封面生成脚本 | `scripts/make_cover.py` |
| 默认配置 | `assets/config.json` |
| 笔记模板 | `assets/templates/note-template.md` |
| 发布前检查清单 | `assets/templates/publish-checklist.md` |
