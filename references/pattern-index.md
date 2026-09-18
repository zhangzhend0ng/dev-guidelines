# Cross-Repo Pattern Index（跨仓模式索引）

> **状态：v1 草稿，待人审。** 生成于 2026-09-18（脚本 `~/.zcode/tmp/zc_m3_pattern_gen.py` 机械归并 + 会话起草措辞）。
> **本表分层**：第一部分是唯一必读的**可复用策略层**；第二部分是**抽象方法**（新条目的生产规则）；
> 附录是索引键（别名/单例），供 grep，不供阅读。领域专属经验一律留在各仓本地，不进本表。
>
> **怎么被使用**（三层）：① 精简卡（触发词+对策一行版）粘进个人 AGENTS.md 每会话常驻；② 本完整版不常驻——由 review/测试 harness 的 checklist 首项引用，在审查与写测试的时机随流程加载；③ 新增经验条目前 grep 本表判别词（超坐检查）。载体是本 git 仓，PR 协作。

---

## §0 快速版（粘贴进 AGENTS.md / .cursor/rules / copilot-instructions.md，每会话常驻）

```markdown
## AI 协作策略卡（来源 dev-guidelines/references/pattern-index.md；完整版与贡献方式见该仓）
- 假绿: 报"全绿/通过"前，先构造一个坏实现证明检查能翻红；翻不红 = 未验证。
- 两态哨兵: 0/0.0/NaN/默认值兼表"合法值"与"未评估"时，先证明读的是哪种语义再消费。
- 死接线: 每个改动附"消费证据"（入口到该点的可达路径 + 消费点 grep）；修一处横向清扫姊妹位点。
- 文档腐化: 引用文档/journal 里的数字前重算一次；断言必须带可复查入口，否则视为过期。
- 编码对称: 同一概念在两处出现时，改一端必 grep 另一端同语义位点；边界/转义/键名检查先于业务逻辑。
- 传输变异: 内容经 shell/heredoc/管道传输前先问"这层会不会改内容"；含转义内容一律走参数化通道。
- 写入副作用: 写既有文件前先证明其当前内容可被毁；同路径写入点全局唯一。
```

## 第一部分 · 可复用策略层（7 张策略卡）

每张三行：**何时触发 / 为什么错 / 对策**。已剥离领域名词，跨项目、跨语言、跨工具适用。

**F1 假绿（false-green）**
触发：任何测试/检查/审查报"全绿、通过、一致"。
为什么错：绿灯只证明"没有反例被构造出来"，不证明"判别力存在"。
对策：给出全绿结论前，先构造一个故意的坏实现/坏数据，证明这套检查能翻红；翻不红 = 未验证。机械 sweep 全绿不算覆盖。

**F2 两态哨兵（two-state-sentinel）**
触发：同一数值或状态可同时表示"合法值"与"未评估/缺省/空"（`0`、`0.0`、`NaN`、`get_default()`、空串、`end=start`）。
为什么错：读的一端取了另一种语义，错误被静默吞掉。
对策：见到哨兵值必先证明"当前读法取的是哪种语义"再消费；设计新接口时禁止一值两义，宁可加显式状态。

**F3 死接线（dead-wiring）**
触发：新加/修改的代码、配置、开关、文档声称生效。
为什么错："计算了没人读"和"接上了不可达"都会让改动空转，且表面成功。
对策：每个改动附一条"消费证据"——从入口到该点的可达路径 + 消费点 grep；修一处后横向清扫姊妹模块的同型位点。

**F4 文档腐化（doc-drift）**
触发：引用文档/注释/journal/汇报里的数字、清单、断言。
为什么错：文字与其描述的对象随时间脱钩，引用即传谣。
对策：引用前重算一次；写下任何断言必须附可复查入口（命令或文件:行）；无入口的断言视为过期。

**F5 编码对称（encoding-symmetry）**
触发：同一概念在两处出现（生产端/消费端、写入/读出、跨接口）。
为什么错：两端对"同一份数据"的编码、解析、规范化、键名、边界规则不一致，错误在接缝处。
对策：改一端必 grep 另一端的同语义位点；边界（字节/字符）、转义、键名一致性的检查先于业务逻辑。

**F6 传输变异（transport-mutation）**
触发：内容经 shell / heredoc / 管道 / 任意"传输层"写入文件或另一进程。
为什么错：传输层会改动内容——转义被吞一层、stdin 被抢占、编码被改写——且改动不可见。
对策：凡传输必先问"这层会不会改内容"；含转义/引号/反斜杠的内容一律走参数化通道（Edit 工具、arg vector），不走 shell 内联。

