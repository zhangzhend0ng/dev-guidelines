<!-- MIGRATED: superseded by cpp/functions/parameter-validation.md -->
# [MIGRATED] Function Design Harness
> **MIGRATED:** This file has moved to [cpp/functions/parameter-validation.md](cpp/functions/parameter-validation.md). This copy will be removed after 2026-08-31.

**Based on:** C++ Core Guidelines (I.6/I.12/I.13), SEI/CERT API00-C (v2025), ISO P1743R0 (Bloomberg BDE).
**Scope:** 函数设计评审 与 新函数编写 时的入参校验决策准则。

---

## 前置决策：函数的 Contract 类型

| Contract | 定义 | 谁负责校验 |
|----------|------|------------|
| **Narrow（窄）** | 函数有前置条件，调用方必须满足 | Caller 负责，Callee 用 `assert()` 捕获 |
| **Wide（宽）** | 接受所有合法输入，每种输入都有定义行为 | Callee 负责，`if` + return/throw |

**核心原则：校验只在接口的恰好一侧发生——不双侧都不校验，也不双侧都校验。**

---

## Checklist（7 条）

### 1. 安全边界判定（SEI/CERT API00-C）
输入是否来自不可信来源（网络、文件、用户输入、跨进程调用）？

- [ ] YES → **必须在 Callee 侧做 if+return/throw 校验，所有构建模式生效。**
- [ ] NO  → 进入第 2 条。

### 2. Public API 判定（SEI/CERT API00-C）
函数是库/模块的对外公开接口吗（非 static / 非匿名 namespace）？

- [ ] YES → **Callee 侧校验**，无法控制所有调用方。
- [ ] NO（static 函数 / 内部 helper）→ 进入第 3 条。

### 3. 校验代价判定（P1743R0）
前置条件是否在运行时**可检查**且**代价合理**（不改变 O 复杂度）？

- [ ] YES → 进入第 4 条。
- [ ] NO（如：`is_sorted()` 使 O(log N)→O(N)，或"比较器是严格弱序"无法检查）
  → **不检查。文档注明窄契约，信任调用方。**

### 4. 校验机制选择（C++ Core Guidelines I.6）
选择正确的校验手段：

| 机制 | 场景 | 构建模式 |
|------|------|----------|
| `if` + return/throw | 外部输入 / Public API / 可恢复的运行时错误 | 始终执行 |
| `assert()` / `Expects()` | 内部函数间，检测程序员 bug | Debug/Assert 构建 |
| 类型系统（`not_null<T>` 等） | 编译期可证明的约束 | 编译期 |

### 5. 空/零值校验（C++ Core Guidelines I.12）
对指针/引用/容器参数：

| 参数类型 | 校验策略 |
|----------|----------|
| 原始指针 | 若可为 nullptr → 必须校验 |
| 引用 | 调用方负责不传空引用（UB 在 caller 侧） |
| `std::vector` / 容器 | 空容器通常是合法输入，行为应定义清楚 |
| `std::optional` | 用 `.has_value()` / `.value_or()` |

### 6. 不制造 Silent Pass-through（P1743R0）
对非法输入定义了一个"无害"默认行为（如 `strlen(nullptr)` 返回 0）？

- [ ] 如果是 → **STOP。会掩藏调用方 bug。改为 assert 或明确报错。**
- [ ] 如果不是 → OK。

### 7. 错误处理一致性
函数校验失败后的处理，与项目中同类函数的风格一致？

- [ ] 与现有代码一致（return false / throw / 弹窗等）

---

## 快速决策树

```
外部/不可信输入？
  ├─ YES → [1] if + return/throw，始终执行
  └─ NO  → Public API？
              ├─ YES → [2] if + return/throw
              └─ NO  → 前置条件可检查且代价低？
                          ├─ YES → [4] assert() / Expects()
                          └─ NO  → [3] 窄契约，文档注明
各分支都必须通过 → [6] 不制造 Silent Pass-through
                  → [7] 错误处理风格一致
```

---

## 参考来源
- [C++ Core Guidelines: I.6 Prefer `Expects()`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i6-prefer-expects-for-expressing-preconditions)
- [SEI/CERT API00-C: Functions should validate parameters](https://wiki.sei.cmu.edu/confluence/display/c/API00-C.+Functions+should+validate+their+parameters)
- [P1743R0: Contracts, UB, and Defensive Programming](http://bloomberg.github.io/bde/white_papers/contracts_ub_and_defensive_programming.html)
