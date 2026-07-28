# 评审报告：Harness 质量门禁（draft → reviewed 候选）

- **日期：** 2026-07-29
- **评审人：** ZCode agent（产出评审，**状态推进由 CODEOWNER 决定**）
- **分支：** project/snapmaker-orca
- **评审对象：** 4 个 draft harness，评估是否满足 `common/meta/harness-evolution.md` Item 1（draft→reviewed）门禁
- **应用 harness：** `common/meta/harness-quality-standards.md`（6 项质量门禁）
- **目的：** 这既是对质量门禁流程本身的 dogfood（harness-driven-review Part B 全流程 B1→B6），也是为 draft→reviewed 状态推进产出 CODEOWNER 评审证据。

## 候选选择依据

4 个候选都有真实使用证据（满足 evolution Item 2 的"已被真实 review 使用"前提）：

| 候选 | 真实使用证据 |
|------|-------------|
| `cpp-feature-design-prerequisites` | feedback log 记录：真实 C++ 审计用过，commit `2b594cc` 据其反馈增补条目 |
| `cpp-layering-and-dip` | feedback log 记录：本仓库自审用过，commit `046319d` 据其做 tier 修正 |
| `common-harness-driven-review` | 本会话深度使用 + 改进（B5/B6 多次修订） |
| `common-harness-evolution` | 本会话深度使用 + Item 3/6 修订 |

## 门禁标准摘要（quality-standards 6 项）

1. 命名/放置一致性：id `<lang>-<slug>`、文件名 `<slug>.md`、目录与 language 一致、category 是 INDEX bucket
2. scope 质量：动作句 + body 声明 defers（覆盖边界）
3. 条目形状：每行 condition→**(tier)**→action→[Rx]，5-12 条，无 tier 膨胀
4. 引用完整性：每个 [Rx] 在 Reference Sources 表 + 注册于 sources.md + timeliness 标签
5. 交叉引用双向性：related 目标反向回链（**validate.py 不查此项，人工门禁**）
6. 反模式结构：4 字段（Appearance/Trap/Consequence/Fix）+ ≥2 个

---

## Harness: cpp-feature-design-prerequisites (cpp/design/feature-design-prerequisites.md)

Items 1,2,3,4,6 — PASS（无发现）

- Item 1（命名/放置）：id/文件名/目录/language 一致；category `design` 是 INDEX bucket（INDEX.md:108）✓
- Item 2（scope）：frontmatter scope 是动作句"Decide what must be designed..."；body 明确 defers 给 interface-contracts（how）和 layering-and-dip（where）✓
- Item 3（条目形状）：7 条，每行 condition→**(tier)**→action→[Rx]；有 .07.1 tier 修正记录（C→A 降级），符合 Anti-Pattern 2 防膨胀 ✓
- Item 4（引用完整性）：R1-R4 全在表；C1/A1/A21/A4 全注册于 sources.md；timeliness 全 verified-2026 ✓
- Item 6（反模式）：3 个 × 4 字段（Appearance/Trap/Consequence/Fix 齐全）✓

Item 5 — FAIL (A)：交叉引用单向
- `cpp/api/abi-compatibility.md` 未反向回链 feature-design-prerequisites（_xref.py 报 ONE-WAY）
- `common/commits/conventional-commits.md` 未反向回链（_xref.py 报 ONE-WAY）
- 修复：在两个目标 harness 的 `related` 字段加入 `cpp/design/feature-design-prerequisites.md`

## Harness: cpp-layering-and-dip (cpp/architecture/layering-and-dependency-inversion.md)

Items 1,2,3,4,5,6 — PASS（无发现）

- Item 1（命名/放置）：一致；category `architecture` 是 INDEX bucket（INDEX.md:38）✓
- Item 2（scope）：动作句；body 明确 defers 给 module-boundaries（物理边界）和 interface-contracts（契约表达），边界清晰 ✓
- Item 3（条目形状）：7 条，结构完整；.07.1 tier 修正（整体 C→A，SOLID 项 C→A），并有专门 Authority Caveat 段落说明无 (C) 独立源——这是防膨胀的正面范例 ✓
- Item 4（引用完整性）：R1-R4 全在表；C1/A20/A19/A22 全注册；timeliness verified-2026 ✓
- Item 5（双向性）：4 个 related 目标全部双向 ✓（_xref.py 全 OK）
- Item 6（反模式）：3 个 × 4 字段齐全 ✓

**额外正面发现：** Authority Caveat 段落明确记录"如何提升至 (C)"的 tier-challenge 路径，是 tier 透明度的范例，可作为其它 harness 模板。

## Harness: common-harness-driven-review (common/code-review/harness-driven-review.md)

