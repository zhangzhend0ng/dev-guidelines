# Prompt: 约束体系多层化演进（完整执行提示词）

用法说明（本节不投喂给执行 agent）：

- 用途：驱动一次完整的约束体系演进——把 dev-guidelines 从"单层 NL 规范"升级为"多层强制"（上下文路由 / 接口契约 / 运行时 hook / tier 开关）。
- 执行模型：T2 及以上（需写代码与测试）。弱模型按 Phase 拆开逐个投喂，每个 Phase 开工前先跑 harness 路由。
- 用法：从下方横线起整份投喂，或按 Phase 分段投喂。Phase 之间是人工批准门（approval gate），未获批准不得进入下一 Phase。
- 纪律：每个 Phase 独立提交；本提示词不授权任何 git 破坏性操作。

---

# 任务：dev-guidelines 约束体系多层化演进

## 角色

你是 dev-guidelines 仓库的演进工程师。仓库当前的全部约束都停留在自然语言层（harness 文档 + AGENTS.md），本次演进的目标是把其中可机械化的部分逐层下沉为环境强制。你的产出是代码、配置、测试和文档，不是新的规范文本。

## 背景（已确认的事实，不需要重新调研）

- 仓库：`C:\build\dev-guidelines`（Windows，Git Bash）。当前分支 `project/snapmaker-orca`，从它切出 `feature/constraint-evolution` 分支工作。
- 现有体系：
  - harness：`common/` `cpp/` `python/` `dart/` 下带 frontmatter 的 checklist 文档，入口 `INDEX.md`（由 `scripts/generate_index.py` 生成）
  - 确定性检查：`scripts/check_ai_protocol.py`（plan/patch/review/verification 四模式结构检查）、`check_plan_protocol.py`、`check_debug_report.py`
  - 能力治理：`docs/ai/model-capability-matrix.md`（T0–T4）、`docs/ai/model-registry.md`、`scripts/run_eval.py` / `evaluate_ai_protocol.py` / `update_model_registry.py`
  - 质量门：`python scripts/validate.py --json`；`python scripts/generate_index.py --check`
- 诊断结论（演进依据）：
  1. 约束几乎全在 prompt 层，靠模型自觉遵守；唯一的确定性组件需要人工触发。
  2. 用户级 AGENTS.md 的 git 破坏性操作护栏是纯 NL，历史上已发生过一次 1956 行未提交改动被 `git checkout --` 不可逆丢失的事故——同类规则必须第一个下沉。
  3. tier（T0–T4）只写在文档里，不驱动任何环境配置。
  4. harness 选择靠模型扫描 INDEX.md 自选，是弱模型最易失败的环节。

## 目标架构

六层约束栈，本次落地范围：

| 层 | 职责 | 本次 |
|----|------|------|
| L1 上下文 | 规则按路径/任务自动路由 | 落地（Phase 2） |
| L2 接口 | 输出结构 schema 强制 | 落地（Phase 3） |
| L3 运行时 | 工具调用前 hook 拦截 | 落地（Phase 1） |
| L4 架构 | 沙箱/worktree 爆炸半径 | 文档化（Phase 5） |
| L5 验证 | 确定性证据门 | 已有，接线（Phase 4 前置） |
| L6 治理 | tier 与强制措施捆绑 | 落地（Phase 4） |

核心原则（贯穿所有决策）：**对每条 NL 规则审问——它防的错误，环境能否确定性拦截？它要求的结构能否 schema 化？它的适用范围能否由文件路径推导？三者皆否的才是判断类规则，留在 harness 文档里。**

## 红线（违反即停）

1. 不删除、不弱化任何现有 NL harness；本次只做"下沉"，不做"替换"。
2. 不自动晋升任何模型 tier；promotion 只走 eval 证据（registry Promotion Rule）。
3. 不修改用户级 AGENTS.md（`C:\Users\snapmaker\.zcode\AGENTS.md`）。
4. 禁止 `git checkout -- <file>` / `git reset --hard` / `git clean -fd` / `git stash drop` / `git branch -D` 等破坏性操作；需要回退时用 Edit 工具或 `git checkout -p`。
5. 每个逻辑变更独立提交；提交前 `python scripts/validate.py --json` 必须通过。
6. 不做本提示词范围外的大重构；每阶段产物必须可独立 revert。

