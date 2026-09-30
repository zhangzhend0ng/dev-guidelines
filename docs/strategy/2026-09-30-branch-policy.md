# 分支策略决策 — `project/snapmaker-orca` 为长期主线

- 日期：2026-09-30
- 决策人：用户（会话内确认）
- 背景：`project/snapmaker-orca` 自 2026-07-27 建立为长寿命项目分支（8d26d70），至 2026-09-30 领先 master 80 commits（constraint-evolution Phase 0-5、Dart harness 批、AI pilot、snapmaker-orca 蒸馏批 1+2）；master 无独立提交。

## 决策

1. **`project/snapmaker-orca` 即长期主线**：项目层（P 级）内容与当前 dev-guidelines 演进工作的集成分支就是它；向 master 回流不是常态化的集成动作。
2. **master 定位 = 定期归档点**：按批次把主线成果（validate 全绿、逻辑独立）合回 master 作为保底快照；回流是同步动作，频率服从内容里程碑（如一个蒸馏批消化完、一个 Phase 收尾），不设固定周期。
3. **分支保护**：该分支不删除、不 force push；特性分支（如 `feature/constraint-evolution`）一律自它切出、合回它。

## 边界

- 本决策只约束 dev-guidelines 仓库自身的分支模型，不改变 SnapmakerOrca 产品仓的 GitHub Flow（见 `projects/snapmaker-orca/workflow-standards.md`）。
- 首次回流建议按工作流分批：constraint-evolution 批 → Dart harness 批 → 蒸馏 follow-up 批，每批合入前过 `python scripts/validate.py --json`。
