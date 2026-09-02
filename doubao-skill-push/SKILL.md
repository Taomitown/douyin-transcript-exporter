---
name: doubao-skill-push
description: 技能仓库一键提交与推送。当用户要求"把技能推到 GitHub""推送技能更新""一键上传技能到 git""同步技能仓库""用 skill-push 推送"时使用。标准流程：检查仓库状态 → 有改动则 add+commit（自定义或自动生成提交信息）→ push 到远程 → 核验本地与远程一致 → 报告结果。也可引导用户直接在终端使用 skill-push 命令。不用于技能内容本身的创作。
---

# 技能仓库一键推送 Skill

## Purpose

把"技能代码一键提交并推送到 GitHub"的流程固化为标准动作，避免每次手敲 git 命令。

**标准流程：检查状态 → 提交 → 推送 → 核验 → 报告**

## 前提（固定配置）

- 技能仓库路径：`/Users/alix/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills`
- 远程：`origin` → `git@github.com:Taomitown/douyin-transcript-exporter.git`（SSH 认证已就绪）
- 分支：`main`
- 忽略项：`wechat-gzh-autopilot/`（独立 git 仓库，不纳入外层跟踪）、敏感文件

## 触发与输入识别

用户提出以下任一要求即触发：

1. "把技能推到 GitHub / 推送到远程 / 上传技能"。
2. "推送技能更新 / 同步技能仓库"。
3. "一键上传 skill 到 git"。
4. 要求把技能改动提交并发布。

可选输入：提交说明（如"优化三视图模板细节"）；未提供时自动生成。

## 标准工作流

### 阶段1｜检查仓库状态

```bash
cd "/Users/alix/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills"
git status --porcelain
git status -sb
```

- 列出有改动的文件。
- 工作区干净：报告"无需推送"，结束流程。

### 阶段2｜敏感信息检查（强制门禁）

若改动涉及疑似敏感文件（`.env`、`id_rsa`、`id_ed25519`、`.pem`、`credential`、`token`、`secret` 等），**中止推送**并提示用户处理，不得提交。

### 阶段3｜提交

- 提交信息优先用用户提供的说明；未提供时按改动内容自动生成（如"更新技能：doubao-three-view-prompt"）。
- 执行：

```bash
git add -A
git commit -m "<提交信息>"
```

### 阶段4｜推送

```bash
git push origin main
```

### 阶段5｜核验

```bash
git fetch origin -q
git status -sb
git ls-remote origin
```

- 确认本地与远程一致（无 ahead/behind），远程 HEAD 与本地最新提交一致。

### 阶段6｜报告

报告：①提交说明 ②最新提交哈希 ③改动文件数 ④远程地址 ⑤本地与远程一致状态。

## 快捷命令（可选路径）

终端已安装一键命令 `skill-push`（位于 `~/.local/bin`，已在 PATH）：

```bash
skill-push                        # 自动生成提交信息
skill-push "优化三视图模板细节"    # 指定提交信息
```

流程与本 Skill 完全一致（含敏感文件拦截），可引导用户直接使用。

## 安全与边界

1. **敏感信息拦截为强制门禁**：不提交 token、密钥、凭据、环境变量文件；发现即中止。
2. `wechat-gzh-autopilot` 为独立仓库，不纳入本仓库跟踪，不强行删除或改写其内容。
3. 推送到远程是发布操作，由系统确认后执行；不在未确认时发布。
4. 不修改、不覆盖用户未要求改动的技能内容；只负责提交与推送已存在的改动。
5. 不使用 `sudo` 或绕过权限；权限问题如实说明。

## Resources

- 本 Skill 自包含，无外部 reference。
- 具体实现脚本见 `scripts/skill-push`（与终端 `skill-push` 命令逻辑一致）。
