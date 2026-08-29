# dev-guidelines Loop Journal

对抗式开发循环 (`$adversarial-development-loop`) 在本仓库的迭代日志。
本仓库是元仓库:harness(markdown checklist,人+AI 消费)+ scripts(Python,机器消费)。
"机器消费产物" 等价于其他项目的 test_core —— 是对抗/枚举的权威校验层。

baseline (iter 0, 2026-08-04):validate.py exit 0 / generate_index.py --check **FAIL** /
check_all.py **exit 1** / test_ai_protocol + test_plan_debug_protocol **PASS** /
75 harness 文件 / 17 scripts。本仓库此前无 journal。

---

## 迭代 1 — INDEX.md 路径分隔符假失步(Windows 反斜杠,CI 阻塞)

### 触发的理论缺口
配置卫生 + 跨平台一致性:`generate_index.py --check` FAIL,但 `validate.py` exit 0。
INDEX.md 的 autogen zone 用了 **Windows 反斜杠** 路径分隔符(`common\ai\foo.md`),
而 generator 产出正斜杠。BACKSLASH 链接在 GitHub markdown 渲染 + 非 Windows clone 上失效。
CI `.github/workflows/validate.yml:42` "Index sync check" 步骤无 continue-on-error
→ **每个触碰 paths 的 PR 当前都会变红**。这是唯一 CI-blocking 问题。

### grep journal 结果(Step 1)
本仓库无既有 journal(首开)。跨项目教训类比:Stratum iter 173(clean Release build
暴露 garbage——不同 build 配置下状态差异潜伏);此处是不同 OS 下生成的文件潜伏。

### 合法 shape 清单 + 覆盖状态
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| generator 产出(正斜杠) | /tmp 离屏生成 | ✓ | ✓ |
| 已提交 INDEX.md(反斜杠) | 72 行含 \,共 144 个,全在路径段小写字母间 | ✓ | ✓ |
| 结构差异 | normalize \→/ 后 diff exit 0 | ✓ | n/a(无结构差异) |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | generate_index --check | GitHub md 渲染 | 非-win clone 链接 |
|----------------|----------------------|---------------|------------------|
| 反斜杠路径 | FAIL ✗(当前) | 渲染坏 ✗ | 失效 ✗ |
| 正斜杠路径 | PASS | 渲染对 | 生效 |

### 初版方案(被推翻点)
方案:运行 generator 重生成 INDEX.md。**未被推翻** —— REFUTE subagent 验证:
72/72 行,纯路径分隔符差异,零结构差异,单根因。

### 对抗审查结论
REFUTE subagent(本会话):
- [blocker] 无。iter 1 方案正确,是唯一 CI-blocking 问题,优先级正确。
- [major] 提示 iter 2/3 退出码 + iter 4 check_review_signals(采纳,后续轮)。
- 确认:重生成是唯一正确动作(手动编辑路径分隔符 = 制造漂移)。

### 修订方案
采纳。单独 commit(配置卫生,非功能)。

### 数据流 hops
无跨层数据(单文件生成)。generator 是 producer,INDEX.md 是产物,--check 是消费者。
全部 ✓。

### 变种横向 grep
同 producer(generator)产出的其他产物? `generate_index.py --output` 离屏 + `--pack` 离屏
+ `--installed` 离屏 —— 全用同一 `build_index_table`,同正斜杠。无其他变种需修。

### 改动文件
- `INDEX.md` (重生成,72 行路径分隔符 \→/)

### 测试证据
- `generate_index.py --check`:exit 1 → **exit 0** ✓
- `check_all.py`:exit 1 → **exit 0** ✓
- autogen zone 反斜杠:144 → **0** ✓
- 行数守恒:97 行 = 97 行 ✓
- meta-tests 不变:ai PASS / plan_debug PASS

### 过程意外
无。单根因,干净修复。

### 遗留 backlog
(本轮无新增;后续轮 backlog 见各自条目)

---

## 迭代 2 — validate.py exit code 3 不可达(--stale 文档承诺未兑现)

### 触发的理论缺口
死代码 / 配置卫生:validate.py docstring(:12)承诺 `3 = stale citations (warn; only with --stale)`,
spec(`docs/specs/2026-05-31-repo-structure-design.md:413,436`)重申 exit 3 契约。但 main() 的
exit 路径(:232-237)在 `all_errors` 为空时,无论 `warnings` 是否非空、`args.stale` 是否 True,
**两条路径都 sys.exit(0)**。exit 3 从未被任何代码路径返回 = 死契约。

### grep journal 结果
spec:413/436 明确定义 exit 3。CI `.github/workflows/validate.yml:39-40` 的 --stale 步骤带
`continue-on-error: true` —— 意图是"stale 不阻塞但暴露"。但 exit 3 不可达 → 该 continue-on-error
是**死配置**(步骤永不失败)。修 exit 3 会让 continue-on-error 重新有意义。

### 合法 shape 清单(exit 路径)
| Shape | 判别 | exit |
|-------|------|------|
| 有 errors + 含 xref | has_cross_ref | 2 |
| 有 errors 无 xref | — | 1 |
| 无 errors + 有 warnings + --stale | args.stale True | **应 3,实际 0(BUG)** |
| 无 errors + 有 warnings 非 --stale | warnings 只在 --stale 下填充,此 shape 不可达 | n/a |
| 无 errors 无 warnings | — | 0 |

### 退化输入×消费者
| 输入＼消费者 | 本地 --stale | CI --stale 步骤 | --json pass 字段 |
|------------|------------|----------------|-----------------|
| 有 stale harness | exit 0(假绿,BUG)→ 修后 3 | exit 0(死 continue-on-error)→ 修后 3 触发 continue-on-error 生效 | pass=true / warnings=[...] |

### 初版方案
改 :235-237 让 warnings 非空时 exit 3。未被推翻。

### 对抗审查结论
REFUTE subagent 确认:exit 3 全路径不可达,grep `sys.exit` 仅 183/234/236/237 四处,无 exit 3。
spec + docstring 双源印证 exit 3 是契约。

### 修订方案
采纳。注释说明 precedence(errors 1/2 压 warnings 3)+ 标注 dead-links 的 exit 4 仍保留(reserve)。
**范围控制**:不本轮碰 --json 的 pass-vs-exit-code 一致性(见过程意外),记 backlog。

### 数据流 hops
无跨层。exit code = producer,argparse/CI/shell = consumer。单点改动。

### 变种横向 grep
同族:exit code 4(--dead-links)。grep 确认无 `sys.exit(4)` + 无 check_dead_links 函数 →
iter 3 处理(用户决定:删 flag + 删 CI job)。

### 改动文件
- `scripts/validate.py`(:232-241 exit 路径重写,恢复 exit 3)

### 测试证据
- 临时把 logging-standards.md 的 last_validated 改 2024-01-01 → `--stale` exit **3** ✓
- 恢复后 `--stale` exit **0** ✓
- `--stale --json`:pass=true / warnings=1 / exit **3** ✓
- 无 errors 时仍 exit 0(未回归)
- meta-tests 不变:ai PASS / plan_debug PASS

### 过程意外 / 与预期偏差
**iter 2 的修改暴露了 --json 模式的一致性 gap**:`pass=true` 但 exit 3。机器消费者若同时查
`pass` 字段和 exit code 会矛盾。**当前无此消费者**(CI 只看 exit code),记 backlog [低]:
应在 JSON 加 `warnings_count` 或文档化"pass 只反映 errors,不反映 warnings"。不在本轮扩范围。

### 遗留 backlog
- [低] --json pass 字段语义:exit 3 + pass=true 的一致性(文档化或加 warnings_count)。

---

## 迭代 3 — --dead-links 空壳 + 每周 CI 假绿(用户决定:删 flag + 删 CI job)

### 触发的理论缺口
假满分 / 死代码:`validate.py --dead-links` 被 argparse 接受(:193)但 main() 从不读 `args.dead_links`,
无 `check_dead_links` 函数(grep 零命中),无 `sys.exit(4)`。**空壳 flag**。更严重:
`.github/workflows/validate.yml:77-88` 的 `dead-links` job 每周一 09:00 UTC 跑它,**无 continue-on-error**
→ 每周假绿(exit 0 = "links verified" 但零工作)。这是活跃的 false-positive 信号,非潜伏。

### grep journal 结果
spec:406/414 文档化 --dead-links 承诺(对外部 URL 检 200)。无实现。REFUTE subagent(B2)定性:
比 iter 2 stale 更紧急(stale 潜伏 + continue-on-error;dead-links 活跃假绿 + 无 continue-on-error)。

### 合法 shape 清单(--dead-links 行为)
| Shape | 判别 | 现状 |
|-------|------|------|
| flag 传入 | args.dead_links True | argparse 接受,main 忽略 |
| 外部 URL 死链 | http(s) 链接 4xx/5xx | **从不检测**(无 checker) |
| exit 4 | warnings 含 dead-link | **不可达**(无 sys.exit 4) |
| CI job 触发 | schedule weekly | 跑,exit 0,假绿 |

### 退化输入×消费者
| 输入＼消费者 | 本地 --dead-links | CI weekly job | spec/docstring |
|------------|------------------|--------------|----------------|
| 死外部 URL | exit 0(假绿) | exit 0(假绿) | 承诺检测(谎) |
| flag 传入 | 静默成功 | n/a | 承诺检测(谎) |

### 初版方案(被推翻点)
三选项:实现 / 删 / 保留+warning。**用户决定:删 flag + 删 CI job**(最诚实、最小改动、不留债)。

### 对抗审查结论
REFUTE subagent(B2/M5):确认空壳 + 活跃假绿,定性比 iter 2 紧急。采纳用户删决策。
**逐跳追踪发现第 4 个消费者**:`harness-evolution.md:122` 提 "validate.py will error on dead link" ——
经核实是指**内部 related 交叉引用**(check_cross_references 确实抓),**非外部 URL**,故该行准确,**不改**。
(若不逐跳追,会误改正确的 harness 条目。)

### 修订方案
- 删 validate.py:--dead-links argparse(:193)+ docstring(:6,13)+ 修 iter 2 注释里的 dead-links 残留
- 删 .github/workflows/validate.yml:dead-links job(:77-88)
- 删 docs/specs:--dead-links 用法(:396)+ 意图(:406)+ exit 4(:414)
- 删 requirements.txt:requests(原为 dead-links 的网络依赖,现全仓无 import)= 死依赖清理

### 数据流 hops(--dead-links 概念的消费者)
| Hop | 消费者 | ✓/✗ |
|-----|--------|-----|
| 1 spec docstring | docs/specs:396,406,414 | ✓ 删 |
| 2 validate.py docstring | :6,13 | ✓ 删 |
| 3 validate.py argparse | :193 | ✓ 删 |
| 4 CI job | validate.yml:77-88 | ✓ 删 |
| 5 requirements requests | requirements.txt:2 | ✓ 删 |
| (harness-evolution.md:122 经核实是内部 xref,非本概念,不改) | | ✓ |

全 5 hops ✓。

### 变种横向 grep
死依赖(requests):grep 全 scripts/ 无 import → 确认死,删。
死 flag:无其他空壳 argparse flag(本轮扫 --pack/--installed/--stale/--json 均有消费者)。

### 改动文件
- `scripts/validate.py` (删 --dead-links argparse + docstring 行 + 修 iter 2 注释残留)
- `.github/workflows/validate.yml` (删 dead-links job)
- `docs/specs/2026-05-31-repo-structure-design.md` (删 --dead-links 用法/意图/exit 4)
- `scripts/requirements.txt` (删 requests 死依赖)

### 测试证据
- `validate.py --dead-links`:unrecognized arguments(exit 2,argparse 拒绝)✓
- `validate.py --help`:无 --dead-links ✓
- `check_all.py` exit 0 ✓
- `.github/workflows/validate.yml` YAML 合法 ✓
- 重装 requirements(无 requests)后:check_all/ai/plan_debug/validate/gen_index 全 PASS ✓
- meta-tests 不变

### 过程意外
逐跳追踪发现 harness-evolution.md:122 看似是 dead-links 消费者,实为内部 xref(准确,不改)。
**范围控制**:spec:402 还写 "Cross-reference bidirectionality" 但 validate.py 的 check_cross_references
只查存在性 + archived/deprecated,**不查双向性**(harness-evolution.md:123 自承 "does NOT catch this")。
spec:402 与代码不符,记 backlog [中],不在本轮扩范围。

### 遗留 backlog
- [低] --json pass 字段语义(iter 2)。
- [中] spec:402 "Cross-reference bidirectionality" 与代码不符(实只查存在性)。文档漂移,非代码 bug。

