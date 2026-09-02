# Doubao 漫剧制作技能集

豆包工作台「漫剧制作」技能集，支持从写小说到出图提示词的完整链路，也可单阶段独立使用。

## 技能清单

| Skill | 功能 |
|---|---|
| doubao-manhua-pipeline | 漫剧制作全流程总控：路由与串联四阶段，支持一条龙与单阶段 |
| doubao-original-novel | 自写小说·原创全流程（抖音漫剧叙事逻辑） |
| doubao-novel-to-script | 小说转剧本·漫剧改编全流程 |
| doubao-script-to-storyboard | 剧本转分镜·即梦/Seedance 2.0 适配全流程 |
| doubao-three-view-prompt | 三视图提示词生成（人物/兵器/神兽/法宝/道具/场景） |

## 全流程数据链路

```
[题材 + 字数 + 大纲]
   → doubao-original-novel        （写小说）→ 小说全文
   → doubao-novel-to-script       （转剧本）→ 完整剧本
   → doubao-script-to-storyboard  （转分镜）→ 完整分镜词（含豆包10秒版）
   → doubao-three-view-prompt     （三视图，复用小说原文）→ 全部三视图提示词
```

## 使用说明

- 每个 Skill 独立可装、独立可用。
- 各 Skill 的详细规则见各自 SKILL.md 与 references 目录。
- 硬约束：原创版权规避、剧情忠于原著、合规核查、先等输入再输出，全程生效。