Items 1,2,3,4,6 — PASS（无发现）

- Item 1：id/文件/目录一致；category `code-review`（INDEX.md:53）✓
- Item 2：scope 动作句；body 明确两个场景（写代码前/审查时）✓
- Item 3：编号用 A1-A3/B1-B6（非 ### N.），共 9 节；每行 condition→**(tier)**→action→[Rx] ✓
- Item 4：R1/R2 在表，注册（dev-guidelines CLAUDE.md/AGENTS.md）；timeliness verified-2026 ✓
- Item 6：3 个反模式 × 4 字段 ✓

Item 5 — FAIL (A)：交叉引用单向
- `common/meta/harness-evolution.md` 未反向回链（_xref.py 报 ONE-WAY）
- `cpp/design/feature-design-prerequisites.md` 未反向回链（_xref.py 报 ONE-WAY）
- 注：harness-evolution 的 related 里确有 quality-standards 和 prior-art-and-reuse 双向，但缺 driven-review 回链
- 修复：在 harness-evolution 加 `common/code-review/harness-driven-review.md`；在 feature-design-prerequisites 已有 layering 回链，需补 driven-review

## Harness: common-harness-evolution (common/meta/harness-evolution.md)

Items 1,2,3,4,6 — PASS（无发现）

- Item 1：一致；category `meta`（INDEX.md:135）✓
- Item 2：scope 动作句，明确治理 lifecycle/tier/deprecation ✓
- Item 3：7 条，结构完整 ✓
- Item 4：R1/R2/R3 在表注册 ✓
- Item 6：3 个反模式（Premature Stabilization / Silent Deprecation / Tier Inflation）× 4 字段 ✓

Item 5 — FAIL (A)：交叉引用单向
- `concepts/01-harness-methodology.md` 未回链 → **判定 N/A（合理）**：concepts 文件无 frontmatter，不是 harness，不强制 related 字段
- `concepts/02-authority-system.md` 未回链 → **判定 N/A（合理）**：同上
- 注：这两个单向链**不计为 FAIL**——concepts 是方法论文档，非 harness 间引用

---

## 发现汇总

| # | Tier | Harness | 位置 | 问题 |
|---|------|---------|------|------|
| 1 | A | quality-standards item 5 | cpp/design/feature-design-prerequisites.md:24-25 | 2 one-way related links (abi-compatibility, conventional-commits) |
| 2 | A | quality-standards item 5 | common/code-review/harness-driven-review.md:28-29 | 2 one-way related links (harness-evolution, feature-design-prerequisites) |

## 结论与状态推进建议

**技术质量门禁：** 4 个候选在 Items 1-4,6 全部 PASS。结构、命名、tier 完整性、引用注册、反模式结构均达标。tier 透明度尤其好（两个 C++ harness 有明确 tier 修正记录，layering-and-dip 有 Authority Caveat 范例）。

**唯一阻塞：** Item 5 双向性——2 个 harness 共 4 条单向 `related` 链（排除 concepts 合理单向）。这是 `validate.py --dead-links` 查不出的缺陷，正是 quality-standards Item 5 标注的"人工门禁"价值所在。

**对 draft→reviewed 的建议：**

- `cpp-layering-and-dip`：**建议立即推进 reviewed**。6 项全 PASS，无任何缺陷，有真实使用证据 + tier 透明度范例。
- 其余 3 个：**修复 4 条单向链后再推进**。修复是机械操作（在目标 related 补回链），不影响技术质量判断。

**流程完整性说明：** evolution Item 1 的 gate 是"CODEOWNER 批准的 PR review"。CODEOWNERS 显示全仓库唯一 CODEOWNER 是 @zhangzhend0ng。本评审由 agent 产出，**满足"评审已执行 + 证据已记录"，但 status 字段推进必须由 CODEOWNER 决定**——agent 不代表所有者批准。

## Dogfood 反思（E 的价值验证）

本次评审验证了 harness-driven-review Part B 全流程：
- B1（先选 harness 再读代码）：先加载 quality-standards 再读候选 ✓
- B3（逐条执行）：6 项 × 4 候选逐条核对 ✓
- B5（报告格式）：完整报告入文件，会话仅 FAIL ✓
- B6（信号检测）：下一步运行 check_review_signals.py

**关键价值证明：** dogfood 发现了 `validate.py`（exit 0）+ `validate.py --dead-links` 都查不出的 4 条单向链缺陷。这证明 quality-standards Item 5 的"人工双向性门禁"不是冗余——它捕获了自动化工具的盲区。若不执行这次 dogfood，这些缺陷会一直留在"技术条件达标但从未评审"的状态。
