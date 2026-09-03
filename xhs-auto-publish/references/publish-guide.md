# 小红书发布流程（浏览器自动化）

发布通过浏览器自动化完成。权威执行规则以 `browser-use-automation-mac` 的 `references/xiaohongshu/publish.md` 为准，本文件是流水线内的落地步骤。

## 入口

- 网页版发布：`https://www.xiaohongshu.com/explore` 右上角「发布笔记」；或创作者中心 `https://creator.xiaohongshu.com` 的发笔记入口。
- 用 `mac_computer_use_tool`（`plane="bu"`）打开并操作。

## 登录处理

- 首次或会话过期：页面出现登录/扫码/验证 → **立即**调 `interaction.request_action`（`type="browserControl"`），提示用户扫码/登录后交回控制权。
- 返回后重新 `bu.snapshot()` 观察，使用全新 ref，不沿用旧 ref。

## 图文发布步骤

1. 新建笔记 → 进入「上传图片」；本地图片用 `bu.upload(ref, 绝对路径)`，或调 `interaction.request_action`（`type="fileUpload"`）让用户选择。
2. 确认图片数量与顺序与笔记 JSON 一致。
3. 用新 ref 填：标题（title）、正文（body）、话题（topics）、可见范围。
4. 预览检查：无截断、无重复文字、账号正确、媒体正确。

## 视频发布步骤

1. 新建「视频笔记」，上传视频文件（`bu.upload` / `fileUpload`）。
2. 设置封面帧（可用 `cover.png` 或自动选帧）。
3. 填标题、正文、话题、可见范围，预览检查。

## 动态发布步骤

1. 用「发动态」入口，填短正文（≤100 字），可附 1 图。
2. 填话题，检查可见范围。

## 发布前确认（必做）

点发布前，调 `interaction.request_action`（`type="browserControl"`）：
- 说明将发布到哪个账号、笔记主题、形态、可见范围；
- 请用户核对后选择发布或取消；用户未批准不点发布。

## 发布后验证（必做）

- 点发布后重新观察页面：找到**已发布成功提示或笔记链接**才算成功。
- 只填好了编辑器、发布按钮仍禁用，不算发布成功；如实报告状态。

## 常见问题

- 上传后预览未出现 → 重新观察或重传该文件，不跳过。
- 发布按钮灰色 → 检查必填字段（标题/正文/媒体）是否齐全。
- 被登录墙/风控拦截 → handoff 给用户处理，不自行绕过。
