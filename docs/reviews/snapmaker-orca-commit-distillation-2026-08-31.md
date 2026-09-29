# Snapmaker/OrcaSlicer Commit 坑位蒸馏报告 — 2026-08-31(批 1+批 2 全量)

- 输入仓库:`C:\coil\Projects\SnapmakerOrca`(upstream remote = github.com/Snapmaker/OrcaSlicer;fork 基线上游 = SoftFever/OrcaSlicer 系)
- 蒸馏面:release_2_3_7 主线(release_2_3_6/main 并入)
- 预筛方法:message 匹配 revert|workaround|hotfix|fix|bug,再用上游克隆 `C:\coil\Projects\OrcaSlicer`(OrcaSlicer/OrcaSlicer @ af9fd10d7a)对象库剔除上游既有 commit,仅保留 Snapmaker 团队 commit
- 版本钉:wxWidgets=3.1.5(SoftFever/Orca-deps-wxWidgets;本项目 P 级 harness `cpp-wxwidgets-3-1-5`);upstream=SoftFever/OrcaSlicer / OrcaSlicer/OrcaSlicer;fork=Snapmaker/OrcaSlicer
- 分类靶:dev-guidelines INDEX.md(2026-08 快照)
- 已有条目:无既有 Orca commit 坑位库(最近邻:dev-guidelines loop-journal Pattern Index — harness 工具域;Snapmaker docs/ 为单次修复文档)
- 可信源白名单:sources.md 注册源(N1-N9/C1-C28/A1-A23)+ 上游仓库

所有 Observation 均经 `git show <hash>` 字符串级核验;行号取父提交(`<hash>^:file`)实测。批 2 为扩容(预筛池全量 57 条)。

---

# 批 1(25 条)

## commit 236f0d350b — fix: crash in solve_extruder_order (Sentry #7256025247) (#754)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-undefined-behavior(条目:"Raw array indexing with computed index → Validate index < size")
- Signal: gap(缺上界校验的数组下标,EN: unchecked-array-index)
- Scenario: GCode/ToolOrdering 切片工具序求解 + 崩溃修复 + 当时在审 Sentry 越界崩溃
- Observation: `solve_extruder_order` 用 extruder id 直接索引 `wipe_volumes`(id 未校验 < size 即当下标);id 来源为配置/工具序数据,超出 wipe_volumes 维度时越界读。修复在函数入口加守卫,越界即返回原序。证据:`src/libslic3r/GCode/ToolOrdering.cpp:177`(父提交)`wipe_volumes[all_extruders[mid_point]][all_extruders[target]]`;diff 引文:
  ```
  +	for (auto id : all_extruders) {
  +    if (id >= wipe_volumes.size())
  +        return all_extruders;
  ```
- root_pattern: 数组下标来自跨层数据(配置/工具序)时,先校验 `< size` 再访问;审查时对"下标来源不是本函数算出的循环变量"的索引一律要求上界证明。
  - [ ] 检查:数组/vector 下标是否来自函数外传入的 id/索引,访问前是否有 `< size` 校验?
- source_status: none —— 上游 main(2026-08)该函数已重构至 `src/libslic3r/GCode/ToolOrderUtils.cpp:923`,同款无守卫下标仍在上游存在;tribal+version-fragile,同步重构时复查。
- evidence: commit=236f0d350b; diff_line=`wipe_volumes[all_extruders[mid_point]][all_extruders[target]]`(ToolOrdering.cpp:177,父提交); source=none(lead: 上游 ToolOrderUtils.cpp:923 同款)
- confidence: high

## commit 2e56dd12ee — Safeguard EdgeGrid.hpp (#752)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-undefined-behavior(条目:"Raw array indexing with computed index")
- Signal: gap(遍历越界仅靠 assert 防护,EN: assert-only-bounds)
- Scenario: EdgeGrid 网格遍历访问器 + 越界崩溃防护 + 当时在审 corrupted 模型遍历越界
- Observation: 四条 `visit_cells` 步进循环沿 (ix,iy)→(ixb,iyb) 走 DDA 时,仅用方向单调 assert(`assert(ix <= ixb)`),终点落在网格外时步进单元越界;release 构建 assert 关闭 → `visitor(iy, ix)` OOB 读。修复在每次步进后加运行时边界检查并 return。证据:`src/libslic3r/EdgeGrid.hpp:224-229`(修复后);diff 引文:
  ```
  +	if (ix < 0 || iy < 0 || ix >= (int64_t)m_cols || iy >= (int64_t)m_rows)
  +		return; 
  ```
- root_pattern: 网格/表遍历若终点可能越界,运行时必须有边界守卫,不能只靠 assert(assert 在 release 被剥离)。
  - [ ] 检查:遍历/步进循环的越界防护是否仅为 assert?release 构建下是否仍有运行时守卫?
- source_status: upstream-known —— 上游 #12806(9478af93e,2026-04-07)以同样 8 行守卫修复同一文件;本 fork 2026-08-21 独立修复,晚于上游 4 个月(https://github.com/OrcaSlicer/OrcaSlicer/pull/12806)。
- evidence: commit=2e56dd12ee; diff_line=`if (ix < 0 || iy < 0 || ix >= (int64_t)m_cols || iy >= (int64_t)m_rows)`; source=https://github.com/OrcaSlicer/OrcaSlicer/pull/12806
- confidence: high

## commit 76ee70bec8 — fix: use literal format string for visibility icon (#756)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(printf 风格 API 误用;taxonomy 无 format-string harness,已 grep 确认)
- Signal: misleading(printf 风格 API 当布局 API 用 + 多余参数被静默吞掉,EN: printf-api-misuse)
- Scenario: GCodeViewer 图例渲染 + 渲染修复 + 当时在审图例可见性图标绘制
- Observation: `ImGui::Text` 是 printf 风格 API,调用者把运行时图标字符串当 format 参数传入,并附带一个不匹配任何重载的 `ImVec2` 布局参数——该参数被 vsnprintf 静默忽略(无编译错),字符串若含 `%` 会错渲染(-Wformat-security)。证据:`src/slic3r/GUI/GCodeViewer.cpp:4550`(父提交);diff 引文:
  ```
  -ImGui::Text(into_u8(visible ? ImGui::VisibleIcon : ImGui::HiddenIcon).c_str(), ImVec2(16 * m_scale, 16 * m_scale));
  +ImGui::Text("%s", into_u8(visible ? ImGui::VisibleIcon : ImGui::HiddenIcon).c_str());
  ```
- root_pattern: 变参/printf 风格 API(ImGui::Text、wxPrintf 等)不允许把运行时字符串当 format,也不会有"多余参数"被合法消费——多余实参被静默吞掉,是 API 误用的强信号。
  - [ ] 检查:printf 风格 API 的 format 参数是否为字面量?是否传了该 API 并不存在的"布局/样式"参数?
- source_status: none —— 图例图标代码为 Snapmaker 专属;tribal。
- evidence: commit=76ee70bec8; diff_line=`ImGui::Text(into_u8(...).c_str(), ImVec2(16 * m_scale, 16 * m_scale))`; source=none
- confidence: high

## commit cef36b121c — fix(login): stop token extraction at first '?', '&' or '#' (#741)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-parsing-validation(外部 URL 解析)
- Signal: under-coverage(分隔符集覆盖不全,EN: incomplete-delimiter-set)
- Scenario: WebSMUserLogin 登录回调 URL 解析 + 修复 + 当时在审 OAuth token 提取
- Observation: token 值提取只以 `?` 为终止符;回调 URL 中 token 后跟 `&state=...` 或 `#frag` 时,整段余串被当 token(无第二个 `?` → npos → 取余部)。修复用 `find_first_of("?&#")`,与 RFC 3986 的 query 参数分隔(`&`)/fragment 起始(`#`)一致。证据:`src/slic3r/GUI/WebSMUserLoginDialog.cpp:187`(父提交);diff 引文:
  ```
  -size_t end = tmpUrl.find("?", start);
  +size_t end = tmpUrl.find_first_of("?&#", start);
  ```
- root_pattern: 手工解析 URL/查询串时,参数值终止符必须覆盖该语法的完整分隔符集(参数分隔 `&`、fragment 起始 `#`),不能只按一个字符猜。
  - [ ] 检查:手工字符串解析是否只按单一分隔符切分,而忽略该语法的其他合法分隔符?
- source_status: authority —— RFC 3986 §3.4(Query)/§3.5(Fragment)(sources.md N3,URL 语法与版本无关)。
- evidence: commit=cef36b121c; diff_line=`tmpUrl.find("?", start)` → `tmpUrl.find_first_of("?&#", start)`; source=https://www.rfc-editor.org/rfc/rfc3986(§3.4/§3.5)
- confidence: high

## commit c61a50495c — fix(login): capture token when oauth callback returns raw json (#758)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(WebView2 导航契约 + HTTP 回调形态,跨子系统)
- Signal: misleading(对第三方回调契约只实现一种形态,EN: single-protocol-assumption)
- Scenario: WebSMUserLogin 登录流程 + 二次修复 + 当时在审 OAuth 回调收不到 token
- Observation: token 捕获只认"回调 URL 携带 token=" 一种形态;第三方端点可 200 返回 raw JSON body,且 WebView2 对该跳转的导航事件不可靠、对话框走 ShowModal 不走 run() → 原导航事件路径整条失效。修复加 500ms 轮询定时器 + RunScript 经 document.title 偷渡 body。diff 内注释自述:
  ```
  +// The oauth callback page must be found by polling: WebView2 does not
  +// reliably deliver navigation events for that hop
  ```
  与 #741 同文件同逻辑区但为**不同检查点**(#741 修分隔符集;#758 修"回调形态只有一种"的根假设)——#741 属单层修复漏下游的例证。
- root_pattern: 对接外部契约(OAuth 回调/Webhook)时,只实现"文档中的一种响应形态"即视为完成;审查应追问:端点实际可能返回哪些形态?事件通知是否可靠?
  - [ ] 检查:与第三方/外部系统的交互是否只覆盖单一响应形态?事件驱动路径是否依赖不可靠的事件送达?
