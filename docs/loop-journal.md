# dev-guidelines Loop Journal — 活跃批(iter 14-)

对抗式开发循环 (`$adversarial-development-loop`) 迭代日志。归档批:
docs/loop-journal-iter001-013.md(iter 1-13)。跨批检索用 glob
`docs/loop-journal*.md`;主题级教训见文末 **Pattern Index**(蒸馏层,优先 grep 这里)。

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

---

## 迭代 20 — pack 工具链卫生:环递归/裸 KeyError/vacuous 安装/空集假满分/gitignore

### 触发的理论缺口
iter 17 扫描 m4/m5/m7/m8/m11。核心是**退化输入假满分家族**(skill 目标缺口清单):
- m4:`resolve_packs` 只有 `seen`,requires 环 → RecursionError(用户自制 pack 即触达);
- m8:空 `installed_paths` 记录 → validate --installed 过滤后 0 harness、0 error、exit 0
  (与 iter 16 空 eval 同族;iter 14 修的是 OS 不匹配型空集,本轮修真·空集型);
- m5/m11:CLI 报错形态不对称(兄弟 validate.py 用干净 ERROR,这里裸 traceback)。

### grep journal 结果(Step 1)
`vacuous pass`/`two-state-empty-input`(iter 16)命中;`misleading-success`(多次)命中;
iter 14(subset 过滤位点 = 本轮消费者守卫的同一函数)。

### 合法 shape 清单 + 覆盖状态(resolve_packs 依赖图)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| 无依赖/链式/菱形共享依赖 | 正常 pack | ✓ | ✓(seen 语义不变) |
| requires 环 A→B→A | m4 | ✓(沙箱实证) | ✓ in_flight 守卫,KeyError 带环成员 |
| 未知 pack id | m5 | ✓ | ✓ install_pack 捕 KeyError → parser.error exit 2 |
| 空 includes 且无依赖 | m8 | ✓ | ✓ install 拒绝 + 两消费者守卫 exit 1 |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | install_pack | validate --pack/--installed | generate_index --pack/--installed |
|----------------|--------------|------------------------------|----------------------------------|
| 环(旧/新) | RecursionError / KeyError 干净报错 | 同 resolve 路径 | 同 |
| 空 installed_paths(旧) | 静默写入 | **PASS 0 harness(假满分)** | **空索引 + --check 绿** |
| 空 installed_paths(新) | 拒绝(exit 2) | exit 1 + ERROR | exit 1 + ERROR |

### 初版方案(被推翻点)
无独立 REFUTE——机械卫生轮,判据:守卫型单分支、无阈值、有 CI smoke(CI "Harness pack
smoke checks" 直接跑这些命令)+ 沙箱实证(环检测仿 iter 17 扫描 agent 的 temp 沙箱法,
patch PACKS_DIR+ROOT 后跑真 resolve_packs)。

### 对抗审查结论(实证代替)
- 环:clean KeyError "circular dependency involving pack: cpp-testing"(旧 RecursionError)✓
- unknown pack:exit 2 干净 error(旧裸 KeyError traceback)✓
- 正常 install/list/--pack 流全 0(无回归)✓
- .gitignore 生效(git check-ignore 验证)✓

### 数据流 hops(installed_paths)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 install_pack 写 | pack.yml includes → installed yml | ✓(空集拒绝) |
| 2 validate/generate_index 读 | yml → selected_paths | ✓(空集 exit 1,不再 vacuous) |

### 变种横向 grep
`resolve_packs`/`installed_paths_for` 消费者:install/export/validate/generate_index 全覆盖
(export_pack 不受影响——它不经 selected_paths,直接用 includes 打包);list_packs 直接下标
→ .get + stderr 警告。PACKS_DIR 缺失 → stderr 警告(lister 仍出空表,诚实表示"无 pack")。

### 改动文件
- `scripts/pack_utils.py`(resolve_packs in_flight 环守卫)
- `scripts/install_pack.py`(KeyError → parser.error;空 installed_paths 拒绝)
- `scripts/list_packs.py`(.get 兜底 + malformed/缺目录 stderr 警告)
- `scripts/validate.py` / `generate_index.py`(selected_paths 空集守卫,对称)
- `.gitignore`(+.dev-guidelines-installed.yml)

### 测试证据(X/X,真实 exit code)
- 环沙箱:KeyError 干净(旧 RecursionError)✓;unknown pack exit 2 ✓
- install/list/--pack 正常流全 0 ✓;五套件 + check_all 全 0 ✓
- git check-ignore 验证 ✓

### 过程意外 / 与预期偏差
沙箱首跑 ValueError(没 patch ROOT,_path 计算撞真仓库根)——**实验环境与生产路径的
隐式耦合(ROOT 常量)本身就是一次小型现状描述错**,patch ROOT 后实证才成立。

### Pattern Index 更新: 新增 vacuous-subset-guard | cycle-detection-in-flight
### 遗留 backlog
- [中] check_review_signals.py:172-174 orphan 误归因(iter 18 记录)。
- m1/m2/m3(check_plan_protocol 判决死代码+strip 不一致;run_ai_protocol_check --json 多文档)
  → iter 21;m6 README 覆盖语义 → 文档轮。

---

## 迭代 21 — 判决死代码预算 + strip 自相矛盾 + --json 拼接非法 JSON(m1/m2/m3,双脚本同族)

### 触发的理论缺口
iter 17 扫描 minor×3。m1 在实施中升格:**LINE_BUDGET 判决死代码同族出现在两个脚本**
(横向 grep:check_plan_protocol:79 与 check_debug_report:95 都被各自 check_exact_shape 的
exact-行数支配,>6/>N 时 shape 必已报错 → budget 错误永不改变判决,只给弱模型消费者加噪声)。
m2 同族双处:section_value 用裸行 startswith 而 shape 检查用 strip 后行 → 行首空格
"shape 过但 empty section 报错"自相矛盾。

### grep journal 结果(Step 1)
`m1/m2/m3`(iter 17/20 backlog);iter 8(命令证据歧义——注意区分:LINE_BUDGET 判决死代码
≠ 死代码不执行,它执行但产出永不起决定作用的错误消息;归类到"对称性/信号噪声"更准)。
LINE_BUDGET=8 在 docs/ai-evaluation-research-2026-08-04.md:15 是设计意图(≤8 行极简)——
历史冻结文档不改;代码里留常量+注释指向,删的是永不改变判决的检查。

