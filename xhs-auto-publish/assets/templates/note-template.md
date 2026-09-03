# 笔记 JSON 模板

复制下面的结构组装待发布笔记，字段含义见 `references/xhs-style.md`。

```json
{
  "title": "（≤20 字爆款标题）",
  "body": "（正文：钩子开头 → 干货主体 → 互动结尾，适度 emoji、分段）",
  "topics": ["#科技", "#AI工具", "#效率神器"],
  "type": "image",
  "media": ["cover.png", "img2.png", "img3.png"],
  "cover_prompt": "（图文形态封面生成提示词：竖版3:4、主体、标题字、配色）",
  "source": "（热点来源与标题，便于追溯）"
}
```

字段说明：
- `type`：`image`（图文）/ `video`（视频）/ `dynamic`（动态）
- `media`：封面/配图/视频文件列表（相对路径或绝对路径，须真实存在）
- `cover_prompt`：仅图文需要，供图片生成能力使用
