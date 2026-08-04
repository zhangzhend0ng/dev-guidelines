# AI 开发能力提升方向:可行性判断(2026-08-04)

**触发**:用户要求对上轮调研推荐的 5 个方向,逐个详细判断可行性与价值,值得做就做。
**方法**:$adversarial-development-loop ENUMERATE → 逐方向判断(接入点/消费者/价值)→ REFUTE
→ 做值得的。**关键约束**:这是元仓库(harness markdown + 校验脚本),不是应用代码——
判断"可行性"的标准是"能否接入既有 harness/protocol/script 层",不是"能否从零造新系统"。

---

## 判断矩阵

| 方向 | 业界热度 | 本仓库接入点 | 真实价值 | 决策 | 理由 |
|---|---|---|---|---|---|
| **1. grounding 检查(review claim→diff)** | HalluJudge F1 0.85 | check_review_findings 已有 file:line 格式检查(:148),但**不查 grounding**;review-without-lines BAD case **未接线**到 test | **高** | ✅ **做** | 已有雏形差最后一步(格式→grounding);BAD fixture 已存在未测;直接补既有检查的盲区 |
| **2. spec→test 自动派生** | SDD 主流 | plan-protocol 是 8 行极简文档,无结构化 test 字段 | 低 | ❌ **不做** | 自动派生需理解任意 Goal 语义(研究级);plan 协议刻意极简(LINE_BUDGET=8),扩结构破坏设计 |
| **3. 弱模型 eval→路由扩展** | RouteLLM 多模型栈 | recommended_tier 唯一消费者=update_model_registry(只写 md) | 低 | ❌ **不做** | 无路由基础设施;本仓库是 harness 仓库不是 agent runtime,造路由=脱离定位 |
| **4. subtle-error harness** | Willison:最危险类 | **是 harness(markdown),非脚本**——契合仓库核心产物 | **中-高** | ✅ **做** | 低成本(写一个 harness);复用 $adversarial-development-loop 实战(假满分/死代码/单层修复);补 code-review 类别 |
| **5. 内部 eval 套件** | METR / Beyond-SWE-bench | 现有 eval 是 generic 协议校验,非能力 eval | 低 | ❌ **不做** | 本仓库的"项目"=harness 自身;从 harness 生成 eval 测 harness = 循环论证;价值低于方向1/4 |

**结论**:做 **方向 1 + 方向 4**。其余 3 个诚实拒绝(非因难,因不契合仓库定位或价值低)。

> ⚠️ **REFUTE 修订(实现前派 2 个对抗 subagent,推翻了上方初判)**——见下方「REFUTE 修订记录」。
> 初判**方向 1 ✅做**被推翻为 ❌(review-mode 无 diff 访问 + plan 语法未冻结 → 假红);
> 初判**方向 2/5 ❌**部分被推翻(narrow 版本可行,但价值仍低);
> 最终只**方向 4 ✅做**(且需正确 grounding,不能引 loop skill)。

---

## 方向 1 详解:grounding 检查(review claim 必须真实存在)

### 现状(ENUMERATE)
`check_ai_protocol.py:144-149` `check_review_findings` 的 file:line 检查:
```python
for finding in finding_lines:
    if not re.search(r"[\w./\\-]+:\d+", finding):
        errors.append("review finding lacks file:line citation")
```
这是**格式检查**(finding 里有没有 `xxx:123` 样的串),**不是 grounding 检查**:
- 不查该 file:line 是否真实存在于被审代码
- 不查 finding 描述是否对应那个位置的实际内容
- HalluJudge 的核心 = claim 拆解 + diff grounding,此处完全没有

### 退化输入×消费者矩阵
| 输入＼消费者 | 现状格式检查 | grounding 应做 |
|------------|------------|--------------|
| finding 含真实 file:line | ✓ PASS | ✓ |
| finding 含**编造的** file:line(不存在) | ✓ **PASS(假绿)** | ✗ FAIL |
| finding 无 file:line | ✗ FAIL | ✗ FAIL |
| finding 含 file:line 但描述与位置不符 | ✓ PASS(假绿) | ✗ FAIL(需语义,超机械检查范围) |

**关键诚实**:grounding 的第一格(编造 file:line)是**机械可检**的——给 review 输入 + 被审文件列表,
查 finding 引用的 path 是否存在。第二格(描述不符)需语义判断,**不做**(超机械检查范围,属 LLM-as-judge)。

### 决策:做**可机械校验的 grounding 子集**
检查 review 中引用的文件路径是否存在于工作树。这是 HalluJudge grounding 函数的最弱版本,
零语义、零 LLM,纯文件存在性。已能挡"编造路径"类幻觉。

---

## 方向 4 详解:subtle-semantic-error harness

Willison 论点:能编译但语义错的代码 > 明显幻觉(后者易被抓)。
这正是 $adversarial-development-loop 反复抓的:假满分、死代码、单层修复、哨兵歧义。
**这些已散落在 loop skill 里,提炼成独立 code-review harness 让所有审查者(非仅 loop 用户)可用。**
契合仓库核心产物(harness markdown)。低成本(写文档 + frontmatter)。