### 合法 shape 清单 + 覆盖状态(plan/debug 输入行)
| Shape | 旧行为 | 新行为 |
|-------|--------|--------|
| 恰 N 行字段(合法) | pass | pass(不变) |
| >N 行 | budget 错误 + shape 错误(双报) | 仅 shape 错误 |
| 行首空格字段行 | **shape 过 + empty-section 错(自相矛盾)** | pass |
| --json 单文件 | 单对象(合法) | 单对象(back-compat 保留) |
| --json 多文件 | **拼接对象(非法 JSON,无消费者可解析)** | 单一 JSON 数组 |
| 多文件含坏 fixture | exit 1 | exit 1(数组含 per-file 对象;回归断言) |

### 初版方案(被推翻点)
- 初版想"删 LINE_BUDGET 常量"→ 被 grep 推翻:研究文档引用它是设计意图,删常量=文档漂移。
  改为:删检查、留常量+注释(设计意图与验收检查分离)。
- run_ai_protocol_check 重构中写出 `if X if not Y else False:` 畸形条件(聚合模式漏计
  failures)+ 丢 `result =` 赋值(UnboundLocalError)——**py_compile 抓不到逻辑错,套件抓到**。

### 对抗审查结论(轻量自对抗,判据:机械+双套件覆盖)
- 多文件 --json 数组、单文件单对象、聚合含坏 fixture exit 1:三断言进 test_ai_protocol。
- 行首空格过 + 无 self-contradiction 文本 + 7 行计划无 "budget" 文本:进 test_plan_debug。

### 数据流 hops(--json 输出)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 checker 单对象 | check_ai_protocol → wrapper 透传(单文件) | ✓ back-compat |
| 2 wrapper 聚合 | 多文件 → JSON 数组 | ✓(json.loads 可解析,断言) |
| 3 exit code | 任一文件失败 → 1 | ✓(含聚合模式,回归断言) |

### 变种横向 grep
LINE_BUDGET 全仓 3 处:check_ai_protocol:49(LINE_BUDGETS dict per-mode——**其 shape 是否
exact?未在本轮核**记 backlog 一眼)、check_debug_report:21(同病已修)、check_plan_protocol:19
(已修)。section_value 双处同修。

### 改动文件
- `scripts/check_plan_protocol.py`(删死检查 + section_value strip + 常量注释)
- `scripts/check_debug_report.py`(同族三处)
- `scripts/run_ai_protocol_check.py`(docstring 契约 + 聚合数组 + infer_mode None 也进数组)
- `scripts/test_ai_protocol.py`(test_wrapper_json 3 组断言)
- `scripts/test_plan_debug_protocol.py`(m1/m2 用例)

### 测试证据(X/X,真实 exit code)
- test_ai_protocol exit 0(含 wrapper-json 3 断言)✓;test_plan_debug exit 0(m1/m2 用例)✓
- test_feedback / check_all / validate / gen_index 全 0 ✓

### 过程意外 / 与预期偏差
1. **Bash heredoc 写代码第 3 次事故**(`\\n` 被吃成真换行 → SyntaxError;`\\x` 同前)。
   确立硬规则:**给 Python 文件写含转义的代码,只用 Edit 工具,不过 Bash heredoc**。
   (iter 19 的 bytes([0xef...]) 规则扩展到 \n。)
2. 初版 Edit 的注释与保留代码矛盾(说 "deliberately unused" 但检查还在)——回读自查抓到。
   注释谎言比没注释更糟。
3. 自己写的畸形条件表达式(聚合模式漏计 failures)——测试断言 exit 1 抓到。教训同 iter 16:
   修复类断言必须覆盖"聚合模式仍计失败"这种跨分支语义。

### Pattern Index 更新: 新增 dominated-check-removal | json-contract-array-vs-object
### 遗留 backlog
- [低] check_ai_protocol.py LINE_BUDGETS(:49)的 shape 是否 exact 行数支配(同族核实,一眼轮)。
- [中] check_review_signals.py:172-174 orphan 误归因(producer 侧)。
- m6 README 覆盖语义 → 文档轮。

---

## 迭代 22 — related 双向性:6/6 单向(wxwidgets)+ 65 条全仓系统性缺口 + spec:402 兑现

### 触发的理论缺口
f99ab5a 给 wxwidgets 加了 255 行 + related 链接,但该文件在 iter 15 之前对机器消费层完全
隐形——新增内容从未被检查。审查发现:**6 个 related 目标全部无反向链接**(不止新加的
toolchain-and-compiler-flags)。全仓 Python 审计:**79 harness / 419 条 related 中 65 条
单向**——AGENTS 规则 5 明文要求双向,但 spec:402 item 4 "Cross-reference bidirectionality"
是 documented-but-never-implemented(iter 3 backlog [中] 的实体)。

### grep journal 结果(Step 1)
`spec:402`(iter 3 backlog);`逐跳追踪避免误改正确代码`(iter 3 harness-evolution:122 先例
——本轮先核实本地 R 表合规,别把"来源注册"误当缺口)。

### 合法 shape 清单 + 覆盖状态(related 链接)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| A→B 且 B related 列 A | 双向(合规) | ✓ | ✓ 保留 |
| A→B,B 无回链 | 单向(违反规则 5) | ✓ 63 条基线 | ✓ --related 报告 + 增量清偿 |
| A→B,B 文件不存在 | 悬挂 | ✓ | check_cross_references 已管(existence),不重复 |
| 本地 R 表 [Rn] 标签 | 非 related 语义 | ✓(R32-R38 全带 verified-2026,合规) | 不动 |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | validate(旧行为) | 跨 harness 导航 | AGENTS 规则 5 |
|----------------|------------------|----------------|---------------|
| 65 条单向链接 | 静默 PASS(假满分) | 断链导航 | 静默违反 |
| 新增(本轮) | --related 报告 63→57(本轮修 6) | ✓ | ✓ 可审计 |

