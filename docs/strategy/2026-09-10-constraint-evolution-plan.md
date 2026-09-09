# 约束体系多层化演进计划（Phase 0 产出）

- 来源提示词：`prompts/constraint-system-evolution.md`（2026-09-10）
- 工作分支：`feature/constraint-evolution`（自 `project/snapmaker-orca` 切出）
- 状态：**待人工批准**。批准后按 Phase 1→5 顺序执行，每阶段结束是一道批准门，未获批准不进入下一阶段。
- 本文档性质：执行清单。每个 Phase 的验收标准细化为可勾选项；执行 agent 逐项完成后打勾并在提交说明附证据。

## 0. 侦察结论

### 0.1 已核实事实（提示词声明 vs 仓库现状）

| 提示词声明 | 核实结果 |
|---|---|
| `validate.py --json` 质量门 | 属实。`pass` 只反映 errors；exit 0/1/2/3（3 仅为 --stale 警告） |
| `generate_index.py --check` | 属实。INDEX 与 frontmatter 不同步时 exit 1 |
| `check_ai_protocol.py` 四模式结构检查 | 属实。plan/patch/review/verification；必填节、非空行预算 6/10/20/8、review 发现必须带 `file:line`、NOT VERIFIED 规则、成功声明必须伴随命令证据 |
| Phase 4 eval 三命令 | 属实。`run_eval.py --model --version`（仅脚手架，不跑模型）、`evaluate_ai_protocol.py <dir> --json --output`、`update_model_registry.py --model --version --report` 与三个脚本的 argparse 完全一致 |
| registry Promotion Rule | 属实。`docs/ai/model-registry.md` 含 Tier Policy 与四步 Promotion Rule；`update_model_registry.py` 要求 report 含 `recommended_tier`，弱模型 eval 最高只推荐 T2，T3/T4 走人工晋升 |
| Phase 4 产物命名 | 属实。`docs/ai/evals/runs/README.md` 规定 `<name>.<mode>.output.md`，prompt 文件必须用 `.txt` 后缀 |
| 试点目录规模 | `common/ai/` 5 份、`cpp/memory/` 3 份、`python/` 5 份、`dart/` 3 份，合计 16 份 harness 需回填 `apply_globs` |
| 脚本工程惯例 | 依赖仅 PyYAML==6.0.2；测试为独立可执行脚本（`scripts/test_*.py`，exit code 判定），由 `check_all.py` 聚合 |

### 0.2 与提示词的差异与需批准人知悉的细节（无硬冲突）

1. **`--mode` 现为必填参数。** Phase 3 新增 `--schema <file>` 时建议保持 `--mode` 必填、`--schema` 只切换检查体（markdown 检查路径一行不动），不做隐式模式推断。
2. **行数预算是"非空行数"计数**，JSON Schema 无法直接表达。Phase 3 需先定义 JSON 编码（如各节 `lines` 字符串数组 + `maxItems` 对齐预算），再谈一一对齐。
3. **Phase 1 高危清单（7 条）是用户级 AGENTS.md 清单的子集**：刻意不含"强制 `git checkout <branch>`"——分支切换有大量合法场景，无法确定性判定"强制"。该缺口由 Phase 5 的 worktree 文档与权限分工补足，属设计决定而非遗漏。
4. **glob 实现建议仅用标准库**（fnmatch / 手写 gitignore 风格语义）。引入 wcmatch 等新依赖按 change-scope-control 第 3 条 (C) 需单独批准，本计划默认不引入。
5. **建议将新测试脚本接入 `check_all.py`**（每阶段一行）。超出提示词字面范围，随各阶段提交，批准人可否决；默认视为接受。
6. **Phase 4 的 `--emit-enforcement` 只生成文档与可粘贴片段**，不直接改任何 AGENTS.md。提示词红线 3 只禁用户级 AGENTS.md；仓库根 AGENTS.md 的片段同样走人工粘贴，保持同一纪律。
7. `docs/strategy/` 现有两份文档为英文，但 (P) 输出语言约定（2026.07）规定 AI 产出的规划/说明文字默认中文。本文档及后续各阶段产出的说明性文档用中文，代码、命令、标识符保留原文。

## 1. 全局纪律（每个 Phase 开工前过一遍）