---

## REFUTE 预期攻击点(实现前)
- [方向1] 是否过度?review 输入可能不含 diff(只有 finding 文本),无法 grounding → 需先确认 review
  protocol 是否要求附 diff/path。若不附,grounding 不可机械做 → 降级为"路径格式 + 存在性(若提供 repo 根)"。
- [方向4] 是否与既有 harness 重复(review-checklist / harness-driven-review)?需 grep 确认无重复。

---

## REFUTE 修订记录(实现前对抗,2 个 subagent)

初判后派 2 个对抗 subagent 证伪,推翻了上方判断矩阵的多项决策。下方是**最终决策**(覆盖上方初判)。

### 方向 1:初判 ✅做 → 最终 ❌ **REJECT**(3 blocker)

REFUTE subagent(方向1 证伪)发现:
1. **[blocker] review-mode 无 diff 访问**:`check_ai_protocol.py` review 模式只读模型输出文本,
   CLI 无 --diff/--repo-root 参数(`run_ai_protocol_check.py:50`)。review 是审**外部 diff**
   (`prompts/weak-model-cpp-review.md:20` 内联 `{DIFF}`)。"路径必须在工作树存在"会**假红每个
   合法 review**(它们引用的是被审项目的路径,非本仓库)。
2. **relocation 到 plan-mode 也被推翻**:plan 的 `Harnesses:` 字段**语法未冻结**——4 种格式
   并存(`;`-路径 / `,`-路径 / prose / 路线图重构版)。任何具体 parser 至少在一个 fixture 上失败。
3. **[blocker] Verification 路径提取假红**:3 个合法 distilled 模板(`conversation-distillation.md:146,160,173`)
   用 prose("reproduction command or NOT VERIFIED"),路径提取会假红或静默失效。

**REFUTE 推荐**:语法冻结前不做;冻结后仅做 Harnesses(非 Verification)+ skip-and-warn。
**采纳**:全 reject(plan schema 正被 `capability-roadmap.md:97-104` 重构,现在做=在流沙上建)。
诚实原则兑现:**不 ship 会假红的代码**(回归工具里漏报 > 误报,但假红阻塞合法输入同样不可接受)。

### 方向 4:初判 ✅做 → 最终 ✅**做**(但修正 grounding)

REFUTE subagent(方向4 证伪)发现:
1. **[major] sourcing 问题**:初判说"复用 $adversarial-development-loop 实战",但 loop skill 是
   ZCode skill,**不在 `references/sources.md`**。`harness-quality-standards.md:94` 禁止"invented"
   anti-patterns;:80-83 要求每 source 注册。引 loop skill = 违反仓库自身 meta-harness。
2. **部分重复** review-checklist(:60-63 correctness / :84 dead code),但**失败类 taxonomy
   (false-perfect/single-layer-fix/sentinel-ambiguity/dead-contract)是真新**。

**修正方案**:用**已注册的权威 source** grounding——NIST AI 600-1 GenAI Profile(C19,可靠性/幻觉)+
Mutation Testing(A17/A18,测试充分性)。放弃 weak 的 OWASP LLM(C16,是应用安全非 subtle-code-defect)。
**采纳并实现** → `common/code-review/ai-generated-code-failure-modes.md`。

### 方向 2:初判 ❌ → 部分推翻(narrow 版可行,但价值仍低)

REFUTE 发现:narrow 版"Verification/Harnesses 字段路径存在性"input-bounded 可行(同接受方向1的逻辑)。
**但**:价值有限(Verification 已有非空门 + 执行时自然暴露),且依赖方向1 同样的语法冻结前提。
**维持 reject**(价值低 + 前提未满足)。

### 方向 3:初判 ❌ → 维持(narrow doc 版价值微小)

REFUTE 确认无路由基础设施属实;仅"路由意图文档表"价值微小,不值得单开。**维持 reject**。

### 方向 5:初判 ❌(循环论证) → 部分推翻(脚本测脚本非循环),但维持

REFUTE:scripts-on-fixtures 测的是**脚本的正确性**(如 command_re regex),非 harness 测 harness,
非循环。**但**现有 test_ai_protocol.py 已部分覆盖,价值低于方向4。**维持 reject**。

---

## 最终结果

**实现:方向 4**(grounded harness)。**Reject:方向 1/2/3/5**。
**净产出**:1 新 harness(`common/code-review/ai-generated-code-failure-modes.md`)+ 4 个 related 反向链接 +
INDEX 同步。全部过 validate/gen_index/check_all/meta-tests。

**最大教训**:初判"业界热+有雏形=做"差点 ship 一个假红检查(方向1)。REFUTE 在实现前抓住
"review-mode 根本没 diff 访问权"——这正是 skill 的核心价值:对抗只攻 known unknowns,而"接入点
是否存在"是可通过读源码核实的 known unknown。**没读 CLI 参数表就判"可行"= 读代码不精确**。