**F7 写入副作用（file-io-hazard）**
触发：以写模式打开既有文件、或同一路径有两处写入。
为什么错：`open(p,'w')` 在求值写入参数前就截断了文件；双写互相覆写。
对策：写既有文件前先证明"它此刻的内容可以被毁"（已提交/已备份/本来就是临时物）；同路径写入点全局唯一。

## 第二部分 · 抽象方法（新条目怎么产生）

**五步法**（从一次事故/纠偏到一条可复用条目）：

1. **剥离**：把事故描述里的所有专名（项目、模块、工具名、数据名）换成类别词。剩下的只有三样：触发条件、失败模式、对策。
2. **泛化测试**：把句子放进一个你从没做过的项目——它还能在正确时机触发吗？需要领域背景才能理解或触发的，回到第 1 步。
3. **三段式落笔**：触发器必须可检测（能 grep / 能提问），对策必须是策略而非步骤（"先证明 X"而不是"点某个按钮"）。
4. **稳定键**：起一个 kebab-case 英文名 + 2–3 个 grep 判别词。名字永不改，后续同义发现只作别名挂上去。
5. **超坐检查**：入册前先 grep 本表。命中既有家族 = 这是该家族的新实锤，不新开条目；四仓已为同一教训付过 4 次学费的教训就是没做这步。

**抽象层级梯**（用本语料的真实案例演示，抽象到 L2 停）：

| 层级 | 例（heredoc 事故） | 复用范围 |
|---|---|---|
| L0 事故 | "iter-754 git-bash heredoc 双反斜杠被吞一层" | 仅本仓本轮 |
| L1 工具规则 | "含转义内容不进 heredoc，用 Edit 工具" | 跨项目（三仓都适用） |
| **L2 策略** | "凡内容经传输层，先问这层会不会改内容" | **跨工具跨场景（本表目标层）** |
| L3 原则 | "小心编码问题" | 空洞，停止 |

停止规则：**向上抽象到"还能检测到触发"为止，向下保留到"不需要知道原事故就能执行"为止。** 再往上就是正确的废话，再往下就是不可迁移的领域知识。

**采集时机**（不靠回忆，靠现场）：用户纠偏 / 测试翻车 / 返工发生的当下，写一句失败反事实——"如果当时〈对策〉，就不会〈失败〉"。这句话天然就是三段式；事后补写的条目质量断崖式下降。

## 附录 · 索引键（供 grep，不供阅读）

**家族 → 别名（仓:名，省略仓名的为多仓重复）**
- F1: fuzz-blind-spot, false-perfect, false-worst, oracle-degeneration, phantom-diff, zero-fixture-branch, misleading-success, fv-exit0-allskip, make-target-name-false-green, partial-instrumentation-false-green, silent-write-failure-exit0, tautological-oracle, non-discriminating-test, assert-against-implementation-not-intention(建议)
- F2: sentinel, modal-default, two-state, two-state-empty-input, get-default-sentinel, unknown-target-two-state, not-assessable, matrix-vs-mechanism-noop, premise-irrelevant-gain, 0.0/NaN 反模式(AGENTS.md)
- F3: dead-branch, single-layer-fix, reachability, config-hygiene(子族：键缺失/作用域/覆盖优先级/was_set), computed-but-dead, config-dead-key, dead-gate, dead-lever-no-op-verified, documented-but-unimplemented, root-vs-symptom(建议)
- F4: stale-doc, stale-claim, stale-exe-probe, journal-fact-drift, spec-as-contract-drift, prose-counts-rot, living-file-assertions, backlog-claim-needs-verification, evidence-needs-nesting-level(建议)
- F5: symmetry, utf8-boundary, json_escape, key-mismatch, escape-symmetry, bytes-as-char-mojibake, filter-mismatch, channel-id-space-mismatch, id-space-parse-parity, format-assumption-refuted, normalization-cross-set-trap, single-layer-bom-fix, bom-frontmatter-exclusion, parser-producer-drift, posix-path-identifier
- F6: heredoc-escape-collapse, heredoc-stdin-conflict, heredoc-edit-hazard(journal 正文补录)
- F7: open-w-truncation, dual-write-same-path-clobber(建议)

**单例（留各仓本地，不进全局表）**：panic-guard, magic-threshold(→F3 子族建议), failure-direction, provenance-vs-claim, moving-reference, timing-without-rc, vote-blind-axis-aligned(→F1 建议), pure-E-no-xy(领域专属)。

## 维护约定

1. 本表核心是第一部分的策略句；附录只维护别名。脚本可重跑机械归并，策略句只经人审修改。
2. 各仓 Pattern Index 保留为本地实例；**新增条目先 grep 本表判别词**，命中即回写家族名。
3. ≥2 月无新命中的家族 → 人审时列淘汰候选。
4. 领域知识（如混色规则）不入本表——它属于项目 docs，不属于可复用层。