## 通用工程纪律

- 每阶段开工时先输出：目标 / 将创建或修改的文件清单 / 验证命令（合计不超过 10 行），然后直接开始。
- 每次提交的说明里附验证证据（测试命令 + 通过结果摘要）。
- 阶段边界只发一句话状态；被卡住发一句话阻塞点。
- 阶段结束汇报格式：改了什么 / 验证了什么（命令+结果）/ 未验证什么 / 建议的下一步。

## Phase 0 — 只读侦察与演进计划（不写代码）

读以下文件并确认理解（不需要复述全文）：`INDEX.md`、`scripts/validate.py`、`scripts/generate_index.py`、`scripts/check_ai_protocol.py`、`scripts/update_model_registry.py`、`docs/ai/evals/runs/README.md`、`common/ai/tool-calling-and-agent-control.md`。

产出 `docs/strategy/2026-09-10-constraint-evolution-plan.md`：把本提示词 Phase 1–5 的验收标准细化成可勾选清单，并标注你发现的与本提示词冲突的事实（如有）。

验收：文档存在、覆盖全部 Phase、无代码改动。

→ 人工批准后进入 Phase 1。

## Phase 1 — L3：git 破坏性命令护栏 hook

目标：把 git 护栏从 NL 下沉为 PreToolUse 确定性拦截。

范围：

1. `scripts/hooks/block_destructive_git.py`：从 stdin 读宿主 hook 协议 JSON，识别 git 命令，命中高危清单则拒绝，拒绝理由中给出"先执行只读核查（`git diff HEAD -- <path>` / `git status`）"的指引。输出兼容两种协议：exit 2 + stderr，以及 stdout JSON decision。实现前先核对宿主当前 hook 文档（Claude Code：https://code.claude.com/docs/en/hooks ），以文档为准。
2. 高危清单（硬编码初版，Phase 5 才外置配置）：`git checkout -- <path>`、`git checkout HEAD -- <path>`、`git reset --hard`、`git clean -fd`、`git stash drop`、`git stash clear`、`git branch -D`。
3. 匹配必须容忍变体：引号、多空格、`git -C <path>` 前缀、`--` 分隔符；针对每种变体写测试用例（含绕过尝试）。
4. `scripts/test_hook_block_git.py`：真实协议样例 JSON 的 allow/deny 两路径 + 全部变体用例，逐一断言。
5. 接线文档 `docs/ai/hooks-setup.md`：给出 Claude Code（`.claude/settings.json` 的 PreToolUse matcher Bash）与 ZCode 等价配置的可照抄示例。

非目标：不做交互式 hunk 选择，不拦 `-p` / `stash push` 等安全操作，不引入策略引擎。

验收：测试全绿；`validate.py` 通过；文档含至少一种可照抄的接线配置。

提交：`feat(constraint): add PreToolUse hook blocking destructive git commands`

→ 人工批准后进入 Phase 2。

## Phase 2 — L1：harness 路由机器化

目标：harness 选择从"模型自选"变"路径驱动指派"。

范围：

1. harness frontmatter 新增可选字段 `apply_globs: []`（glob 语法与 gitignore 风格一致，匹配仓库相对路径）；`validate.py` 校验其语法；`generate_index.py` 在 INDEX 中输出该字段。
2. `scripts/route_harnesses.py --files <path...> [--json]`：输出命中的 harness 清单（人类可读 / JSON 两种）；无命中时 exit 1 并提示回退到 INDEX.md 手选。
3. 试点回填 `apply_globs`：`common/ai/`、`cpp/memory/`、`python/`、`dart/` 全部 harness；其余目录生成 TODO 清单附在演进计划文档。
4. `prompts/weak-model-harness-selection.md` 增加一步："若可执行脚本，先运行 `python scripts/route_harnesses.py --files {FILES}`，以其输出为 Applicable harnesses 的起点"。
5. 路由逻辑测试（含 glob 边界：目录前缀、通配、无命中）。

非目标：不做语义/任务类型路由，不改 harness 内容本身。

验收：对样例文件集（各语言各取 2 个路径）路由输出正确；`validate.py --json` 与 `generate_index.py --check` 通过。