- [ ] 在 `feature/constraint-evolution` 分支工作；每 Phase 恰好一个提交，可独立 revert
- [ ] 提交前 `python scripts/validate.py --json` 通过（红线 5）
- [ ] Phase 触碰 harness frontmatter 或 INDEX 时，`python scripts/generate_index.py --check` 通过
- [ ] 不删除、不弱化任何现有 NL harness（红线 1）
- [ ] 不自动晋升任何模型 tier（红线 2）
- [ ] 不修改 `C:\Users\snapmaker\.zcode\AGENTS.md`（红线 3）
- [ ] 全程无 `git checkout --` / `reset --hard` / `clean -fd` / `stash drop|clear` / `branch -D`（红线 4）；回退用 Edit 或 `git checkout -p`
- [ ] 阶段结束按固定格式汇报：改了什么 / 验证了什么（命令+结果）/ 未验证什么 / 建议下一步

## 2. Phase 1 — L3：git 破坏性命令护栏 hook

适用 harness：`common/security/input-validation.md` (N)（stdin JSON 按不可信输入处理）、`python/security/input-deserialization.md` (N)、`common/ai/tool-calling-and-agent-control.md` (C)（高危动作门）。

范围清单：

- [ ] `scripts/hooks/block_destructive_git.py`：从 stdin 读宿主 hook 协议 JSON；解析出 shell 命令；识别 git 命令；命中高危清单则拒绝，拒绝理由中给出只读核查指引（先 `git diff HEAD -- <path>` / `git status`）
- [ ] 双协议输出：exit 2 + stderr 与 stdout JSON decision 两种拒绝方式都支持；allow 时静默放行
- [ ] 实现前核对宿主当前 hook 文档（Claude Code：<https://code.claude.com/docs/en/hooks>），以文档为准；若协议与提示词描述不符，把差异写进 `docs/ai/hooks-setup.md` 并按文档实现
- [ ] 高危清单 7 条硬编码（Phase 5 才外置）：`git checkout -- <path>`、`git checkout HEAD -- <path>`、`git reset --hard`、`git clean -fd`、`git stash drop`、`git stash clear`、`git branch -D`
- [ ] 变体容忍并各配用例：引号包裹子命令、多余空白、`git -C <path>` 前缀、`--` 分隔符
- [ ] 绕过尝试用例（必须仍被拦），起始集：`git  checkout --  f`（多空格）、`git "checkout" -- f`（引号）、`git -C sub reset --hard`、`git -c x=y clean -fd`（config 前缀）、`FOO=1 git reset --hard`（env 前缀）、`git --work-tree=x reset --hard`（全局选项前缀）；实现时允许补充、不允许删减
- [ ] 非 git 命令、安全操作（`checkout -p`、`stash push`、`branch -d`）必须放行——防误拦用例
- [ ] `scripts/test_hook_block_git.py`：真实协议样例 JSON 的 allow/deny 两路径 + 上述全部用例，逐一断言；独立可执行、exit code 判定（沿用 `test_*.py` 惯例）
- [ ] `docs/ai/hooks-setup.md`：Claude Code（`.claude/settings.json` 的 PreToolUse matcher Bash）可照抄示例 + ZCode 等价配置（`.zcode` 下当前无 hooks 配置，从零写示例并标注"以宿主当前文档为准"）
- [ ] （建议）`check_all.py` 接入 `test_hook_block_git.py`

非目标：不拦交互式/安全操作；不引入策略引擎；不在仓库内激活 hook。

验收命令：

```bash
python scripts/test_hook_block_git.py   # exit 0，全部断言通过
python scripts/validate.py --json       # pass: true
```

风险与回退：hook 脚本入仓库不改变任何运行时行为（需宿主主动配置才生效），合入本身零风险；回退 = revert 单提交。
NOT VERIFIED（预先声明）：宿主端真实拦截属端到端行为，需在真实会话配置 hook 后人工验证一次；仓库内只做协议级测试。

提交：`feat(constraint): add PreToolUse hook blocking destructive git commands`

→ 人工批准。

## 3. Phase 2 — L1：harness 路由机器化

适用 harness：`common/meta/harness-quality-standards.md` (A)（frontmatter 变更）、`common/documentation/documentation-standards.md` (C)。

范围清单：