- source_status: none —— WebSMUserLoginDialog 为 Snapmaker 专属(2.1.2 合并引入);tribal。
- evidence: commit=c61a50495c; diff_line=`m_callback_timer = new wxTimer(this, CALLBACK_POLL_TIMER_ID); m_callback_timer->Start(500);`; source=none
- confidence: high

## commit b826bb2257 — fix: first layer height should not override variable layer height profile (#757)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(切片逻辑不变量;taxonomy 无切片正确性 harness)
- Signal: misleading(错误不变量触发数据丢弃,EN: wrong-invariant-regeneration)
- Scenario: PrintObject 层高 profile 更新 + 修复 + 当时在审"可变层高被吞"
- Observation: 再生成触发条件把 `layer_height_profile[1] != first_object_layer_height` 当作非法;而首层高由 `generate_object_layers()` 单独硬编码应用,profile 首段本就不必等于它——条件误判 → 从 3MF 加载的有效可变层高 profile 被清空并替换为固定层高(用户数据丢失)。证据:`src/libslic3r/PrintObject.cpp:3930`(父提交);diff 引文:
  ```
  -if (layer_height_profile.empty() || layer_height_profile[1] != slicing_parameters.first_object_layer_height || has_dithering_ranges) {
  +if (layer_height_profile.empty() || has_dithering_ranges) {
  ```
- root_pattern: "数据合法性检查"必须与被检查数据的真实语义一致;把"两个值不同"当非法前,先确认二者是否本就该解耦。
  - [ ] 检查:再生成/丢弃用户数据的触发条件,其不变量假设是否与真实数据语义一致?
- source_status: none —— 上游 main(2026-08)PrintObject.cpp:4000 仍保留同款条件;tribal+version-fragile。
- evidence: commit=b826bb2257; diff_line=`layer_height_profile[1] != slicing_parameters.first_object_layer_height` 从再生成条件删除(PrintObject.cpp:3930,父提交); source=none(lead: 上游 PrintObject.cpp:4000 仍带同条件)
- confidence: high

## commit 7dd8497c5f — fix: add wasm and otf MIME types to HttpServer (#751)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(扩展名→Content-Type 映射表;无 harness 覆盖)
- Signal: under-coverage(映射表缺条目,EN: mime-map-gap)
- Scenario: 内嵌 HttpServer 静态资源服务 + 修复 + 当时在审 flutter_web 资源加载失败
- Observation: write_response 的扩展名→content-type if-else 链缺 `.wasm`/`.otf`,未知扩展落默认 `application/octet-stream`(HttpServer.cpp:850 实测默认值);wasm 模块需 `application/wasm` 才能实例化 → 内嵌 UI 的 WASM 资源加载失败。修复补两条映射。证据:`src/slic3r/GUI/HttpServer.cpp:855-870`;diff 引文:
  ```
  +else if (ends_with(file_path, ".wasm"))
  +    content_type = "application/wasm";
  ```
- root_pattern: 白名单式映射表(扩展名/选项/枚举→输出)新增消费类型时必须同步审计映射表;缺条目不报错,只静默产出错误输出。
  - [ ] 检查:本改动新增了会被映射表消费的文件类型/取值吗?对应表项是否补齐?
- source_status: none —— HttpServer 的 MIME 链为 Snapmaker 专属改写;tribal。
- evidence: commit=7dd8497c5f; diff_line=`else if (ends_with(file_path, ".wasm")) content_type = "application/wasm";`; source=none
- confidence: high

## commit c7f426abfd — Fix ini bug from sentry (#750)
- verdict: **finding**(同 commit 两处检查点,共享同一根模式)
### finding
- kind: pitfall
- target: cpp-integer-safety(unsigned wrap 条目 + 变长除数条目同时命中)
- Signal: gap(空容器参与 size 算术无守卫,EN: empty-container-arithmetic)
- Scenario: DailyTips/HintNotification 渲染空 ini 内容 + Sentry 崩溃修复 + 当时在审空数据输入
- Observation: 两处同根:①DailyTips `content_lines.size() - 1` 空容器时 unsigned 下溢为 SIZE_MAX → `content_lines[i+1]` 立即越界;②HintNotification `rand() % m_loaded_hints.size()` 空容器时除零。修复均在空容器时提前返回。证据:`src/slic3r/GUI/DailyTips.cpp:168-169`、`src/slic3r/GUI/HintNotification.cpp:321`(父提交);diff 引文:
  ```
  +if(!content_lines.empty()){
          for (int i = 0; i < content_lines.size() - 1; i += 2) {
  ```
- root_pattern: 任何 `v.size() - N` / `% v.size()` 出现在数据可能为空的路径上,必须先做空/边界守卫;size 参与算术不等于 size 合法。
  - [ ] 检查:容器 size 参与减法/取模/除法的位置,空容器时行为是什么?是否有守卫?
- source_status: upstream-known + none —— DailyTips:上游 2025-08-25 已用 `has_cjk()` 重构修复(8dd88df97b),分支滞后约一年;HintNotification:上游 main 仍无守卫(HintNotification.cpp:322 同款)。
- evidence: commit=c7f426abfd; diff_line=`for (int i = 0; i < content_lines.size() - 1; i += 2)`(DailyTips.cpp:168,父提交)+ `m_hint_id = rand() % m_loaded_hints.size();`(HintNotification.cpp:321,父提交); source=https://github.com/OrcaSlicer/OrcaSlicer(has_cjk 8dd88df97b,2025-08)
- confidence: high

## commit 8168f5f0c5 — Fix consumable sync crash when device not mounted (#740)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(业务不变量"耗材数 ≥1",跨同步/预设子系统)
- Signal: gap(计数无下界守卫,EN: missing-lower-bound)
- Scenario: 耗材同步对话框 + 崩溃修复 + 当时在审"同步把耗材清成 0"
- Observation: 设备未挂载时同步列表为空,sync 流程把耗材数降为 0(`set_num_filaments(0)`)并继续走 `syncedData[i]` 逐项更新;下游"新增耗材"路径假设 filament ≥1,0 状态触发崩溃。修复在 effective_size==0 时直接 return(注释:"The number of filaments cannot be reduced to zero")。证据:`src/slic3r/GUI/Plater.cpp:9244`(父提交)及随后的 `set_num_filaments(effective_size,...)` 与 `syncedData[i]` 循环;diff 引文:
  ```
  +// The number of filaments cannot be reduced to zero.
  +if (effective_size == 0)
  +    return;
  ```
- root_pattern: 同步/覆盖类操作把业务计数压到领域不变量之下(如 0 耗材)前必须有下界守卫;崩溃点往往不在写 0 处而在下游首个假设 ≥1 的位置。
  - [ ] 检查:同步/批量覆盖路径是否可能把计数/集合压到领域不变量之下?下游是否假设了该不变量?
- source_status: none —— 同步对话框为 Snapmaker 专属;tribal。
- evidence: commit=8168f5f0c5; diff_line=`if (effective_size == 0) return;`(Plater.cpp:9242-9246); source=none
- confidence: mid

## commit d6d943178f — ASA/ABS not heat-resistant (#721)
- verdict: **finding**
### finding
- kind: pitfall
- target: common-config-option-registration("新选项的每个注册位点都要触及"同族:数据位点未补)
- Signal: under-coverage(新选项未覆盖既有 profile 实例,EN: profile-data-gap)
- Scenario: Snapmaker 耗材 profile 维护 + 修复 + 当时在审 ABS 被当非高温材料
- Observation: `filament_is_high_temperature` 由 #504(ed29afecd9 "Feature top cover")引入后,既有 ABS(以及 ASA)profile 未补该键 → 默认 0 → 机器把高温柔性料当普通料处理。修复给 Snapmaker ABS @U1 全 nozzle 档位补 `"filament_is_high_temperature": ["1"]`。证据:`resources/profiles/Snapmaker/filament/Snapmaker ABS @U1 0.2 nozzle.json:46`;diff 引文:
  ```
  -  "filament_type": ["ABS"]
  +  "filament_type": ["ABS"],
  +  "filament_is_high_temperature": ["1"]
  ```
- root_pattern: 引入新 config 选项后,必须审计**所有既有取值实例**(profile/预设/存档)的默认语义;缺键不报错,只静默错分类。
  - [ ] 检查:新增选项时,现有 profile/预设/存档是否全部补齐了新键的语义值?