---

## 迭代 4 — check_review_signals.py 退出码反转 + 无去重写副作用(REFUTE 推翻 A/B 选 C)

### 触发的理论缺口
死契约 + 假满分 + 配置卫生:check_review_signals.py docstring(:26-27)承诺
"0 = always (advisory; never blocking)",但 --audit-harnesses 路径 return 1 三处
(:243 dry-run / :250 写后 / :258 缺文件)。**写副作用**:audit 发现 tier 通胀时
append_to_log 向**被追踪文件** common/meta/harness-feedback-log.md 追加,且**无去重**
→ 每次 check_all.py 跑都重复追加相同块。check_all.py:50 不传 --dry-run。

### grep journal 结果
兄弟脚本 check_feedback_signals.py(:18-19, :150)是 advisory 契约的**正确范例**
(总 return 0,findings 打 stdout)。证明本脚本 docstring 是真契约,audit 分支是 drift。

### 合法 shape 清单(--audit-harnesses exit paths)
| Shape | 旧 exit | 应 exit | 处理 |
|-------|---------|---------|------|
| 无 findings | 0 | 0 | ✓(已对) |
| dry-run + findings | 1(最糟的谎) | 0 | ✓ 改 |
| findings + 写 log | 1(谎) | 0 | ✓ 改 |
| 缺 review-report 文件 | 1 | 1 | ✓(合法 usage error) |
| review 模式无 signals | 0 | 0 | ✓ |
| review 模式 dry-run | 0 | 0 | ✓(与 audit dry-run 现一致) |

### 退化输入×消费者
| 输入＼消费者 | check_all SUMMARY | tracked log 文件 | 干净 git tree |
|------------|------------------|-----------------|--------------|
| tier 通胀,旧代码 | exit 1(慢性失败) | 重复增长(无去重) | dirty |
| tier 通胀,新代码 | exit 0 + findings 列在 SUMMARY | 不写(check_all 传 --dry-run)| clean |
| 无通胀 | exit 0 | 不写 | clean |

### 初版方案(被推翻点)
两选项 A(修 docstring 保 return 1)/ B(return 0 保 docstring 意图)。**REFUTE subagent 推翻**:
- A 错:return 1 是 hack(comment 自承),非设计;docstring 与兄弟脚本契约一致 = 真契约。
- B 错:check_all.py:56-62 SUMMARY 只列失败脚本名,不看 findings → B 让通胀在 SUMMARY 隐形
  (除非也改 check_all 解析 stdout)→ 隐形 = 风险 (a)。
- 两者都保留无去重写副作用 = 独立 [blocker]。

### 对抗审查结论
REFUTE subagent 定性 **Option C 是唯一正确**:audit return 0(advisory)+ check_all 传
--dry-run 且 SUMMARY 显式列 advisory findings + append_to_log 加去重。三件一起做。
**实证验证(关键,证明 no-dedup 是真 bug 非 REFUTE 空谈)**:合成 inflation(R1 N→A),
跑 audit x3:旧代码 log 82→87→92→97 行逐次增长(每次 +5)。REFUTE 的理论定性经实证坐实。

### 修订方案(Option C,采纳)
1. check_review_signals.py:audit 三处 return 1 → return 0(advisory);docstring 改
   "0 = scan ran; 1 = usage error";append_to_log 加同日(harness+signal+item_ref+detail)指纹去重。
2. check_all.py:audit 调用传 --dry-run(不写 tracked 文件);run() 加 capture 选项;
   SUMMARY 显式列 advisory findings(从 audit stdout 提取 "- " 行)。

### 数据流 hops(tier-inflation 信号)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 audit_harness_tiers 发现 | detector → main | ✓ |
| 2 main 打印 + append_to_log | main → stdout + log 文件 | ✓(去重后) |
| 3 check_all run() 捕获 | subprocess → SUMMARY | ✓(capture) |
| 4 SUMMARY 列 advisory | check_all → 用户 | ✓ |

### 变种横向 grep
同族"advisory 脚本谎报 exit 1":check_feedback_signals.py 经核**正确**(总 return 0)。
同族"写副作用":validate.py 无写副作用(只读);其他 check_* 脚本待扫(iter 8+)。

### 改动文件
- `scripts/check_review_signals.py` (docstring + audit exit codes + append_to_log 去重)
- `scripts/check_all.py` (run() capture + --dry-run + advisory SUMMARY)

### 测试证据
- audit 有 findings:exit 0 ✓(旧 1)
- audit --dry-run:exit 0 ✓(旧 1,最糟的谎)
- 去重:run1 写 1 条(82→87 实测后重测 77→82),run2-4 写 0 条(log 不再增长)✓
- check_all(干净):exit 0,"All checks passed." ✓
- check_all(有通胀):exit 0,"All checks passed (with advisory findings above)" + 列出 harness ✓
- check_all 不写 tracked log(--dry-run):git diff 空 ✓
- 缺 review-report:exit 1(合法 usage error)✓
- review 模式无 signals:exit 0 ✓
- validate/gen_index/ai/plan_debug 全 PASS(无回归)✓

### 过程意外
**指纹首版写错**:初版 fingerprint 用 "header + Signal + Observation" 三行,但实际 block
是 "header + Signal + Scenario + Observation" 四行(Scenario 在中间)→ 指纹永远不匹配 →
去重失效。实证抓到(run 87→92→97 仍增长),修指纹为四行后去重生效。
教训:dedup 指纹必须与实际写入 layout 完全一致,别凭记忆。

**假绿陷阱(本会话第二次)**:`python3 ... | head -2; echo $?` 报 exit=0,实际是 head 的
exit 非 python 的。直接 `python3 ... >/dev/null 2>&1; echo $?` 才是真 exit。Step 5 证据纪律
兑现:不信管道末端的 exit code。

### 遗留 backlog
- [低] --json pass 字段语义(iter 2)。
- [中] spec:402 "Cross-reference bidirectionality" 与代码不符(iter 3)。
- [低] audit 去重指纹是 4 行完整匹配;若 detail 文本微改(如 path 变),不算同一条。可接受(通胀点稳定)。

---

## 迭代 5 — tier-cell 正则 `[N CAP]` 匹配空格(潜伏解析 bug,iter 4 audit 之下)

### 触发的理论缺口
死代码 / 假满分:`check_review_signals.py:80,87` 用字符类 `[N CAP]` 意图匹配
N/C/A/P,但**方括号内的空格是字面量** → 实际匹配 `{N, space, C, A, P}`,会接受
空 tier 单元格。被下游 filter `if t in "NCAP"`(:83)和 `not in TIER_RANK`(:113)
**巧合救回**正确结果(因 `" " in "NCAP"` = False),但正则本身是 trap。

### grep journal 结果
REFUTE iter 4 subagent(M4/m4)定性:此 bug 在 iter 4 audit 之下,audit 报告可靠性
受影响。本轮独立修。

### 合法 shape 清单(tier 单元格内容)
| Shape | 旧正则 `[N CAP]` | 新正则 `[NCAP]` |
|-------|-----------------|----------------|
| `N`/`C`/`A`/`P` | ✓ 匹配 | ✓ 匹配 |
| 空格 ` ` | ✓ **误匹配**(bug) | ✗ 不匹配 |
| 小写 `n` | ✗ | ✗ |
| 其他字母 | ✗ | ✗ |

### 退化输入×消费者
| 输入＼消费者 | parse_harness_items | parse_harness_frontmatter_tier | audit 结果 |
|------------|--------------------|-------------------------------|-----------|
| 空 tier 单元格 | 旧:返回 [' ']→filter 救回 [];新:直接 [] | 旧:返回 ' '→filter 救回 None;新:None | 无差异(filter 救回)但正则 trap 消除 |

### 初版方案
`[N CAP]` → `[NCAP]` 两处。移除现在多余的 salvage filter(`if t in "NCAP"`)。
**未被推翻**。

### 对抗审查结论
轻量自对抗(单行正则改,有实证测试)。实证:旧正则 `re.search('[N CAP]', '| R1 |   |')`
匹配空格(repr ' ');新 `[NCAP]` NO MATCH。

### 修订方案
采纳。两处(`:80` source_tiers + `:87` fm_tier)同改,加注释防回退("Do NOT write
[N CAP]"). 移除 `:83` salvage filter(正则正确后多余,但保留 `:113` 的 TIER_RANK 校验
fm_tier 合法性,那是语义校验非 trap-salvage)。

### 数据流 hops
无跨层。正则 = producer,audit 比较逻辑 = consumer。单点。

### 变种横向 grep
同族"方括号含意外空格"正则:grep `\[.* .*\]` in scripts/ —— 仅这两处 + `[A-Z]\d+`(无空格,安全)。
同族"正则匹配过宽":detect_signals 的 `\*\*\([N CAP]\)\*\*`(:166)——**同样 bug,第三处**!
本轮一并修(横向 grep 兑现)。

### 改动文件
- `scripts/check_review_signals.py`(`:80,:87,:166` 三处 `[N CAP]`→`[NCAP]` + 注释;移除 :83 salvage filter)

### 测试证据
- 合成 harness 含空 tier 单元格:source_tiers=['N'](空格单元格被排除)✓
- 真实 harness(logging/raii/harness-evolution):items+sources 解析不变 ✓
- audit --dry-run:exit 0,"No tier inflation" ✓
- check_all / ai / validate 全 PASS(无回归)✓

### 过程意外
**横向 grep 发现第三处**:`detect_signals:166` 的 `\*\*\([N CAP]\)\*\*` 同 bug
(item 级 tier-mismatch 检测的正则)。原 REFUTE 只报 :80/:87 两处,横向 grep 兑现补第三处。
教训:REFUTE 报的"已知"也要横向 grep 找同变种(Step 6 强制)。

### 遗留 backlog
(无新增;iter 2/3 backlog 不变)

---

## 迭代 6 — T2-cap 是正确的;eval README 假晋升承诺 + 模板枚举误导(REFUTE 选 B)

### 触发的理论缺口
对称性 / 假承诺:evaluate_ai_protocol.py recommend_tier()(:53-70)只能返回 T0/T1/T2,
但 update_model_registry.py(:26-29,:38)有 T3/T4 渲染分支。REFUTE subagent 定性:
**T2-cap 是正确的**(T3/T4 定义上需人门控——model-registry.md Tier Policy + capability-matrix
要求 strong-model/repo-specific eval/human approval,弱模型 eval 无法产生这些信号)。
真正 bug 在文档:**eval README:16 假承诺 "T2->T3 requires passing patch and review cases"**,
误导操作员以为弱模型 eval 能认证 T3。

### grep journal 结果
REFUTE iter 6 subagent 三选项 A(补 T3/T4 规则)/ B(cap 正确,修文档)/ C(删 T3/T4 handler)。
定性 B:A 会假阳性能力声明(用 T2 证据认证需人门控的 T3);C 破坏手动 T3/T4 行渲染。
capability-matrix.md:14,32 + model-registry.md:14-15 双源印证 T3/T4 是人门控。

### 合法 shape 清单(tier 来源)
| Shape | producer | 现状 |
|-------|----------|------|
| 自动 eval 产出 | recommend_tier() | T0/T1/T2 ✓(cap 正确) |
| 手动 registry 编辑 | 人写 markdown | T3/T4 ✓(forward-compat handler 渲染) |
| 假承诺 "eval 产 T3" | README:16(谎) | 文档 bug |

### 退化输入×消费者
| 输入＼消费者 | 操作员决策 | registry 渲染 | 能力声明 |
|------------|-----------|--------------|---------|
| README:16 假承诺(旧) | 误信 eval 可认证 T3 | n/a | **假阳性** |
| README:16 修正后 | 知 eval cap T2,T3/T4 需人门控 | n/a | 诚实 |

### 初版方案(被推翻点)
三选项待决。**REFUTE 选 B**,推翻 A/C。采纳 B。

### 对抗审查结论
REFUTE subagent:[major] README:16 假晋升承诺(唯一 must-do);[minor] 模板枚举误导;
[minor] update_model_registry 无 tier 校验(防 typo 渲染成 T0)。

### 修订方案(采纳)
1. docs/ai/evals/weak-model/README.md:14-16 — 删假 T2->T3 承诺,改"weak-model eval caps at T2"。
2. docs/ai/weak-model-evaluation-report.template.md:39 — 枚举标注 "T3/T4 require manual promotion"。
3. update_model_registry.py — 加 VALID_TIERS 白名单 + 注释"T3/T4 是 forward-compat 非死代码",防未来误删。