- [ ] harness frontmatter 新增可选字段 `apply_globs: []`（gitignore 风格 glob，匹配仓库相对 posix 路径）；不填 = 不参与路由，行为与现状完全一致
- [ ] `validate.py` 校验 `apply_globs`：必须为字符串列表、每项是合法 glob（语法错误报 error）；不改其他必填字段语义
- [ ] `generate_index.py` 在 INDEX 表中输出该字段（新列或等价形式），重新生成后 `--check` 同步
- [ ] `scripts/route_harnesses.py --files <path...> [--json]`：输出命中 harness 清单（人类可读 / JSON 两种）；无命中 exit 1 并提示回退到 INDEX.md 手选；入参路径统一归一化为 posix（Windows 反斜杠入参必须可匹配）
- [ ] 试点回填 16 份：`common/ai/`（5）、`cpp/memory/`（3）、`python/`（5）、`dart/`（3）；其余目录的 TODO 清单追加到本文档第 8 节
- [ ] `prompts/weak-model-harness-selection.md` 增加一步：可执行脚本时先跑 `python scripts/route_harnesses.py --files {FILES}`，以其输出为 Applicable harnesses 的起点（保持 6 行预算不变）
- [ ] 测试（沿用 `test_*.py` 惯例）：目录前缀、`*`/`**` 通配、无命中 exit 1、多 harness 同时命中、反斜杠路径归一化、非法 glob 被 validate 拒绝
- [ ] （建议）`check_all.py` 接入路由测试

非目标：不做语义/任务类型路由；不改任何 harness 的 checklist 内容。

验收命令：

```bash
python scripts/route_harnesses.py --files src/physics.cpp src/main.py lib/ui.dart agent/tools.py docs/README.md
# 期望：cpp 路径命中 cpp/memory 系；py 路径命中 python 系；dart 路径命中 dart 系；
#       agent/tools.py 命中 common/ai 系；docs/README.md 无命中 exit 1
python scripts/validate.py --json && python scripts/generate_index.py --check   # 双绿
```

风险与回退：`apply_globs` 为可选字段，未回填的 harness 行为零变化；回退 = revert 单提交。

提交：`feat(constraint): path-driven harness routing via apply_globs`

→ 人工批准。

## 4. Phase 3 — L2：输出契约 schema 化

适用 harness：`python/security/input-deserialization.md` (N)（校验外部 JSON）、`common/documentation/documentation-standards.md` (C)。

范围清单：

- [ ] `docs/ai/schemas/{plan,patch,review,verification}.schema.json` 四份，字段与 `check_ai_protocol.py` 现有检查一一对齐：必填节 → required 属性；行数预算（6/10/20/8）→ 定义的 JSON 编码（见 0.2 第 2 条）上限；`file:line` 引用 → review 发现项的 pattern；NOT VERIFIED 语义 → verification/patch 的条件必填表达；每字段写足 description
- [ ] 明确边界：纯文本层启发式（forbidden noise 词表、成功声明×命令证据交叉检查）不强行塞进 schema，保留在 `--schema` 模式的检查器代码中并在 schema description 里注明
- [ ] `check_ai_protocol.py` 新增 `--schema <file>`：校验纯 JSON 文件或 markdown 内嵌 JSON；`--mode` 保持必填；不传 `--schema` 时走原 markdown 检查（非破坏，一行不改）
- [ ] `prompts/weak-model-*.md` 各加一行附注：宿主支持 structured output 时按对应 schema 输出
- [ ] `docs/ai/evals/runs/README.md` 更新 JSON 用法
- [ ] 测试：`docs/ai/evals/weak-model/good-runs/` 样例转 JSON 后必须全部通过；反例三组——缺必填字段、超行数预算、verification 缺 NOT VERIFIED——必须各自失败；旧 markdown 模式对现有样例回归通过
- [ ] （建议）`check_all.py` 接入 schema 测试

非目标：不迁移历史 eval 产物；不改 `evaluate_ai_protocol.py` 输入格式；不动 `run_ai_protocol_check.py`（markdown 默认路径不受影响）。

验收命令：

```bash
python scripts/test_ai_protocol_schema.py   # 或等效测试脚本；exit 0
python scripts/validate.py --json           # pass: true
```

风险与回退：schema 文件为纯新增，checker 的 `--schema` 为可选参数；回退 = revert 单提交。

提交：`feat(constraint): JSON Schema output contracts for four protocol modes`

→ 人工批准。

## 5. Phase 4 — L6：tier 变开关（含 eval 点火前置）

适用 harness：`common/ai/ai-evaluation-and-regression-strategy.md` (C)、`common/documentation/documentation-standards.md` (C)。

前置任务（先做，做不完不阻塞本阶段机制交付）：

- [ ] 按 `docs/ai/evals/runs/README.md` 流程用一个在用模型点火一次真实 eval：`run_eval.py` 脚手架 → 人工填入 `<name>.<mode>.output.md` 四份产物 → `evaluate_ai_protocol.py` → `update_model_registry.py`
- [ ] 产物未就绪时：只交付机制，不宣称任何 tier 生效变化（红线 2）

