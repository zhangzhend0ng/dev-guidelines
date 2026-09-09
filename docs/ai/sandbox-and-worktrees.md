# 沙箱与 Worktree：爆炸半径控制边界

**定位：worktree 是并发边界，不是安全边界。** 本文说明何时用独立 worktree 控制改动的影响范围，以及它与运行时 hook（L3）、宿主权限系统在防线上的分工。

## 1. 三层防线的分工

| 机制 | 层 | 防的是什么 | 防不了什么 |
|------|----|------------|------------|
| 权限系统（宿主 allow/ask/deny） | 架构 | 工具能力本身（能否写文件、能否联网） | 合法工具被用于破坏性目的 |
| PreToolUse hook（`scripts/hooks/block_destructive_git.py`） | 运行时 | 具体高危命令形态（`reset --hard` 等，见 `config/policy.yml`） | 清单外的破坏形态（`git restore`、无 `--` 的路径式 checkout）、命令替换 |
| 独立 worktree | 架构 | 爆炸半径——出问题时受限在工作区内 | 仓库级操作（见第 3 节局限） |

三者是叠加关系，不是替代关系：hook 拦"已知高危命令"，权限拦"能力"，worktree 限制"出事后波及的范围"。

## 2. 何时使用独立 worktree

满足任一条件时，用 `git worktree add <path> <branch>` 把改动隔离到独立工作区：

- 改动规模大或不确定（多文件、重构、依赖升级），主工作区还有其他未提交工作；
- 需要并行推进两条互不干扰的验证线；
- 执行 agent 的自主度较高（T3/T4），希望把"误操作损害"限制在一个可整体丢弃的目录里。

worktree 的正确抽象是**并发与丢弃单位**：隔离失败、隔离实验、隔离并行流。它给的不是安全保证——worktree 内跑的 hook、权限与主工作区完全相同。

## 3. Worktree 的局限（不是沙箱）

- **共享同一个 `.git`。** 对象库、refs、stash、config 都是仓库级的：在 worktree 里 `git branch -D`、改 config、`stash drop`，影响是全局的，主工作区一起受损。
- **hook 高危清单仍然生效也仍然必要**——worktree 不会让 `reset --hard` 变安全，只会缩小它波及的检出文件范围。
- **不隔离文件系统与凭据。** worktree 目录能读到的环境变量、SSH key、全局 gitconfig 与主工作区相同；不要把 worktree 当敏感数据边界用。
- **跨 worktree 的 ref 竞争依然存在**：两个 worktree 检出同一分支会被 git 拒绝，但顺序操作同一分支的竞态要靠流程纪律（约定谁拥有哪个分支）。

## 4. 操作纪律

- 进入 worktree 前先确认主工作区的未提交改动已提交或 stash（可逆暂存）——worktree 删除（`git worktree remove`）不保护其中未提交的工作。
- worktree 内同样适用 git 破坏性命令护栏（hook 在宿主层拦截，与工作区无关）；人工操作时同样先只读核查（`git diff HEAD -- <path>` / `git status`）再动手。
- 实验性 worktree 的预期生命周期是"用完即弃"：合入或删除，不留长期分支僵尸。

## 参见

- [Git 破坏性命令护栏 hook 接线](hooks-setup.md) — L3 运行时防线
- [Harness Evolution and Lifecycle Governance](../../common/meta/harness-evolution.md) — 本文所属的约束体系演进的治理规则
- 用户级 AGENTS.md「Git 破坏性操作护栏」— 本仓库护栏规则的原始出处（1956 行丢失事故）