### 数据流 hops(tier 概念)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 recommend_tier | eval → report.json (T0/T1/T2) | ✓ |
| 2 update_model_registry | report.json → registry.md 行 | ✓(白名单校验) |
| 3 手动 T3/T4 | 人 → registry.md | ✓(forward-compat handler) |
| 4 README 晋升承诺 | doc → 操作员决策 | ✓(修正后诚实) |

### 变种横向 grep
同族"文档承诺与代码不符":spec:402 双向性(iter 3 backlog)同族。capability-matrix.md
经核与 model-registry.md 一致(无新矛盾)。

### 改动文件
- `docs/ai/evals/weak-model/README.md` (删假 T3 晋升承诺,改 cap T2 说明)
- `docs/ai/weak-model-evaluation-report.template.md` (枚举标注 manual)
- `scripts/update_model_registry.py` (VALID_TIERS 白名单 + 校验 + forward-compat 注释)

### 测试证据
- T0/T1/T2/T3/T4 全接受(exit 0)✓
- T02/t2/T5/T 全拒(argparse error exit 2)✓
- registry 还原干净(git diff 空)✓
- check_all / validate / ai 全 PASS(无回归)✓

### 过程意外
REFUTE 发现的 README:16 比原触发点(T2-cap)更严重——是唯一**主动误导操作员**的行。
原以为 update_model_registry T3/T4 handler 是 bug,实为 forward-compat(手动晋升路径)。
若不 REFUTE 直接走 A(补 T3/T4 规则),会引入假阳性能力声明。

### 遗留 backlog
(iter 2/3 backlog 不变)

---

## 迭代 7 — SKIP_DIRS 三副本重复(提取共享常量,防漂移)

### 触发的理论缺口
配置卫生 / 对称性:`{".git",".claudine","archive","templates","docs",".github"}` 在
validate.py:28 + generate_index.py:43 + check_review_signals.py:105 三处**逐字重复**。
任一脚本加/减目录需同步改三处,否则两脚本对"哪些是 harness"分歧(validate 看 X / index 漏 X)。
REFUTE iter 1 subagent(m1)定性 drift risk。

### grep journal 结果
本会话实证:iter 1 见 INDEX 61 行 vs grep 75 harness 文件差异(部分是 archive/templates,
部分是多算)——正是 skip set 不一致的表现之一。

### 合法 shape 清单
| Shape | 判别 |
|-------|------|
| 单一权威定义 | 一处定义,其余 import |
| 三副本(旧) | 三处独立字面量,易漂移 |

### 初版方案
提取到 pack_utils.py(已是三脚本共享的 import 源)作 HARNESS_SKIP_DIRS,三脚本 import。
**未被推翻**(轻量自对抗,机械重构)。

### 对抗审查结论
轻量自对抗。验证三脚本 harness count 一致(validate 72 == generate 72)证无漂移。

### 修订方案
采纳。pack_utils.py 加 HARNESS_SKIP_DIRS + 注释(防未来误删);三脚本 import 替代字面量。

### 数据流 hops
无跨层。skip set = producer,harness walker = consumer。单点定义。

### 变种横向 grep
同族"跨脚本字面量重复":TIER_RANK(check_review_signals 独有,无重复);VALID_TIERS(iter 6 新增,
仅 update_model_registry 独有)。无其他重复需合并。

### 改动文件
- `scripts/pack_utils.py` (加 HARNESS_SKIP_DIRS 常量)
- `scripts/validate.py` (import 替代字面量)
- `scripts/generate_index.py` (import 替代字面量)
- `scripts/check_review_signals.py` (import 替代字面量)

### 测试证据
- 单一定义残留检查:仅 pack_utils.py:16 ✓
- validate.find_harnesses == generate_index.find_harnesses == 72 ✓(无漂移)
- check_all / validate / gen_index / ai / plan_debug / audit 全 PASS ✓

### 过程意外
无。机械重构,实证无漂移。

### 遗留 backlog
(iter 2/3 backlog 不变)

---

## iter 8-10:R1 重枚举(Step 0)

iter 1-7 锁定在 validate/generate_index/check_review_signals/check_all/evaluate/update_model_registry
+ 共享常量。**R1 双向扩张要求**:不重扫已审维度。剩余未审脚本:
- check_feedback_signals.py(兄弟,iter 4 仅对比契约未深扫)
- check_ai_protocol.py / check_plan_protocol.py / check_debug_report.py(协议检查器)
- run_ai_protocol_check.py / evaluate_ai_protocol.py(已浅扫 tier)
- export_pack.py / install_pack.py / list_packs.py(pack 工具链)
每轮 Step 0 枚举该脚本的合法 shape + 退化输入,再对抗。

---

## 迭代 8 — check_ai_protocol.py 命令证据检查可被 name-drop 绕过(CI 活跃,eval gate)

### 触发的理论缺口
假满分 + 退化输入:check_ai_protocol.py:180-191 的命令证据检查用**裸子串匹配**
("cmake" in lowered),且 "python " 带尾空格(与其他 5 工具不对称)。弱模型在 residual-risk
行 name-drop 一个工具名("will use cmake")即满足 has_command_signal → 空 Verification run +
假成功声明 = **false green**。这是 weak-model eval gate 的核心检查。

### grep journal 结果
R1 扫描 subagent(扫 8 未审脚本)发现:[major] 此 bug(CI 活跃,fixture 一步之遥滑过)+
[major] export_pack.py rmtree 无校验(local-only)+ [minor] review-finding 死检查。
兄弟 check_debug_report.py:66 用 `\b(...)\b` 正确(证明作者知正确模式)。

### 合法 shape 清单(命令证据输入)
| Shape | 旧裸子串 | 旧 `\s` lookahead | 新 `(?=(?:[/.=]| +\S))` |
|-------|---------|-------------------|----------------------|
| 真 cmd `python scripts/x.py` | ✓("python ") | ✓ | ✓ |
| 真 cmd `cmake --build` | ✓("cmake") | ✓ | ✓ |
| name-drop 行尾 `will use cmake\n` | ✓(**误匹配**) | ✓(\n 匹配 \s,**误匹配**) | ✗(需同行有内容) |
| 裸散文 `prefer cmake` | ✓(误匹配) | ✗ | ✗ |
| 工具+名词 `the cmake build` | ✓(误匹配) | ✓ | ✓(残留歧义,见过程意外) |

### 退化输入×消费者
| 输入＼消费者 | 旧 check_ai_protocol | 新 | CI test_ai_protocol |
|------------|---------------------|----|----|
| 空 Verification + name-drop | exit 0(**假绿**) | exit 1(挡) | fixture 一步之遥→现在挡住 |
| 真 cmd 在 Verification run | exit 0 | exit 0 | good fixtures 仍过 |

### 初版方案(被推翻点)
初版 lookahead `(?=\s|/|\.|=)`。**实证推翻**:\s 匹配行尾换行符 \n → name-drop "will use cmake\n"
仍匹配 → bypass 未挡。改 lookahead 为同行内容 `(?=(?:[/.=]| +\S))`。

### 对抗审查结论
R1 扫描 subagent 提供攻击面;实证证明初版 lookahead 不足(\s 陷阱)。无独立 REFUTE(单函数改,
meta-test 套件即对抗——good fixtures 必过、bad fixture 必挡)。

### 修订方案(采纳)
lookahead 要求工具名同行后跟 `/`/`.`/`=` 或"空格+非空格"。挡 name-drop 行尾 + 裸散文。
残留歧义(tool+普通名词 如 "the cmake build")记录 backlog——语法层无法区分 "cmake build"(名词短语)
与 "cmake --build"(命令),兄弟 check_debug_report.py 同样接受此歧义。

### 数据流 hops
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 弱模型输出 | model → .output.md fixture | ✓ |
| 2 check_ai_protocol 命令证据 | fixture → has_command_signal | ✓(regex 修后) |
| 3 test_ai_protocol 套件 | bad/good fixtures → CI gate | ✓ |

### 变种横向 grep
同族"裸子串匹配当证据":check_debug_report.py:66 已用 `\b\b`(更严但仍歧义 tool+noun);
check_plan_protocol / check_feedback_signals 无命令证据检查。无其他变种。

### 改动文件
- `scripts/check_ai_protocol.py`(:180-191 命令证据 regex 重写)

### 测试证据
- name-drop "will use cmake" 行尾:exit 1(挡)✓(旧 exit 0 假绿)
- 裸散文 "prefer cmake":exit 1 ✓
- 空 residual 无命令:exit 1 ✓
- 真 cmd(cmake --build / python x.py / ctest --test-dir):regex 直接匹配 ✓
- **test_ai_protocol 套件(meta-test,真实 CI gate):PASS** ✓
- test_plan_debug / check_all:PASS ✓

### 过程意外 / 与预期偏差
1. **初版 lookahead `(?=\s|...)` 被 \n 击穿**:\s 含换行符,name-drop 在行尾时 \n 满足 \s →
   bypass 未挡。实证抓到(直接调 check_verification_claims 返回 [],与期望矛盾)→ 深挖发现 \s 陷阱。
   教训:lookahead 用 \s 时必须考虑行尾换行。
2. **shell word-splitting 假红**:`for chk in "..."; do python3 scripts/$chk` 把带空格的命令拆错
   → generate_index/check_review 误报 FAIL。直接单跑 exit 0。第二次踩同类(shell 末端信号不可信)。
3. **tool+名词残留歧义**:"the cmake build" vs "cmake --build" 语法层无法分。兄弟脚本同接受。
   记 backlog,不强推(会 false-red 真 cmd)。

### 遗留 backlog
- [低] 命令证据 tool+名词歧义(the cmake build)——语法层限制,需语义检查或更强结构化输出。
- [低] export_pack.py rmtree 无 --out 校验(local-only 数据删除风险,R1 扫描 [major])。
- [低] check_ai_protocol.py:153 review-finding 死检查(总被 section 检查掩盖)。

---

## 迭代 9 — export_pack.py rmtree 无校验(local 数据删除,加 sentinel + 保护路径)

### 触发的理论缺口
配置卫生 / 数据安全(R1 扫描 [major],iter 8 backlog):export_pack.py:49-50
`if export_root.exists(): shutil.rmtree(export_root)` 无校验。--out 默认 "dist",
export_id = pack_ids join。`export_pack.py cpp-testing --out <dir>` 若 <dir>/cpp-testing
存在(含无关用户内容)→ **静默删除**。

### grep journal 结果
R1 扫描 subagent 定性 local-only(CI 恒用 fresh /tmp/dev-guidelines-dist),但真数据删除。
实证(本轮):mkdir /tmp/x/cpp-testing + precious.txt → 跑 export → precious.txt **YES-DELETED**。

### 合法 shape 清单(export_root 状态)
| Shape | 旧行为 | 新行为 |
|-------|--------|--------|
| 不存在 | mkdir | mkdir |
| 前次 export(有 export.yml) | rmtree ✓ | rmtree ✓(sentinel 在) |
| **用户无关内容(无 sentinel)** | **rmtree(数据删除)** | **refuse + 清晰错误** |
| --out = ROOT/home/cwd | rmtree 子目录(危险) | argparse error 拒绝 |

### 退化输入×消费者
| 输入＼消费者 | 旧 | 新 |
|------------|----|----|
| --out . / .. / ~ | 静默删 cwd/home 子目录 | 拒绝(protected paths) |
| --out <含无关内容的 dir> | 删 | 拒绝(sentinel 缺) |
| --out <前次 export> | 删+重建 ✓ | 删+重建 ✓(sentinel 在) |
| --out /tmp/dev-guidelines-dist(CI) | ✓ | ✓ |

### 初版方案
sentinel(export.yml)+ protected paths(ROOT/home/cwd)拒绝。**未被推翻**(轻量自对抗,
CI flow 即回归测试)。

### 对抗审查结论
轻量自对抗。关键:CI flow(--zip 到 /tmp)必须仍过 → 实测 TEST 4 过。
sentinel 选 export.yml(每次 export 必写,:85)。

### 修订方案(采纳)
1. `_is_safe_out_dir`:拒 ROOT/home/cwd/其祖先。
2. rmtree 前查 export.yml sentinel;缺则 RuntimeError(→ main 捕获转 argparse error)。
3. main 包 RuntimeError → parser.error(干净错误非 traceback)。

### 数据流 hops
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 export.yml 写入 | export_pack → export_root | ✓(每次必写) |
| 2 re-export 读 sentinel | export_pack → 决策 rmtree | ✓ |
| 3 protected path 校验 | main → _is_safe_out_dir | ✓ |

### 变种横向 grep
同族"无校验 rmtree":install_pack.py 无 rmtree(只写);其他脚本无删除操作。无变种。

