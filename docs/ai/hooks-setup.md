# Git 破坏性命令护栏 hook 接线指南

`scripts/hooks/block_destructive_git.py` 把用户级 AGENTS.md 的 git 破坏性操作护栏从自然语言下沉为 PreToolUse 运行时拦截。配置一次后，宿主在执行任何 Bash 命令前都会把命令交给本脚本判定，命中高危清单即拒绝。

## 拦截什么

高危清单（7 条，与用户级 AGENTS.md 一致的子集）：

| 模式 | 说明 |
|------|------|
| `git checkout -- <path>` / `git checkout <ref> -- <path>` | `--` 分隔的路径式还原，不可逆丢弃未提交改动 |
| `git reset --hard` | 丢弃工作区/暂存区 |
| `git clean -f`（含 `-fd` `-xdf` `--force`） | 强制删除未跟踪文件 |
| `git stash drop` / `git stash clear` | 不可逆丢弃 stash |
| `git branch -D`（含 `--delete --force`） | 强删未合并分支 |

**不拦**：`git checkout -p` / `--patch`（AGENTS.md 推荐的细粒度回退工具）、`reset --soft`、`clean -n`、`stash push`、`branch -d` 等安全操作。

变体容忍：引号包裹子命令、多余空白、`git -C <path>`、`-c <k=v>`、env 前缀（`FOO=1 git ...`）、其他全局选项、复合语句（`&&` `;` `|` 换行，引号内不分隔）、命令替换（`$(git reset --hard)`、反引号——由二级文本网兜底）。

## 拦截协议（以宿主当前文档为准）

依据 Claude Code hooks 文档（https://code.claude.com/docs/en/hooks ，核对于 2026-09）：

- **输入**：stdin 一个 JSON 对象，命令在 `tool_input.command`。
- **放行**：exit 0，无输出。
- **拒绝协议 A（默认）**：exit 2 + stderr 说明，宿主把 stderr 作为拒绝理由反馈给模型。
- **拒绝协议 B**：`--output json` → exit 0 + stdout JSON `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}`。

拒绝理由中固定包含只读核查指引（先 `git diff HEAD -- <path>` / `git status`）与细粒度替代工具（Edit 逐 hunk / `git checkout -p` / `git stash push`）。

## Claude Code 接线（可照抄）

`.claude/settings.json`（项目级）或 `~/.claude/settings.json`（用户级）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PROJECT_DIR}/scripts/hooks/block_destructive_git.py\""
          }
        ]
      }
    ]
  }
}
```

- `matcher` 用 `Bash|PowerShell`（官方文档对 shell 命令检查的建议写法）；Windows 上 shell form 经 Git Bash 执行。
- 仓库不在项目根时，把 `${CLAUDE_PROJECT_DIR}` 换成本仓库绝对路径。
- 需要拒绝协议 B 时，在 command 末尾加 ` --output json`。

## ZCode 接线

ZCode 的 hook 配置与 Claude Code 同构（`.zcode/settings.json`，`PreToolUse` 事件 + `matcher` + `type: command`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python C:/build/dev-guidelines/scripts/hooks/block_destructive_git.py"
          }
        ]
      }
    ]
  }
}
```

**注意**：hook 协议细节各家迭代很快，字段名与配置位置以宿主**当前版本文档**为准，不要照抄本文示例里的字段名；接入后务必先用下面的自测命令在真实会话里验证一次拦截。

## 手动自测

不接宿主、直接验证脚本行为：

```bash
# 应拦截（exit 2，stderr 带只读核查指引）
echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}' \
  | python scripts/hooks/block_destructive_git.py

# 应放行（exit 0，无输出）
echo '{"tool_name":"Bash","tool_input":{"command":"git checkout -p HEAD~1 -- f"}}' \
  | python scripts/hooks/block_destructive_git.py

# JSON 决议协议
echo '{"tool_name":"Bash","tool_input":{"command":"git clean -fd"}}' \
  | python scripts/hooks/block_destructive_git.py --output json

# 全量回归
python scripts/test_hook_block_git.py
```

## 被拦截后怎么办

1. 先只读核查：`git diff HEAD -- <path>`、`git status`，看清影响范围。
2. 按目标改用细粒度工具：局部改动用 Edit 逐 hunk 改写；选择性回退用 `git checkout -p`；可逆暂存用 `git stash push`。
3. 确属误拦（安全操作被拦）→ 在仓库提 issue 并附触发命令原文，不要绕过。

## 已知缺口（演进材料）

- `git restore`（checkout 的现代等价物）未列入清单。
- `git checkout .` / `git checkout <path>`（无 `--` 的路径式还原）：路径与分支名无法从命令串确定性区分，不拦；同理"强制切换分支覆盖改动"不可判定。
- 二级文本网为保安全偏向误拦：`echo "run git reset --hard"` 这类引用高危词的 echo 也会被拦。
- 配置目前硬编码在脚本 `DESTRUCTIVE_RULES`；外置到 `config/policy.yml` 属于演进 Phase 5。