- source_status: none —— 选项与 profile 均为 Snapmaker 专属;tribal。
- evidence: commit=d6d943178f; diff_line=`"filament_is_high_temperature": ["1"]` 追加至 Snapmaker ABS @U1 各 nozzle profile; source=none(选项引入自 #504 ed29afecd9)
- confidence: high

## commit 675866c502 — fix: resolve ambiguous ternary operands breaking GCC/Clang builds
- verdict: **finding**(批 2 由 cannot-reconstruct 升级,见 #530 同形修复)
### finding
- kind: pitfall
- target: cpp-wxwidgets-3-1-5(wxString 常量/临时值形态陷阱,本项目 P 级)
- Signal: misleading(wxEmptyString 在三元中的类型形态破坏 GCC/Clang 编译,EN: wxEmptyString-ternary)
- Scenario: 侧边栏喷头直径下拉 + 编译修复 + 当时在审 GCC/Clang 构建断裂
- Observation: `diam_str.empty() ? wxEmptyString : wxString(diam_str) + "mm"` —— 三元两分支为"全局 const wxString 左值"与"wxString 临时表达式右值",GCC/Clang 判定操作数组合不可解析,MSVC 放行 → Linux/Flatpak 构建断裂。修复把左值侧改为 `wxString()` 纯右值。批 2 的 #530(FilamentColorDialog.cpp:726 同形 `wxEmptyString : FromStdString(...)`)独立复现同一坑,机制由双实例坐实。证据:`src/slic3r/GUI/Plater.cpp:9462`;diff 引文:
  ```
  -diameter_combo->SetValue(diam_str.empty() ? wxEmptyString : wxString(diam_str) + "mm");
  +diameter_combo->SetValue(diam_str.empty() ? wxString() : wxString(diam_str) + "mm");
  ```
- root_pattern: wxEmptyString(全局 wxString 对象)与 wxString 表达式混用于三元操作符,GCC/Clang 编译失败;三元两分支保持同形(同为临时值/同为左值)。
  - [ ] 检查:三元表达式两分支是否混用 wxEmptyString 常量与 wxString 表达式?两分支类型/值类别是否一致?
- source_status: none —— Snapmaker 专属代码;机制为编译器行为差异,无白名单权威源;tribal+version-fragile(升级 wxWidgets 时复查)。
- evidence: commit=675866c502(+佐证 a4c7f48992 #530 同形修复); diff_line=`? wxEmptyString : wxString(diam_str) + "mm"`; source=none
- confidence: mid(机制由双实例坐实;具体编译器诊断未留存)

## commit 74c01ad75f — Fix Flatpak build: add missing <wx/wupdlock.h> (#739)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-build-system("Every file includes what it directly uses" + "No transitive include reliance")
- Signal: gap(缺失 include 靠传递包含/预编译头掩盖,EN: transitive-include-reliance)
- Scenario: ParamsPanel/Timelapse 弹窗 + 构建修复 + 当时在审 Flatpak(PCH=OFF)编译失败
- Observation: 两文件使用 `wxWindowUpdateLocker` 却未包含 `<wx/wupdlock.h>`;MSVC 构建经其他头传递包含而通过,Flatpak 构建(wxGTK,PCH=OFF)断裂。修复补显式 include。证据:`src/slic3r/GUI/ParamsPanel.cpp:21`、`src/slic3r/GUI/Timelapse/TimelapseDownloadPopup.cpp:10`;diff 引文:
  ```
  +#include <wx/wupdlock.h>
  ```
- root_pattern: 文件必须包含其直接使用的符号;PCH/传递包含掩盖的缺失 include 会在换构建配置时爆发。
  - [ ] 检查:本文件使用的符号是否都由本文件直接 include 提供?是否依赖传递包含或 PCH?
- source_status: none —— 触发文件为 Snapmaker 专属;坑本身为通用 include 卫生;tribal。
- evidence: commit=74c01ad75f; diff_line=`#include <wx/wupdlock.h>`(ParamsPanel.cpp / TimelapseDownloadPopup.cpp); source=none
- confidence: mid

## commit f1e9f78696 — Fix Flatpak build with SLIC3R_PCH=OFF (#712)
- verdict: **duplicate**(duplicate-of: 74c01ad75f)
- 理由:同一坑位、同一检查点(文件顶部缺失 include,靠 PCH/传递包含掩盖,Flatpak PCH=OFF 暴露);修复同为补显式 include(MixedFilamentBatchDialog.cpp 补 `<wx/wupdlock.h>`、MixedFilamentColorMapPanel.hpp 补 `<array>`)。

## commit c6e16f7da5 — Fix syntax errors introduced by crash hardening (#735) (#738)
- verdict: **finding**
### finding
- kind: pitfall
- target: snapmaker-orca-workflow("Atomic commits: one logical change, must compile"(P);#735 628+/205- 亦超 "≤500 lines unless split plan")
- Signal: gap(提交未经编译验证即合入,EN: unverified-hotfix)
- Scenario: #735 崩溃加固大提交(SSWCP/MQTT/GCodeViewer try/catch 包裹)+ 修复 + 当时在审紧随其后的语法错误修复
- Observation: #735 的 try/catch 机械包裹产生括号/关键字失衡(MoonRaker.cpp 残留多余 `{`、SSWCP.cpp `catch` 前 `try` 丢失),以语法错误形态合入,须 #738 紧急修复。message 直陈:"Fix syntax errors introduced by crash hardening (#735)"。diff 引文:
  ```
  -        {
           try {
  ```
  (MoonRaker.cpp:866-868,消除 #735 遗留的多余左括号)
- root_pattern: 大规模机械包裹(try/catch/作用域)提交必须过编译/CI 再合入;"崩溃加固"类 hotfix 尤其容易括号失衡,且常与功能改动混在一个大 commit 里。
  - [ ] 检查:本次提交是否含大段 try/catch/作用域包裹?合入前是否在目标平台编译通过(而非仅审阅)?
- source_status: none —— 内部流程问题;tribal。
- evidence: commit=c6e16f7da5; diff_line=`-        {` → `try {`(MoonRaker.cpp / SSWCP.cpp); source=none
- confidence: mid

## commit 73d5b2a170 — fix: stay on Preview when re-dropping the same G-code (#732)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(UI 视图状态机;无 harness 覆盖)
- Signal: misleading(静默 no-op 守卫 + 未知内容先切页,EN: silent-noop-guard)
- Scenario: 拖放/加载 G-code + 修复 + 当时在审重复拖放同一文件时视图乱跳
- Observation: 两个叠加错误:①OnDropFiles 在知道拖的是什么之前就无条件切 3D 编辑器(Plater.cpp:10460 父提交)——only-gcode 模式重复拖放时闪空 3D 页;②load_gcode 的同文件守卫直接 return(Plater.cpp:18776 父提交)——用户无任何反馈,停在错误视图。修复:非 only-gcode 才切 3D,同文件时显式切回 Preview 并重绘。diff 引文:
  ```
  -    m_mainframe.select_tab(size_t(MainFrame::tp3DEditor));
  +    if (!m_plater.only_gcode_mode()) {
  +        m_mainframe.select_tab(size_t(MainFrame::tp3DEditor));
  ```
- root_pattern: 守卫路径"静默 return"必须自问:调用方期望的最终状态(视图/反馈)谁负责恢复?先于内容判定切换 UI 状态 = 竞态式的观感错误。
  - [ ] 检查:提前 return 的守卫路径是否留下调用方不可见的状态差异?UI 切换是否发生在内容判定之前?
- source_status: none —— 上游 main(2026-08)Plater.cpp:14694 仍保留同款静默守卫;tribal+version-fragile。
- evidence: commit=73d5b2a170; diff_line=`m_mainframe.select_tab(size_t(MainFrame::tp3DEditor));` 移入 only_gcode_mode 守卫; source=none(lead: 上游 Plater.cpp:14694 同款)
- confidence: high

## commit fdbd87498a — fix gcode preview bug (#765)
- verdict: **finding**(两处独立逻辑错误)
### finding
- kind: pitfall
- target: orphan(预览渲染几何逻辑;无 harness 覆盖)
- Signal: misleading(边界阈值/布尔运算符语义误用,EN: boundary-and-boolean-slips)
- Scenario: GCodeViewer 层元数据/路径区间过滤 + 修复 + 当时在审预览错层/漏段
- Observation: 两处:①层元数据端点更新条件 `move_id - last_travel_s_id > 1` 阈值过严——相邻 travel(`差值==1`)时端点不更新 → 层段边界缺失;②路径-层区间过滤 lambda 用 `||` 连接首尾端点判定(GCodeViewer.cpp:3338 父提交),跨界的路径被误纳 → 错层显示;修复改 `> 0` 与 `&&`。证据:`src/slic3r/GUI/GCodeViewer.cpp:961`(父提交);diff 引文:
  ```
  -if (move_id - last_travel_s_id > 1 && !m_layers.empty())
  +if (move_id - last_travel_s_id > 0 && !m_layers.empty())
  ```
- root_pattern: 区间/边界判定在"恰好相邻""端点恰在界上"处的行为必须逐边界推演;`||`/`&&` 表达"任一/全部"语义时要与意图比对。
  - [ ] 检查:边界条件(差值==1/0、端点==界值)在判定式中行为是否正确?布尔运算符与"全部满足/任一满足"语义一致吗?
- source_status: none —— 两行为 BambuStudio 导入系代码,上游已重构无此两行;tribal。
- evidence: commit=fdbd87498a; diff_line=`move_id - last_travel_s_id > 1` → `> 0`(GCodeViewer.cpp:961)+ `||` → `&&`(GCodeViewer.cpp:3338); source=none
- confidence: mid

## commit 785c690f47 — Fix crashes during GUI shutdown/recreation (#753)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-lifetime(容器 reset 后持有的索引失效)
- Signal: gap(reset 后过期索引无守卫,EN: stale-index-after-reset)
- Scenario: GUI 重建/语言切换中 Sentry 崩溃 + 修复 + 当时在审 shutdown→reset_canvas_volumes 后的场景访问
- Observation: `GLVolume::transformed_non_sinking_bounding_box()` 直接 `objects[object_idx()]->volumes[volume_idx()]`(父提交 3DScene.cpp:359),模型数据经 `mainframe->shutdown()->reset_canvas_volumes()` 清空后索引过期 → 越界访问;而 `ProgressDialog::Update()` 内部 `YieldFor` 派发事件,使 `on_slicing_completed` 在重建期间重入执行。修复:索引/plater 空指针检查 + `is_recreating_gui()` 重入门。diff 引文:
  ```
  -return GUI::wxGetApp().plater()->model().objects[object_idx()]->volumes[volume_idx()]->mesh().transformed_bounding_box(trafo, 0.0);
  +if (obj_idx < 0 || obj_idx >= (int) objects.size() || !objects[obj_idx])
  +    return bounding_box().transformed(trafo);
  ```
- root_pattern: 持有"对象集合索引"的渲染/缓存对象,在集合可能被整体 reset 的生命周期内访问必须校验索引;事件循环重入(YieldFor)是把"事后才发生的失效"提前暴露的放大器。
  - [ ] 检查:渲染/缓存对象持有的集合索引,在集合被 clear/reset 后是否仍会被访问?重入路径(YieldFor/模态泵)是否已防护?
- source_status: none —— 上游 main(2026-08)3DScene.cpp 该函数仍无边界检查;tribal+version-fragile。
- evidence: commit=785c690f47; diff_line=`objects[object_idx()]->volumes[volume_idx()]` 加边界/空检查(3DScene.cpp:356-372); source=none(lead: 上游 3DScene.cpp 无同款)
- confidence: high

## commit d583aed761 — fix: avoid boost::any_cast type mismatch crash in SSWCP filament mapping (#546)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-type-safety(类型化访问的解引用前检查)
- Signal: misleading(存在性检查 ≠ 类型安全访问,EN: has-vs-typed-access)
- Scenario: SSWCP 耗材映射 + 崩溃修复 + 当时在审 filament_type 类型不匹配
- Observation: 旧码 `if (full_config.has("filament_type")) { ... full_config.option<ConfigOptionStrings>("filament_type")->values.size() ... }`——`has()` 只查键存在,`option<T>()` 在动态类型不符时返回 nullptr(Config.hpp:2022-2027 实测),`->values` 空指针解引用/旧版 any_cast 抛异常 → 崩溃。修复:先取类型化指针,判 nullptr 与空 values 再使用。证据:`src/slic3r/GUI/SSWCP.cpp:3310-3322`(父提交);diff 引文:
  ```
  -if (full_config.has("filament_type")) {
  +if (const auto* filament_type_opt = full_config.option<ConfigOptionStrings>("filament_type");
  +    filament_type_opt != nullptr && !filament_type_opt->values.empty()) {
  ```
- root_pattern: 按名取配置值时,"键存在"与"类型正确"是两个独立前提;用 `has()` 后的无检查 `option<T>()` 解引用即赌类型。
  - [ ] 检查:按名取配置/字典值后是否直接解引用?类型化取值前是否判空/判类型?
- source_status: none —— SSWCP 为 Snapmaker 专属子系统;tribal。
- evidence: commit=d583aed761; diff_line=`full_config.has("filament_type")` + `option<ConfigOptionStrings>("filament_type")->values.size()`(SSWCP.cpp:3310-3313,父提交); source=none
- confidence: mid

## commit 2710d0545b — fix: guard extruder() call in check_filament_temp_mixing (#547)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-type-safety(缺键访问,同 #546 家族不同检查点:存在性 vs 类型)
- Signal: gap(缺 key 存在性检查,EN: missing-key-access)
- Scenario: 混合耗材温度校验 + 崩溃修复 + 当时在审 extruder 键缺失
- Observation: `model_object->config.extruder()` 展开为 `dynamic_cast<const ConfigOptionInt*>(option("extruder"))->value`(Config.hpp:2346 实测)——键缺失时 `option()` 返回 nullptr,空指针解引用。修复加 `!has("extruder") ||` 前置。证据:`src/slic3r/GUI/Plater.cpp:20795`(父提交);diff 引文:
  ```
  -if (model_object->config.extruder() == 0)
  +if (!model_object->config.has("extruder") || model_object->config.extruder() == 0)
  ```
- root_pattern: 便捷访问器(`opt_int`/`extruder()` 等)内部不查键存在性;调用前必须确认键在(或访问器本身有默认值语义)。
  - [ ] 检查:便捷类型访问器调用处,其键是否保证存在?访问器本身是否对缺键有定义行为?
- source_status: none —— check_filament_temp_mixing 为 Snapmaker 新增路径;tribal。
- evidence: commit=2710d0545b; diff_line=`model_object->config.extruder() == 0` 前加 `has("extruder")`(Plater.cpp:20795,父提交); source=none
- confidence: high

## commit a3a2ffb397 — fix: prevent OOM crash on large 3MF files with runtime memory guard (#642)
- verdict: **finding**
### finding
- kind: pitfall
- target: common-input-validation("Max file size enforced" 同族:大输入无资源上限)
- Signal: gap(大输入无资源上限/内存守卫,EN: unbounded-input-memory)
- Scenario: 大 3MF 切片 + 防御式修复 + 当时在审 OOM 崩溃
- Observation: 大 3MF 输入处理无内存上限,切片过程中可用内存耗尽 → OOM 崩溃;修复新增运行时内存守卫(PrintBase.hpp 增 `MEM_GUARD_THRESHOLD` 512MB + `throw_if_canceled()` 内回调检查)。证据:`src/libslic3r/PrintBase.hpp:491-506`;diff 引文:
  ```
  +static constexpr size_t MEM_GUARD_THRESHOLD = 512ULL * 1024 * 1024; // 512 MB
  ```
- root_pattern: 接受外部大输入的处理路径需要资源上限或运行期止损点;"崩在 OOM"说明上限缺失而非实现瑕疵。
  - [ ] 检查:接受外部文件/流/网络输入的路径是否设定了大小上限或资源守卫?
- source_status: none —— 内存守卫为 Snapmaker 新增功能;tribal。
- evidence: commit=a3a2ffb397; diff_line=`MEM_GUARD_THRESHOLD = 512ULL * 1024 * 1024` + throw_if_canceled 内守卫; source=none
- confidence: mid

## commit 1e20a8d472 — fix bug which cause by wipe_tower_tatal commit (#493)
- verdict: **finding**
### finding
- kind: pitfall
- target: common-fix-verification("Fix touches adjacent behavior → run targeted non-regression checks")
- Signal: under-coverage(功能提交的相邻行为未回归验证,EN: adjacent-behavior-regression)
- Scenario: wipe_tower_total 功能提交 + 后续修复 + 当时在审"功能提交带出的两个回归"
- Observation: 前序 wipe_tower_total 提交引入两处相邻回归:①G-code 发射顺序把 `unretract()` 移到 `travel_to_z()` 之前(G-code.cpp:780-785 父提交),回抽发生在 Z 恢复前;②`wipe_tower_filament` 进入 config diff 计算 → 换板误触发重切片(PrintApply.cpp:239-243)。修复:unretract 移回;diff 计算显式跳过该自动管理键。diff 引文:
  ```
  -deretraction_str += gcodegen.unretract();
   deretraction_str += gcodegen.writer().travel_to_z(z, "Force restore layer Z", true);
  ```
- root_pattern: 功能提交若触碰语句顺序/配置 diff 语义等"相邻行为",必须在同一变更内验证相邻路径;事后由后续 commit 追认回归 = 相邻行为未被纳入回归面。
  - [ ] 检查:本提交是否调整了语句执行顺序或配置 diff/序列化语义?相邻消费路径(生成器/重切片触发器)是否验证过?
- source_status: none —— 内部回归;tribal。
- evidence: commit=1e20a8d472; diff_line=`unretract()` 移至 `travel_to_z` 之后(G-code.cpp:780-785)+ `wipe_tower_filament` diff 跳过(PrintApply.cpp:239-243); source=none
- confidence: mid

## commit 4143994c91 — revert wiep tower filament (#501)
- verdict: **cannot-reconstruct** —— 整体回滚 prime_multi_material 自动选择特性,回滚原因与触发缺陷不在 message/diff 中;夹带的 `std::min(x - e_done, remaining)` 钳制其目标机制无法从 diff 单独还原。

## commit fcdd0dd387 — revert filament&extruder
- verdict: **cannot-reconstruct** —— 无说明的大规模实验回滚(单 commit 5418 行 G-code.cpp 回退),"当初的错误"无 message/diff 证据。

## commit a9823f19ea — Fix wrong warning info & revert exceeding boundary (#141)
- verdict: **cannot-reconstruct** —— "exceeding boundary" 特性整体回滚(3DScene.cpp ±946 行),回滚原因未陈述。

## commit b8bf1a8fe1 — Revert "Feature boundary test lxy (#128)"
- verdict: **not-a-pitfall** —— 测试特性(BoundaryValidator + 文档)整体回滚的纯决策记录,无缺陷机制主张。

---

# 批 2(32 条,预筛池补齐)

## commit 7eb46ececd — fix: avoid boost::any_cast type mismatch crash in extruders_count sync (#542)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-type-safety(any 载荷类型假设)
- Signal: misleading(事件载荷类型硬编码为 int,EN: any-payload-type-assumption)
- Scenario: Tab 值变更事件 + 崩溃修复 + 当时在审 extruders_count 同步
- Observation: `boost::any_cast<int>(value)` 把事件载荷硬编码为 int;触发路径实际载荷类型与之不符时抛 `bad_any_cast` → 未捕获崩溃。修复改为从 `nozzle_diameter` 配置值推演数量,彻底移除 any_cast。证据:`src/slic3r/GUI/Tab.cpp:1843`(父提交);diff 引文:
  ```
  -auto num_extruder = static_cast<size_t>(boost::any_cast<int>(value));
  +size_t num_extruder = (nozzle_diameter != nullptr) ? nozzle_diameter->values.size() : 0;
  ```
- root_pattern: 对事件/变体载荷做 `any_cast<T>` 前必须知道 T 与触发路径的契约;载荷类型会随来源变化时,改走类型化配置源。
  - [ ] 检查:any/变体载荷的 `any_cast` 类型是否与所有触发路径的写入类型一致?
- source_status: none —— Snapmaker 专属事件链;tribal。
- evidence: commit=7eb46ececd; diff_line=`boost::any_cast<int>(value)`(Tab.cpp:1843,父提交); source=none
- confidence: mid

## commit 773b2841a3 — fix: NetworkTestDialog thread-safety crash (#544)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-thread-safety(跨线程 GUI 更新未 marshal)
- Signal: gap(非主线程直接碰 GUI + 关闭检查在副作用之后,EN: gui-thread-marshaling)
- Scenario: 多线程网络测试对话框 + 崩溃修复 + 当时在审后台线程更新 UI
- Observation: `update_status()` 由工作线程调用,wxQueueEvent/UI 更新未经主线程 marshal;且 `if (m_closing.load()) return;` 写在 wxQueueEvent 副作用**之后**,关闭检查形同虚设。修复:非主线程经 `CallAfter` 转主线程;`m_closing` 检查前置。证据:`src/slic3r/GUI/NetworkTestDialog.cpp:1154-1172`;diff 引文:
  ```
  +	if (!wxThread::IsMain()) {
  +		wxGetApp().CallAfter([weak_this = weak_this, job_id, info]() {
  ```
- root_pattern: GUI 更新必须 marshal 到主线程(wxGetApp().CallAfter);防御性状态检查必须放在副作用之前才有效。
  - [ ] 检查:可从工作线程触达的 UI 更新路径是否 marshal 到主线程?防御检查是否位于副作用之前?
- source_status: none —— Snapmaker 专属对话框;tribal。
- evidence: commit=773b2841a3; diff_line=`wxGetApp().CallAfter(...)` + `m_closing.load()` 前置(NetworkTestDialog.cpp:1154-1172); source=none
- confidence: high

## commit 24593a3b77 — fix: prevent NULL FILE* crash when loading missing G-code (#648)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-undefined-behavior(空指针解引用防护)
- Signal: gap(fopen 失败未检查即用,EN: unchecked-fopen)
- Scenario: G-code 解析入口 + 崩溃修复 + 当时在审缺失文件路径
- Observation: `FilePtr in{boost::nowide::fopen(...)}` 后未检查 `in.f == nullptr` 即调用 `::fread(buffer.data(), 1, ..., NULL)` —— CRT invalid-parameter 崩溃(Windows)/UB(其他平台)。修复:打开失败记录日志并返回 false。证据:`src/libslic3r/GCodeReader.cpp:126-129`(父提交);diff 引文:
  ```
  +    if (in.f == nullptr) {
  +        BOOST_LOG_TRIVIAL(error) << "GCodeReader::parse_file_raw_internal: "
  +                                 << "failed to open file '" << filename << "'";
  +        return false;
  ```
- root_pattern: 系统调用/文件打开失败的 NULL 返回必须立即检查;把可能为 NULL 的 FILE*/句柄传给下游 API = 崩溃定时炸弹。
  - [ ] 检查:fopen/OpenFile 等调用的返回值是否在传给下游 API 前检查?
- source_status: none —— Snapmaker 修复点;坑本身为通用错误处理;tribal。
- evidence: commit=24593a3b77; diff_line=`if (in.f == nullptr) { ... return false; }`(GCodeReader.cpp:126-129); source=none
- confidence: high

## commit 2144e1f41f — Fix bed temperature to max over all used filaments (#699)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(混合打印温度逻辑;无 harness 覆盖)
- Signal: misleading(单一值未聚合所有使用对象,EN: single-value-not-max)
- Scenario: 混合打印 G-code 导出 + 修复 + 当时在审首层床温偏低于其他耗材
- Observation: `bed_temperature_initial_layer_single` 及 `first_layer_bed_temperature` 只取 initial_extruder 的床温;混合打印时其他耗材需要更高床温,床被加热不足 → 首层粘附失败。修复:max 遍历 `print.extruders()` 全部使用挤出机。证据:`src/libslic3r/GCode.cpp:2304`(父提交);diff 引文:
  ```
  -int first_layer_bed_temperature = get_bed_temperature(0, true, print.config().curr_bed_type);
  +int first_layer_bed_temperature = get_bed_temperature_max(print, true);
  ```
- root_pattern: 从"单一初始挤出机"推导影响全打印的物理量(床温/腔温)时,必须聚合所有使用中的对象;单值取首项是混合打印的经典错误。
  - [ ] 检查:影响全局的物理量(床温/腔温/时间)取值是否只来自初始/首个对象,而非所有使用对象的最大/聚合值?
- source_status: none —— 混合打印路径为 Snapmaker 扩展;tribal。
- evidence: commit=2144e1f41f; diff_line=`get_bed_temperature(0, true, ...)` → `get_bed_temperature_max(print, true)`(GCode.cpp:2304); source=none
- confidence: high

## commit 7cd680da41 — fix: resolve app freeze and optimize texture compression (#498)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(GL 纹理 API 契约;无 harness 覆盖)
- Signal: misleading(压缩纹理声明与数据实际格式不符,EN: compressed-format-data-mismatch)
- Scenario: 文本纹理生成 + 修复 + 当时在审渲染卡死/纹理错乱
- Observation: `glTexImage2D(..., GL_COMPRESSED_RGBA_S3TC_DXT5_EXT, ..., data.data())` 把**未压缩 RGBA** 数据按 DXT5 压缩格式上传——内部格式声明与实际数据格式不符,GL 按 16 字节/4×4 块解释原始像素 → 纹理内容错乱/驱动异常。修复:先 `rygCompress` 压缩,再走 `glCompressedTexImage2D` 上传。同 commit 还修复 WebPresetDialog 分离线程捕获 `this` 且无终止信号的 UAF(detach + 析构不 join)。证据:`src/slic3r/GUI/GLTexture.cpp:537-552`;diff 引文:
  ```
  +rygCompress(compressed.data(), data.data(), m_width, m_height, 1, compressed_size);
  +glsafe(::glCompressedTexImage2D(GL_TEXTURE_2D, 0, GL_COMPRESSED_RGBA_S3TC_DXT5_EXT, ...
  ```
- root_pattern: GL 压缩纹理必须用 glCompressedTexImage2D 上传压缩数据;glTexImage2D 配压缩 internalformat 传原始数据 = 契约违反,不报错但输出未定义。
  - [ ] 检查:GL 纹理上传的内部格式与数据实际编码是否一致?压缩格式是否走了 glCompressedTexImage2D?
- source_status: none —— Snapmaker 专属纹理路径;tribal。
- evidence: commit=7cd680da41; diff_line=`GL_COMPRESSED_RGBA_S3TC_DXT5_EXT` + `data.data()`(GLTexture.cpp:537,父提交); source=none
- confidence: mid

## commit 09c82be4ea — fix: enable XML_LARGE_SIZE in expat to support 3MF >2GB (#590)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-integer-safety(size/index 类型宽度不足)
- Signal: gap(第三方库默认 32 位 size,大输入溢出,EN: library-size-width)
- Scenario: expat 依赖构建配置 + 修复 + 当时在审 >2GB 3MF 解析失败
- Observation: expat 默认 `XML_Size`/`XML_Index` 为 32 位,>2GB 3MF 解析时内部大小/索引溢出 → 解析失败或损坏;且顶层 CMakeLists 曾以手写静态库方式旁路 deps_src/expat,绕过了带 XML_LARGE_SIZE 的 target。修复:`target_compile_definitions(expat PUBLIC XML_LARGE_SIZE)` 并收敛构建入口。证据:`deps/EXPAT/expat/CMakeLists.txt:76-79`;diff 引文:
  ```
  +target_compile_definitions(expat PUBLIC XML_LARGE_SIZE)
  ```
- root_pattern: 处理可能超过 2GB 输入的库,必须显式启用 64 位 size 配置;旁路依赖构建入口会连配置一起旁路掉。
  - [ ] 检查:处理大文件/大数据的第三方库,其 size/index 类型宽度配置(如 XML_LARGE_SIZE、LFS)是否启用?是否有旁路构建入口遗漏该配置?
- source_status: none —— 构建配置为 fork 内修复;expat 官方文档不在白名单内;tribal+version-fragile。
- evidence: commit=09c82be4ea; diff_line=`target_compile_definitions(expat PUBLIC XML_LARGE_SIZE)`(deps/EXPAT/expat/CMakeLists.txt:76); source=none
- confidence: mid

## commit 72dddfead3 — fix mqtt connect fail bug (#508)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(位域 ABI 与协议布局;无 harness 覆盖)
- Signal: misleading(_Bool 位域打包与协议不符,EN: bool-bitfield-abi)
- Scenario: 内置 paho-mqtt-c 客户端 + 修复 + 当时在审 MQTT 连接失败
- Observation: vendored paho-mqtt-c 的 MQTT 固定头位域用 `bool dup : 1`/`bool retain : 1`;`_Bool` 位域在部分编译器/ABI 下按 8 位单元打包,与线协议逐位布局不符 → 连接报文头损坏 → 连不上。修复:`typedef unsigned int bit` 并替换位域类型(修复注释自引上游 issue)。证据:`src/mqtt/externals/paho-mqtt-c/src/MQTTPacket.h:28-37`;diff 引文:
  ```
  +typedef unsigned int bit;
  ...
  -	bool dup : 1;
  +	bit dup : 1;
  ```
- root_pattern: 线协议/序列化结构体的位域必须使用与 ABI 预期一致的整数类型,禁止 `_Bool`;vendored 库本地补丁要记录上游 issue 链接以便同步。
  - [ ] 检查:协议/序列化结构体的位域是否用了 _Bool 或非预期类型?vendored 库补丁是否记录上游 issue?
- source_status: none + lead —— 修复注释引用 eclipse-paho/paho.mqtt.c#1576(白名单外,仅线索);tribal。
- evidence: commit=72dddfead3; diff_line=`typedef unsigned int bit;` + `bit dup : 1`(MQTTPacket.h:31-72); source=none(lead: https://github.com/eclipse-paho/paho.mqtt.c/issues/1576)
- confidence: high

## commit ca5a26da2c — fix(sentry): disable pc_name tag reporting for privacy (#709)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(遥测数据最小化;无 harness 覆盖)
- Signal: misleading(上报默认携带个人数据,EN: pii-in-telemetry)
- Scenario: Sentry 崩溃上报 + 修复 + 当时在审隐私合规
- Observation: 崩溃上报默认附带 `pc_name` 标签(机器名属个人数据),无最小化评审即上线;修复将其注释停用(两处:initSentryEx 与 sentryReportLogEx)。证据:`src/sentry_wrapper/SentryWrapper.cpp:314-320`;diff 引文:
  ```
  +// PC name is personal data; intentionally disabled for privacy.
  +// std::string pcName = common::get_pc_name();
  ```
- root_pattern: 遥测/崩溃上报字段应默认最小化;上报个人数据(机器名/用户名/路径)前必须显式决策,而非"顺手带上"。
  - [ ] 检查:遥测/崩溃上报字段是否包含可识别个人数据(pc_name/用户名/全路径)?是否经过最小化评审?
- source_status: none —— Snapmaker 专属 Sentry 配置;tribal。
- evidence: commit=ca5a26da2c; diff_line=`sentry_set_tag("pc_name", pcName.c_str())` 注释停用(SentryWrapper.cpp:317-319); source=none
- confidence: high

## commit e60059ac74 — fix: preserve Match-mode state when switching modes (#602)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(UI 状态机)
- Signal: misleading(状态被重复初始化覆盖,EN: state-reinit-overwrite)
- Scenario: 混色对话框模式切换 + 修复 + 当时在审 Match 模式调整丢失
- Observation: 同会话内再进 Match 模式时,`on_mode_changed` 无条件从 `m_result` 重新初始化匹配三元组/权重 → 用户本次会话的调整被 2:1:1 默认值覆盖。修复:首次进入才初始化,同会话重入仅重建图例(`m_match_state_persisted`)。证据:`src/slic3r/GUI/MixedFilamentDialog.cpp:2929-2935`;diff 引文:
  ```
  +if (m_match_state_persisted) {
  +    rebuild_match_legend();
  +} else {
  ```
- root_pattern: "初始化/回填"逻辑必须区分首次进入与重入;把持久状态当一次性初始化源 = 覆盖用户调整。
  - [ ] 检查:模式切换/重入路径是否会重新执行初始化,覆盖同一会话中已存在的用户状态?
- source_status: none —— Snapmaker 专属对话框;tribal。
- evidence: commit=e60059ac74; diff_line=`m_match_state_persisted` 分支(MixedFilamentDialog.cpp:2932-2948); source=none
- confidence: high

## commit da278db86c — Fix sentry bug 347 (#591) (#608)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-stl-containers(容器插入结果未检查;条目族"容器修改与失效"相邻)
- Signal: gap(emplace 结果未检查 + 索引复用,EN: unchecked-emplace)
- Scenario: 反序列化重建打印板 + 崩溃修复 + 当时在审 print/gcode 映射错位
- Observation: 反序列化时用递增 `m_print_index` 作键插入 `m_print_list`/`m_gcode_result_list`;索引已被占用时 `emplace` 静默失败,新分配的 Print/GCodeResult 泄漏,且板被绑定到**旧映射对象** → 后续访问错位崩溃。修复:while 找未用索引 + 检查 emplace 返回值 + 失败清理。证据:`src/slic3r/GUI/PartPlate.cpp:5282-5298`;diff 引文:
  ```
  +while (m_print_list.count(m_print_index) > 0 || m_gcode_result_list.count(m_print_index) > 0)
  +{
  +    ++m_print_index;
  +}
  ```
- root_pattern: 以自增计数作 map 键时,插入结果必须检查(键冲突会静默失败并泄漏);新对象与映射集合必须原子一致。
  - [ ] 检查:map/set 插入返回值是否检查?自增键是否可能已被占用?失败路径是否清理已分配对象?
- source_status: none —— Snapmaker 专属打印板逻辑;tribal。
- evidence: commit=da278db86c; diff_line=`while (m_print_list.count(m_print_index) > 0 ...)` + `if (!print_result.second || !gcode_result.second)`(PartPlate.cpp:5285-5296); source=none
- confidence: high

## commit 90dce10786 — Fix filament sync color matching logic (#601)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(色彩科学度量;无 harness 覆盖)
- Signal: misleading(感知不准确的色差公式,EN: non-perceptual-color-metric)
- Scenario: 耗材颜色匹配算法 + 修复 + 当时在审颜色匹配错配
- Observation: 色差用 CIE76(Lab 空间欧氏距离),感知均匀性差 → 相近颜色匹配错乱;修复换 CIEDE2000(`DeltaE00`)并调整匹配策略(同类型优先 + 全量兜底)。证据:`src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.cpp:81-90`;diff 引文:
  ```
  -float delta_e_cie76(...) { ... return std::sqrt(dL * dL + da * da + db * db); }
  +float delta_e_ciede2000(...) { ... return DeltaE00(L1, a1, b1v, L2, a2, b2v); }
  ```
- root_pattern: 感知类度量(色差/相似度)必须使用感知均匀的公式(CIEDE2000 等);CIE76 欧氏距离在低饱和/近色区失真。
  - [ ] 检查:颜色/感知相似度计算是否使用了感知均匀度量(CIEDE2000),而非 CIE76 欧氏距离?
- source_status: none —— Snapmaker 专属算法;CIEDE2000 标准文献不在白名单;tribal。
- evidence: commit=90dce10786; diff_line=`delta_e_cie76` → `delta_e_ciede2000`(FilamentSyncAlgorithm.cpp:81-90); source=none
- confidence: mid

## commit a9ca118bd6 — fix: prevent crashes during GLCanvas3D destruction (#486)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-raii(析构路径外部副作用)
- Signal: gap(析构路径调用带外部副作用的重置函数,EN: dtor-external-side-effects)
- Scenario: GLCanvas3D 析构/删板崩溃 + 修复 + 当时在审析构期间访问 plater/通知管理器
- Observation: `~GLCanvas3D()` 调 `reset_volumes()`,其内部访问 `wxGetApp().plater()` 的通知管理器并派发选择通知——析构期间外部 GUI 子系统可能已销毁 → 崩溃(#467/#475)。修复:析构模式跳过通知/选择副作用。证据:`src/slic3r/GUI/GLCanvas3D.cpp:1203-1210`;diff 引文:
  ```
  -    reset_volumes();
  +    reset_volumes(ResetVolumesMode::CanvasDestruction);
  ```
- root_pattern: 析构路径调用的清理函数不得触碰外部子系统(通知/焦点/事件派发);销毁模式必须与正常模式分离。
  - [ ] 检查:析构/清理路径调用的函数是否带外部副作用(通知管理器/事件派发/焦点)?销毁模式下是否跳过?
- source_status: none —— Snapmaker 专属崩溃族;上游无同款;tribal。
- evidence: commit=a9ca118bd6; diff_line=`reset_volumes(ResetVolumesMode::CanvasDestruction)`(GLCanvas3D.cpp:1206); source=none
- confidence: high

## commit 41bb403500 — fix: add notify_sidebar parameter to Selection::clear() (#492)
- verdict: **duplicate**(duplicate-of: a9ca118bd6)
- 理由:同一坑位(GLCanvas3D 析构路径的外部副作用)、同一检查点(清理函数派发侧栏/通知副作用);#486 修 reset_volumes 层、#492 修其下游 Selection::clear→handle_sidebar_focus_event 层,同崩溃族(#467/#475)的互补层次。

## commit 2fd734b3a2 — Fix low-resolution screen controls on Mac (#582)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-wxwidgets-3-1-5(DIP/物理像素转换,本项目 P 级 harness 有对应检查点:"Mouse coordinates: convert logical to physical" / "Test on Retina")
- Signal: misleading(布局用位图物理尺寸/手除 DPI 缩放,EN: dip-vs-physical)
- Scenario: Retina 下控件布局与命中测试 + 修复 + 当时在审低分屏控件错位
- Observation: 两处 DIP 误用:①下拉箭头布局用 `arrowBmp.GetWidth()/GetHeight()`(Retina 下位图为 2× 物理尺寸)定位 → 箭头错位;②命中测试 `evt.GetY() / GetDPIScaleFactor()` 整数除法(scale=2 时奇数像素截断)→ 行命中偏移。修复:布局改用 `FromDIP` 尺寸、命中测试改用 `ToDIP`。证据:`src/slic3r/GUI/filamentsync/FilamentColorMapBox.cpp:259-270`、`MachineFilamentPicker.cpp:258-261`;diff 引文:
  ```
  -const int ax     = (w - arrowW) / 2;
  +const int ax = (w - arrowSz) / 2;
  ```
- root_pattern: wx 布局必须用 DIP 语义尺寸(FromDIP/ToDIP),位图物理尺寸只用于渲染;命中测试不得手除缩放因子(截断)。
  - [ ] 检查:布局/命中测试是否混用位图物理尺寸与 DIP?是否有 `GetWidth()/GetDPIScaleFactor()` 式手除?
- source_status: none —— Snapmaker 专属控件;机制为 wxWidgets DIP 语义,harness 已含检查点;tribal。
- evidence: commit=2fd734b3a2; diff_line=`arrowBmp.GetWidth()` → `FromDIP(g_arrowSize)` + `evt.GetY() / GetDPIScaleFactor()` → `ToDIP(evt.GetY())`; source=none
- confidence: high

## commit 761718a5ea — Fix: top-cover machine end gcode (#584)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(机器 profile 数据;无 harness 覆盖)
- Signal: gap(机器 gcode 模板未覆盖按对象打印序列,EN: gcode-template-coverage)
- Scenario: U1 顶盖机器 end gcode + 修复 + 当时在审按对象打印撞件
- Observation: Snapmaker U1 全 nozzle 档位的 `machine_end_gcode` 只有 `PRINT_END\nTIMELAPSE_STOP`,未处理 `print_sequence=by object`——按对象打印时喷头不回抬 Z,结束动作可能撞到已打印件;修复在 end gcode 前置条件抬 Z 段。证据:`resources/profiles/Snapmaker/machine/Snapmaker U1 (0.2 nozzle).json:38`;diff 引文:
  ```
  -"machine_end_gcode": " PRINT_END\nTIMELAPSE_STOP",
  +"machine_end_gcode": "{if print_sequence == \\\"by object\\\"}\\nG91\\nG1 X2 Y2 Z1 F24000\\nG90\\nG1 Z{max_layer_z+2} F600\\n{endif}\\nPRINT_END\\nTIMELAPSE_STOP",
  ```
- root_pattern: 机器 gcode 模板必须覆盖全部打印序列形态(by object/by layer/按对象抬 Z);模板审计比照切片器实际会发出的序列。
  - [ ] 检查:机器 start/end gcode 模板是否覆盖 print_sequence 全形态?抬 Z/避让动作是否在所有序列下都成立?
- source_status: none —— Snapmaker 专属 profile;tribal。
- evidence: commit=761718a5ea; diff_line=`machine_end_gcode` 增 by-object 抬 Z 段(Snapmaker U1 各 nozzle json:38); source=none
- confidence: mid

## commit 9490f113e5 — fix: top cover filament temp mixing - three fixes (#543)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(UI 状态同步)
- Signal: under-coverage(校验/状态变化未同步到所有消费入口,EN: state-sync-gap)
- Scenario: 温混门控/通知同步 + 修复 + 当时在审切片按钮与门控不一致
- Observation: 三处状态不同步:①切片按钮使能未检查 in-use 混合耗材不兼容(`has_incompatible_mixed_filament_in_use` 缺失)——门控存在但按钮入口漏挂;②验证失败/清空时未同步耗材温混通知(`sync_filament_temp_mixing_notification` 缺失);③加载项目后只对当前板做状态初始化,Slice All 依赖的全板状态不一致。证据:`src/slic3r/GUI/MainFrame.cpp:1915-1921`、`Plater.cpp:12326-12330`;diff 引文:
  ```
  +else if (m_plater->has_incompatible_mixed_filament_in_use())
  +{
  +    enable = false;
  +}
  ```
- root_pattern: 新增校验/门控条件时,必须枚举所有消费该状态的 UI 入口(按钮使能/通知/批量模式)并同步;漏挂入口 = 门控形同虚设。
  - [ ] 检查:校验/门控条件新增后,所有消费入口(按钮使能/通知/批量路径)是否同步挂载?
- source_status: none —— Snapmaker 专属温混逻辑;tribal。
- evidence: commit=9490f113e5; diff_line=`has_incompatible_mixed_filament_in_use()` 接入切片使能(MainFrame.cpp:1918-1920); source=none
- confidence: mid

## commit 38ef299ca7 — fix: unify filament temp mixing blocking with plate error gating (#589)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-lifetime(临时对象链悬垂;I18N.hpp:55 实锤)
- Signal: misleading(返回指向临时对象内部缓冲的指针,EN: temporary-chain-dangling)
- Scenario: i18n 工具链 + 门控统一 + 当时在审翻译字符串偶发乱码/崩溃
- Observation: `I18N::translate_utf8()` 返回 `wxGetTranslation(wxString(...)).ToUTF8().data()` 构造的 std::string——取临时 wxString 内部缓冲指针再拷贝;标准上临时对象活到完整表达式结束,但 MSVC /O2 历史上对该链误优化,缓冲提前销毁 → 读已释放内存(commit 注释自述,并点名同类 #648 崩溃)。修复:tr_u8 改为命名局部变量 + null 短路,绕开该链。注意 `translate_utf8`/`_u8L` 本体现仍存在(I18N.hpp:55),坑未根除。证据:`src/slic3r/GUI/I18N.hpp:55`(当前树实测)+ `Plater.cpp:208-240`;diff 引文:
  ```
  +// In practice, however, MSVC has historically mis-optimized such chains under
  +// /O2 (the buffer sometimes gets destroyed before the std::string reads it)
  ```
- root_pattern: `临时对象.ToUTF8().data()` 式链取内部指针构造返回值,依赖"临时对象存活到完整表达式结束"的微妙规则;优化器/编译器差异可打破——命名局部变量 + 显式拷贝是唯一稳的写法。
  - [ ] 检查:返回值是否由"临时对象链取内部指针"构造(如 `.ToUTF8().data()`、`.c_str()` 链)?是否命名局部变量保活再拷贝?
- source_status: none —— fork 内自述根因;tribal+version-fragile(换编译器/优化级别需复查)。
- evidence: commit=38ef299ca7; diff_line=tr_u8 重写注释自述 MSVC /O2 误优化机制(Plater.cpp:211-229); source=none
- confidence: mid(机制为 commit 自述;标准上属编译器差异)

## commit e46f5191b5 — fix bug 2.3.5-30 (#518)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(领域默认值约定)
- Signal: misleading(默认值破坏"0=未指定"约定,EN: default-value-convention)
- Scenario: 对象添加默认挤出机 + 修复 + 当时在审新增对象被绑定到挤出机 1
- Observation: `Model::add_object` 三处把默认 `extruder` 设为 1(1-based,注释沿自 BBS);而系统其余部分以 0 表示"未指定/默认"(如 #547 的 `extruder()==0` 判定、GUI_Factories 以 `has? value : 0` 兜底)——新对象被显式绑定挤出机 1,单挤出机机器上该 id 可能不存在 → 2.3.5-30 号缺陷。修复:默认值改 0。证据:`src/libslic3r/Model.cpp:458-462`;diff 引文:
  ```
  -new_object->config.set_key_value("extruder", new ConfigOptionInt(1));
  +new_object->config.set_key_value("extruder", new ConfigOptionInt(0));
  ```
- root_pattern: 领域 id 的"0=未指定"约定必须全系统一致;默认值写入要对照其余消费点的判定语义,而非沿用上游注释。
  - [ ] 检查:新对象/新记录的默认 id 是否与系统"未指定/默认"约定(0)一致?有无与上游遗留的 1-based 默认冲突?
- source_status: none —— fork 内修复;上游(及 BambuStudio 系)仍带 1-based 默认;tribal。
- evidence: commit=e46f5191b5; diff_line=`ConfigOptionInt(1)` → `ConfigOptionInt(0)`(Model.cpp:458-462); source=none
- confidence: mid

## commit d58709de2a — bugfix for resource update (#513)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(运行期资源替换原子性;无 harness 覆盖)
- Signal: gap(非原子目录替换,EN: non-atomic-replace)
- Scenario: 资源在线更新 + 修复 + 当时在审更新中断损坏
- Observation: 资源目录更新直接就地覆盖,更新中断/失败会留下半写状态;修复引入 `atomic_replace_directory`(拷到 .new → validate_staging → 改名就位,失败回滚 .old)。证据:`src/libslic3r/Utils.hpp:682-690`;diff 引文:
  ```
  +// Copy source tree to target + ".new", run validate_staging, then rename into place
  +bool atomic_replace_directory(...);
  ```
- root_pattern: 运行期替换正在使用的资源/配置目录必须原子(暂存+校验+改名),就地覆盖中断即损坏。
  - [ ] 检查:运行期资源/配置/数据替换是否原子?中断/失败是否有回滚路径?
- source_status: none —— Snapmaker 专属资源更新;tribal。
- evidence: commit=d58709de2a; diff_line=`atomic_replace_directory` 引入(Utils.hpp:688-692); source=none
- confidence: mid

## commit e8a518e2ce — fix: replace Cancel button style with explicit border width (#529)
- verdict: **not-a-pitfall** —— 按钮外观微调(移除 SetStyle、补 SetBorderWidth),纯样式决策,无缺陷机制可蒸馏。

## commit 0f9ae760be — fix log not support enumerate. (#525)
- verdict: **finding**
### finding
- kind: pitfall
- target: cpp-type-safety(作用域枚举无隐式转换)
- Signal: misleading(scoped enum 直接流式化,EN: scoped-enum-streaming)
- Scenario: 日志语句 + 编译修复 + 当时在审 FlutterWebCopyStatus 日志
- Observation: `BOOST_LOG_TRIVIAL(error) << ... << m_flutter_web_copy_status` —— `FlutterWebCopyStatus` 为 `enum class`(GUI_App.hpp:641 实测),作用域枚举无隐式转换、无 operator<< → 该语句任何编译器都不编译;说明此前的代码以未编译状态合入(#530 的 GUI_App.cpp:2343 同款语句同日修复)。修复:`static_cast<int>(status)`。证据:`src/slic3r/GUI/GUI_App.cpp:2318-2321` + `GUI_App.hpp:641`;diff 引文:
  ```
  -BOOST_LOG_TRIVIAL(error) << "FlutterWebCopyStatus not exit " << status;
  +BOOST_LOG_TRIVIAL(error) << "FlutterWebCopyStatus not exit " << static_cast<int>(status);
  ```
- root_pattern: `enum class` 值流式化/序列化前必须显式转换;若代码曾"编译通过",说明该行从未被编译(编译门禁缺失)。
  - [ ] 检查:scoped enum 是否被直接流式化/隐式使用?涉及日志/序列化语句的提交是否在 CI 编译面内?
- source_status: authority —— C++ 标准 [dcl.enum](scoped 枚举无隐式转换)(sources.md N1);机制与编译器无关。
- evidence: commit=0f9ae760be; diff_line=`<< status` → `<< static_cast<int>(status)`(GUI_App.cpp:2321); source=ISO/IEC 14882 [dcl.enum](N1)
- confidence: high

## commit 6a2c0715ae — Feature filament sync bugfix (#554)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(操作顺序与序列化回写)
- Signal: misleading(UI 同步先于数据修改 + 删除未回写,EN: stale-order-writeback)
- Scenario: 耗材同步对话框 + 修复 + 当时在审混合耗材删除后 UI/存档不一致
- Observation: `on_filaments_change(num_filaments)` 在混合耗材删除块**之前**执行——UI 用删除前的旧状态刷新;且删除混合耗材后未把新列表序列化回 `mixed_filament_definitions`,存档仍含已删条目。修复:on_filaments_change 移到删除块之后,并回写序列化。证据:`src/slic3r/GUI/Plater.cpp:8251-8265`;diff 引文:
  ```
  -const size_t num_filaments = effective_size;
  -wxGetApp().plater()->on_filaments_change(num_filaments);
  ...
  +if (auto* opt = preset_bundle->project_config.option<ConfigOptionString>("mixed_filament_definitions"))
  +    opt->value = preset_bundle->mixed_filaments.serialize_custom_entries();
  ```
- root_pattern: 状态变更后的 UI 通知必须发生在数据修改完成后;删除/变更集合后必须同步序列化回写,否则存档与内存不一致。
  - [ ] 检查:UI 通知/刷新是否位于数据修改之后?集合变更后是否有序列化回写?
- source_status: none —— Snapmaker 专属同步流;tribal。
- evidence: commit=6a2c0715ae; diff_line=`on_filaments_change` 移后 + `serialize_custom_entries()` 回写(Plater.cpp:8251-8265); source=none
- confidence: mid

## commit db8875be08 — Feature filament sync bugfix (#541)
- verdict: **cannot-reconstruct** —— 移除 TPU 名称拼接特殊分支(95A HF),改为通用分支;但"特殊分支为何错误、与设备侧命名如何失配"在 message/diff 中无证据,机制不可还原。

## commit 63d7d8dbea — fix: v233 feedback bugfixes - fuzzy skin, infill filament, toolpath routing (#449)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(序列化格式向后兼容;无 harness 覆盖)
- Signal: misleading(3MF 属性改名无旧键回退读取,EN: format-key-rename-compat)
- Scenario: 3MF 模糊皮肤读写 + 修复 + 当时在审旧文件模糊皮肤数据丢失
- Observation: 模糊皮肤 3MF 属性由 `paint_fuzzy` 改名 `paint_fuzzy_skin` 后,读取端只认新键——旧版本保存的文件该数据静默丢失。修复:读取改 `{CUSTOM_FUZZY_SKIN_ATTR, CUSTOM_FUZZY_SKIN_ATTR_OLD}` 键组回退。证据:`src/libslic3r/Format/bbs_3mf.cpp:275-278`、`3666-3673`;diff 引文:
  ```
  +static constexpr const char* CUSTOM_FUZZY_SKIN_ATTR_OLD  = "paint_fuzzy";
  ...
  -...bbs_get_attribute_value_string(attributes, num_attributes, CUSTOM_FUZZY_SKIN_ATTR));
  +...bbs_get_attribute_value_string(attributes, num_attributes, {CUSTOM_FUZZY_SKIN_ATTR, CUSTOM_FUZZY_SKIN_ATTR_OLD}));
  ```
- root_pattern: 已发布序列化格式的键改名必须保留旧键回退读取(读新优先、旧兜底);否则旧存档静默丢数据。
  - [ ] 检查:序列化键改名是否带旧键回退?旧版本存档在本版本下是否仍可完整读取?
- source_status: none —— fork 内修复;tribal。
- evidence: commit=63d7d8dbea; diff_line=`CUSTOM_FUZZY_SKIN_ATTR_OLD = "paint_fuzzy"` 键组回退(bbs_3mf.cpp:278,3669); source=none
- confidence: high

## commit d508b03466 — fix: first-layer honeycomb sparse infill alignment (#457)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(切片/填充几何逻辑)
- Signal: misleading(首层线宽误入内部填充间距,EN: first-layer-width-leak)
- Scenario: 稀疏填充跨层对齐 + 修复 + 当时在审首层蜂窝错位
- Observation: `layerm.flow(frInfill, layer_height)` 在第 0 层自动套用首层线宽(`m_layer->id() == 0` 分支),内部填充**间距**随之偏离其余层 → 首层稀疏填充与其他层错位。修复:flow 增加 `use_initial_layer_width=false` 参数,间距计算不走首层宽度。证据:`src/libslic3r/Fill/Fill.cpp:938-945`;diff 引文:
  ```
  -params.spacing = layerm.flow(frInfill, layer.object()->config().layer_height).spacing();
  +params.spacing = layerm.flow(frInfill, layer.object()->config().layer_height, false).spacing();
  ```
- root_pattern: "首层线宽"这类只影响单层的参数,不得泄漏进需要跨层一致的几何量(填充间距/对齐)计算。
  - [ ] 检查:跨层一致性的几何量计算是否被仅首层生效的参数(线宽/宽度)污染?
- source_status: none —— FS 系作者提交;tribal。
- evidence: commit=d508b03466; diff_line=`flow(frInfill, layer_height)` → `flow(frInfill, layer_height, false)`(Fill.cpp:941); source=none
- confidence: high

## commit 5cc838b33a — add wipe tower feature and fix wipe tower bug (#446)
- verdict: **cannot-reconstruct** —— 特性+修复混提(WipeTower2.cpp ±389 行),"fix wipe tower bug"的缺陷机制无法从混合 diff 中隔离。

## commit 5c784f04c7 — chore: downgrade WebSocket debug log levels (#670)
- verdict: **not-a-pitfall** —— 日志级别下调的 chore,无缺陷机制。

## commit fb7ed51dc2 — Fix the compilation error. (#539)
- verdict: **cannot-reconstruct** —— `*wxWHITE : *wxBLACK` → `wxColour(...)` 的编译修复;具体编译器诊断与机制无法从单 hunk 还原(与 #675866c502/#530 同属"三元操作数形态"族但形态不同,不并案)。

## commit 4d77d7f657 — fix linux build fail (#540)
- verdict: **duplicate**(duplicate-of: 74c01ad75f)
- 理由:同一坑位、同一检查点——MachineFilamentPicker.hpp 使用 wxPanel 未包含 `<wx/panel.h>`,靠传递包含在 MSVC 下通过、Linux/GCC 断裂;修复同为补显式 include,与 #739/#712 同族。

## commit a4c7f48992 — fix mac build fail questions (#530)
- verdict: **duplicate**(duplicate-of: 675866c502)
- 理由:同一坑位、同一检查点——FilamentColorDialog.cpp:726 `_selectedSku.empty() ? wxEmptyString : FromStdString("sku " + _selectedSku)` 的 wxEmptyString-三元形态,与 #675866c502 同形修复(包成 `wxString(wxEmptyString)`);其第二 hunk(enum class 日志流式化)与 #525 同族,已在 #525 条记录。双实例使 #675866c502 升级为 finding。

## commit b63ab9afb9 — feature fix mac web interrupted question. (#679)
- verdict: **finding**
### finding
- kind: pitfall
- target: orphan(一次性状态标志失忆)
- Signal: misleading(一次性标志未随重入事件复位,EN: one-shot-flag-staleness)
- Scenario: 打印机 WebView 注入 API key + 修复 + 当时在审 Reload 后页面无鉴权
- Observation: `m_apikey_sent` 一次性标志置位后永不复位——context-menu Reload 等重新加载触发 `SendAPIKey` 直接 return,页面不再注入 X-API-Key → 请求无鉴权被中断。修复:去掉一次性标志,每次 document load 重注入,JS 侧幂等标记防堆叠。证据:`src/slic3r/GUI/PrinterWebView.cpp:125-132`;diff 引文:
  ```
  -if (m_apikey_sent || m_apikey.IsEmpty())
  +if (m_apikey.IsEmpty())
  ```
- root_pattern: 一次性状态标志(m_xxx_sent/done)必须审视其重入事件(Reload/重载/重连)是否要求复位;用幂等操作替代"只做一次"。
  - [ ] 检查:一次性标志在重入事件(Reload/重连/重建)下是否需要复位?"只做一次"是否有幂等替代方案?
- source_status: none —— Snapmaker 专属 WebView;tribal。
- evidence: commit=b63ab9afb9; diff_line=`m_apikey_sent` 移除,重注入 + JS 幂等标记(PrinterWebView.cpp:127-131); source=none
- confidence: high

## commit e464184157 — feat: top cover detection and related fixes (#521)
- verdict: **cannot-reconstruct** —— feat+fix 混合提交(顶盖检测特性 + 相关修复),缺陷机制无法与特性 diff 隔离。

---

## summary(全量)
输入 57(revert/workaround/hotfix/fix 预筛池,release_2_3_7 主线 Snapmaker 团队 commit)
→ finding 43(批 1:20,批 2:23)/ duplicate 4(#712→#739,#492→#486,#540→#739,#530→#675866c502)/ cannot-reconstruct 7(#501,#fcdd0dd387,#141,#541,#446,#539,#521)/ not-a-pitfall 3(#b8bf1a8fe1,#529,#670)

## discarded
- none(所有已审条目均获 verdict;cannot-reconstruct 7 条按规则保留 verdict 而非静默丢弃)

## notes(喂给 harness-evolution / projects/snapmaker-orca)
1. **高频坑类:空容器算术与边界守卫**——#750×2、#740、#642、#754、#752 等 ≥5 commit 同根("size 参与算术/索引前无空与边界守卫")。cpp-integer-safety 已有 unsigned-wrap/divisor==0 条目,建议聚合为"容器 size 参与算术/索引前的空守卫"检查点;cpp-undefined-behavior 的 index-bounds 条目在本批命中 2 次。
2. **跨平台构建断裂反复出现(≥8 起)**:#712/#739/#540(缺 include)、#675866c502/#530(三元 wxEmptyString)、#539、#525/#530 第二 hunk(enum class 流式化)、#738(语法错误)、#735 遗留——根因是 MSVC-only 开发 + 无平台矩阵编译门禁。建议 snapmaker-orca-workflow 加"合入前 Linux/Flatpak(GCC/Clang)编译门禁"或平台矩阵 CI(P 级);cpp-build-system 已有 include 卫生条目,但"未编译即合入"是流程缺口。
3. **fix-of-fix 族(≥4 起)**:#735→#738、wipe_tower_total→#493、#525/#530 的未编译合入——common-fix-verification 有 adjacent-behavior 条目,建议加"修复/大改动提交必须过编译与相邻路径回归"检查点。
4. **fork 与上游修复不同步(3 起)**:#752 上游 2026-04 已修、#750(DailyTips)上游 2025-08 已修,分支 2026-08 才自修;#754/#757/#753/#732/#750(HintNotification)上游至今未修。建议 projects/snapmaker-orca/workflow 增加"定期同步上游 fix 清单"约定。
5. **orphan 占比高(24/43)**:UI 状态机(#732/#602/#543/#554/#679)、契约假设(#741/#758)、渲染几何(#765/#756/#498/#457)、切片不变量(#757/#699/#584/#518)、序列化兼容(#449/#513)、色彩度量(#601)、位域 ABI(#508)、遥测 PII(#709)、GL API(#498)——taxonomy 缺"UI 状态机/契约假设/领域不变量/序列化兼容"类 harness;本批为候选语料。
6. **wxWidgets 坑聚类(4 起,均归 P 级 harness)**:#582(DIP/物理像素)、#675866c502/#530(wxEmptyString-三元)、#739/#712/#540(缺 wx include)。`cpp-wxwidgets-3-1-5` harness 已有 DPI 检查点,建议增补"wxEmptyString 与临时 wxString 三元混用"条目(3 实例,含独立复现)。
7. **版本钉执行**:wxWidgets=3.1.5 约束下无版本不符引用;上游检索均按 2026-08 上游 main 核对;RFC 3986(URL 解析)与 ISO C++ [dcl.enum](scoped enum)两处 authority 引用满足白名单约束。