范围清单：

- [ ] `update_model_registry.py` 新增 `--emit-enforcement`：从 registry 生成 `docs/ai/tier-enforcement.md`（tier → 强制措施映射表 + AUTO-GENERATED 标记 + 生成时间戳），并打印可粘贴进仓库根 AGENTS.md 的片段（带 AUTO-GENERATED 标记；脚本不直接改任何 AGENTS.md，见 0.2 第 6 条）
- [ ] 映射表初版与提示词一致：T0/T1 hook 只读 + weak-model 模板 + 禁写操作；T2 允许 Edit + PostToolUse 自动协议检查 + 仍禁高危 git；T3 多文件改动 + plan 批准 + 路由脚本必读清单；T4 放开 shell + 高危 git 仍拦
- [ ] 映射与 registry Tier Policy 逐条对照不冲突（T0/T1 无代码编辑、T2 小补丁需 plan 批准、T3 需 repo 专属 eval、T4 需工具控制 harness）
- [ ] 一致性测试：registry 行变化 → emit 输出随之变化（fixture registry 两态对比）

验收命令：

```bash
python scripts/update_model_registry.py --emit-enforcement   # 生成 + 打印片段
python scripts/test_tier_enforcement.py                      # 或等效测试；exit 0
python scripts/validate.py --json                            # pass: true
```

风险与回退：`tier-enforcement.md` 带 AUTO-GENERATED 标记可随时再生成；`--emit-enforcement` 为可选参数；回退 = revert 单提交。
NOT VERIFIED（若 eval 未点火）：映射表的"生效"未经验证，仅机制交付——在阶段汇报中明确声明。

提交：`feat(constraint): tier-to-enforcement mapping emitted from model registry`

→ 人工批准。

## 6. Phase 5 — L4：worktree 工作流与策略外置

适用 harness：`common/security/input-validation.md` (N)（YAML 配置校验 + fail-closed）、`common/planning/rollback-and-migration-plan.md` (C)。

范围清单：

- [ ] `docs/ai/sandbox-and-worktrees.md`：明确 worktree 是并发边界不是安全边界；何种改动规模应使用独立 worktree；与 hook（Phase 1）和权限配置的分工表
- [ ] 高危清单从 `block_destructive_git.py` 硬编码抽到 `config/policy.yml`（版本化；字段说明 + 注释齐全）
- [ ] hook 读配置；配置缺失或解析失败时 fail-closed（拒绝并说明原因，绝不静默放行）
- [ ] 回归：`test_hook_block_git.py` 全部用例不改一行仍全绿
- [ ] （建议）`check_all.py` 接入 policy 加载测试

非目标：不做策略引擎/规则 DSL；不改 hook 协议层。

验收命令：

```bash
python scripts/test_hook_block_git.py   # 回归全绿，exit 0
python scripts/validate.py --json       # pass: true
```

风险与回退：`policy.yml` 缺失即 fail-closed，最坏结果等于现状（宿主未配置 hook）；回退 = revert 单提交。

提交：`feat(constraint): externalize hook policy config; document worktree boundaries`

→ 人工批准，演进收尾。

## 7. 整体完成定义（DoD）

- [ ] L1（路由）/ L2（schema）/ L3（hook）/ L6（tier 开关）有可运营实现并有测试
- [ ] L4（worktree）/ L5（验证接线）有文档化接入点
- [ ] 所有新增脚本有对应测试文件；`validate.py --json` 与 `generate_index.py --check` 全绿
- [ ] 每个 Phase 独立提交，提交说明含验证证据（命令 + 结果摘要）
- [ ] 最终汇报按层汇总：层 → 落地物 → 文件 → 证据 → 仍未覆盖项（含 `apply_globs` 未回填目录清单、eval 待点火模型清单）

## 8. 未回填目录 TODO（Phase 2 试点后由执行 agent 补全勾选）

- [ ] `common/` 其余子目录（code-review、commits、debugging、planning、security、testing 等）
- [ ] `cpp/` 其余子目录（correctness、functions、concurrency、templates 等）
- [ ] `prompts/`、`projects/`（如适用）

## 9. 批准记录

| Phase | 内容 | 批准人 | 日期 |
|-------|------|--------|------|
| 0 | 本计划 | | |
| 1 | git 护栏 hook | | |
| 2 | harness 路由 | | |
| 3 | 输出契约 schema | | |
| 4 | tier 开关 | | |
| 5 | worktree + 策略外置 | | |