### 改动文件
- `scripts/export_pack.py`(_is_safe_out_dir + EXPORT_SENTINEL + rmtree 守卫 + main 错误处理)

### 测试证据
- --out . / .. / ~ :exit 2(protected 拒绝)✓
- 用户内容(precious.txt):survives(refuse rmtree)✓
- 前次 export re-export:exit 0(sentinel 在,rmtree 允许)✓
- CI flow(--zip):exit 0,zip+sha256 创建 ✓
- check_all / validate / ai 全 PASS ✓

### 过程意外
初版 RuntimeError 在 CLI 直接抛 traceback(不友好)。main 包 try/except 转 parser.error
→ 干净 argparse 错误(exit 2)。UX 改进。

### 遗留 backlog
- [低] 命令证据 tool+名词歧义(iter 8)。
- [低] check_ai_protocol.py:153 review-finding 死检查(iter 8)。

---

## 迭代 10 — check_debug_report.py `g++` 永不匹配(\b 在 + 后失效,iter 8 同族)

### 触发的理论缺口
假最差 / 退化输入(R1 变种横向 grep,iter 8 同族):check_debug_report.py:66-72
`has_command_signal` 用 `\b(g\+\+)\b`,但 **\b 在非词字符 + 后不触发** → `g++` 在所有形式
(含真 cmd `g++ main.cpp`)全 False。debug report 用 g++ 作 verification 命令 → false RED
("verification requires command evidence")。诚实原则 #3:回归工具里漏报(false-negative)与
误报等险。R1 扫描 subagent 当初标 [minor]"niche",实证证明是真 false-RED(全形式失效)。

### grep journal 结果
iter 8 修 check_ai_protocol 命令证据;横向 grep(iter 8 backlog 同族)发现 check_debug_report
是兄弟实现,但其 `g++` 边界有独立 bug(\b 陷阱)。R1 变种级扩张兑现——不重扫已审维度,
扩到兄弟脚本的同变种。

### 合法 shape 清单(命令工具)
| 工具 | 旧 `\b...\b` | 新 `(?=\s|[/.=]|$)` |
|------|-------------|---------------------|
| python/pytest/cmake/clang/gcc(词尾词) | ✓ | ✓ |
| **g++(+ 后无 \b)** | **✗ 全 False** | ✓ 全 True |
| msbuild/lldb/gdb | ✓ | ✓ |

### 退化输入×消费者
| 输入＼消费者 | 旧 has_command_signal | 新 |
|------------|----------------------|----|
| `g++ main.cpp`(真 cmd) | **False(false-RED)** | True |
| `python x.py` | True | True |
| 无工具 | False | False |

### 初版方案
trailing `\b` → `(?=\s|[/.=]|$)`(兼容 g++ 的非词尾)。**未被推翻**(实证驱动)。

### 对抗审查结论
轻量自对抗。实证:旧全 False(含 g++ main.cpp);新全 True。回归 plan_debug 套件过。

### 修订方案(采纳)
trailing anchor 改 `(?=\s|[/.=]|$)`,注释说明 \b 在 + 后失效的原因。tool+名词散文歧义
("the cmake build")保留接受(同 iter 8,语法层限制)。

### 数据流 hops
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 debug report Verification 段 | report → has_command_signal | ✓(g++ 修后) |
| 2 check_debug_report 决策 | signal → errors | ✓ |

### 变种横向 grep
同族"命令证据 \b 陷阱":check_ai_protocol.py 已修(iter 8);check_debug_report.py 本轮修;
check_plan_protocol.py 无命令证据检查。无其他变种。

### 改动文件
- `scripts/check_debug_report.py`(has_command_signal trailing anchor \b→`(?=\s|[/.=]|$)`)

### 测试证据
- g++ main.cpp / g++ -o x / bare g++ / ran g++ :全 True(旧全 False)✓
- python/cmake/clang 等:仍 True ✓
- 无工具:False ✓
- test_plan_debug_protocol 套件:PASS ✓
- test_ai_protocol / check_all / validate:PASS ✓

### 过程意外
R1 扫描当初标 [minor] "niche"——实证推翻(全形式失效,非 niche)。教训:审查者的严重度
判断需实证校验,别照单接受。

### 遗留 backlog
- [低] 命令证据 tool+名词歧义(iter 8,两脚本共用,语法层限制)。
- [低] check_ai_protocol.py:153 review-finding 死检查(iter 8)。

---

## 收口(iter 11)— 10 轮对抗循环汇总

**Date:** 2026-08-04
**Status:** ✅ 用户要求"$adversarial-development-loop 规划后续走个10轮迭代"完成。
本节是累计汇报(skill 终止条件:测试增量/文件数/blocker-major/backlog/shape 覆盖/hops)。

### 触发
用户:`$adversarial-development-loop 规划后续走个10轮迭代`。目标 = 本仓库
(dev-guidelines 元仓库:harness markdown + Python 校验脚本)。"机器消费产物" = scripts/
(validate.py / generate_index.py / check_* / meta-tests),等价于其他项目的 test_core。
本仓库此前无 journal。

### 10 轮概览(iter 1-10)

| iter | 主题 | REFUTE / 证据 | 产出 |
|---|---|---|---|
| 1 | INDEX.md 反斜杠路径分隔符(CI 阻塞) | REFUTE 验证单根因 | 重生成,--check 0 |
| 2 | validate.py exit 3 不可达 | REFUTE 验证 + spec 双源 | 恢复 exit 3,实证触发 |
| 3 | --dead-links 空壳 + 每周 CI 假绿 | REFUTE B2(活跃假绿) | 删 flag + CI job + requests 死依赖 |
| 4 | check_review_signals 退出码反转 + 无去重写副作用 | **REFUTE 推翻 A/B 选 C** + 实证 no-dedup | Option C:advisory exit 0 + 去重 + check_all 不写 |
| 5 | tier-cell 正则 `[N CAP]` 匹配空格 | 横向 grep 兑现 3 处 | `[NCAP]` x3 + 注释 |
| 6 | T2-cap 正确;eval README 假 T3 晋升承诺 | **REFUTE 选 B**(A/C 推翻) | 删假承诺 + 白名单校验 |
| 7 | SKIP_DIRS 三副本重复 | 轻量自对抗 | 提取 HARNESS_SKIP_DIRS 到 pack_utils |
| 8 | check_ai_protocol 命令证据 name-drop 绕过(CI 活跃) | R1 扫描 + 实证(\s 陷阱) | lookahead 同行内容 |
| 9 | export_pack.py rmtree 无校验(数据删除) | 实证 precious.txt 删除 | sentinel + protected paths |
| 10 | check_debug_report `g++` 永不匹配(\b 陷阱,iter 8 同族) | R1 变种横向 grep + 实证 | trailing anchor 修 |

### 累计指标

**健康检查**:baseline(validate PASS / generate_index --check **FAIL** / check_all **exit 1** /
meta-tests PASS)→ **全部 PASS**(validate / generate_index --check / test_ai_protocol /
test_plan_debug_protocol / check_all 五项绿)。**CI-blocking 问题(iter 1)从 FAIL→PASS**。
**REFUTE subagent**:4 个独立 subagent(scope / iter 4 / iter 6 / iter 8 R1-scan):
- **1 个推翻整方向**(iter 4:推翻 A/B 两选项 → Option C)
- **1 个推翻严重度判断**(iter 6:推翻"加 T3/T4 规则",确证 T2-cap 正确)
- **1 个 refuted 我的"check_all bool-OR bug"候选**(iter 0 scope:代码正确,我差点修对代码)
- **1 个发现我漏的缺口家族**(iter 8 R1-scan:check_ai_protocol bypass + export_pack + g++)

**代码**:15 文件改动,~272 insertions / 146 deletions(不含新 journal)。1 新文件(loop-journal.md)。

**blocker/major 累计(REFUTE + 实证抓到的)**:
- iter 1:INDEX.md Windows 反斜杠(CI 阻塞)
- iter 2:exit 3 死契约(spec 双源承诺)
- iter 3:--dead-links 空壳 + 每周 CI 假绿
- iter 4:[blocker] no-dedup 写副作用(实证 log 逐次增长)+ [blocker] docstring 反转 +
  REFUTE 推翻 A/B(若走 A 会 ship 慢性失败;走 B 会隐藏通胀)
- iter 5:[major] 正则 `[N CAP]` 含空格(横向 grep 兑现 3 处)
- iter 6:[major] eval README 假 T3 晋升承诺(REFUTE 发现,比原触发点更严重)
- iter 8:[major] 命令证据 name-drop 绕过(CI 活跃,fixture 一步之遥)+ 初版 \s 陷阱被实证推翻
- iter 9:[major] export_pack rmtree 无校验(实证 precious.txt 删除)
- iter 10:同族 g++ 永不匹配(实证全形式 false-RED;R1 当初误标 minor)
- **实现中发现对抗清单外的 bug**:iter 3 harness-evolution.md:122 疑似消费者(经核实是
  内部 xref 非 dead-links,不改——逐跳追踪避免误改正确代码)

### shape 覆盖表(累计)

| Datum | Shapes 枚举 | 覆盖 |
|---|---|---|
| validate.py exit codes | 0/1/2/3(4 删) | 全(iter 2/3) |
| --dead-links flag | 实现/空壳/删 | 删(iter 3) |
| check_review_signals audit exit | 0/1(谎)/advisory-0 | advisory-0(iter 4) |
| tier-cell 内容 | N/C/A/P/空格/小写/其他 | 全(iter 5,空格挡) |
| tier 来源 | 自动 T0-T2/手动 T3-T4 | 全(iter 6,白名单) |
| SKIP_DIRS | 单一权威/三副本 | 单一(iter 7) |
| 命令证据输入 | 真 cmd/name-drop/散文/tool+名词 | 全(iter 8/10,残留 tool+名词歧义) |
| export_root 状态 | 不存在/前次 export/用户内容/protected | 全(iter 9) |

### 数据流 hops 状态(累计,跨层改动全闭合)

| 跨层 datum | hops | 状态 |
|---|---|---|
| INDEX.md autogen zone(generate→INDEX→--check) | 1/1 ✓(iter 1) |
| validate exit code(argparse→main→CI exit) | 3/3 ✓(iter 2) |
| --dead-links 概念(spec/validate/CI/requirements 4 消费者) | 4/4 ✓(iter 3,全删) |
| tier-inflation 信号(audit→log→check_all SUMMARY→用户) | 4/4 ✓(iter 4) |
| tier-cell 正则(3 处 producer→audit/detect 消费) | 3/3 ✓(iter 5) |
| tier 概念(eval→registry→手动 T3/T4) | 4/4 ✓(iter 6) |
| SKIP_DIRS(pack_utils→3 脚本 walker) | 3/3 ✓(iter 7) |
| 命令证据(弱模型输出→check_ai_protocol→CI) | 3/3 ✓(iter 8) |
| export sentinel(写入→re-export 读→rmtree 决策) | 3/3 ✓(iter 9) |
| g++ 命令证据(debug report→has_command_signal) | 2/2 ✓(iter 10) |

**全 hops ✓,无 ✗**。

### REFUTE 救场的方向(避免 ship 的灾难)

最关键的 REFUTE 推翻(若不 REFUTE 会 ship 坏东西):
1. **iter 4 REFUTE 推翻 A/B 选 C**:若走 A(保 return 1 修 docstring),health-check 慢性
   失败;若走 B(return 0 不改 check_all),tier 通胀在 SUMMARY 隐形。C 三件一起做才对。
2. **iter 4 REFUTE 发现 no-dedup**:我原以为"写副作用"是配置卫生小问题,实证证明 log 每次
   check_all 重复增长——会污染 check_feedback_signals 的 re-review 阈值。
3. **iter 6 REFUTE 推翻"加 T3/T4 规则"**:若走 A,弱模型 eval 用 T2 证据认证需人门控的 T3 →
   假阳性能力声明。T2-cap 是正确的,bug 在文档(假晋升承诺)。
4. **iter 0 scope REFUTE refuted 我的 check_all bool-OR 候选**:代码正确(已 normalize 为 bool),
   我差点"修"正确的代码。

### 过程意外 / 跨轮教训(下一轮 PLAN 必 grep)

- **shell 末端信号陷阱(本会话 3 次)**:`cmd | head; echo $?` 报 head 的 exit 非 cmd 的;
  `for chk in "a b"; python3 scripts/$chk` word-split 带空格命令 → 假红。每次直接
  `cmd >/dev/null 2>&1; echo $?` 才是真 exit。Step 5 证据纪律反复兑现。