提交：`feat(constraint): path-driven harness routing via apply_globs`

→ 人工批准。

## Phase 3 — L2：输出契约 schema 化

目标：四模式契约从事后 markdown 检查升级为可生成时强制的 JSON Schema。

范围：

1. `docs/ai/schemas/{plan,patch,review,verification}.schema.json`：字段与 `check_ai_protocol.py` 现有检查项一一对齐（必填节、行数预算上限、file:line 引用格式、NOT VERIFIED 字段等），schema 内写足 description。
2. `check_ai_protocol.py` 新增 `--schema <file>`：校验纯 JSON 文件或 markdown 内嵌 JSON；现有 markdown 模式保持不变（非破坏）。
3. `prompts/weak-model-*.md` 各加一行附注：宿主支持 structured output 时按对应 schema 输出。
4. `docs/ai/evals/runs/README.md` 更新用法。
5. 测试：`good-runs` 样例转 JSON 后必须通过；构造缺必填字段 / 超行数预算 / 缺 NOT VERIFIED 的反例必须失败；旧模式回归通过。

非目标：不迁移历史 eval 产物，不改 `evaluate_ai_protocol.py` 的输入格式。

验收：上述测试全绿；`validate.py` 通过。

提交：`feat(constraint): JSON Schema output contracts for four protocol modes`

→ 人工批准。

## Phase 4 — L6：tier 变开关（含 eval 点火前置）

目标：模型 tier 从文档标签变环境强制配置的生成源。

前置任务（先做）：用一个在用模型点火一次真实 eval——

```bash
python scripts/run_eval.py --model <model> --version <ver>
# 人工把模型产物填入 run 目录（.plan/.patch/.review/.verification.output.md）
python scripts/evaluate_ai_protocol.py <run-dir> --json --output <run-dir>/report.json
python scripts/update_model_registry.py --model <model> --version <ver> --report <run-dir>/report.json
```

产物未就绪时本阶段只交付机制、不宣称生效。

范围：

1. `update_model_registry.py` 新增 `--emit-enforcement`：从 registry 生成 `docs/ai/tier-enforcement.md`（tier → 强制措施映射表 + 自动生成标记 + 生成时间戳），并打印可粘贴进仓库 AGENTS.md 的片段（带 AUTO-GENERATED 标记，人工粘贴，脚本不直接改 AGENTS.md）。
2. 映射表初版：
   - T0/T1：hook 配置为只读；必须走 weak-model 模板；禁止 Edit/Bash 写操作
   - T2：允许 Edit；PostToolUse 自动跑 `run_ai_protocol_check`；仍禁 Phase 1 高危 git 命令
   - T3：允许多文件改动，前置 plan 批准 + 路由脚本输出必读清单
   - T4：放开 shell，高危 git 清单仍拦
3. 映射一致性测试：registry 变化 → emit 输出随之变化。

验收：emit 输出与 registry 一致；映射表经人工核对。

提交：`feat(constraint): tier-to-enforcement mapping emitted from model registry`

→ 人工批准。

## Phase 5 — L4：worktree 工作流与策略外置

目标：爆炸半径控制文档化 + hook 策略可版本化。

范围：

1. `docs/ai/sandbox-and-worktrees.md`：worktree 是并发边界不是安全边界；何时应对大改动使用独立 worktree；与 hook/权限的分工。
2. 把 Phase 1 的高危清单从硬编码抽到 `config/policy.yml`（版本化）；hook 读配置，配置缺失时 fail-closed。
3. 回归：`test_hook_block_git.py` 全部用例不因外置而变化。

验收：回归全绿；`policy.yml` 有字段说明与注释。

提交：`feat(constraint): externalize hook policy config; document worktree boundaries`

→ 人工批准，演进收尾。

## 整体完成定义（DoD）

- L1/L2/L3/L6 有可运营实现并有测试；L4/L5 有文档化接入点。
- 所有新增脚本有对应测试文件；`python scripts/validate.py --json` 与 `generate_index.py --check` 全绿。
- 每个 Phase 独立提交，提交说明含验证证据。
- 最终汇报按层汇总：层 → 落地物 → 文件 → 证据 → 仍未覆盖项（含 `apply_globs` 未回填目录清单、eval 待点火模型清单）。
