# AI 协作经验系统接入（零操作版 — 把本文件发给你的 AI 即可）

## 给使用者：你只做一件事

把下面这句话发给你的 AI（把路径换成你机器上本仓库的位置）：

> 请读取 `<本仓库路径>/docs/ai/onboarding-30min.md`，严格执行其中"AI 安装程序"一节。
> 全程不需要询问我、不需要我操作；完成后按第 4 步模板汇报。

若你的 AI 无法访问该路径（未 clone 本仓库）：把本文件全文粘贴给它，附上面这句话。
本仓库不存在时，先让人把它放到你能访问的位置（clone 或解压均可），本系统不需要安装任何依赖（仅需 Python ≥3.10 做 hook）。

---

## AI 安装程序（执行对象：AI 代理）

你要完成 4 步安装。**约束：全部幂等；所有配置改动先备份、失败即回滚；不修改本仓库任何文件；不动用户的其他配置。**

### 步骤 0 · 环境自检

- 判定宿主工具与用户级配置路径：ZCode → `~/.zcode/cli/config.json` + `~/.zcode/AGENTS.md`；Claude Code → `~/.claude/settings.json` + 用户级 `CLAUDE.md`；其他工具 → 只执行步骤 1，跳过步骤 2，报告注明。
- 探测 Python：`python -c "import sys; print(sys.executable)"`，需 ≥3.10；找不到 → 跳过步骤 2 并报告。
- 记录本仓库绝对路径（你读取本文件的位置）。

### 步骤 1 · 安装快速卡（所有工具，必做）

1. 读 `<repo>/references/pattern-index.md` 的 **§0 快速版**代码块。
2. 目标文件 = 用户级 AGENTS.md / CLAUDE.md。**幂等规则**：目标已含标题行 `AI 协作策略卡（来源 dev-guidelines` → 先删除整节再插入新版；否则追加到文件末尾。
3. 除该节外不得改动文件任何其他内容。插入后回读确认。

### 步骤 2 · 接线 git 破坏性命令拦截（仅 ZCode / Claude Code）

1. 先跑回归：`python <repo>/scripts/test_hook_block_git.py`——**非全绿即停止并报告，不接线**。
2. 备份配置文件：复制为 `<原名>.bak-<今日日期>`。
3. **JSON 解析式合并**（禁止整文件覆写）：读入配置 → 保留全部既有键（如 `mcp`）→ 写入 hook 配置 → `json.load` 回读校验后完成。已存在同 matcher 的 Bash hook → 在其 `hooks` 数组内追加（按脚本路径去重），不重复建条目。
4. 配置形状（两宿主不同，路径用步骤 0 探测的绝对值）：
   - **ZCode**：`hooks.enabled=true` + `hooks.events.PreToolUse`，`type: "process"`（Windows 下不经 shell），详见 `docs/ai/hooks-setup.md`"ZCode 接线（实测验证版）"——按该节照抄，替换 python 与脚本路径。
   - **Claude Code**：`hooks.PreToolUse` 直挂数组（无 enabled/events 包裹），`type: "command"`，形状见同一文件的 Claude Code 段。
5. 拦截面只有 7 条不可逆命令；**不要**自行扩大清单（不拦 commit/push/add）。

### 步骤 3 · 自测（安全，按设计无害）

在一次性 scratch 仓验证：`mktemp -d` → `git init` → 写入一个文件并 commit → 追加一行未提交内容 → 执行 `git checkout -- <该文件>`。

- 被拦截（出现 `[block_destructive_git]`）→ hook 已生效，最好结果；
- 命令真实执行了 → 属预期：多数宿主**不热加载** hook，新会话/重启后才生效；scratch 仓是弃子，无损失。
- 结束后删除 scratch 仓。

### 步骤 4 · 按模板汇报

```
[接入报告]
宿主工具 / 配置路径 / Python：<...>
快速卡：已插入 <文件>（新增节 / 替换旧节）
hook：回归 N 项全绿；配置已合并（备份：<路径>）；JSON 校验通过 / 未接线（原因）
自测：scratch 仓被拦截 / 已执行（宿主不热加载，新会话生效）
试用期：请从今天起记录三样，第 4 周交回——①卡触发（日期+哪张卡+发生了什么）②hook 拦截（日期+命令）③不适感（一句话）
```

失败处理：任一步骤失败 → 用备份恢复对应文件 → 报告失败点与原因 → 停止，不做部分安装。

---

## 试用期判定标准（团队侧，使用者无需行动）

第 4 周回收记录 + 30 分钟访谈。三项（卡真实触发过 / 拦截发生过 / 贡献通道可用——贡献按 `common/ai/writing-reusable-patterns.md` 五步法提 PR）≥2 项成立才扩大范围。