- **实证推翻 REFUTE 的严重度判断**:iter 10 g++ bug,R1 扫描标 [minor] "niche",实证证明
  全形式失效(false-RED 阻合法 cmd)。审查者的严重度需实证校验。
- **初版方案被实证推翻**:iter 8 初版 lookahead `(?=\s|...)` 被 \n 击穿(\s 含换行)→ name-drop
  行尾仍匹配 → bypass 未挡。实证抓到(直接调函数返回 [] 与期望矛盾)→ 改同行内容 lookahead。
- **逐跳追踪避免误改正确代码**:iter 3 harness-evolution.md:122 疑似 --dead-links 消费者,
  经核实是内部 xref 非 dead-links,不改。若不逐跳,会"修"正确的 harness 条目。
- **横向 grep 兑现(iter 5/10)**:iter 5 修 [N CAP] 横向 grep 发现第三处(detect_signals);
  iter 10 从 iter 8 backlog 横向 grep 兄弟脚本发现 g++ 同族 bug。Step 6 强制兑现。

### 终止条件评估

- **R1**:10 轮连续新发现(iter 1 CI 阻塞 → iter 2 死契约 → iter 3 假绿 → iter 4 推翻 A/B
  → iter 5 正则 trap → iter 6 假承诺 → iter 7 重复 → iter 8 绕过 → iter 9 数据删除 →
  iter 10 同族 false-RED),每轮新维度,未触发"连续 2 轮无新缺口"。
- **R4**:无静默轮——每轮都有实证验证的产出。置信度合理。
- **用户要求 10 轮**:完成(iter 1-10 + 本收口)。

### 遗留 backlog(完整清单,按优先级)

**[低]**:
- 命令证据 tool+名词歧义("the cmake build" vs "cmake --build")——两脚本共用,语法层限制,
  需语义检查或更强结构化输出。兄弟 check_debug_report.py 同接受。
- check_ai_protocol.py:153 review-finding 死检查(总被 section 检查掩盖,无错误信号,纯死代码)。
- validate.py --json `pass` 字段语义:exit 3 + pass=true 的一致性(文档化或加 warnings_count)。
- spec:402 "Cross-reference bidirectionality" 与代码不符(实只查存在性)。文档漂移。

### 下一步建议(非本轮范围)

- 61 个 harness 全是 draft 状态,从未 reviewed——可做 harness 内容质量审查(维度切换,
  脱离机器消费层,但高价值)。
- 强结构化弱模型输出(解命令证据 tool+名词歧义):要求 Verification 段用结构化字段而非散文。
- 0 号发现类问题(跨平台生成物潜伏):加 CI 检查 INDEX.md 在 linux 渲染(防 Windows 反斜杠再入)。

---

## 迭代 12(研究方向)— 5 个业界方向逐个判断:REFUTE 推翻初判,只做方向4

### 触发
用户:"根据推荐,每个去详细判断可行性,价值,如果值得做就做"。基于上轮调研(HalluJudge/SDD/
RouteLLM/METR/Willison)的 5 个方向。

### grep journal
本会话 iter 1-10 全在 scripts 契约层;本轮切到"研究方向判断"——R1 模块级扩张(从已审 scripts
扩到 harness 内容 + 业界方向对接)。无同类过往教训。

### ENUMERATE:5 方向 × 真实接入点矩阵(Step 0)
| 方向 | 业界锚点 | 本仓库接入点(读源码核实) | 初判 |
|---|---|---|---|
| 1 grounding | HalluJudge | check_review_findings:148 格式检查(非 grounding) | ✅做 |
| 2 spec→test | SDD | plan-protocol 8 行无结构化 test 字段 | ❌不做 |
| 3 eval→routing | RouteLLM | recommended_tier 唯一消费者=update_model_registry(只写 md) | ❌不做 |
| 4 subtle-error | Willison | 是 harness(markdown),契合仓库产物 | ✅做 |
| 5 internal eval | METR | 现有 eval 是 generic 协议校验 | ❌不做 |

### 对抗审查(2 REFUTE subagent,实现前)
**subagent A(证伪方向1实现)**:3 [blocker] 推翻方向1整方向:
- review-mode **无 diff 访问**(CLI 无 --diff/--repo-root,`run_ai_protocol_check.py:50`);
  review 审外部 diff(`prompts/weak-model-cpp-review.md:20` 内联 {DIFF})→ "路径在工作树存在"假红每个合法 review
- relocation 到 plan-mode:`Harnesses:` **语法未冻结**(4 格式:;-路径 / ,-路径 / prose / 重构版)
- Verification 路径提取假红 3 个 distilled 模板
**subagent B(证伪方向4 sourcing + 反驳 2/3/5 reject)**:
- [major] 方向4 sourcing:loop skill 不在 sources.md,违反 harness-quality-standards:94/80-83
- [major] 方向2 reject 太广:narrow 版(字段路径存在性)可行(但价值低 + 同语法前提)
- [minor] 方向5 循环论证过强:脚本测脚本非循环(但价值低)

### 修订方案(逐条 采纳/反驳/backlog)
- **方向1**:**全 reject**(采纳 subagent A)。语法冻结前不做;冻结后仅 Harnesses+skip-warn。诚实原则:不 ship 假红代码。
- **方向4**:**做,但修正 grounding**(采纳 subagent B)。用 NIST C19 + Mutation A17/A18(已注册权威),
  弃 OWASP C16(weak)与 loop skill(未注册)。
- **方向2**:维持 reject(narrow 可行但价值低 + 依赖方向1语法冻结)。
- **方向3**:维持 reject(narrow doc 版价值微小)。
- **方向5**:维持 reject(非循环但现有 test_ai_protocol 部分覆盖,价值低)。

### 数据流 hops(方向4 harness 接入既有 harness 网络)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 sources.md 注册(C19/A17/A18 已在) | sources → harness [Rx] | ✓ |
| 2 harness [R1]/[R2] → Reference Sources 表 | body tag → table | ✓ |
| 3 related: 4 目标 → 反向链接 | bidirectional | ✓(4/4) |
| 4 validate.py 校验 frontmatter+xref | harness → validate | ✓(exit 0) |
| 5 generate_index 收录 | harness → INDEX | ✓ |

### 改动文件
- `common/code-review/ai-generated-code-failure-modes.md`(新 harness,6 检查项 + 2 anti-pattern + Reference Sources)
- `common/code-review/review-checklist.md`(related 反向链接)
- `common/code-review/harness-driven-review.md`(related 反向链接)
- `common/testing/testing-strategy.md`(related 反向链接)
- `common/ai/ai-evaluation-and-regression-strategy.md`(related 反向链接)
- `INDEX.md`(同步收录)
- `docs/ai-evaluation-research-2026-08-04.md`(新,判断矩阵 + REFUTE 修订记录)

### 测试证据
- validate.py exit 0 ✓
- generate_index --check exit 0 ✓(harness 收录)
- 4 个 related 反向链接全部 bidirectional ✓
- [R1]/[R2] tag 全部经 Reference Sources 表解析到注册 source ✓
- check_all / test_ai_protocol / test_plan_debug 全 PASS ✓

### 过程意外 / 与预期偏差
**初判"方向1 ✅做"差点 ship 假红检查**。我自己在判断矩阵里标了"高价值+有雏形",还写了个 REFUTE
flag(方向1 review 可能无 diff)但**没核实就继续**。REFUTE subagent 读 CLI 参数表才发现 review-mode
根本没有 diff/repo-root 入参——"接入点是否存在"是可读源码核实的 known unknown,**没读就判可行 = 读代码
不精确**(Rationalization Table:"方案里的现状我记得是 X")。这正是 skill 的核心价值:对抗攻的正是
这种"我以为是"。

**方向4 sourcing 自我纠正**:初判想引 loop skill 作 source,REFUTE 抓出违反仓库自身 meta-harness
(harness-quality-standards:94)。改用已注册的 NIST C19 + Mutation A17/A18——既诚实(权威 source)
又契合(可靠性与测试充分性正是 subtle-error 主题)。**弃 OWASP C16 因其是应用安全,与 subtle-code-defect
主题 weak**——不该为了"看起来多源"硬塞不契合的 source。

### 遗留 backlog
- [中] 方向1 grounding:待 plan schema 冻结(capability-roadmap 重构完成后)再评估 Harnesses 路径
  存在性 + skip-warn 语义。
- [低] 方向2 narrow 版同上,待语法冻结。
- iter 1-10 backlog 不变。

---

## 迭代 13 — Phase 6 eval 基础设施(run_eval.py 渲染器)+ REFUTE 推翻原方案

### 触发
用户:能力缺口诊断后选 "①真实 eval 跑一次(Phase 6 最小闭环)"。决定先搭基础设施(不跑真模型)。

### grep journal(Step 1)
Phase 6(`ai-task-checklist.md:89-100`)承诺 `docs/ai/evals/runs/<model>/<date>/` 但目录不存在。
`evaluate_ai_protocol.py`(check→tier→report)+ `update_model_registry.py`(写 registry)已完整,
CI 已测。唯一真空缺:无脚本填 prompt 模板占位符。ENUMERATE:8 个真实占位符(非 9,无 {GOAL})。

### 合法 shape 清单(prompt 占位符 × 时序依赖)
| Mode | 模板 | 占位符 | 静态可填? |
|---|---|---|---|
| plan | harness-selection | {TASK},{FILES} | ✓ |
| patch | cpp-patch | {EDIT_SCOPE},{HARNESSES},{PATCH_PLAN},{COMMANDS} | 部分({PATCH_PLAN} 需 plan 输出) |
| review | cpp-review | {HARNESSES},{DIFF} | 部分({DIFF} 需 patch 输出) |
| verification | verification-report | {COMMANDS},{COMMANDS_RUN} | 部分({COMMANDS_RUN} 需实跑) |

### 退化输入×消费者矩阵(关键陷阱)
| 输入＼消费者 | infer_mode | evaluate | check_budget |
|---|---|---|---|
| `prompt-plan.md`(原方案命名) | **误匹配 plan 模式**(blocker b) | 污染 tier | prompt 超 6 行预算→假失败 |
| `prompt-plan.txt`(采纳) | None(不匹配) | 不发现 | n/a |
| 空 output stub | n/a | n/a | 超 plan 6 行预算→过不了(blocker c) |

### 初版方案(被推翻点)
原方案:prompt 用 `.md` 后缀 + `--evaluate` flag + 一次渲染全 4 prompt + 预生成空 output stub + 列 9 占位符(含 {GOAL})。
**REFUTE subagent 抓 2 blocker + 5 major**:
- [blocker b] `prompt-plan.md` 以 `.plan.md` 结尾 → infer_mode 误匹配 → 污染 evaluate
- [blocker c] 空 output stub 超 plan 6 行预算 → 过不了 checker
- [major a] {GOAL} 是臆造占位符(4 模板均无);4 模板有时序依赖,不能一次渲染全
- [major h] --evaluate 违背"纯渲染器"选择 + 因 (b) 而坏
- [major i] 无 ground truth/checker 是结构性的

### 对抗审查结论
REFUTE 全采纳。逐条核实:`infer_mode` 对 `prompt-plan.md` 确实匹配(blocker b 坐实);
4 模板占位符已读,确认无 {GOAL}(blocker a 坐实);plan LINE_BUDGET=6=REQUIRED_SECTIONS 数,stub 必超(blocker c 坐实)。

### 修订方案(v2,采纳)
1. prompt 文件用 `.txt` 后缀(彻底避 infer_mode)。
2. 砍 `--evaluate`(用户填完 output 直接跑既有 evaluate_ai_protocol.py)。
3. 砍 `{GOAL}`;按 8 真实占位符。
4. 承认时序依赖:plan prompt 全填;patch/review/verification 标 UNFILLED note + 保留占位符。
5. 不预生成 output stub(blocker c);改打印指引。
6. README 诚实声明:scaffolding 非 evidence;checker 结构性非语义;debug mode 不在本期。

### 数据流 hops
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 task spec → run_eval 渲染 | spec → prompt-*.txt | ✓ |
| 2 prompt-*.txt 不被 infer_mode 发现 | .txt 后缀 → infer_mode None | ✓(blocker b 隔离) |
| 3 用户填 output → evaluate | .output.md → evaluate_ai_protocol | ✓(端到端 T2) |
| 4 evaluate report → registry(可选) | report.json → update_model_registry | ✓(既有链路) |

### 改动文件
- `scripts/run_eval.py`(新,纯模板渲染器,~140 行)
- `docs/ai/evals/runs/README.md`(新,目录约定 + 命名红线 + 诚实声明)