### 初版方案(被推翻点)
- 初版 grep sources.md 找 R32-R38 → **自己 grep 姿势错**(sources.md 是 N/C/A 来源族注册表,
  [Rn] 是 harness 本地表)。核实后本地表合规,撤销该"缺口"。(Rationalization:"行号/现状
  我记得是 X"的反面:核查工具的语义也要先核实。)
- 方案 v1 想把检查做成 hard error(spec 原文承诺)→ 推翻:65 条存量会让 CI 全红,
  内容清偿需要逐条语义判断(反向链接要有意义,不能机械互填)。改为**报告型 --related**
  (仿 --stale 先例:CI continue-on-error,可见非阻塞),spec 同步为实际行为。

### 对抗审查结论(轻量自对抗,判据:报告型检查无 verdict 副作用 + 内容修复由审计自证)
- 审计函数输出即验证:63(基线)→ 57(修 6),wxwidgets 从 one-way 清单消失(grep=0)。
- Git Bash 循环再次不可靠(FILE-MISSING 误报)——全仓审计坚持用 Python(iter 14 教训第 2 次)。

### 数据流 hops(related 链接)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 harness frontmatter related | A → B | ✓ 既有 |
| 2 反向 entry | B → A | ✓ 本轮补 6 条 |
| 3 --related 审计 | validate → 报告/JSON | ✓(advisories 键) |
| 4 CI 步骤(continue-on-error) | validate.yml → 可见性 | ✓ |

### 变种横向 grep
spec 同 block 顺藤摸出 **2 处 iter 3 遗留死文本**:"Dead-link check runs weekly"(功能 iter 3
已删)+ "requests (pinned in requirements.txt)"(依赖 iter 3 已删)——一并修(同文件同族,
doc-drift 家族)。此为 iter 3 backlog [中] 的完整闭环。

### 改动文件
- `scripts/validate.py`(+check_related_bidirectionality + --related flag + JSON 键)
- 6 个目标 harness(反向 related entry:thread-safety/raii/const-correctness/
  cmake-include-hygiene/toolchain-and-compiler-flags/input-validation)
- `docs/specs/2026-05-31-repo-structure-design.md`(item 4 改实际行为 + 2 处 iter 3 死文本)
- `.github/workflows/validate.yml`(+advisory step)

### 测试证据(X/X,真实 exit code)
- `validate --related`:63→**57** advisories;wxwidgets one-way **0** ✓
- `validate --related --json`:advisories 数组 + pass:true(报告不伤 verdict)✓
- validate 裸跑/--stale exit 0(退出码语义零变化)✓;check_all/gen_index/三套件全 0 ✓
- YAML 合法 ✓

### 过程意外 / 与预期偏差
1. 我的全仓审计(65)与 validate --related(63 基线)差 2:审计脚本把"body 提及"算双向、
   validate 只认 frontmatter——两个"审计器"口径不同。**以新 check 的口径为准**(AGENTS 规则 5
   明文"related field lists A")。教训:同一规则的两个实现必须先对齐判据再比数。
2. Python 写 frontmatter 注入(保 CRLF)一把过——但成功归功于逐文件 assert,非运气。

### Pattern Index 更新: 新增 documented-but-unimplemented | advisory-burndown
### 遗留 backlog
- [中] 57 条存量单向 related(清单:`validate.py --related`)——增量清偿,后续轮每轮清一批。
- [低] check_ai_protocol.py LINE_BUDGETS(:49)支配性核实。
- [中] check_review_signals.py:172-174 orphan 误归因。
- m6 README 覆盖语义。

---

## 迭代 23 — producer 误归因修复:orphan FAIL 不再伪造 target(两态决策,含历史改写)

### 触发的理论缺口
iter 18 backlog [中]。两态决策:misattributed 信号的 **SIGNAL 真实**(确有未按 Item 框架的
FAIL)、**TARGET 未知**(报告行不点名 harness)——旧代码硬钉到 `harness_files[0][0]`,
伪造了 14 条日志(5 条挂"AGENTS"——非 harness;9 条挂 ccc——实为协议级发现非其内容缺口),
驱动假 re-review 旗标。同族第二处:inoperable N/A(:185,注释自承"use first")。

### grep journal 结果(Step 1)
`two-state-empty-input`(iter 16——同原则不同位点:这里是"目标不可观测"而非"数据不可观测");
iter 18 F2 预留("修生产者归因使计数下降时,测试反向断裂"——本轮兑现测试同步)。

### 合法 shape 清单 + 覆盖状态(信号 target 可知性)
| Shape | 判别 | UNDERSTOOD? | 方案覆盖? |
|-------|------|-------------|-----------|
| 单 harness scope 报告 | len==1 | ✓(归因可靠推理) | ✓ 归因到该 harness |
| 多 harness scope | len>1 | ✓ | ✓ "orphan" 伪目标 |
| 空 scope | len==0 | ✓ | ✓ 维持跳过(既有行为,不扩) |
| tier-mismatch 多目标 yield(:195-200) | 保守过归因,语义不同 | ✓ | 显式不动(逐 harness tier 比较是其价值) |

### 退化输入×消费者矩阵
| 退化输入＼消费者 | feedback-log | check_feedback summary | harness-evolution Item 3 决策 |
|----------------|--------------|------------------------|------------------------------|
| 旧:multi-scope orphan | 14 条假 target | ccc 9×/AGENTS 5× 假旗标 | 假 re-review 建议 |
| 新:orphan 伪目标 | target 诚实未知 | orphan 14×gap 旗标(真) | 人可挖的未归因信号池 |

### 初版方案(被推翻点)
- 初版想"只修 producer,历史日志不动"→ 推翻:假旗标是**活跃误导输出**(summary 驱动
  Item 3 决策),留着=继续撒谎。改:14 条历史条目 retarget(`— AGENTS, orphan` /
  `— ccc, orphan` → `— orphan, orphan`)+ Outcome 更正注记。
- Outcome 注记是否破坏 dedup 指纹?核实:fingerprint = header+Signal+Scenario+Observation
  四行(:238-241),**Outcome 不在指纹内** → 注记安全(实证:audit dry-run 无重写)。
- 逐条判读后才改:AGENTS 5 条观察全是 GUI PR FAIL(与 AGENTS.md 无关);ccc 9 条是协议级
  发现(其中 2 条嵌了 [Item 3]/[R1] 引用却没匹配 ITEM_LINE_RE——FAIL 行格式变体,记 backlog)。
  **没有机械批量改**,每条读过。

### 对抗审查结论(轻量自对抗)
- hid_to_log_id("orphan") 路径核实:文件不存在 → stem 分支 → "orphan" ✓ parser 安全。
- retarget 后 producer 重跑同输入:新 header `— orphan, orphan` 与旧条目日期不同 → 无假去重。
- 单 harness scope 保留归因:合理推断并注释理由(报告只覆盖一个 harness 时,未框架 FAIL
  大概率属于它)。

### 数据流 hops(信号 target)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 detect_signals yield | attribution_target() → append_to_log | ✓ |
| 2 log 条目 header | producer → check_feedback parser | ✓(orphan 可解析) |
| 3 summary 旗标 | summary → Item 3 决策 | ✓(假旗标清除) |
| 4 历史条目 | 14 条 retarget + 注记 | ✓(audit dry-run 零重写) |

### 变种横向 grep
harness_files[0] 全仓出现:仅 detect_signals 两处(均已改);hid_to_log_id 的 tool/ 前缀分支
不受影响。FAIL 行格式变体(嵌 Item 引用不匹配 ITEM_LINE_RE)= 新 backlog [低]。

### 改动文件
- `scripts/check_review_signals.py`(attribution_target() 两态规则 + 注释)
- `common/meta/harness-feedback-log.md`(14 条 retarget + Outcome 更正注记)
- `scripts/test_feedback_signals.py`(orphan>=10 / AGENTS 绝迹 / 旗标名断言更新)

### 测试证据(X/X,真实 exit code)
- check_feedback:orphan **14×gap FLAGGED**,ccc/AGENTS 无旗标 ✓;total 24 守恒 ✓
- audit --dry-run:无 tier inflation、零重写 ✓;test_feedback exit 0(新断言)✓
- ai/pd/check_all/validate/gen_index 全 0 ✓;--related 57(守恒)✓

### 过程意外 / 与预期偏差
1. Edit 遇 "File has been modified since read"(本会话首次)——前一轮 pack_utils Edit 改过
   同文件的行号状态。重读后再改,**冲突检测是保障不是阻碍**。
2. Retarget 后 summary 的 re-review 建议从"ccc/AGENTS(假)"变为"orphan:14×(真)"——
   修复让旗标数没变少但语义翻转:给人挖的信号池,不是给 harness 定罪的判决。

### Pattern Index 更新: 新增 unknown-target-two-state | forged-attribution
### 遗留 backlog
- [低] FAIL 行格式变体(嵌 [Item N]/[R1] 引用不匹配 ITEM_LINE_RE → 误判 orphan)——观察 2 例。
- [中] 57 条单向 related 清偿。
- m6 README 覆盖语义;[低] LINE_BUDGETS 支配性。

---

## 迭代 24 — 存量 57 条单向 related 一次性清偿(全仓归零)

### 触发的理论缺口
iter 22 backlog 的清偿轮。AGENTS 规则 5((P) 约定):related 必须双向。57 条 across 31 个
目标文件 —— 全部为 harness→harness 对(docs/ 目标无 frontmatter,check 里显式豁免)。

### grep journal 结果(Step 1)
`advisory-burndown`(iter 22);iter 22 的插入逻辑复用(6 文件版推广到 N 文件,含
"已链接"幂等跳过)。

### 方案(无对抗轮,判据:纯 frontmatter 追加 + 审计器自证归零)
- 按 target 分组(31 文件 57 条),每文件一次插入;已有 related 字段的追加、缺失的新建。
- 幂等保护:目标列表已含该条目则跳过(重复运行安全)。
- 归零验证 + diff 纯净性抽检(31 files, 57 insertions, 零 body 改动)。

### 语义权衡(显式记录)
盲互惠可能产生语义噪声(细粒度 harness 挂到 hub harness 的反链)——但规则 5 是仓库自己
立的 (P) 宪法,reciprocity 即标准;导航粒度粗不影响正确性。若未来觉得某反链无意义,
按 harness-evolution 正常流程删**两端**。

### 测试证据(X/X,真实 exit code)
- `validate --related --json`:advisories **57→0**,pass:true ✓
- 文本输出:"Related links are fully bidirectional." ✓
- 六套件 + check_all + gen_index 全 0 ✓;diff stat:31 files / +57 / -0 ✓

### 过程意外 / 与预期偏差
管道 + heredoc 抢 stdin(`cmd | python - <<EOF` 把脚本源当数据)→ 空输入崩溃。改为脚本内
subprocess 自取。**Shell 数据流第三种坑**(前有:管道末端 exit、/tmp 映射)。

### Pattern Index 更新: 新增 heredoc-stdin-conflict
### 遗留 backlog
- [低] FAIL 行格式变体(嵌 [Item N]/[R1] 引用不匹配 ITEM_LINE_RE)。
- m6 README 覆盖语义;[低] LINE_BUDGETS 支配性。

---

## 迭代 25 — 三个 [低] backlog 清账:一个修复、两个实证"不是病"、一个新同族第三处

### 触发的理论缺口
清账轮:iter 2(--json pass 语义)+ iter 8(:153 "死检查")+ iter 21(LINE_BUDGETS 支配性)。
**实证纪律的两个方向都兑现了**:该修的修了;被控诉的两项经实验无罪释放——
"审查者的严重度判断需实证校验"反过来也成立:**backlog 的指控也需要实证校验**。

### grep journal 结果(Step 1)
`documented-but-unimplemented`(iter 22——validate docstring 与 JSON 契约同步属同族);
`non-discriminating-test`/`现状描述错`。

### 三项裁决(各带实验)
| 项 | 指控 | 实验 | 裁决 |
|----|------|------|------|
| --json pass 语义 | exit 3 + pass:true 矛盾 | 键核查 | **修**:+warnings_count + docstring 契约("pass 反映 errors only") |
| check_ai_protocol:153 死检查 | "总被 section 检查掩盖" | 构造含未引用 finding 的合法节结构 review → **exit 1 正确触发** | **无罪**:检查活着且正确,保留 |
| LINE_BUDGETS(:49)支配性 | 疑似 iter 21 同族死代码 | 对照:check_ai_protocol 的 shape 检查是 **substring 存在性**,非 exact 行数 → budget 是活判决 | **无罪**:不支配,保留 |
| (新发现)section_value strip | m2 家族第三处(检查子串命中、提取裸行 startswith → 缩进节"在但空") | 构造缩进节 plan → 修复前 empty-section 假错 | **修** + 测试 |

### 数据流 hops(无跨层;JSON 消费者契约)
| Hop | 写者→读者 | ✓/✗ |
|-----|-----------|-----|
| 1 validate JSON +warnings_count | validate → 机器消费者 | ✓(键显式,判别 exit 0/3) |

### 变种横向 grep
section_value 家族全量:check_plan_protocol(修,iter 21)/ check_debug_report(修,iter 21)/
check_ai_protocol(修,本轮)= 全部 3 处闭环;check_feedback_signals 无此函数。

### 改动文件
- `scripts/validate.py`(docstring 契约 + warnings_count 键)
- `scripts/check_ai_protocol.py`(section_value strip + 注释)
- `scripts/test_ai_protocol.py`(+test_leading_space_section,用对的节名)

### 测试证据(X/X,真实 exit code)
- test_ai_protocol exit 0(新断言:缩进节 plan 通过)✓;JSON 键含 warnings_count ✓
- :153 反证实验(修复前口径):合法节 + 无引用 finding → exit 1 ✓
- pd/fb/check_all 全 0 ✓

### 过程意外 / 与预期偏差
1. **heredoc 第 4 次咬人**(`\\n` 又被吃)——自己 iter 21 立的"含转义代码只用 Edit 工具"规则
   被自己违反。修复时遵守了(Read+Edit)。**规则立了就要查自己是否执行**(与 skill 的
   Pattern Index 机械完成标志同构:立规者最易豁免自己)。
2. fixture 节名错配第 2 次(plan 两协议):check_ai_protocol 的 plan 节是
   Objective/Applicable harnesses/...,不是 check_plan_protocol 的 Goal/Harnesses/...。
   **同形不同约,写 fixture 先查 REQUIRED_SECTIONS**。

### Pattern Index 更新: 新增 backlog-claim-needs-verification | presence-vs-extraction-asymmetry
### 遗留 backlog
- [低] FAIL 行格式变体(嵌 [Item N]/[R1] 引用不匹配 ITEM_LINE_RE)。
- m6 README 覆盖语义。

---

## 迭代 26 — --stale 悬崖预报(无罪)+ README install 语义歧义修复(m6)

### 触发的理论缺口
iter 2 让 exit 3 可达后,--stale 的 CI 步骤(continue-on-error)何时开始"失败"?**悬崖预报**:
解析全部 (last_validated, review_cycle) 组合 → 下一次悬崖 **2026-11-26(1 harness)**,主波
2027-05/06(59 个,12m 周期 cohort 集中于 2026-06 初检)。周期分布:12m×73、24m×9。
**结论:机制正常,近期无误报风暴**——无罪释放,预报入档,不需要代码改动。
(注:12m 按 360 天算,与日历月差 5 天——语义近似,可接受,记录在案。)

### grep journal 结果(Step 1)
`exit-code 契约`(iter 2);m6(iter 17/25 backlog)。检查消费方:check_stale 的
"两者都有值才判"跳过语义——今天 0 个不可解析(82/82 有 cycle)。

### 合法 shape 清单(review_cycle × last_validated)
| Shape | 数量 | 处置 |
|-------|------|------|
| "12m" 周期 | 73 | 不动 |
| "24m" 周期 | 9 | 不动 |
| 缺 last_validated/cycle | 0 | (跳过分支今天不可达,保留——防未来漏字段) |

### m6 修复(README 两处)
Quick Start 与 Modular Packs 两处的连续 install 示例读作累积;实际 `install_pack.py` 每次
**替换**记录(且 .dev-guidelines-installed.yml 已 gitignored,iter 20)。加显式说明 +
"一次命令传全部 pack"提示 + 替换语义段落。

### 测试证据(X/X,真实 exit code)
- 悬崖脚本:输出预报(无代码改动)✓;validate --stale exit 0(现状无 overdue)✓
- README 两处更新,validate/check_all 全 0 ✓

### 过程意外 / 与预期偏差
无。本轮是核查轮:两个怀疑(--stale 悬崖会炸、README 误导)一个无罪、一个坐实。

### Pattern Index 更新: N/A(staleness-cliff 预报写入本条目备查)
### 遗留 backlog
- [低] FAIL 行格式变体(嵌 [Item N]/[R1] 引用不匹配 ITEM_LINE_RE)。
- [信息] staleness 主波 2027-05/06:约 59 harness 同时 overdue——**届时 CI advisory 会一次性
  变吵**,建议 2027-04 前启动一轮批量 re-review(本条目即提醒)。

---

## 迭代 27 — FAIL 格式变体裁决:检测器无罪,协议"暗示格式"补显式(1 行 prompt 修复)

### 触发的理论缺口
iter 23 backlog:2 条日志条目嵌 [Item 3]/[R1] 引用却被判 orphan——是检测器误伤还是真违规?

### 排查(证据链)
1. ITEM_LINE_RE(:57):`^\s*Item\s+(\d+)\s*[—:\-]\s*(\w+)` —— 协议期望格式 `Item N: PASS/FAIL`。
2. ORPHAN_FAIL_RE(:61):FAIL 开头且无 Item 前缀。
3. 协议出处:code-review-with-harness.md:49 "item-by-item pass/fail"(**暗示**);
   weak-model-cpp-review.md:11 "必须点名 harness 与 checklist item"(约定存在,行格式未给)。
4. 那 2 条 FAIL 行(FAIL 在前、item 引用埋在自由文本)不匹配 ITEM_LINE_RE = **真格式违规**,
   orphan 分类正确——信号本就是"未按协议框架的 finding"。

**裁决:检测器无罪,zero 代码改动。** 可行动 residue:协议只暗示格式没明示——弱模型恰恰
依赖显式格式 → review prompt Rules 补 1 行(含正例 + "无 Item 前缀会被记为协议 gap"警告)。

### 测试证据
- test_ai_protocol(review fixtures 含 good-review)exit 0(prompt 改动不破坏检查器)✓
- check_all exit 0 ✓

### 过程意外 / 与预期偏差
grep "Item" prompts/weak-model-cpp-review.md 返回空(Git Bash grep 第 3 次不可靠),换
Read 全文核实。**跨平台文本检索一律 Python/Read,已第 3 次证明。**

### Pattern Index 更新: N/A(裁决入档;protocol-format-explicit 教训并入本条目)
### 遗留 backlog
- [信息] staleness 主波 2027-05/06(见 iter 26)。

---

## 迭代 28 — DOGFOOD(skill Step 5.5):CI 等价全序列 12/12 + 真实 eval 工作流链

### 触发
skill Step 5.5:每批必须用真实消费者流程跑一次,非仓库 fixture。本仓库的"真实消费者"=
CI(全步骤序列)+ eval 操作员工作流(run_eval scaffold → 填输出 → evaluate → registry)。

### 执行与结果
1. **CI 等价全序列(Windows 腿;CI 是 Linux 腿)**:validate --json/--stale/--related →
   gen_index --check → test_ai_protocol → eval good-runs → plan_debug → feedback →
   list_packs → install → validate --installed → gen_index --pack:**12/12 exit 0** ✓
2. **真实 eval 工作流链(dogfood-model 骨架,验后即删)**:
   - run_eval scaffold:4 prompt + task-spec ✓;step-4 注记与实际行为一致 ✓
   - evaluate 空 run:**exit 2 + "not assessable"** + report tier:null(iter 16 契约经
     真实工作流兑现)✓
   - update_model_registry 吃 tier-less report:**拒绝,消息含 empty/not-assessable**
     (iter 16 registry 守卫经真实工作流兑现)✓;model-registry.md 零污染 ✓

### 过程意外 / 与预期偏差
**自己又踩管道末端陷阱**(2>&1 | tail 后 echo $? 量了 tail 的 exit,把 exit 2 看成 0)
——本会话第 3 次主动记录此坑,skill 里它是被记录最多的 trap,依然会踩。修正:关键 exit
一律裸跑测量。教训没有过时,只有暂时记住。

### Pattern Index 更新: N/A(dogfood 全绿;pipeline-exit 陷阱再确认)
### 遗留 backlog
- [信息] staleness 主波 2027-05/06(见 iter 26)。

---

## 迭代 29 — 元审查:用仓库自己的 harness(ai-generated-code-failure-modes)审本会话自己的 diff

**Part A(适用 harness)**:common/code-review/ai-generated-code-failure-modes.md(tier A,
iter 12 新增,scope 正是"AI 写的、编译过、测试绿、但可能错"的代码——本会话 15 个 commit
全是 AI 写的,完美适用)。**Part B 逐项**:

| 项 | tier | 判定 | 证据(file:line / 实测) |
|----|------|------|------------------------|
| 1 假满分/退化输入 | (N) | **PASS** | 每轮 shape 表入账;新增成功样输出反向追源:related [] (validate.py check_related_bidirectionality)、warnings_count=0、attribution_target——均为真实成功非伪装;iter 14/16/18 的三个旧假满分已修 |
| 2 单层修复 | (N) | **FAIL→已补救** | iter 15 BOM 修 3 处漏同语义兄弟 → iter 17 扫描抓到 → iter 19 补 9 处 + 8 处免疫有因。**诚实记录:本会话真实发生过单层修复,批内被自己的扫描轮抓获** |
| 3 承诺契约不兑现 | (N) | **FAIL→本轮修** | evaluate docstring 承诺 exit 1(有 case 失败)但**无测试覆盖**;补:坏 fixture 单 case 目录 → exit 1 断言(test_ai_protocol test_evaluate)。argparse flag 全被读 ✓;check_feedback docstring 契约 iter 18 已同步 ✓ |
| 4 阈值无出处 | (C) | **PASS** | 新常量均带注释(LINE_BUDGET 指向研究文档、threshold≥1 守卫带理由、orphan 伪目标带两态说明);check_stale 360 天月为既有近似,iter 26 记录 |
| 5 不可失败测试 | (C) | **FAIL→本轮补证** | iter 25 leading-space 测试是**修后才加**,缺 red-state 证据;本轮补:旧提取函数在 fixture 上返 ''(实证输出 repr '')→ 旧代码必发 empty-section 错 → 测试判别性成立。其余新测试逐一过变异审问(空目录 exit 2/registry 拒绝/数组契约/BOM——变异任一对应修复即红) |
| 6 状态描述漂移 | (A) | **PASS(带事故)** | 本会话 3 次现状描述错(iter 16 rglob、iter 22 grep 姿势、iter 14 oracle)——全被 REFUTE/实证当轮拦截并记录;流程现状:关键现状主张一律实测 |

**Verdict:PASS with remediations**——两项 FAIL 均为本轮修补;一项单层修复事故批内自查捕获。
元结论:harness 抓到了循环自己的真实漏洞(exit 1 无测试、判别性证据缺失)——**产品在
自己的生产者身上有效**。

### 测试证据
- test_ai_protocol exit 0(+evaluate exit-1 断言)✓;旧提取函数反证实验(repr '')✓
- check_all exit 0 ✓

### Pattern Index 更新: 新增 dogfood-harness-on-own-diff | red-state-retro-evidence
### 遗留 backlog
- [信息] staleness 主波 2027-05/06(见 iter 26)。

---

## 迭代 30 — spec 6.1 契约逐条对账:又两处 documented-but-unimplemented(iter 3 同族终局)

### 触发的理论缺口
iter 22 只修了 spec item 4——本轮把 Performs 清单 **7 项 + Usage 行**逐条对照实现:
| spec 条款 | 实况 | 裁决 |
|-----------|------|------|
| 1 frontmatter completeness | check_frontmatter(且超承诺:校验 type/status/tier/language 值域) | 如实扩写 |
| 2 tier consistency "no deprecated sources without replacement" | **复合承诺无对应实现**:值域校验在 validate(item 1);tier-vs-source 一致性住在 check_review_signals 的 advisory audit;"deprecated sources" 措辞与 cross_references 的 deprecated **link** 警告混淆 | 如实拆写(指明真实住所) |
| 3 category↔path coupling | **无实现**,且机制上需编辑性映射表,不可机械 | 如实改写(声明式 category,无路径耦合) |
| 4 --related | iter 22 实现;但我自己写的"59+ burn down"已过时(iter 24 清零) | 更新(自己上轮的文本本轮过时——时效性教训) |
| 5/6/7 id 唯一/--stale/--json | 实现 ✓(--stale 补"双字段才判"语义;--json 补 warnings_count) | 如实扩写 |
| Usage 行 | 缺 --pack/--installed/--related(subset 模式是 iter 14 上下文的大功能) | 补 + 新增 item 8(subset 空集守卫 iter 20) |

### grep journal 结果(Step 1)
`documented-but-unimplemented`(iter 22 Pattern Index——同类第三/四处,本族终局);
`exit-code 契约`(iter 2/16/25)。

### 教训(本族的结构性根因)
spec 写于实现之前(desired state),实现落后/偏离后**没有任何机制逼 spec 同步**——validate
的 docstring 与 spec 是两个独立文档。已处理的四个实例(iter 3 两处、iter 22 item 4、本轮
item 2/3)全部靠对抗循环撞见。结构性缓解留给 harness-evolution 判断(spec 是否该降格为
"设计意图史"而非"契约"),不在本轮扩scope。

### 测试证据
- 纯文档同步:validate/check_all exit 0 ✓;每条新表述均从函数清单反推(check_frontmatter
  值域分支 :61-75、cross_references deprecated 分支 :137-141)

### Pattern Index 更新: 新增 spec-as-contract-drift
### 遗留 backlog
- [信息] staleness 主波 2027-05/06。
- [低] spec 6.3 CI 步骤清单未含 --related advisory 步骤(workflow 文件为准,收益低不追)。

---

## 迭代 31 — 宣称 vs 现实:AGENTS/README 数字宣称全数腐烂(去计数化修复)

### 触发的理论缺口
skill Rationalization Table:"journal 里写了 X,那就是 X —— 数字类陈述复核一手源"。
本轮把该规则指向**导航文档**:AGENTS.md 宣称 registry "29 entries"(实际 **37** 行,漂移 8);
README 宣称 "**65 harnesses**"(实际 **82**——BOM 修复后 +4,历史增量 +13)。

### 审计结果(全量)
| 宣称 | 一手源 | 裁决 |
|------|--------|------|
| INDEX static 8 链接 | 8/8 存在 | ✓ |
| AGENTS "29 entries" | sources.md 37 行 | **DRIFT → 去计数** |
| README "65 harnesses" | find_harnesses=82 | **DRIFT → 去计数**(指向 INDEX 生成目录,天然保鲜) |
| README "(29 entries)" 树注 | 37 | **DRIFT → 去计数** |
| README Python 3.10+ | CI pins 3.10 | ✓ |
| harness 82 vs INDEX autogen 82 | generator | ✓ MATCH |
| journal "75 harness"(iter 0) | 冻结史志 | 不改(史志不是宣称) |

### 修复原则
**导航文档不写会腐烂的数字**——计数留给生成物(INDEX.md autogen zone,由 --check 守护)。
指针保留,数字删除;README 的 harness 计数改指向 INDEX。

### 测试证据
- validate/gen_index/check_all exit 0 ✓(AGENTS/README 非受检对象,无回归面)

### Pattern Index 更新: 新增 prose-counts-rot
### 遗留 backlog
- [信息] staleness 主波 2027-05/06;[低] spec 6.3 步骤清单。

---

## 迭代 32 — 最后未审位点:templates 一致性(无罪)+ 全 pack export E2E(6/6 绿)

### 触发的理论缺口
R1 边界扫描:scripts/ 全审完(19 文件)、spec/README/AGENTS/prompt/harness 抽样/CI/日志
均已覆盖。剩最后一个从未核对的 producer-consumer 对:**templates/harness.template.md →
validate REQUIRED_FIELDS**(从模板新建的 harness 能否过校验?不能 = 模板欺骗作者)。

### 结果
1. **模板 16/16 必填字段对齐** REQUIRED_FIELDS;值域(status=draft、tier/language 占位在
   合法集内)、`related: []` 空表、`stable_since: ""` 空串(validate 只拒 None 不拒 "")—
   全部兼容。**无罪**。软观察:模板示例日期冻结在 2026.05(作者需自行更新 version/
   last_validated)——占位值语义,可接受,记录。
2. **全 6 pack export --zip E2E**:ai-dev/common-core/cpp-core/cpp-security/cpp-testing/
   python-core 全 exit 0,zip+sha256 齐备(iter 20 的 _path/manifest 改动广度验证)✓。

### 测试证据
- 6/6 export exit 0 ✓;validate/gen_index/check_all exit 0 ✓

### R4 置信度自评
本轮 + 前三轮(29 元审查 2 漏、30 spec 2 处、31 数字 2 处漂移)仍在新维度产出新发现,
未触发"连续 2 轮无新发现"。但发现尺寸在收窄(blocker→major→minor→无罪),符合批次尾部
特征。下一轮按 skill 批次收尾协议执行。

### Pattern Index 更新: N/A
### 遗留 backlog
- [信息] staleness 主波 2027-05/06;[低] spec 6.3 步骤清单。


---

## 批次收口(iter 14-33,2026-08-30)— 20 轮对抗循环累计汇报

### 触发
用户:`$adversarial-development-loop`(bak-20260808 版)**迭代20轮**。硬约束照办:14-33
共 20 轮,每轮 7 步闭环 + journal 落盘,无单方面缩减。

### Pattern Index(主题级蒸馏,优先 grep 本节)

**项目约定类(长寿命,活跃)**:
- **posix-path-identifier**:跨机器提交的路径标识符(pack.yml includes/INDEX 链接/manifest)必须在产出点 as_posix();runtime str() 在 Windows 反斜杠 → subset 过滤静默空转(iter 14)
- **two-state-empty-input**:空输入=不可观测,不是 0 分也不是满分;诚实答案是退出评分 + null(iter 16)
- **get-default-sentinel**:`dict.get(k, DEFAULT)` 把"缺 key"伪装成 DEFAULT(iter 16/23 两例)
- **open-vocabulary-parser**:读侧解析器的词表必须开放(生产者词表会长),窄词表=静默丢数据(iter 18)
- **advisory-burndown**:存量违规清偿用 report-only 检查(仿 --stale),CI continue-on-error,不阻塞增量修复(iter 22/24:59→0)
- **unknown-target-two-state**:信号真实但目标未知时,用显式伪目标(orphan),不伪造归因(iter 23)
- **prose-counts-rot**:导航散文不写会腐烂的数字;计数归生成物(INDEX autogen,--check 守护)(iter 31)
- **spec-as-contract-drift**:spec 写于实现前,无机制逼同步——四实例全靠对抗撞见(iter 3/22/30)

**已修 bug 档案类(短寿命,修复确认后归档)**:
- **bom-frontmatter-exclusion**:`^---` 锚被 BOM 击穿 → harness 全 OS 静默排除;utf-8-sig 全读入点(iter 15/19)
- **parser-producer-drift / partial-parse-silence**:ENTRY_RE 闭词表丢 15/24 条 + 部分解析无声(iter 18)
- **single-layer-bom-fix**:iter 15 修 3 处漏同语义兄弟——扫描抓到,iter 19 补面(诚实事故)
- **forged-attribution**:harness_files[0] 归因伪造 14 条日志(iter 23)
- **vacuous-subset-guard / cycle-detection-in-flight**:空集假满分、依赖环递归(iter 20)
- **dominated-check-removal / presence-vs-extraction-asymmetry**:被 exact-shape 支配的预算检查;presence 子串 vs 提取裸行的自相矛盾(iter 21/25)
- **json-contract-array-vs-object**:多文件 --json 拼接对象不可解析(iter 21)
- **documented-but-unimplemented**:spec item 4 + item 2/3 复合承诺无实现(iter 22/30)
- **non-discriminating-test / living-file-assertions**:改前就绿的断言;活日志上的 ==N 断言必腐(iter 16/18)
- **false-alarm-fatigue**:漂移警报必须在健康日志上为 0,否则狼来了(iter 18 F1)
- **backlog-claim-needs-verification**:backlog 指控也要实证——两项"死代码"指控被无罪释放(iter 25)
- **red-state-retro-evidence**:修后才加的测试要补改前红的反证(iter 29)
- **dogfood-harness-on-own-diff**:用自己的 harness 审自己的 diff,有效(iter 29)
- **heredoc-stdin-conflict**:管道+heredoc 抢 stdin;含转义代码只走 Edit 工具(4 次事故)
- **vacuous** 家族补充:**cycle** 见上;**spec/协议显式格式**:弱模型要行格式模板(iter 27)

### 累计指标

- **commits**:22(含 journal)· **diff**:60 files,+2598/−101
- **测试**:原 2 套件 → **3 套件**(新增 test_feedback_signals.py,CI+check_all 接线);
  断言增量:evaluate 6 组、BOM 3 组、wrapper-json 3 组、feedback 10 组、leading-space 1 组、
  exit-1 契约 1 组(全套 exit 0)
- **CI**:validate.yml +3 步(feedback 测试/--related/--installed 序列原已有);
  Windows 本地 CI 等价序列 12/12 绿(dogfood)
- **REFUTE/扫描 subagent**:5 个独立(iter 14/16/17-scan/18 + iter 8 先例模式)
  ——**4 次推翻方案级错误**(iter 14 四处事实错含 oracle、iter 16 现状描述错+死代码方案、
  iter 17 抓 2 blocker 生产环境漏报、iter 18 驳回主打特性的假阳性设计)
- **机器消费层健康度**:baseline(gen_index --check FAIL/check_all exit 1)→ 全绿且
  新增 3 类守护(--check 恒守、--related 双向性、BOM/subset/环/空集守卫)

**blocker/major 累计(批内修复)**:
1. [B] subset 模式 Windows 全空转(iter 14)2. [B] feedback parser 丢 15/24 条(iter 18)
3. [B] 不匹配 header 合并腐蚀(iter 18)4. [M] 空记录静默 T0 入库(iter 16)
5. [M] BOM 9 处假错面(iter 15/19)6. [M] 阈值 0 崩溃违约(iter 18)
7. [M] orphan 伪造归因 14 条(iter 23)8. [M] requires 环 RecursionError(iter 20)
9. [M] vacuous subset 假满分(iter 14/20)10. [M] 65 条单向 related + spec 未实现(iter 22/24)
11. [M] spec item 2/3 复合承诺(iter 30)12+. 数字漂移/判决死代码/--json 非法/strip 自相矛盾等 minor 若干

### shape 覆盖(累计新增)
路径标识符 4 shape(iter 14)· frontmatter 可解析性 4(+UTF-16 显式不做)(iter 15)·
eval 目录 5 shape + registry 4(iter 16)· ### header 8 shape(iter 18)· 依赖图 4(iter 20)·
target 可知性 4(iter 23)· staleness 组合(12m/24m 全量)(iter 26)

### 盲区回收(本批反复出现但 skill 分类法未覆盖)
1. **工具层转义吞噬**(Bash heredoc 连吃 \x/\n 4 次)——skill 只有"shell 末端信号"类,
   没有"写文件必须 Edit 工具"的硬规则;已在本 journal 立规则并自执行。
2. **审计器口径先行**:同一规则的两个实现(我的 ad-hoc 审计 vs validate check)必须先对齐
   判据再比数(iter 22 差 2 的教训)——属于"现状描述错"的变体,但发生在**工具自身**。
3. **fixture 语法先于样本**:测试作者连续写错被测语法(空格 id/错协议节名)——fixture
   敏感性检查应前移到"写样本前先读被测器的 shape 清单"。

### 终止条件评估
- **R1**:20 轮每轮新维度/新发现(反斜杠→BOM→两态→parser→归因→spec→数字→模板),
  无静默轮;发现尺寸收敛(blocker→minor→无罪)符合批次尾部特征。
- **R4**:dogfood 双重验证(CI 等价 + 真实工作流)后置信度有实证支撑,非"多轮安静后的高置信"。
- **用户指令 20 轮**:完成(14-33)。本节即 skill 终止条件要求的累计汇报。