### 测试证据
- 渲染默认 param-validation task:4 prompt-*.txt + task-spec.yml ✓
- plan prompt 全填(0 残留 `{`)✓
- patch/review/verification UNFILLED note + 保留占位符 ✓
- **blocker b 隔离**:runs/ 目录所有文件 infer_mode 返回 None ✓
- **端到端**:填 good-runs 内容作 output → evaluate 推荐 T2 / 4 case 全 pass / report.json 生成 ✓
- 自定义 --task spec:正确填 + 回写 task-spec.yml ✓
- idempotency guard:重跑同目录 exit 1(refused)✓
- 回归:validate / gen_index / check_all / ai / plan_debug 全 PASS ✓

### 过程意外 / 与预期偏差
1. **REFUTE 抓到的 blocker b 是真救命**:原方案 `prompt-plan.md` 会让 evaluate 把 prompt 当 output 检查 → tier 永远 T0/T1 → 假信号。若不 REFUTE 直接 ship,所有未来 eval 都被污染。
2. **空 run 的 evaluate 返回 T0 + exit 0**:既有 `recommend_tier()` 的 `if not results: return "T0"` 把空输入当"差"而非"不可评估"。是 evaluate 既有行为(非本次引入),记 backlog [中]。我的 run_eval 已打印诚实 NOTE 缓解。
3. **shell 末端信号陷阱第 4 次**:`cmd | head; echo $?` 报 head 的 exit。idempotency guard 误报 exit=0,直接跑才见 exit=1。

### 遗留 backlog
- [中] evaluate_ai_protocol.py recommend_tier 空输入返 T0(假信号)→ 应区分"无数据"vs"差"。
- [低] Phase 6 debug mode(check_debug_report.py)未接入 run_eval。
- iter 1-12 backlog 不变。

---

## 迭代 14 — INDEX 同步回归暴露 OS 相关路径标识符族(subset 假满分 + 反斜杠链接复发)

### 触发的理论缺口
baseline 复查(不信 journal 旧数字)发现 `gen_index --check` exit 1 / `check_all` exit 1——
f99ab5a(wxwidgets +255 行)后未重生成 INDEX。深挖后真根因更大:**iter 1 只重生了产物没修 producer**。
`str(Path.relative_to(ROOT))` 在 Windows 产反斜杠 → generator 每次在 Windows 重生成都会把
144+ 反斜杠写回 INDEX(iter 1 修复在同一 OS 上复发);且 subset 模式(`--pack`/`--installed`)
用 OS keys 比对提交的正斜杠标识符 → **静默过滤掉全部 harness(假满分,双脚本)**。

### grep journal 结果(Step 1)
关键词 `INDEX`/`backslash`/`sync` 命中 iter 1(同 producer 产物;iter 1 结论"重生成是唯一
正确动作"被本轮推翻为不完整——产物级修复,producer 未修)。`shell 末端信号` 命中 4 次教训,
本轮再次兑现(mktemp -d 的 /tmp 路径 Windows Python 不可见,export_pack 假 exit 2)。

### 合法 shape 清单 + 覆盖状态(repo-relative path identifier)
| Shape | 判别字段 | UNDERSTOOD? | 方案覆盖? |
|-------|----------|-------------|-----------|
| A 提交的正斜杠标识符(pack.yml includes/export.yml/INDEX 链接) | 机器跨产物 | ✓ | ✓ 产出点规范化 |
| B 运行时 OS-native 字符串 | Windows 反斜杠 | ✓ | ✓ 不再进产物 |
| C display-only console print(feedback/run_eval/review_signals 306/354) | 纯 print | ✓(REFUTE 逐处核实) | 不动(合法) |
| D 混合比较位点(runtime B vs committed A) | bug 位点 | ✓ REFUTE 全仓扫描确认无第 5 处 | ✓ 3 处产出点 |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | gen_index 默认 | gen_index --pack | validate --pack | packs/index.yml | GitHub 渲染 |
|----------------|---------------|------------------|-----------------|-----------------|------------|
| Windows 运行(旧) | 反斜杠链接 ✗ | **0 行空索引 ✗(假满分)** | **pass:true 0 校验 ✗** | 反斜杠进 manifest ✗ | 链接坏 ✗ |
| Windows 运行(新) | 正斜杠 ✓ | 41 行 ✓ | 41 命中 ✓ | posix ✓ | ✓ |
| Linux 运行 | 不变 ✓(as_posix≡str,REFUTE 核 (f)) | 不变 ✓ | 不变 ✓ | 不变 ✓ | 不变 ✓ |

### 初版方案(被推翻点)
方案 v1:3 处 as_posix + 重生成 + "修 12 处静态区" + 测试 oracle "==9 行"。
**REFUTE subagent 抓 4 major**:
- [major-1] oracle 错:installed_paths_for 递归解析依赖(cpp-testing→cpp-core→common-core)
  =50 条 selected,正确 oracle **41**。按字面执行会诱导把正确实现"修坏"。
- [major-2] **整个 shape 漏掉**:wxwidgets-3-1-5.md 带 UTF-8 BOM,parse_frontmatter 的
  `^---` 锚定 pos 0 永不匹配 → 该 harness 在**所有 OS 上被静默排除出 INDEX 和 validate**
  (全仓 4 个 BOM harness:wxwidgets-3-1-5/qt6-core/qt6-qml/output-language)。
  validate 假满分有第二个独立根因,"重生成拿到 wxwidgets 行"不可达。
- [major-3] `_path` 不进 export.yml;真实去向是 pack_index() → **packs/index.yml**。
- [major-4] 静态区 6 链接(12 字符)非"12 处";autogen 78 非 72;84=78+6 巧合相等。

### 对抗审查结论
REFUTE 总评:三处代码修复正确、必要、位置精准,不推翻;方案 4 处事实错误必须先修。
minor 全采纳(测试命名具体化/generate_index:45 变量复用/python-core 补测/过渡态顺序)。
(g) 无更小修法:两处过滤点 replace 是单层修复;产出点规范化是每处必要、无冗余的最小根因修复。

### 修订方案(逐条)
- 采纳 major-1/3/4 + minor 全部。
- major-2(BOM)→ **独立成 iter 15**(同族假满分第二根因;改 utf-8-sig 会改变 INDEX 规模
  78→82 且 validate 将首次真正检查这 4 个文件,必须显式轮次,不顺手改)。
- 数据流修正:_path → packs/index.yml(REFUTE 核实)。

### 数据流 hops(path identifier)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 find_harnesses keys | generate_index/validate → subset 过滤 | ✓(posix) |
| 2 build_index_table 链接 | generate_index → INDEX.md → GitHub/克隆 | ✓(posix) |
| 3 _path | pack_utils → packs/index.yml(机器跨) | ✓(posix) |
| 4 installed_paths(pack.yml includes,本就 posix) | → 过滤比对 | ✓(现已可匹配) |

### 变种横向 grep
`relative_to` 全仓 11 处逐一定性:7 处 display-only print(合法不动);export_pack.py:42
archive.write(path, relpath) 用 Path 对象(OS 无关);check_review_signals.py:274/:140 已有
replace 先例;check_review_signals.py:120 仅用 parts[0](OS 无关 tuple)。**无第 6 处需改**
(REFUTE 独立全仓扫描交叉确认)。

### 改动文件
- `scripts/generate_index.py`(:44-55 rel 变量 + as_posix + 注释)
- `scripts/validate.py`(:173-176 as_posix + 注释)
- `scripts/pack_utils.py`(:24,:34 _path as_posix)
- `INDEX.md`(重生成 78 行全 posix + 静态区 6 链接手修,共 12 字符清零)

### 测试证据(X/X,真实 exit code,无管道末端)
- `gen_index --check` exit 1 → **0** ✓;`check_all` exit 1 → **0** ✓;validate/meta-tests 全 0 ✓
- `--pack cpp-testing` 生成区行数 **41**(REFUTE oracle)✓,反斜杠行 0 ✓(改前 0 行)
- validate keys 78/78 posix;subset 命中 41(改前 0)✓;gen_index keys 78/78 posix ✓
- export_pack --zip exit 0,zip+sha256 创建,packs/index.yml manifests 全 posix ✓
- INDEX.md 反斜杠字符计数 **0** ✓(84→0)
- wxwidgets 行仍 0(BOM,iter 15 输入)✓ 符合预期

### 过程意外 / 与预期偏差
1. **REFUTE 推翻方案的测试 oracle(major-1)**:初版 oracle 若被执行,正确实现会"测试失败"——
   错误的验收线比没有验收线更危险(诱导修坏正确代码)。
2. **BOM 排除是纯运气外发现的**:baseline 复查 → 反斜杠 → REFUTE 追问"wxwidgets 行去哪了"
   才暴露。4 个 harness 从未被 validate 检查过(含 iter 26 计划审查的 wxwidgets 自己)。
3. **Git Bash grep 静默漏报**:grep -r 反斜杠链接返回空(Python 扫描证实 INDEX.md 有 84)。
   skill Rationalization Table"grep 静默=没有"再次兑现;跨平台扫描用 Python 才权威。
4. **mktemp -d /tmp 陷阱(Git Bash 映射)**:Windows Python 收到 /tmp 路径 → export_pack 假
   exit 2,差点误判回归。shell 末端/边界信号第 5 次教训。

### Pattern Index 更新: 新增 posix-path-identifier | bom-frontmatter-exclusion
### 遗留 backlog
- iter 15 必做:BOM 容错(utf-8-sig)→ INDEX 78→82 行 + validate 首次真实检查 4 个 BOM harness。
- iter 1-13 backlog 不变。

---

## 迭代 15 — BOM frontmatter:4 个 harness 在所有 OS 上被静默排除(validate+index 双盲区)

### 触发的理论缺口
死代码/假满分(iter 14 REFUTE [major-2] 移交):BOM 在 `---` 前 → `re.match(r"^---...")`
锚定 pos 0 永不匹配 → wxwidgets-3-1-5/qt6-core/qt6-qml/output-language 四个 harness
**从未被 validate 校验、从未进 INDEX**。f99ab5a 的 255 行 wxwidgets 内容在 INDEX 里不可见,
`--check` 还绿——双重假象。

### grep journal 结果(Step 1)
`bom-frontmatter-exclusion`(iter 14 Pattern Index 新增,立即兑现)。Producer 全集 grep:
全仓恰 3 处 frontmatter 解析/门控(validate.py:43、generate_index.py:31、
check_review_signals.py:125),无第 4 处;check_review_signals.py:91/104 的正则
(`^###\d`/`^tier:` MULTILINE)本身 BOM 免疫。

### 合法 shape 清单(harness .md frontmatter 可解析性)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| plain `---` 开头 | 多数 78 文件 | ✓ | ✓(行为不变) |
| BOM+`---` | 4 文件 | ✓ | ✓(utf-8-sig 收编) |
| 无 frontmatter/坏 YAML | 非 harness 文件 | ✓ | ✓(设计内排除,不变) |
| CRLF 行尾 | `\s*\n` 兼容 | ✓ | ✓(不受影响) |
| UTF-16 文件 | 无此 shape | n/a | 显式不处理(无实例) |

### 初版方案(被推翻点)
无独立 REFUTE——iter 14 的 REFUTE 已对 BOM 修法做过对抗审查("唯一值得加的正确性扩展,
须显式决策"),本轮按其触点清单执行 + 实证协议。**自证风险已知**(skill 已知结构局限),
实证兜底:改动前/后 harness 计数 78→82、4 文件逐个进入 validate、全 suite 真实 exit code。

### 对抗审查结论(实证协议代替)
- utf-8-sig 是超集解码:BOM 无文件逐字节一致 → 78 个既有文件零回归(实测 validate 0)。
- REFUTE 预警"4 文件首次受检可能冒新 error"→ 实测 **0 新 error**(四文件干净)。
- 无 MATH-no-op 风险:读入侧单点改,无下游重映射。

### 修订方案(采纳)
3 处读入点 `encoding="utf-8-sig"` + 注释(不strip BOM 写回——文件保持原样,解析容错,
避免无谓 diff 噪声;未来编辑器再写 BOM 也不再复发)。

### 数据流 hops(harness 文件 → 解析 → 消费)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 parse_frontmatter(validate) | harness → 校验集 | ✓(82) |
| 2 parse_frontmatter(generate_index) | harness → INDEX 行 | ✓(82) |
| 3 startswith("---") gate(check_review_signals audit) | harness → tier 通胀审计 | ✓(utf-8-sig) |

### 变种横向 grep
其他 BOM 产物:INDEX.md 自身带 BOM(生成器 read/write utf-8 原样透传,GitHub 渲染无碍,
**显式不改**——改它会制造无谓 diff,且无消费者受损)。scripts/*.py 无 BOM。

### 改动文件
- `scripts/validate.py`(parse_frontmatter utf-8-sig + 注释)
- `scripts/generate_index.py`(同上)
- `scripts/check_review_signals.py`(audit 循环 read_text utf-8-sig + 注释)
- `INDEX.md`(重生成,82 行,+third-party/qt6/wxwidgets/output-language)

### 测试证据(X/X,真实 exit code)
- py_compile 3 脚本 OK ✓
- find_harnesses 78 → **82** ✓;4 文件逐个确认在 keys ✓
- validate exit 0(4 文件首次受检,0 新 error)✓
- `gen_index --check` exit 0 ✓;check_all exit 0 ✓;meta-tests 0/0 ✓
- INDEX autogen rows **82**;wxwidgets 行出现(posix 链接)✓;反斜杠计数 0 ✓

### 过程意外 / 与预期偏差
1. **Edit 工具吞行事故**:改 check_review_signals 时 old_string 含 `if not text.startswith("---"):`
   而 new_string 漏掉该行 → 门控被删、孤儿 `continue`(若不回读核实,audit 对所有文件
   无条件 continue = 新假满分)。**回读抓到,立即修复**。教训:多行 Edit 后必须回读关键
   控制流区域(不能只信"edit 成功")。
2. REFUTE 预警的新 error 未出现(4 文件干净)——预警属实但方向偏保守,如实记录。

### Pattern Index 更新: N/A(bom-frontmatter-exclusion 已于 iter 14 登记,本轮为该条目的修复落地)
### 遗留 backlog
- iter 16 起按计划(recommend_tier 两态决策)。
- INDEX.md 自身 BOM:显式不改(无消费者受损;改=无谓 diff)。

---

## 迭代 16 — recommend_tier 空输入假 T0 + registry 缺 key 默认 T0(两态决策,双 sentinel-conflation)

### 触发的理论缺口
iter 13 backlog [中] 兑现。两态决策(诚实性硬原则 1):空 eval = **真·不可观测**(信号根本
没产出),诚实答案不是 T0(假最差/false-negative)也不是满分,是**退出评分**。旧行为把
空输入评成 T0 + exit 0(misleading-success 家族),且经 `update_model_registry.py:81`
`.get("recommended_tier", "T0")` **流进持久 model registry**。REFUTE 又挖出第二个同族:
**缺 key 也默认 T0**(sentinel 缺失子类)。

### grep journal 结果(Step 1)
`not-assessable`/`misleading-success`(iter 13 过程意外栏)命中;`两态决策` 命中 skill 原则;
`exit-code 契约` 命中 iter 2(validate exit 3 documented-but-unreachable——本轮测试落点教训同源)。

### 合法 shape 清单 + 覆盖状态(evaluate 输入目录 × registry 输入 report)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| A 非空有 fail | T1(有 plan 过)/T0 + exit 1 | ✓ | 不变 ✓ |
| B 非空全过 | T2/T1/T0 + exit 0 | ✓ | 不变 ✓(good-runs 回归) |
| C 目录在但 0 匹配文件 | 空 results | ✓ | **exit 2 + null + N/A** ✓ |
| D 目录不存在/是文件 | — | ✓(REFUTE 实测 rglob 静默返 [],**非** traceback) | is_dir 检查 + exit 2 ✓ |
| E checker 崩溃 | 计 fail | ✓ | 不变 ✓ |
| F registry:tier 合法/非法/None/缺 key | .get 语义 | ✓ | None/缺 key → parser.error ✓ |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | evaluate exit | report.json | markdown 报告 | model-registry.md(持久) |
|----------------|--------------|-------------|--------------|------------------------|
| 空 run(旧) | 0(假绿) | "T0" | "Recommended tier: T0"(假证据落盘) | **静默写入 T0 行** |
| 空 run(新) | 2 | null | N/A (0 cases — not assessable) | 拒绝(exit 2) |
| 缺 key report(旧) | n/a | n/a | n/a | **静默写入 T0 行**(REFUTE 复现后还原) |
| 缺 key report(新) | n/a | n/a | n/a | 拒绝(exit 2) |

### 初版方案(被推翻点)
**REFUTE subagent 推翻 4 处**:
- [major-1] 我宣称"缺目录→裸 traceback"**是假的**——rglob 对不存在目录静默返 [](三条
  Python 版本实测)。Shape D 早就静默坍缩成 C。**没实测就写现状 = iter 68 式错误再犯**。
- [major-2] item 1(空→None)在 main 提前守卫后成死代码;单独提交反而泄漏 repr "None"。
  采纳替代方案:main 层单点拥有,recommend_tier 只加防御注释。
- [major-3] registry 对显式 null **今天就拒**(None not in VALID_TIERS);真增量只有缺 key。
  我的测试用例"null→exit 2"改前就绿 = 非判别性测试。改用缺 key 用例(改前红)。
- [major-4] 测试没落点 = documented-but-unreachable 家族(iter 2 exit 3 同源)。落进 CI
  已跑的 test_ai_protocol.py;registry 测试走 parser.error 先于 REGISTRY 写入的顺序,零污染。
- [major-5] 文档同步打错靶:两份 README 无陈旧内容;真缺口是 **run_eval.py:187 打印的
  下一步命令**(新 scaffold 空 run 目录踩 exit 2 的最高频现实触发点)。
- (g) exit 2 论证成立:1 已被"有 case 且失败"占用,混码毁掉"零证据 vs 不及格证据"的区分;
  C/D 分 stderr 文案;docstring 写明 2 兼覆盖 argparse usage。

### 对抗审查结论
核心方向(空输入不可评分为 T0)不能被推翻;方案 4 处事实/设计错误先修。**Tiebreaker 实证**:
REFUTE 的每个"现状"主张都带实测(good-runs 4 fixture T2、registry 静默写行复现后还原、
rglob 三版本行为)。

### 修订方案(采纳 REFUTE 替代方案 v2)
1. evaluate main:is_dir 守卫(D,含"传了文件"情形,文案 "not a directory or does not exist")
   + 空 files 分支(C,文案 "no AI output files matched ... not assessable"),报告仍落盘
   (null/N/A)但 exit 2;recommend_tier 不改 + 防御注释;markdown tier_label 守卫。
2. update_model_registry:.get 无默认 + None/缺 key → parser.error(消息含 empty/not-assessable)。
3. docstring 退出码契约(0/1/2 + 2 兼 usage);run_eval docstring + 打印的 step-4 注记。
4. test_ai_protocol.py 新增 test_evaluate:good-runs T2/exit0、空目录 exit2+null+stderr、
   缺目录 exit2+文案、registry 缺 key exit2。

### 数据流 hops(空 eval 信号)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 candidate_files 空 | main → exit 2 | ✓ |
| 2 report.json recommended_tier null | evaluate → update_model_registry | ✓(拒绝) |
| 3 markdown N/A | evaluate → 人 | ✓(字符串级验证) |
| 4 run_eval step-4 文案 | run_eval → 操作员 | ✓(预设期望) |

### 变种横向 grep
同族 ".get 默认 sentinel":全 scripts/ grep `.get(` 带 "T0"/哨兵默认——仅 update_model_registry
一处;`report.get("pass")`(evaluate:48)默认 None 是保守方向(不当 pass),合法。
同族 "空输入假信号":recommend_tier 是唯一评分聚合点(check_ai_protocol 无聚合)。

### 改动文件
- `scripts/evaluate_ai_protocol.py`(docstring 契约 + main 守卫 + tier_label + 防御注释)
- `scripts/update_model_registry.py`(:81-89 无默认 + 拒绝消息)
- `scripts/test_ai_protocol.py`(+test_evaluate 5 组断言,CI 已接线)
- `scripts/run_eval.py`(docstring step 4 + 打印注记)

### 测试证据(X/X,真实 exit code)
- test_ai_protocol **全过(含 5 组新断言)** exit 0 ✓;test_plan_debug exit 0 ✓
- 空 run --output:exit **2** ✓,报告落盘 "Recommended tier: N/A (0 cases — not assessable)"
  (字符串级)✓
- good-runs:T2 + exit 0(回归)✓;validate/gen_index/check_all exit 0(无回归)✓
- py_compile 4 脚本 OK ✓

### 过程意外 / 与预期偏差
1. **现状描述错再犯(被 REFUTE 拦截)**:我在没实测的情况下写"缺目录→traceback"——正是
   Rationalization Table"方案里的现状我记得是 X"条目。rglob 静默返 [] 是 pathlib 远古行为,
   反直觉(rglob 不 exist 检查)。**永远实测现状,哪怕"显然"**。
2. **Edit 工具第二次吞块**:docstring Edit 的 new_string 含闭合 `"""` 而 old_string 只有
   opening 行 → 原 Usage 块成孤儿顶层代码,py_compile 抓到,修复。两轮连续踩 Edit 粒度坑
   ——教训:跨"语句边界"的 Edit 必须让 old/new 完整覆盖被替换区域。
3. 非判别性测试教训:改前就绿 的断言什么都没证明(REFUTE major-3)——修复类测试必须
   先证明它在旧代码上是红的。

### Pattern Index 更新: 新增 two-state-empty-input | get-default-sentinel | non-discriminating-test
### 遗留 backlog
- iter 17 起按计划(未审脚本扫描)。
- argparse usage exit 2 与 not-assessable exit 2 共码(靠 stderr 文案区分)——可接受,显式记录。

---

## 迭代 17 — R1 模块级扩张:5 个未深扫脚本对抗扫描(产 iter 18-20 攻击面)

### 触发
R1 双向扩张:iter 14-16 全在已审维度纵深,本轮扩到从未深扫的 check_plan_protocol /
run_ai_protocol_check / install_pack / list_packs / check_feedback_signals。
R1 扫描 subagent 模式(iter 8 先例):一个扫描 agent 产分级清单,后续轮逐个修。

### grep journal 结果(Step 1)
关键词 `feedback-log`/`兄弟脚本`/`R1 扫描` 命中 iter 4(check_feedback 仅对比契约)、
iter 8(R1-scan 先例 + 7.7M token 教训:本轮沿用 targeted,单 agent 单对象组)。

### 扫描产出(全部带实测证据,详见 agent 报告;关键项)
**[blocker]**
- B1 check_feedback_signals.py:44-49+62-80:ENTRY_RE 限定符组只认 `, item N|general`,
  生产者写 `, orphan`(check_review_signals.py:174)→ 真实日志 24 条只解析 9 条;
  08-07 checklist 9×gap(应触发 ≥3 阈值)、AGENTS 5×gap 均漏报,exit 0。
  **生产环境已生效的漏报。部分解析(非零丢失)完全静默(:130-133 只在零解析时提示)。**
- B2 同文件 :62-80:不匹配的 `###` header 不重置 `current` → 后随 Signal 行覆写上一条目
  (temp 复现:harness-a misleading 被覆写成 gap,harness-b 整体消失)。
**[major]**
- M1 :100-111 + 62-80:`--threshold 0` + 存在无 Signal 条目 → IndexError 崩溃 exit 1,
  违反 docstring "exit 0 always"(:18-19)。temp 复现。
- M2 **iter 15 BOM 修复是单层修复**(Step 4 横向 grep 没做全,扫描抓到):check_plan_protocol.py:31、
  check_feedback_signals.py:59、pack_utils.py:23/33/71、check_ai_protocol read_input 均漏 utf-8-sig。
  带 BOM 的合法 plan 被判假错;带 BOM 的反馈日志 total_entries: 0。
**[minor] m1-m11**(详单见扫描报告):plan LINE_BUDGET=8 判决死代码+无出处;check_plan_protocol
strip 语义不一致(自相矛盾报错);run_ai_protocol_check --json 多文件输出非单一合法 JSON;
install_pack requires 环 RecursionError + 未知 pack 裸 KeyError;README 覆盖语义漂移;
.dev-guidelines-installed.yml 不在 .gitignore;空 installed_paths → vacuous pass(iter 16 同族);
en-dash header 静默丢弃;加粗信号值计入 UNKNOWN;list_packs 直接下标。

### 设计取舍(核实后不改)
run_ai_protocol_check 无 --diff(已知限制,iter 12 记录);advisory exit-0 契约本体正确;
缺文件 traceback fail-closed 可接受;infer_mode None 已被唯一消费者守卫。

### 本轮结论
- iter 18 = B1+B2+M1(check_feedback_signals parser 重写 + 阈值守卫 + 未解析计数警告,
  同一处 parser 重写顺带覆盖 m9/m10)。
- iter 19 = M2 BOM 补面(机械;iter 15 同语义兄弟位点)。
- iter 20 = pack 工具链卫生(m4 环检测/m5 干净报错/m7 .gitignore/m11 list_packs 守卫 +
  m8 消费者空集守卫)。
- m1/m2/m3 → iter 21;m6 → 文档轮。

### Pattern Index 更新: 新增 parser-producer-drift | partial-parse-silence | single-layer-bom-fix
### 遗留 backlog
m1-m11 见扫描报告(逐轮消化);m6 README 覆盖语义明示。

---

## 迭代 18 — check_feedback_signals 解析器重写(B1 漏 15/24 条 + B2 合并腐蚀 + M1 阈值崩溃)

### 触发的理论缺口
iter 17 扫描 [blocker]×2 + [major]×1。**B1 是生产环境已生效的漏报**:ENTRY_RE 限定符闭集
`item\s+\d+|general` 不认生产者词表(`orphan`/`frontmatter`/手写 `item 20/37`)→ 真实日志
24 条只解析 9 条,ccc 9×gap 与 AGENTS 5×gap 的 re-review 触发全漏,exit 0 无警告。

### grep journal 结果(Step 1)
`parser-producer-drift`(iter 17 Pattern Index 新增,兑现);`exit-code 契约` 命中 iter 2/16
(documented-but-unreachable 与 usage-error 语义族);`misleading-success` 命中(部分解析静默
= B1 的危害形态,危害不在解析错误本身而在"summary 看起来健康")。

### 合法 shape 清单 + 覆盖状态(### header 行)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| `### date — target, item N (detail)` | 经典条目 | ✓ | ✓ |
| `### date — target, orphan` / `, frontmatter` | 生产者词表(iter 17 B1) | ✓ | ✓ 开放限定符 |
| `### date — target, <手写任意限定词>` | 手工条目 | ✓ | ✓ `[^()]+?` |
| en-dash `–` 分隔符 | m9 | ✓ | ✓ `[—–-]` |
| `### date — target 散文无逗号` | F3 宽接受面 | ✓(REFUTE 实测) | 不解析,计 unparsed |
| `#### ...` 4+# 行 | F4(真实日志从未出现) | ✓ | 同 flush 规则,防未来漂移 |
| `## Log` 之前的 schema 模板 `### <YYYY...>` | F1 假阳性源 | ✓(REFUTE 实测恒=1) | 不计 unparsed |
| Signal 值加粗 `**gap**` | m10 前瞻 | ✓ | `.strip("*")` 归一 |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | parse_log | summary/flagged | harness-evolution Item 3 决策 |
|----------------|-----------|-----------------|------------------------------|
| 真实日志(旧) | 9/24 | ccc 9×gap→not flagged(漏) | 无 re-review(错) |
| 真实日志(新) | 24/24 | ccc 9×gap→FLAGGED | 触发 re-review(对) |
| `--threshold 0`(旧) | IndexError→exit 1 | 崩溃 | 违约 |
| `--threshold 0`(新) | parser.error exit 2 | — | usage error,契约自洽 |

### 初版方案(被推翻点)
**REFUTE subagent 实测驳回 2 major + 补 4 minor**:
- [major-F1] unparsed 计数在健康日志恒=1(:39 schema 模板行)→ 漂移警报"出生即狼来了"。
  修:只在 `## Log` 标记后计数。**方案的主打特性差点自身就是 bug**。
- [major-F2] CI 断言 `==24` 写在活日志上必腐(append-only 但生产者会追加);ccc≥3 期望内嵌
  生产者误归因噪声(orphan FAIL 记到 harness_files[0],AGENTS 条目全是 GUI PR FAIL)。
  修:下界断言 + 测试注释局限;**生产者误归因记 backlog**(后轮)。
- [minor] F3 开放限定符放宽假接受面(散文行形状匹配)——记录,可接受;F4 `####` 豁免保护
  假想场景→并入 flush 规则;F5 测试补 frontmatter 词表;F8 :39 schema 模板同步;F9 CI 注册
  点=validate.yml(check_all 仅本地),parse_log 签名改 tuple 安全(唯一消费者)。
- (a)(c)(d) 全被 REFUTE 实测驳回(吞括号不存在/strip 安全/exit 2 自洽)。

### 对抗审查结论
解析核心经 REFUTE 复刻实测:真实日志 24/24 解析、ccc gap=9 触发。采纳全部修正后无保留意见。

### 修订方案(采纳)
ENTRY_RE 开放限定符+三 dash;HEADER_RE `^#{3,}\s` flush;unparsed 仅 `## Log` 后计数;
Signal 归一;threshold<1 → parser.error;JSON+文本双通道 unparsed 警告;:39 模板行同步;
新 test_feedback_signals.py 注册 CI+check_all。

### 数据流 hops(日志条目)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 生产者追加(check_review_signals :248) | → 日志 | ✓(词表实测) |
| 2 parse_log 解析 | 日志 → entries | ✓ 24/24(旧 9/24) |
| 3 聚合触发 | summary → flagged_for_rereview | ✓ ccc/AGENTS |
| 4 harness-evolution Item 3 | 输出 → 人决策 | ✓(本轮起有真信号) |
| 5 unparsed 警告 | parse_log → 漂移可见性 | ✓(F1 修正后健康日志=0) |

### 变种横向 grep
生产者词表全集 {item N(:185/200), orphan(:174), frontmatter(:305)} 全覆盖;M2(BOM 同语义
兄弟位点,含本文件 :59)→ iter 19;m6/m8 等 pack 族 → iter 20。**生产者侧误归因**
(:172-174 harness_files[0][0])= 新 backlog [中](属 check_review_signals,不与本读侧修复混)。

### 改动文件
- `scripts/check_feedback_signals.py`(重写 :32-80 解析器 + main 守卫 + 双通道警告)
- `scripts/test_feedback_signals.py`(新,10 组断言,CI+check_all 注册)
- `.github/workflows/validate.yml`(+1 step)
- `scripts/check_all.py`(+注册)
- `common/meta/harness-feedback-log.md`(仅 :39 schema 模板行文档同步)

### 测试证据(X/X,真实 exit code)
- test_feedback_signals exit 0(10 组断言)✓;真实日志:total **24**(旧 9)、unparsed **0**、
  flagged=[AGENTS, ccc] ✓
- check_all exit 0(含新测试)✓;test_ai_protocol / plan_debug / validate / gen_index 全 0 ✓
- YAML 合法 ✓

### 过程意外 / 与预期偏差
1. **我自己 fixture 三连错**(被自家测试抓到):`en-dash target` 带空格(harness id 语法
   不允许)、可解析数错数 7(实 6)、真实日志断言要求当前数据不存在的 frontmatter 条目。
   3 次迭代 fixture 才绿——fixture 敏感性纪律(改动前/后输出确实变)兑现,但也说明
   测试作者需要先对齐被测语法再写样本。
2. Edit 工具第 3 次粒度事故(main 守卫编辑带出一行垃圾),回读清理。**连续三轮 Edit 事故
   ——跨行 old/new 必须自查后回读**,已成本轮固定动作。
3. REFUTE 复刻实现这个动作(把方案正则逐字跑真实数据)是本轮最高价值步骤——F1 的恒=1
   假阳性纯靠运行发现,读代码读不出来。

### Pattern Index 更新: 新增 open-vocabulary-parser | living-file-assertions | false-alarm-fatigue
### 遗留 backlog
- [中] check_review_signals.py:172-174 orphan FAIL 误归因 harness_files[0][0](AGENTS 条目
  实为 GUI PR FAIL)——生产者侧,后轮修(修后 ccc/AGENTS 计数会变,需同步测试注释)。
- iter 19 = M2 BOM 补面;iter 20 = pack 工具链(m4/m5/m7/m11+m8)。

---

## 迭代 19 — BOM 补面:iter 15 的同语义兄弟位点(M2 单层修复补完)

### 触发的理论缺口
iter 17 扫描 [major-M2]:iter 15 的 utf-8-sig 只落在 3 处 harness 解析点,**同语义位点
(协议检查器输出读取、pack YAML、eval report JSON)漏改**——带 BOM 的合法 plan 被
`line 1 must start with Goal:` 假错;BOM YAML 会被 PyYAML 拒;BOM JSON 被 json.loads 拒。
Step 4 横向 grep 未做全,扫描抓到(诚实记录:这是我的单层修复)。

### grep journal 结果(Step 1)
`single-layer-bom-fix`(iter 17 登记);iter 15(修复落点与"免疫有因"清单)。

### 合法 shape 清单 + 覆盖状态(读入点 × BOM 敏感性)
| 位点 | BOM 敏感机制 | 处置 |
|------|-------------|------|
| check_plan_protocol:31 / check_debug_report:33 / check_ai_protocol:74(输出读取) | line-1/pos-0 锚定 | **修** |
| check_review_signals:320(review report) | 行首正则族 | **修** |
| pack_utils:23/33/71(pack.yml/installed.yml) | PyYAML 拒 \ufeff token | **修** |
| update_model_registry:80(report.json) | json.loads 拒 BOM | **修** |
| run_eval:88/102(task spec/template) | PyYAML / 透传进 prompt | **修** |
| check_review_signals:91/104/273 | MULTILINE 正则,item/id 非 pos-0 | 免疫,不改(记录理由) |
| check_review_signals:229(log dedup) | substring in | 免疫,不改 |
| update_model_registry:91(REGISTRY 读改写) | BOM round-trip 无害 | 不改 |
| generate_index:108/159(INDEX read/write) | BOM round-trip 自洽;修=无谓 diff | 不改(iter 15 已显式决策) |

### 初版方案(被推翻点)
无独立 REFUTE——机械多点位补面,判据:单分支、无阈值、有现成回归套件(两套 CI 测试各加
BOM 用例)。自证风险由"改前红/改后绿"实证兜底:扫描 agent 已实测改前 BOM plan 假错;
本轮改后直接实验 exit 0。

### 对抗审查结论(实证代替)
- 新 BOM 用例进 test_ai_protocol + test_plan_debug(CI 已接线,防 documented-but-unreachable)。
- 免疫位点逐一给机制理由(见 shape 表),不留"顺手全改"的对称性噪声。

### 数据流 hops(BOM 字节)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 Windows 编辑器产 BOM 文件 | → 协议检查器/pack/eval 读取 | ✓ utf-8-sig |
| 2 解析锚定(line 1 / YAML token / JSON) | → 判定 | ✓ 不再假错 |

### 变种横向 grep
`read_text(encoding="utf-8")` 全仓 17 处逐一分类(上表);修 9 处、免疫 8 处有因。
无第 10 处遗漏(grep 权威,非 Git Bash grep——iter 14 教训)。

### 改动文件
- `scripts/check_plan_protocol.py` / `check_debug_report.py` / `check_ai_protocol.py` /
  `check_review_signals.py`(:320)/ `pack_utils.py`(×3)/ `update_model_registry.py` /
  `run_eval.py`(×2)——共 9 处 utf-8-sig + 注释
- `scripts/test_ai_protocol.py`(+test_bom:eval 格式 BOM fixture)
- `scripts/test_plan_debug_protocol.py`(+BOM'd 双 fixture 用例)

### 测试证据(X/X,真实 exit code)
- test_ai_protocol exit 0(含 BOM 用例)✓;test_plan_debug exit 0(含双 BOM 用例)✓
- check_plan_protocol 直接实验:BOM'd good plan exit **0**(改前假错,扫描实证)✓
- test_feedback / check_all / validate / gen_index 全 0(无回归)✓

### 过程意外 / 与预期偏差
1. **Bash 工具转义层二次咬人**:`b"\xef\xbb\xbf"` 经 heredoc+工具层变成文件内乱码字符
   (Python `\\x`→`\x`→hex 转义被吃),SyntaxError 抓到;第一次修复搜索串又构造错
   (U+FEFF 单字符 vs 3 个 Latin-1 字符)。最终用 `bytes([0xef,0xbb,0xbf])` 免转义形式。
   **教训:含字节转义的代码必须用免转义构造(bytes([...])),不过 heredoc。**
2. 实验 fixture 错配:用 plan 协议样张喂 check_ai_protocol(两种 plan 格式不同)→ 假红;
   换 eval 格式 fixture 后绿。**跨格式 fixture 不可混用**。

### Pattern Index 更新: N/A(single-layer-bom-fix 已于 iter 17 登记,本轮落地)
### 遗留 backlog
- iter 20 = pack 工具链(m4 环检测/m5 干净报错/m7 .gitignore/m11 list_packs + m8 空集守卫)。






