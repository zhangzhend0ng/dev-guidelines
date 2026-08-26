---

type: harness

id: "cpp-wxwidgets-3-1-5"

title: "wxWidgets 3.1.5 Pitfalls, Limitations, and Best Practices Checklist"

language: "cpp"

category: "third-party"

tier: "P"

scope: "Avoid known pitfalls and limitations when using wxWidgets 3.1.5 across wxMSW, wxGTK, and wxOSX ports"

version: "2026.08"

status: "draft"

stable_since: ""

last_validated: "2026-08-26"

review_cycle: "12m"

tags: [wxwidgets, gui, cross-platform, wxmsw, wxgtk, wxosx, third-party]

based_on:

  - "[P] wxWidgets 3.1.5 docs/changes.txt — Incompatible Changes and Release Notes (2021-04-14)"

  - "[P] wxWidgets GitHub Issues milestone 3.1.5 (#36 closed PRs/issues)"

  - "[P] wxWidgets GitHub Issues — wxGLCanvas EGL/Wayland (#26248, #26250, #26340, #26410)"

  - "[P] wxWidgets GitHub Issues — wxDataViewCtrl crashes (#18057, #18167, #18337, #24148, #24382)"

  - "[P] wxWidgets GitHub Issue #21105 — wxGTK wxPostEvent + threads"

  - "[P] wxWidgets GitHub Issue #26490 — wxPropertyGrid DPI regression"

  - "[P] wxWidgets Discussion Forum — Wayland wxGLCanvas EGL backend problems (t=49312)"

  - "[P] Stack Overflow wxwidgets tag — high-vote common pitfalls"

  - "[P] wxWidgets GitHub Issues — wxOSX macOS platform pitfalls (menu bar, App Nap, file association, Retina, pasteboard, sheets, status item)"

  - "[P] wxWidgets 3.1.5 docs — overviews (sizer.h, roughguide.h, customwidgets.h, exceptions.h, html.h)"

  - "[P] wxWidgets 3.1.5 docs/doxygen/overviews/string.h, cmake.h, unicode.h — cross-platform UI/UX best practices"

  - "[P] wxWidgets 3.1.5 interface/wx/string.h — utf8_str/ToUTF8/mb_str/wc_str buffer lifetime documentation"

  - "[P] wxWidgets 3.1.5 interface/wx/window.h — Freeze/Thaw/wxWindowUpdateLocker documentation"

  - "[P] wxWidgets 3.1.5 docs/doxygen/overviews/customwidgets.h — custom widget creation patterns"

  - "[P] wxWidgets 3.1.5 interface/wx/popupwin.h — wxPopupTransientWindow lifecycle"

  - "[P] wxWidgets GitHub Issues — wxWebView Edge backend (#19814, #16862, #21455)"

  - "[P] wxWidgets 3.1.5 docs/doxygen/classwx_display.h — wxDisplay::GetPPI(), GetScaleFactor(), and GetDPIScaleFactor() DPI query APIs"

  - "[P] wxWidgets 3.1.5 docs/msw/install.md, docs/gtk/install.md, docs/osx/install.md — platform-specific build instructions"

  - "[P] wxWidgets GitHub Issues #19278, #24454, #22227 — CMake find_package with MinGW-w64, Xcode 8.3 i386 build failure"

  - "[P] Snapmaker/OrcaSlicer GitHub Actions 'Build all' runs #32856432114, #32696369649 — real-world wxWidgets 3.1.5 cross-toolchain compile failures (wxString ?: ambiguity; constexpr wxMediaState out-of-range)"

  - "[P] Snapmaker/OrcaSlicer GitHub Actions 'Build all' runs #32143560654, #32025650653, #31679936598 — Flatpak builds: 'wxWindowUpdateLocker was not declared in this scope' (declared in <wx/wupdlock.h>, missing explicit include)"

  - "[P] wxWidgets 3.2.0 docs/changes.txt (3.2.0 release section, 2022-07-07) — fixes since 3.1.5 used as reverse evidence of 3.1.5 build defects"
related:

  - "cpp/concurrency/thread-safety.md"

  - "cpp/memory/raii.md"

  - "cpp/correctness/const-correctness.md"

  - "cpp/build/cmake-include-hygiene.md"

  - "cpp/build/toolchain-and-compiler-flags.md"

  - "common/security/input-validation.md"

supersedes: []

changelog:
  - "2026.08: Added R38 (3.2.0 changes.txt reverse evidence) — items in §137/§139/§140: no CMake config file before 3.2.0, wxOSX i386-by-default + no arm64, newer-toolchain warnings (clang 13/gcc 11/MSVC C++20), older Cairo/glibc build fixes"
  - "2026.08: Added Section 132 item + R37 — OrcaSlicer Flatpak CI evidence: wxWindowUpdateLocker not declared in scope; verified declaration lives in <wx/wupdlock.h> (not wx/window.h); added include-hygiene item (wx/treebook.h no longer includes wx/treectrl.h)"
  - "2026.08: Added Section 141 with real-world CI compile-failure evidence from Snapmaker/OrcaSlicer Build all runs (wxString ?: ambiguity on GCC/Clang vs MSVC; constexpr wxMediaState out-of-range on Xcode 26 clang); added reference label R36"
  - "2026.08: Added Sections 137-140 (multi-platform compilation: wxGTK/wxMSW/wxOSX build-time requirements; cross-platform wx-config/CMake/ABI integration) from official install docs and GitHub build issues; added reference labels R32-R35"
  - "2026.07: Adversarial audit (Phase 1-4) against wxWidgets v3.1.5 source — corrected fabricated/nonexistent APIs (§52 SetAppNapEnabled, §54b MSWGetContentScaleFactor + GetDPIScaleFactor semantics, §61/§62 FromDIP signatures, §92 MSWEnableDarkMode, §96 wxFD_USE_LEGACY_DIALOG); corrected §131 wc_str/c_str build-conditional behavior and removed fabricated printf quote (N→P tier fix); fixed version attribution (wxBitmapBundle 3.1.5→3.1.6, wxActivityIndicator 3.1.5→3.1.0, wxEVT_DPI_CHANGED 3.1.5→3.1.6); fixed §1 build option names (wxUSE_STL_BASE_WXSTRING→wxUSE_STL, wxUSE_UTF8_LOCALE→wxUSE_UTF8_LOCALE_ONLY); filled empty Anti-Pattern 2; §134 tab/typo cleanup"
  - "2026.07: Audit fixes — Section 3 wxPaintDC removed from wxGLCanvas; single-backtick code fences converted; Wayland detection improved (XDG_SESSION_TYPE); Section 5 workaround clarified; Section 50 wording fixed (multi-resolution); Section 54b added (fractional DPI, GetDPIScaleFactor, wxDisplay, X11 GDK_SCALE, MSWGetContentScaleFactor); R31 reference added for wxDisplay DPI APIs; R8 restored, R9 removed; based_on and Reference Sources table updated"
  - "2026.07: Sections 131-136 added (ToUTF8 buffer lifetime UB, Freeze/Thaw, Custom widget paint, wxPopupTransientWindow, wxWebView Edge backend, ImGui+wxGLCanvas)"
  - "2026.07: Initial draft from wxWidgets 3.1.5 changelog, GitHub issues, forum posts, and Stack Overflow"

---

# wxWidgets 3.1.5 Pitfalls, Limitations, and Best Practices Checklist

**Based on:** wxWidgets 3.1.5 changelog ([P]), GitHub Issues milestone 3.1.5 ([P]), wxGLCanvas EGL issues ([P]), wxDataViewCtrl crash issues ([P]), wxPostEvent+threads #21105 ([P]), wxPropertyGrid DPI #26490 ([P]), forum t=49312 ([P]), Stack Overflow ([P]).

**Scope:** Known pitfalls, platform-specific limitations, and best practices for wxWidgets 3.1.5 (released 2021-04-14). Covers wxMSW, wxGTK, wxOSX ports. Does NOT cover wxQt (experimental) or wxUniversal (rarely used).

---

## Prerequisites

**Version context:** wxWidgets 3.1.5 is a development release (odd minor version = unstable branch). The stable branch is 3.0.x. Code written against 3.1.5 may require adjustments when migrating to 3.2.x (stable, released 2022-07). Key incompatibilities from 3.0→3.1 are documented in `docs/changes.txt`.

**Platform matrix:**

| Port | Backend | Key Risk Areas |

|------|---------|----------------|

| wxMSW | Win32 / GDI / Direct2D | DPI awareness, wxPropertyGrid, wxListCtrl repaint |

| wxGTK | GTK+ 2.x / 3.x | Wayland/EGL, wxGLCanvas, wxDataViewCtrl native vs generic |

| wxOSX | Cocoa | macOS 11+ compatibility, WKWebView migration, Retina |

**Event model:** wxWidgets uses a per-thread event queue. Only the main thread should touch GUI objects. Worker threads communicate via `wxThreadEvent` / `CallAfter()` / `QueueEvent()`.

---

## Checklist

### 1. wxString Encoding and Conversion  **(P)** [R1][R8]

```cpp
wxString internal representation differs by build configuration (`wxUSE_UNICODE` is default on since 3.0, but `wxUSE_UNICODE_WCHAR` vs `wxUSE_UNICODE_UTF8` selects the internal storage, and `wxUSE_STL` / `wxUSE_UTF8_LOCALE_ONLY` further affect behavior). Mixing `c_str()` return types across boundaries is the #1 source of mysterious assertion failures and encoding corruption.
```

- [ ] Never pass `wxString::c_str()` to non-wx APIs expecting `const char*` without explicit conversion → **(P)** [R1]

- [ ] Use `wxString::utf8_string()` (new in 3.1.5) or `wxString::ToUTF8()` for UTF-8 output → **(P)** [R1]

- [ ] Use `wxString::mb_str(wxConvUTF8)` for narrow-char output with known encoding → **(P)** [R1]

- [ ] Use `wxString::wc_str()` for `wchar_t*` (Windows API calls) → **(P)** [R1]

- [ ] Never use `(const char*)str` implicit conversion — it asserts in Unicode builds → **(P)** [R1]

```cpp
// Good — explicit encoding conversion
wxString path = wxFileName::GetFullPath();
FILE* f = fopen(path.utf8_string().c_str(), "r");
```

```cpp
// Good — wchar_t for Win32 API
```

```cpp
wxString windowTitle = frame->GetTitle();
```

```cpp
::SetWindowTextW(hwnd, windowTitle.wc_str());
```

```cpp
// Bad — implicit conversion asserts in Unicode builds
```

```cpp
FILE* f = fopen(path.c_str(), "r");  // may assert: no const char* conversion
```

```cpp
// Bad — assumes internal encoding is UTF-8
```

```cpp
std::string s = str.c_str();  // garbage on wxUSE_UNICODE_WCHAR builds
```

### 2. wxGLCanvas on Wayland/EGL  **(P)** [R3]

```cpp
wxGTK 3.1.5 introduced EGL-based wxGLCanvas backend for Wayland support (PR #2038, PR #2015). This backend has known stability issues with multiple GL canvases, popup windows, and surface lifecycle management.
```

- [ ] If targeting Wayland: test with `GDK_BACKEND=wayland` explicitly, not just X11 fallback → **(P)** [R3]

- [ ] Multiple wxGLCanvas objects in one window under Wayland: verify they render independently — known context-sharing issues → **(P)** [R3]

- [ ] wxGLCanvas inside wxPopupWindow: known positioning bug on EGL+Wayland (#26250) → **(P)** [R3]

- [ ] Destroying wxGLCanvasEGL: known crash on Wayland+Manjaro (#26248), dangling surface on unrealize (#26340) → **(P)** [R3]

- [ ] High CPU load with EGL enabled: known performance regression (#24977) → **(P)** [R3]

- [ ] Workaround: `GDK_BACKEND=x11` for GL-heavy applications on Wayland compositors → **(P)** [R3]

```cpp
// Good — detect Wayland and provide fallback
if (wxGetEnv("WAYLAND_DISPLAY", nullptr) || wxGetEnv("XDG_SESSION_TYPE", nullptr) == "wayland") {
    // EGL backend may have issues; offer X11 fallback
    wxLogWarning("Wayland detected. If OpenGL issues occur, "
                 "try running with GDK_BACKEND=x11");
```
}

```cpp
// Good — single GL canvas, verified working
```

```cpp
wxGLAttributes attrs;
```

attrs.PlatformDefaults().MinVersion(3, 3).EndList();

auto* canvas = new wxGLCanvas(parent, attrs, wxID_ANY);

```cpp
// Bad — multiple GL canvases assuming shared context works (Wayland/EGL)
```

auto* canvas1 = new wxGLCanvas(this, attrs, wxID_ANY);

auto* canvas2 = new wxGLCanvas(this, attrs, wxID_ANY);

```cpp
// Context sharing may silently fail on EGL; render output may be blank
```

### 3. wxGLCanvas High-DPI Coordinate Handling  **(P)** [R1]

Since 3.1.x, wxGLCanvas uses physical pixels on high-DPI displays under wxGTK3 and wxOSX. Logical coordinates from `wxWindow::GetSize()` must be multiplied by `GetContentScaleFactor()` before passing to OpenGL functions.

- [ ] All OpenGL viewport/glx size calls use `GetClientSize() * GetContentScaleFactor()`, not raw `GetClientSize()` → **(P)** [R1]

- [ ] Mouse coordinates in GL handlers: convert from logical to physical pixels → **(P)** [R1]

- [ ] Test on Retina/macOS and HiDPI Windows at 150% and 200% scaling → **(P)** [R1]

```cpp
// Good — physical pixel coordinates for GL
void OnPaint(wxPaintEvent&) {
    if (!IsShown()) return;
    SetCurrent(*m_context);
    const wxSize size = GetClientSize() * GetContentScaleFactor();
    glViewport(0, 0, size.x, size.y);
    // ... render ...
    SwapBuffers();
```
}

```cpp
// Bad — logical pixels, blurry/wrong on HiDPI
```

```cpp
void OnPaint(wxPaintEvent&) {
```

```cpp
    const wxSize size = GetClientSize();
```

```cpp
    glViewport(0, 0, size.x, size.y);  // half-resolution on Retina
```

}

### 4. wxDataViewCtrl Model Lifecycle and Crashes  **(P)** [R4]

```cpp
wxDataViewCtrl has a long history of crash bugs related to model lifetime, item deletion during editing, and cross-platform behavioral differences between native (GTK/macOS) and generic implementations.
```

- [ ] `AssociateModel(nullptr)` before model destruction: clear notifier reference (#25686) → **(P)** [R4]

- [ ] Do NOT delete model items during `wxEVT_DATAVIEW_ITEM_EDITING_DONE` — crash on macOS (#18337) → **(P)** [R4]

- [ ] `wxDataViewModel::ItemsAdded`/`ItemsDeleted` must be called from main thread — crash in worker thread (#24148) → **(P)** [R4]

- [ ] `wxTreeListCtrl::DeleteAllItems` — crash if called during selection event (#18045) → **(P)** [R4]

- [ ] `wxDataViewCtrl` with `wxVSCROLL`/`wxHSCROLL` style on macOS — crash (#17028); remove these styles → **(P)** [R4]

- [ ] Model `DecRef()` to zero then immediate control access: use `wxDataViewCtrl::AssociateModel(nullptr)` first → **(P)** [R4]

```cpp
// Good — detach model before destruction
```
m_dataView->AssociateModel(nullptr);  // clear control's reference
model->DecRef();                      // now safe to release

```cpp
// Good — defer deletion out of editing callback
```

```cpp
void OnEditingDone(wxDataViewEvent& event) {
```

```cpp
    QueueEvent(new wxThreadEvent(wxEVT_COMMAND_DELETE_ITEM,
```

```cpp
                                 event.GetItem()));
```

}

```cpp
// Bad — delete during edit callback, crash on macOS
```

```cpp
void OnEditingDone(wxDataViewEvent& event) {
```

```cpp
    m_model->DeleteItem(event.GetItem());  // crash: dangling pointer
```

}

### 5. wxPropertyGrid DPI Awareness  **(P)** [R6]

```cpp
wxPropertyGrid has a known regression where text appears too small when moved between monitors with different DPI (#26490, also affects 3.2.x). The root cause is `WS_EX_COMPOSITED` default change.
```

- [ ] Test wxPropertyGrid with DPI scaling change (200%→100%→200%) on wxMSW → **(P)** [R6]

- [ ] If text shrinks after DPI change: toggle `wxTAB_TRAVERSAL` style off then on via `SetWindowStyleFlag()` to force re-evaluation of `WS_EX_COMPOSITED`, or recreate the control → **(P)** [R6]

- [ ] Do NOT rely on `wxPropertyGrid` auto-scaling for custom property editors — call `wxWindow::SetFont()` explicitly after DPI change → **(P)** [R6]

### 6. Thread Safety: wxPostEvent and GUI Access  **(P)** [R5][R2]

Only the main thread may touch GUI objects. Worker threads must use `wxThreadEvent` / `QueueEvent()` / `CallAfter()`. `wxPostEvent` from non-main thread on wxGTK historically had issues where event handler could execute in the calling thread (#21105).

- [ ] All GUI access from worker threads via `CallAfter()` or `QueueEvent()` only → **(P)** [R2]

- [ ] `wxMutexGuiEnter()`/`wxMutexGuiLeave()` is discouraged — use event-based communication instead → **(P)** [R5]

- [ ] `wxPostEvent` from worker thread on wxGTK: verify event executes in main thread (use `wxThread::IsMain()` assertion in handler) → **(P)** [R5]

- [ ] `wxThread::Wait()` from main thread on a joinable thread that touches GUI: deadlock risk — use detached threads + events → **(P)** [R2]

```cpp
// Good — thread-safe GUI update via CallAfter
void WorkerThread::Entry() {
    int progress = ComputeProgress();
    wxTheApp->CallAfter([this, progress]() {
        m_gauge->SetValue(progress);  // runs in main thread
    });
```
}

```cpp
// Good — thread-safe via wxThreadEvent
```

```cpp
wxThreadEvent* evt = new wxThreadEvent(wxEVT_COMMAND_UPDATE_PROGRESS);
```

evt->SetInt(progress);

```cpp
wxQueueEvent(m_handler, evt);
```

```cpp
// Bad — direct GUI access from worker thread (crash/UB)
```

```cpp
void WorkerThread::Entry() {
```

```cpp
    m_gauge->SetValue(50);  // NO: not main thread
```

}

### 7. wxMSW Event Handling: Alt-Space, Alt-F4, wxEVT_KEY_DOWN  **(P)** [R1]

Since 3.1.x, wxMSW no longer always lets the system process `WM_SYSKEYDOWN` events. If you handle `wxEVT_KEY_DOWN` and don't call `event.Skip()`, standard key combinations like Alt-Space and Alt-F4 stop working.

- [ ] In `wxEVT_KEY_DOWN` / `wxEVT_CHAR` handlers: call `event.Skip()` for system keys (Alt-*, F4, etc.) → **(P)** [R1]

- [ ] Do NOT consume Alt+key combinations unconditionally in key handlers → **(P)** [R1]

- [ ] Test Alt-Space (system menu) and Alt-F4 (close) after adding key event handlers → **(P)** [R1]

```cpp
// Good — skip unhandled keys
void OnKeyDown(wxKeyEvent& event) {
    if (event.GetKeyCode() == WXK_F5) {
        Refresh();
    } else {
        event.Skip();  // let system handle Alt-Space, Alt-F4, etc.
    }
```
}

```cpp
// Bad — consumes all keys, breaks system shortcuts
```

```cpp
void OnKeyDown(wxKeyEvent& event) {
```

```cpp
    if (event.GetKeyCode() == WXK_F5) {
```

```cpp
        Refresh();
```

```cpp
    }
```

```cpp
    // missing event.Skip() — Alt-F4 won't close the window
```

}

### 8. wxWebView: WKWebView Migration and Edge  **(P)** [R1]

```cpp
wxOSX switched to WKWebView (from deprecated WebView/WebKit) in 3.1.5 (PR #2113). wxMSW wxWebViewEdge requires GCC/Clang fix (PR #2245). IE-based wxWebView is deprecated.
```

- [ ] wxOSX: do NOT use `wxWebView::RegisterEngine(wxWEBVIEW_ENGINE_WEBKIT)` — WKWebView is the only backend now → **(P)** [R1]

- [ ] wxMSW: `wxWebViewEdge` with GCC/Clang: apply build fix or use MSVC → **(P)** [R1]

- [ ] IE-based `wxWebView` (`wxWebViewIE`): deprecated, plan migration to Edge → **(P)** [R1]

- [ ] `webview` library is NOT in default `wx-config --libs` output — request explicitly: `wx-config --libs std,webview` → **(P)** [R1]

### 9. Incompatible Behavior Changes from 3.0  **(P)** [R1]

Several behavioral changes from 3.0→3.1 are silent (compile fine, different runtime behavior). These are the most common surprises.

- [ ] `wxYield()` now generates `wxEVT_IDLE` events on wxMSW — idle handlers may fire unexpectedly → **(P)** [R1]

- [ ] `wxTE_PROCESS_ENTER` now required for `wxEVT_TEXT_ENTER` from multiline `wxTextCtrl` (was automatic in wxMSW 3.0) → **(P)** [R1]

- [ ] `wxFileDialog::GetPath()` / `GetFilename()` assert with `wxFD_MULTIPLE` — use `GetPaths()` instead → **(P)** [R1]

- [ ] `wxAuiNotebook::RemovePage()` now hides the removed page — call `Show()` if reusing → **(P)** [R1]

- [ ] `wxBitmap` with 0 width/height now fails (used to succeed on wxMSW) → **(P)** [R1]

- [ ] `wxGLCanvas` uses physical pixels on HiDPI — see Item 3 → **(P)** [R1]

- [ ] `wxWS_EX_VALIDATE_RECURSIVELY` is now default — `Validate()` recurses into children → **(P)** [R1]

- [ ] wxMSW dotted/dashed pens: better appearance but much slower — use `wxPenInfo::LowQuality()` for performance → **(P)** [R1]

- [ ] `wxChoice::GetString()` now asserts on invalid index (was silent) → **(P)** [R1]

### 10. Build System: setup.h, wx-config, CMake Targets  **(P)** [R1][R7][R8]

"setup.h no such file" is a commonly reported build issue. CMake targets were renamed in 3.1.4 to `wx::*` namespace.

- [ ] Use `wx-config --cxxflags --libs` (Unix) or `setup.h` via `wxWidgets_USE_FILE` (CMake) — never hardcode `include "wx/setup.h"` paths → **(P)** [R7]

- [ ] CMake: `find_package(wxWidgets COMPONENTS core base)` then `target_link_libraries(app ${wxWidgets_LIBRARIES})` → **(P)** [R7]

- [ ] CMake targets: `wx::core`, `wx::base` (since 3.1.4); library names start with `wx` prefix → **(P)** [R1]

- [ ] Static build: `wxCmpNatural()` linking fix applied in 3.1.5 (PR #2050) — if you backport to 3.1.4, cherry-pick this fix → **(P)** [R1]

- [ ] `webview` library: NOT in default `wx-config --libs` — specify `std,webview` → **(P)** [R1]

- [ ] macOS: minimum SDK is 10.11, Xcode 7.2.1+ — older SDKs fail to build → **(P)** [R1]

```cmake

# Good — modern CMake with wxWidgets

find_package(wxWidgets COMPONENTS core base gl REQUIRED)

target_link_libraries(myapp PRIVATE ${wxWidgets_LIBRARIES})

target_include_directories(myapp PRIVATE ${wxWidgets_INCLUDE_DIRS})

# Bad — hardcoded setup.h path

target_include_directories(myapp PRIVATE

```cpp
    /usr/local/include/wx-3.1/wx/setup.h)  # fragile, version-specific
```

### 11. wxGrid Performance and Attribute Handling  **(P)** [R1]

```cpp
wxGrid with many cells/attributes is a known performance bottleneck. 3.1.5 includes optimizations (PR #2229) but patterns matter.
```

- [ ] Use `wxGridCellAttr` via `SetAttr()` / `SetColAttr()` in bulk, not per-cell `SetCellValue()` + `SetCellAlignment()` → **(P)** [R1]

- [ ] `wxGrid::AutoSizeColumns()` on large grids: call once after batch updates, not per-row → **(P)** [R1]

- [ ] `wxEVT_GRID_RANGE_SELECTING`/`SELECTED` events (new in 3.1.5): use for live feedback, but throttle if grid is large → **(P)** [R1]

- [ ] Auto-wrapped cells: known infinite loop bug, fixed in 3.1.5 — verify if upgrading from 3.1.4 → **(P)** [R1]

### 12. macOS 11 (Big Sur) Compatibility  **(P)** [R1]

```cpp
wxOSX 3.1.5 includes many macOS 11 fixes. If targeting macOS 11+, verify these areas.
```

- [ ] `wxSplitterWindow` painting regression on macOS 11 (PR #2306) → **(P)** [R1]

- [ ] Window background tinting on macOS 11 (fixed) — verify custom background colors → **(P)** [R1]

- [ ] System UI font handling on macOS 11 (fixed) — verify `wxSystemSettings::GetFont()` → **(P)** [R1]

- [ ] `wxDataViewCtrl` columns resizing on macOS 11 (fixed) — verify column drag behavior → **(P)** [R1]

- [ ] `wxPreferencesEditor` appearance on macOS 11 (improved) → **(P)** [R1]

---

### 13. Event Handling: Bind() vs Event Tables vs Connect()  **(P)** [R10]

```cpp
wxWidgets 3.1.5 official documentation recommends `Bind()` over static event tables and the deprecated `Connect()`. `Bind()` supports lambda handlers, functor binding, and runtime unbinding — event tables only support static, same-class binding.
```

- [ ] Use `Bind(wxEVT_XXX, &Handler, this)` for all new code; prefer over `BEGIN_EVENT_TABLE`/`EVT_XXX` macros → **(P)** [R10]

- [ ] Never use `Connect()` — deprecated since 2.9, use `Bind()` → **(P)** [R10]

- [ ] `Bind()` with lambda: capture `this` explicitly, avoid dangling captures if the handler may outlive the object → **(P)** [R10]

- [ ] Unbind before destroying the handler object to avoid dangling callback → **(P)** [R10]

- [ ] Mixing event tables and `Bind()` in the same class: confusing and error-prone — choose one approach → **(P)** [R10]

```cpp
// Good — modern Bind() with lambda
```
button->Bind(wxEVT_BUTTON, [this](wxCommandEvent& evt) {
```cpp
    OnButtonClick(evt);
```
});

```cpp
// Good — Bind to member function
```

button->Bind(wxEVT_BUTTON, &MyFrame::OnButton, this);

```cpp
// Bad — Connect() deprecated, no type safety
```

button->Connect(wxEVT_BUTTON, wxCommandEventHandler(MyFrame::OnButton));

```cpp
// Bad — static event table, can't bind to lambda or external object
```

BEGIN_EVENT_TABLE(MyFrame, wxFrame)

```cpp
    EVT_BUTTON(ID_BUTTON, MyFrame::OnButton)
```

END_EVENT_TABLE()

### 14. Sizer Layout Pitfalls  **(P)** [R1][R11]

```cpp
wxSizer layout has several known edge cases: `wxPanel` does not auto-Layout when children are hidden (#18964), `wxWrapSizer` reports wrong minimal size with >1 item (#12464), and spacers with min size -1 cause infinite loops (#11842).
```

- [ ] `wxPanel` with hidden children: call `Layout()` explicitly after `Show(false)` on a child → **(P)** [R11]

- [ ] `wxWrapSizer` with multiple items: verify minimal size calculation, may report wrong → **(P)** [R1]

- [ ] Spacers: never use min size of -1 — infinite loop in `wxSizer::Layout()` (#11842) → **(P)** [R1]

- [ ] `SetFont()` on GTK >= 3.6: best size not updated — call `InvalidateBestSize()` then `Layout()` → **(P)** [R1]

- [ ] `wxFlexGridSizer` with many items (>1000): known performance issues — consider `wxGrid` instead → **(P)** [R1]

- [ ] Use `wxSizerFlags` for cleaner, more readable sizer configuration → **(P)** [R10]

- [ ] `wxSHAPED` flag with `wxWrapSizer`: known assert after wrapped sizer changes (#4598) → **(P)** [R1]

```cpp
// Good — explicit Layout after hiding a child
```
m_textCtrl->Show(false);
m_panel->Layout();  // wxPanel won't auto-layout on child hide (#18964)

```cpp
// Good — wxSizerFlags for readable config
```

sizer->Add(button, wxSizerFlags(0).Center().Border(wxALL, 5));

```cpp
// Bad — spacer with -1 min size, infinite loop (#11842)
```

sizer->AddStretchSpacer(1);  // OK: positive proportion

// sizer->Add(0, 0, -1);     // BAD: -1 proportion crashes

```cpp
// Bad — assumes wxPanel auto-layouts on child hide
```

m_textCtrl->Show(false);

// missing m_panel->Layout() — panel keeps stale layout

### 15. Mouse Capture and Modal Dialogs  **(P)** [R10]

Some events (drag, item selection) capture the mouse via `wxWindow::CaptureMouse()`. Showing a modal dialog from such a handler makes the dialog appear unresponsive — it receives no mouse input.

- [ ] Avoid showing modal dialogs from mouse-capture event handlers (e.g. `wxEVT_LIST_ITEM_SELECTED`, `wxEVT_SPLITTER_SASH_POS_CHANGING`) → **(P)** [R10]

- [ ] If a modal dialog is required during mouse capture: break capture with `dialog.CaptureMouse(); dialog.ReleaseMouse();` → **(P)** [R10]

- [ ] Prefer `CallAfter()` or `QueueEvent()` to defer dialog display out of the capture scope → **(P)** [R10]

```cpp
// Good — defer dialog to after mouse release
void OnItemSelected(wxListEvent& event) {
    CallAfter([this, item = event.GetItem()]() {
        ShowItemDetailsDialog(item);  // runs after mouse is released
    });
```
}

```cpp
// Bad — modal dialog during mouse capture, dialog is unresponsive
```

```cpp
void OnItemSelected(wxListEvent& event) {
```

```cpp
    wxMessageDialog dlg(this, "Selected: " + GetItemText(event.GetItem()));
```

```cpp
    dlg.ShowModal();  // user can't click — mouse is captured by list
```

}

```cpp
// Workaround — if dialog must be shown immediately
```

```cpp
void OnItemSelected(wxListEvent& event) {
```

```cpp
    wxMessageDialog dlg(this, "...");
```

```cpp
    dlg.CaptureMouse();   // break existing capture
```

```cpp
    dlg.ReleaseMouse();   // release immediately
```

```cpp
    dlg.ShowModal();
```

}

### 16. wxMutexGuiEnter/Leave: Deprecated and Unsafe  **(P)** [R2][R12]

The official thread overview explicitly states `wxMutexGuiEnter()`/`wxMutexGuiLeave()` are not safe (ticket #10366). Use event-based communication instead.

- [ ] Never use `wxMutexGuiEnter()`/`wxMutexGuiLeave()` — deprecated and unsafe → **(P)** [R12]

- [ ] For worker-to-main communication: use `QueueEvent()`/`CallAfter()` exclusively → **(P)** [R2]

- [ ] Deriving from both `wxThread` and `wxEvtHandler` to receive events in a worker thread: does NOT work — use `wxThreadHelper` instead → **(P)** [R2]

- [ ] `wxThreadEvent` with `YieldFor()`: use `GetEventCategory()` to prevent out-of-order processing during yield → **(P)** [R2]

---

### 17. Dark Mode and Theme Consistency  **(P)** [R1][R13]

```cpp
wxWidgets 3.1.5 has limited dark mode support — dark mode was introduced in macOS 10.14 (Mojave) and Windows 10 1809. The framework relies on native theming but custom-drawn controls, hardcoded colors, and `wxSystemSettings` may not adapt correctly.
```

- [ ] Do NOT hardcode `*wxBLACK`/`*wxWHITE` for backgrounds — use `wxSystemSettings::GetColour(wxSYS_COLOUR_WINDOW)` → **(P)** [R13]

- [ ] `wxSYS_COLOUR_BTNFACE` in dark mode: known wrong value on wxMSW (#24634) — verify before relying → **(P)** [R13]

- [ ] Custom-drawn controls (e.g. `wxGrid`, `wxDataViewCtrl` custom renderers): must check `wxSystemSettings::GetAppearance()` (3.1.5+) and adjust colors → **(P)** [R1]

- [ ] wxMSW: `wxCheckBox` dark mode appearance inconsistent (#26569), spin control colors break (#26198) — test native controls in dark mode → **(P)** [R13]

- [ ] wxOSX: combobox dropdown button doesn't honour dark mode (#25681), `GetThemeBackgroundColour()` on `wxNotebook` ignores dark mode (#25527) → **(P)** [R13]

- [ ] `wxInfoBar` colors from tooltip on GTK (#25048) — verify appearance → **(P)** [R13]

- [ ] Grid lines invisible in dark mode on macOS Tahoe (#25783) — grid line color may match background → **(P)** [R13]

```cpp
// Good — system-aware color
wxColour bg = wxSystemSettings::GetColour(wxSYS_COLOUR_WINDOW);
```
dc.SetBackground(wxBrush(bg));

```cpp
// Good — check appearance (3.1.5+)
```

```cpp
if (wxSystemSettings::GetAppearance().IsDark()) {
```

```cpp
    dc.SetTextForeground(*wxWHITE);
```

} else {

```cpp
    dc.SetTextForeground(*wxBLACK);
```

}

```cpp
// Bad — hardcoded color, invisible in dark mode
```

dc.SetBackground(*wxWHITE);  // white-on-white in dark mode

dc.SetTextForeground(*wxBLACK);

### 18. Keyboard Navigation and Tab Traversal  **(P)** [R1][R14]

Tab traversal behavior differs significantly across platforms. wxOSX/Cocoa uses geometric position-based navigation (not child order), wxSearchCtrl with `wxTE_PROCESS_ENTER` breaks tab traversal (#12808), and `wxPropertyGrid` tab traversal has issues on wxGTK (#23354).

- [ ] wxOSX/Cocoa: Tab navigation uses geometric position, NOT child window order (#17341) — do NOT assume tab order = creation order on macOS → **(P)** [R14]

- [ ] wxOSX: "Full keyboard access" = "All controls" in System Preferences changes Tab behavior — test with this setting enabled → **(P)** [R14]

- [ ] `wxSearchCtrl` + `wxTE_PROCESS_ENTER`: breaks tab traversal (#12808) — avoid this combination or handle manually → **(P)** [R14]

- [ ] `wxPropertyGrid` tab traversal on wxGTK (#23354) — verify focus moves correctly → **(P)** [R14]

- [ ] `wxTAB_TRAVERSAL` + `wxTextCtrl`: may dis-enable text control, preventing tab between controls (#16902) → **(P)** [R14]

- [ ] `wxGrid` on `wxDialog`: keyboard problems (#3449) — handle navigation explicitly → **(P)** [R14]

- [ ] Use `wxWindow::MoveBeforeInTabOrder()` / `MoveAfterInTabOrder()` to enforce explicit tab order → **(P)** [R1]

- [ ] Accessibility: wxAccessible is MSW-only and limited; prefer native control semantics; verify screen reader compatibility (#9510, #21562) → **(P)** [R14]

```cpp
// Good — explicit tab order on macOS (geometric nav doesn't respect creation order)
```
#ifdef __WXOSX__
```cpp
    textCtrl->MoveBeforeInTabOrder(button1);
    button1->MoveBeforeInTabOrder(button2);
```
#endif

```cpp
// Good — handle wxEVT_NAVIGATION_KEY for custom navigation
```

```cpp
void OnNavigationKey(wxNavigationKeyEvent& event) {
```

```cpp
    // custom tab order logic
```

```cpp
    event.Skip();  // let default handle if not custom
```

}

```cpp
// Bad — assumes tab order = creation order (fails on macOS)
```

// Created: textCtrl, then button1, then button2

// On macOS, tab may go to button2 before button1 based on geometry

### 19. Window Deletion and Close Event Lifecycle  **(P)** [R15]

Window deletion has a specific lifecycle in wxWidgets. Using `delete` instead of `Destroy()` can cause events to be sent to destroyed windows. `EVT_CLOSE` handlers must decide whether to destroy, and `wxDialog` default behavior does NOT destroy (it may be stack-allocated).

- [ ] Never use `delete window` for wxWindow-derived objects — use `wxWindow::Destroy()` (deferred deletion) → **(P)** [R15]

- [ ] `EVT_CLOSE` handler: call `event.Skip()` to allow default destruction, or `event.Veto()` to cancel → **(P)** [R15]

- [ ] `wxDialog` default close behavior: does NOT destroy (simulates Cancel) — call `Destroy()` explicitly if dynamic → **(P)** [R15]

- [ ] `wxFrame` default close behavior: calls `Destroy()` automatically → **(P)** [R15]

- [ ] Child windows: deleted from parent destructor — close child frames/dialogs explicitly in parent close handler if needed → **(P)** [R15]

- [ ] `wxWindow::Close()` does NOT guarantee destruction — it generates `EVT_CLOSE`, handler decides → **(P)** [R15]

- [ ] Application exits when last top-level window is destroyed — put cleanup in `wxApp::OnExit()`, not in window destructor → **(P)** [R15]

```cpp
// Good — Destroy() for deferred deletion
void OnClose(wxCloseEvent& event) {
    if (!SaveChanges()) {
        event.Veto();  // user cancelled, don't close
        return;
    }
    event.Skip();  // let default handler destroy the window
```
}

```cpp
// Good — explicit Destroy for dynamically created dialog
```

```cpp
wxDialog* dlg = new wxDialog(this, wxID_ANY, "Modal");
```

dlg->ShowModal();

dlg->Destroy();  // safe deferred deletion

```cpp
// Bad — delete operator, events may be sent to destroyed window
```

```cpp
wxDialog* dlg = new wxDialog(this, wxID_ANY, "Modal");
```

dlg->ShowModal();

delete dlg;  // DANGER: pending events may reference dlg

```cpp
// Bad — assumes Close() destroys the window
```

frame->Close();

// frame may still exist if EVT_CLOSE handler vetoed

---

### 20. wxImage Alpha Channel and Transparency  **(P)** [R16]

```cpp
wxImage/wxBitmap alpha handling has many historical bugs: `wxMemoryDC::DrawBitmap()` with alpha loses existing DC contents (#14403), `wxImage::HasAlpha()` not detecting alpha (#13110), `wxImage::Paste()` not blending alpha (#12458, fixed in 3.1.5), BMP alpha loading issues (#12762), GIF decoder changes transparent to pink (#18014).
```

- [ ] `wxImage::HasAlpha()` may return false even when alpha data exists — check `GetAlpha()` pointer directly → **(P)** [R16]

- [ ] `wxMemoryDC::DrawBitmap()` with alpha bitmap: may clear destination — use `wxDC::DrawBitmap()` with `useMask=true` or manual blending → **(P)** [R16]

- [ ] `wxImage::Paste()`: alpha blending fixed in 3.1.5 (PR #2056) — if upgrading from 3.1.4, verify paste behavior → **(P)** [R16]

- [ ] GIF transparency: transparent colour becomes pink (#18014) — convert to PNG or handle mask manually → **(P)** [R16]

- [ ] BMP with alpha: not properly loaded (#12762) — use PNG for alpha bitmaps → **(P)** [R16]

- [ ] Use `wxBITMAP_PNG()` for embedded alpha bitmaps, not `wxBITMAP()` (XPM has no alpha) → **(P)** [R17]

```cpp
// Good — PNG for alpha transparency
wxBitmap bmp(wxBITMAP_PNG(logo));  // supports alpha
```

```cpp
// Good — check alpha via pointer, not HasAlpha()
```

```cpp
if (image.GetAlpha() != nullptr) { /* has alpha */ }
```

```cpp
// Bad — XPM for alpha (no alpha support)
```

```cpp
wxBitmap bmp(wxBITMAP(logo));  // XPM: no transparency or alpha
```

**20a. 32-bit alpha-bitmap RGB corruption is fatal on `wxDC::DrawBitmap` but harmless via `wxGCDC`/`wxGraphicsContext`.** When a 32-bit `wxBitmap` carries per-pixel alpha, the RGB channels of fully-transparent pixels (alpha=0) are often corrupted (commonly zero/black). Drawing this bitmap through `wxDC::DrawBitmap(..., useMask=false)` (or `wxMemoryDC::DrawBitmap`) **reads those corrupted RGB values and renders them as black corners/edges**. Drawing the *same* bitmap through `wxGCDC`/`wxGraphicsContext` is harmless, because alpha blending computes `dst = src.rgb * src.a + dst.rgb * (1 - src.a)` — when `src.a == 0` the corrupted RGB is never read and the background shows through. So: **the RGB-at-alpha-0 corruption only bites on the `wxDC::DrawBitmap` path; switching to `wxGCDC` is both the fix and the reason the corruption stops mattering** (see also #37).

```cpp
// Bad — wxDC::DrawBitmap renders alpha=0 RGB (corrupted) as black corners
wxAutoBufferedPaintDC dc(this);
dc.DrawBitmap(alphaBitmap, x, y, false);  // black corners on wxMSW

// Good — wxGCDC blends; alpha=0 pixels discard RGB, background shows through
wxAutoBufferedPaintDC pbdc(this);
wxGCDC dc(pbdc);                          // wraps the DC in a graphics context
dc.DrawBitmap(alphaBitmap, x, y, false);  // correct transparency, no black corners
```

### 21. Clipboard and wxDataObject  **(P)** [R16]

Clipboard operations with non-ASCII/Unicode text have known crash bugs: copying Unicode text crashes on macOS (#13442), multibyte text to clipboard crashes (#4381).

- [ ] Clipboard operations must be on main thread — never from worker threads → **(P)** [R16]

- [ ] `wxDataObject` custom formats: derive from `wxDataObjectSimple`, implement `GetDataSize`/`GetDataHere`/`SetData`/`GetFormat` → **(P)** [R16]

- [ ] Unicode text to clipboard on macOS: known crash (#13442) — use `wxTextDataObject` which handles encoding → **(P)** [R16]

- [ ] `wxTheClipboard->Open()`/`Close()` must be paired — never leave clipboard open across event handlers → **(P)** [R16]

- [ ] Primary selection (X11 only): `wxTheClipboard->UsePrimarySelection(true)` for middle-click paste → **(P)** [R16]

```cpp
// Good — main thread, paired open/close, wxTextDataObject
if (wxTheClipboard->Open()) {
    wxTheClipboard->SetData(new wxTextDataObject(text));
    wxTheClipboard->Close();
```
}

```cpp
// Bad — clipboard from worker thread (crash/UB)
```

```cpp
void WorkerThread::Entry() {
```

```cpp
    if (wxTheClipboard->Open()) {  // NO: not main thread
```

```cpp
        wxTheClipboard->SetData(new wxTextDataObject(text));
```

```cpp
    }
```

```cpp
    // missing Close() — clipboard locked
```

}

### 22. XRC (XML Resource) Loading  **(P)** [R16]

XRC loading has several pitfalls: `wxXmlResource::Load()` is case-sensitive even on Windows (#15243), XRC via HTTP regressed (#19109), and `Unload()` fails in some cases (#10577).

- [ ] XRC filenames: case-sensitive even on Windows (#15243) — use exact case in paths → **(P)** [R16]

- [ ] XRC via HTTP: restored in 3.1.5 (was broken from 2.8.x) — verify if loading from URL → **(P)** [R16]

- [ ] `wxXmlResource::Unload()`: may fail (#10577) — prefer destroying and recreating the resource → **(P)** [R16]

- [ ] Validators cannot be specified in XRC — iterate controls after `LoadDialog()` to set validators → **(P)** [R17]

- [ ] XRC object names: must match C++ variable names — use `XRCID("name")` and `XRCCTRL(parent, "name", Type)` → **(P)** [R17]

```cpp
// Good — exact case, validators set after load
wxXmlResource::Get()->LoadDialog(this, "MyDialog");  // case must match file
wxTextCtrl* text = XRCCTRL(*this, "name_text", wxTextCtrl);
```
text->SetValidator(wxTextValidator(wxFILTER_ALPHA, &m_data));

```cpp
// Bad — wrong case on Windows (may work locally, fail on deploy)
```

```cpp
wxXmlResource::Get()->LoadDialog(this, "mydialog");  // case mismatch
```

### 23. wxSocket in Multi-threaded Contexts  **(P)** [R16]

```cpp
wxSocket has known thread-safety issues: crash inside wxThread (#18492), events still dispatched on main thread even with `wxSOCKET_BLOCK` (#15259), and `wxSocketImpl::Close` from wrong thread (#17031).
```

- [ ] wxSocket operations in worker threads: known crash (#18492) — use main thread or dedicated socket thread with `wxSOCKET_BLOCK` → **(P)** [R16]

- [ ] `wxSOCKET_BLOCK` mode: events still dispatched on main thread (#15259) — do not assume blocking = no events → **(P)** [R16]

- [ ] `wxSocketImpl::Close`: must be called from the thread that created the socket (#17031) → **(P)** [R16]

- [ ] `wxEVT_SOCKET` handler: must be on main thread, use `wxThreadEvent` to forward to worker → **(P)** [R16]

- [ ] Socket destruction: `Destroy()` (deferred) not `delete` — see Item 19 → **(P)** [R16]

### 24. wxListCtrl Known Issues  **(P)** [R16]

```cpp
wxListCtrl in report mode has many historical issues: crash on diagonal scroll on macOS (#24649), "selected" status kept for removed entries (#12378), `FindItem(int)` very slow (#9870), and infinite repaint loop with `wxLC_HRULES` on wxMSW (fixed in 3.1.5).
```

- [ ] macOS: diagonal scroll crash (#24649) — use `wxListCtrl::SetDoubleBuffered()` or switch to `wxDataViewCtrl` → **(P)** [R16]

- [ ] After deleting items: stale selection state may remain (#12378) — call `SetItemState(item, 0, wxLIST_STATE_SELECTED)` explicitly → **(P)** [R16]

- [ ] `FindItem(int)` on large lists: very slow (#9870) — maintain own index map → **(P)** [R16]

- [ ] `wxLC_HRULES` infinite repaint: fixed in 3.1.5 — verify if upgrading from 3.1.4 → **(P)** [R1]

- [ ] For large data sets (>1000 items): prefer `wxDataViewCtrl` (virtual model) over virtual `wxListCtrl` → **(P)** [R1]

### 25. wxComboBox and wxChoice Event Issues  **(P)** [R16]

```cpp
wxComboBox has known event pitfalls: ID 1000 conflicts (#15647), Escape key closing dialogs too early (#12952), `wxEVT_KILL_FOCUS` not received on macOS (#9862), and `wxCB_READONLY` clearing issues.
```

- [ ] wxComboBox ID: avoid `wxID_ANY`-generated IDs near 1000 — conflicts with default ID range (#15647) → **(P)** [R16]

- [ ] Escape key: may close dialog prematurely (#12952) — handle `wxEVT_CHAR_HOOK` to intercept Escape → **(P)** [R16]

- [ ] `wxEVT_KILL_FOCUS`: not received on macOS (#9862) — use `wxEVT_TEXT` or `wxEVT_COMBOBOX` instead → **(P)** [R16]

- [ ] `wxCB_READONLY`: clearing with `Clear()` may cause asserts — use `SetSelection(wxNOT_FOUND)` → **(P)** [R1]

- [ ] `wxEVT_COMBOBOX` vs `wxEVT_TEXT`: combo fires on selection, text fires on typing — choose correct event → **(P)** [R17]

### 26. wxFileName and Path Handling  **(P)** [R16]

```cpp
wxFileName path handling has Unicode and platform-specific issues: non-Latin filenames not found (#11404), long path support missing on Windows (#25033), and `wxConvAuto` reading flaws (#10670).
```

- [ ] Non-Latin filenames: `wxFileSystem::FindFirst()` may not find (#11404) — use `wxFileName` methods, not `wxFileSystem` → **(P)** [R16]

- [ ] Windows long paths (>260 chars): not supported (#25033) — use `\\?\` prefix manually or limit path length → **(P)** [R16]

- [ ] `wxConvAuto`: may misdetect encoding for ASCII files (#10670) — specify encoding explicitly → **(P)** [R16]

- [ ] `wxFileName::Normalize()`: multiple leading `..` bug fixed (#19109 era) — verify path normalization → **(P)** [R1]

- [ ] `wxFileDialog::GetPath()` with `wxFD_MULTIPLE`: asserts — use `GetPaths()` (see Item 9) → **(P)** [R1]

### 27. wxDC: Device Context Selection and Usage  **(P)** [R17]

The official dc.h overview defines strict rules for DC selection. Using the wrong DC type causes asserts, drawing artifacts, or missing updates.

- [ ] `wxPaintDC`: ONLY use inside `wxEVT_PAINT` handler — using outside asserts or draws nothing → **(P)** [R17]

- [ ] `wxClientDC`: for drawing outside paint events — never use inside `wxEVT_PAINT` handler → **(P)** [R17]

- [ ] `wxWindowDC`: paints whole window including decorations — not available on all non-MSW platforms → **(P)** [R17]

- [ ] `wxScreenDC`: paints on screen directly — rarely needed, usually wrong approach → **(P)** [R17]

- [ ] Parameterize drawing by `wxDC&` — same code works for screen, printer, bitmap → **(P)** [R17]

- [ ] `wxGraphicsContext` (newer): supports alpha, anti-aliasing — prefer over `wxDC` for new code → **(P)** [R17]

```cpp
// Good — wxPaintDC in paint handler
void OnPaint(wxPaintEvent&) {
    wxPaintDC dc(this);
    DrawContent(dc);
```
}

```cpp
// Good — wxClientDC outside paint handler
```

```cpp
void OnUpdate() {
```

```cpp
    wxClientDC dc(this);
```

```cpp
    DrawContent(dc);
```

}

```cpp
// Bad — wxPaintDC outside paint event (asserts)
```

```cpp
void OnUpdate() {
```

```cpp
    wxPaintDC dc(this);  // WRONG: only in wxEVT_PAINT
```

}

```cpp
// Bad — wxClientDC in paint handler (may cause artifacts)
```

```cpp
void OnPaint(wxPaintEvent&) {
```

```cpp
    wxClientDC dc(this);  // WRONG: use wxPaintDC in paint handler
```

}

### 28. wxValidator Lifecycle and Dialog Integration  **(P)** [R17]

The official validator.h overview documents specific lifecycle requirements. Validators must be cloned (copy ctor + `Clone()`), `InitDialog()` must be called for non-dialog windows, and XRC-loaded dialogs need manual validator assignment.

- [ ] Custom validators: must implement copy constructor AND `Clone()` — validators are cloned internally by wxWidgets → **(P)** [R17]

- [ ] Non-dialog windows: call `wxWindow::InitDialog()` explicitly before `Show()` — dialogs do this automatically → **(P)** [R17]

- [ ] `wxID_OK` default handler: calls `Validate()` then `TransferDataFromWindow()` — do NOT duplicate in your handler → **(P)** [R17]

- [ ] `wxWS_EX_VALIDATE_RECURSIVELY` is now default (3.1+) — `Validate()` recurses into child windows → **(P)** [R1]

- [ ] XRC-loaded dialogs: validators not in XRC — iterate controls and `SetValidator()` after `LoadDialog()` → **(P)** [R17]

```cpp
// Good — custom validator with Clone()
class MyValidator : public wxValidator {
```
public:
```cpp
    MyValidator(MyValidator&&) = default;
    MyValidator(const MyValidator&) = default;  // copy ctor required
    wxObject* Clone() const override { return new MyValidator(*this); }
    // ...
```
};

```cpp
// Good — InitDialog for non-dialog windows
```

m_panel->InitDialog();  // transfers data to controls

m_panel->Show(true);

```cpp
// Bad — missing Clone(), validator corrupts after copy
```

```cpp
class MyValidator : public wxValidator {
```

```cpp
    // no Clone() — wxWidgets clones internally, UB
```

};

### 29. wxScrolledWindow and Scrollbar Model  **(P)** [R17]

The official scrolling.h overview documents that base `wxWindow` does NOT handle scroll events — only `wxScrolledWindow` does. Mixing scrollbar APIs without `wxScrolledWindow` is a common mistake.

- [ ] Base `wxWindow` with scrollbars: does NOT scroll — use `wxScrolledWindow` for automatic scrolling → **(P)** [R17]

- [ ] `wxScrolledWindow`: use `SetScrollbars(pixelsPerUnitX, pixelsPerUnitY, ...)` or `SetVirtualSize()` + `SetScrollRate()` → **(P)** [R17]

- [ ] `wxGrid` implements its own scrolling — do NOT wrap in `wxScrolledWindow` → **(P)** [R17]

- [ ] `wxScrolled<T>`: use `CalcScrolledPosition()`/`CalcUnscrolledPosition()` for coordinate conversion → **(P)** [R17]

- [ ] `EnableScrolling(false)` disables scrollbar event generation but scrollbars may still appear visually → **(P)** [R17]

### 30. Bitmap Resource Macros and Platform Portability  **(P)** [R17]

The official bitmap.h overview documents that XPM has no alpha support, and `wxICON()`/`wxBITMAP()` macros handle platform differences. Using wrong macros causes invisible icons or resource-not-found errors.

- [ ] Use `wxICON(name)` and `wxBITMAP(name)` macros for cross-platform resources — NOT manual `#ifdef` blocks → **(P)** [R17]

- [ ] Alpha transparency: use `wxBITMAP_PNG(name)` — XPM and BMP have no alpha → **(P)** [R17]

- [ ] Windows `.ico` resources: `wxICON("name")` loads from resource section on MSW → **(P)** [R17]

- [ ] macOS: resources loaded from `Contents/Resources/` in app bundle → **(P)** [R17]

- [ ] `wxBitmapHandler`: rarely needed — use `wxImage` for loading most formats → **(P)** [R17]

---

### 31. wxAUI: wxAuiManager and wxAuiNotebook  **(P)** [R18]

```cpp
wxAUI has known stability issues: crash after closing all wxAuiNotebook tabs on macOS (#15417), `SavePerspective` ignores notebook state (#4363), docking crash on KDE4 (#4841), `wxAuiManager::UnInit()` must be called before frame destruction.
```

- [ ] `wxAuiManager::UnInit()` must be called before the managed frame is destroyed — otherwise crash → **(P)** [R18]

- [ ] wxAuiNotebook: closing all tabs may crash on macOS (#15417) — keep at least one tab or handle `wxEVT_AUINOTEBOOK_PAGE_CLOSED` → **(P)** [R18]

- [ ] `SavePerspective()`/`LoadPerspective()`: notebook state not saved correctly (#4363) — verify perspective restore → **(P)** [R18]

- [ ] wxAUI docking: crash on KDE4/KWin (#4841) — test docking on multiple Linux WMs → **(P)** [R18]

- [ ] `wxAuiPaneInfo`: use `Destroy()` not `delete` for pane windows — see Item 19 → **(P)** [R18]

- [ ] wxAUI uses native floating frames — do NOT subclass `wxAuiFloatingFrame` → **(P)** [R18]

### 32. wxFont Platform Differences  **(P)** [R18]

```cpp
wxFont behavior differs across platforms: `SetFaceName()` no longer sets face name on macOS (#19210), `SetFaceName()` resets font size on GTK (#10475), and font dialog behavior is platform-specific (#20325).
```

- [ ] `wxFont::SetFaceName()` on macOS: may not take effect (#19210) — use `wxFont(wxFontInfo().FaceName(name))` constructor → **(P)** [R18]

- [ ] `wxFont::SetFaceName()` on GTK: resets font size (#10475) — set size AFTER face name → **(P)** [R18]

- [ ] `wxFontInfo` (3.1+): prefer over old `wxFont` constructors for cleaner, less error-prone construction → **(P)** [R18]

- [ ] Font encoding: use `wxFontEncoding` with `wxFontMapper` for non-Unicode text — see Item 1 → **(P)** [R18]

- [ ] Fractional font sizes: supported since 3.1.5 — `wxFontInfo().PixelSize(wxSize(0, 14.5))` → **(P)** [R1]

```cpp
// Good — wxFontInfo (3.1+) for clean construction
wxFont font(wxFontInfo(12).FaceName("Arial").Bold());
```

```cpp
// Good — set size after face name on GTK
```

```cpp
wxFont font = *wxNORMAL_FONT;
```

font.SetFaceName("Arial");

font.SetPointSize(12);  // set AFTER face name

```cpp
// Bad — SetFaceName resets size on GTK
```

font.SetFaceName("Arial");  // size now reset

// font.SetPointSize(12);  // missing — size is wrong

### 33. wxTaskBarIcon Platform Limitations  **(P)** [R18]

```cpp
wxTaskBarIcon has significant platform differences: doesn't work on Ubuntu Unity/KDE Plasma 5 (#15644), icon deleted from tray causing crash (#17188), blurry icon on HiDPI GTK3 (#19048), and cannot be used to exit program (#10672).
```

- [ ] Linux: wxTaskBarIcon requires `libnotify`/AppIndicator support — may not work on Unity/Plasma 5 (#15644) → **(P)** [R18]

- [ ] Icon deleted from tray: crash if accessed after OS removes it (#17188) — handle `wxEVT_TASKBAR_LEFT_DOWN` carefully → **(P)** [R18]

- [ ] HiDPI: tray icon blurry on GTK3 (#19048) — provide multi-resolution icon → **(P)** [R18]

- [ ] Exiting program from tray icon: needs `Destroy()` or delayed delete (#10672) — see Item 19 → **(P)** [R18]

- [ ] macOS: `wxTaskBarIcon` uses `NSStatusItem` — different menu behavior than Windows → **(P)** [R18]

### 34. wxLog in Multi-threaded Applications  **(P)** [R19]

The official log.h overview documents that logging from worker threads is safe since 2.9.1, but messages are buffered and flushed in main thread. Custom log targets may produce out-of-order messages.

- [ ] `wxLog*` functions: safe from any thread since 2.9.1 — messages buffered until `wxLog::Flush()` in main thread → **(P)** [R19]

- [ ] Custom log target: messages from different threads may appear out of order — `wxLog` guarantees per-thread ordering only → **(P)** [R19]

- [ ] `wxLogNull`: only affects the CURRENT thread — other threads still log → **(P)** [R19]

- [ ] `wxLogGui` (default): shows messages in message box on flush — may show many messages at once → **(P)** [R19]

- [ ] `wxLog::EnableLogging(false)`: only affects current thread — use per-thread → **(P)** [R19]

- [ ] Early/late logging: `wxLogStderr` used automatically if GUI not available — custom log target must handle startup/shutdown → **(P)** [R19]

```cpp
// Good — logging from worker thread (safe, buffered)
void WorkerThread::Entry() {
    wxLogMessage("Progress: %d%%", progress);  // buffered, flushed in main thread
```
}

```cpp
// Good — suppress logging in current thread only
```

{

```cpp
    wxLogNull logNo;  // suppresses in THIS thread only
```

```cpp
    wxFile::Access("file.txt");  // no error log
```

}  // restored

```cpp
// Bad — assumes wxLogNull affects all threads
```

{

```cpp
    wxLogNull logNo;
```

```cpp
    // other threads still log — race condition if relying on suppression
```

}

### 35. wxPrintout and Printing  **(P)** [R18]

Printing has platform-specific crash risks: exception on Windows 11 from VS debugger (#23850), wxGTK printing crash (#14033), and macOS shows error message (#11779).

- [ ] wxMSW: printing to PDF may throw exception under debugger (#23850) — handle exceptions in print callback → **(P)** [R18]

- [ ] wxGTK: printing crash (#14033) — verify `GtkPrint` backend availability → **(P)** [R18]

- [ ] wxOSX: printing may show error message (#11779) — verify `NSPrintOperation` setup → **(P)** [R18]

- [ ] `wxPrintout::OnPrintPage()`: return false to stop, true to continue — do NOT throw → **(P)** [R18]

- [ ] `wxDC` for printing: use `wxPrintout::GetDC()`, not window DC — page coordinates differ → **(P)** [R18]

- [ ] `MapScreenSizeToDevice()` / `FitThisSizeToPageSize()`: call in `OnBeginPrinting()` for correct scaling → **(P)** [R18]

### 36. wxSplitterWindow  **(P)** [R18]

```cpp
wxSplitterWindow has known issues: can't remove sash on Windows (#24966), painting regression on macOS 11 (fixed in 3.1.5, PR #2306), and sash position persistence.
```

- [ ] Removing sash (unsplit): may fail on Windows (#24966) — call `Unsplit()` then `SetSashPosition(0)` → **(P)** [R18]

- [ ] macOS 11: painting regression fixed in 3.1.5 (PR #2306) — verify if upgrading → **(P)** [R1]

- [ ] `wxEVT_SPLITTER_SASH_POS_CHANGING`: mouse is captured — do NOT show modal dialog (see Item 15) → **(P)** [R18]

- [ ] `SetSashGravity()`: 0.0 to 1.0, controls sash position on resize — verify behavior on all platforms → **(P)** [R18]

- [ ] `UpdateSize()`: call after changing children to recalculate → **(P)** [R18]

### 37. wxGraphicsContext vs wxDC  **(P)** [R17]

`wxGraphicsContext` (newer) supports alpha, anti-aliasing, and transformations. `wxDC` (older) is simpler but less capable. Mixing them incorrectly causes artifacts.

- [ ] New drawing code: prefer `wxGraphicsContext` over `wxDC` for alpha/anti-aliasing → **(P)** [R17]

- [ ] `wxGraphicsContext::Create(wxDC*)`: bridge for mixed code — but DC drawing and GC drawing on same surface may conflict → **(P)** [R17]

- [ ] `wxGraphicsPath`: construct paths, then `StrokePath()`/`FillPath()` — do NOT mix with `wxDC::DrawLine` → **(P)** [R17]

- [ ] `wxGCDC`: wraps `wxGraphicsContext` as `wxDC` — use for code parameterized by `wxDC&` → **(P)** [R17]

- [ ] Anti-aliasing: `wxGraphicsContext` always anti-aliases; `wxDC` does not → **(P)** [R17]

### 38. wxConfig (Settings Persistence)  **(P)** [R18]

```cpp
wxConfig stores application settings. On Windows it uses the Registry; on Unix, INI files; on macOS, `~/Library/Preferences`. Known issues with 64-bit integers (fixed in 3.1.5) and registry path limits.
```

- [ ] 64-bit integers: supported since 3.1.5 (`Read/Write` with `wxLongLong`) — verify if upgrading → **(P)** [R1]

- [ ] Registry path: limited to 255 chars on Windows — long group names may fail → **(P)** [R18]

- [ ] `wxConfigBase::Get()`: returns global instance — `Set()` to replace with custom → **(P)** [R18]

- [ ] `wxFileConfig`: use for portable INI/XML files instead of Registry → **(P)** [R18]

- [ ] `Flush()`: call before exit to ensure data written — not automatic on all platforms → **(P)** [R18]

- [ ] Encoding: keys/values stored as wxString — verify encoding for non-ASCII (see Item 1) → **(P)** [R18]

### 39. wxStandardPaths and Application Deployment  **(P)** [R18]

`wxStandardPaths` returns platform-specific paths for resources, data, and config. Misusing it causes "file not found" errors on deploy.

- [ ] `GetResourcesDir()` / `GetLocalizedResourcesDir()`: macOS = `Contents/Resources/`, Windows = exe dir, Linux = `/usr/share/appname` → **(P)** [R18]

- [ ] `GetDataDir()`: macOS = `Contents/Resources/`, Linux = `/usr/share/appname`, Windows = exe dir → **(P)** [R18]

- [ ] `GetUserConfigDir()`: macOS = `~/Library/Preferences`, Linux = `~/.config`, Windows = `%APPDATA%` → **(P)** [R18]

- [ ] `GetExecutablePath()`: may return empty on some platforms — fallback to `argv[0]` → **(P)** [R18]

- [ ] `InstallPrefix`: `wxStandardPaths::Get().GetInstallPrefix()` returns wxString since 3.1.x → **(P)** [R1]

- [ ] macOS app bundle: resources must be in `Contents/Resources/`, NOT hardcoded paths → **(P)** [R18]

```cpp
// Good — platform-independent resource path
wxString resPath = wxStandardPaths::Get().GetResourcesDir() + "/myresource.dat";
```

```cpp
// Bad — hardcoded path, breaks on macOS/Linux
```

```cpp
wxString resPath = "/usr/share/myapp/myresource.dat";  // wrong on macOS
```

### 40. wxString Tokenization and Splitting  **(P)** [R18]

```cpp
wxString splitting has common pitfalls: `wxStringTokenize` vs `wxString::Split` behavior differences, empty token handling, and encoding issues.
```

- [ ] `wxStringTokenize`: returns `wxArrayString`, skips empty tokens by default — use `wxStringTokenizer::wxTOKEN_RET_EMPTY` to keep → **(P)** [R18]

- [ ] `wxString::Split()`: (3.1+) splits into `wxVector<wxString>`, keeps empty tokens → **(P)** [R18]

- [ ] `wxStringTokenizer` mode: `wxTOKEN_DEFAULT` skips empty, `wxTOKEN_RET_EMPTY` keeps, `wxTOKEN_RET_EMPTY_ALL` keeps leading/trailing → **(P)** [R18]

- [ ] Multi-char delimiters: `wxStringTokenizer` supports them, but behavior differs from `Split()` → **(P)** [R18]

- [ ] Encoding: tokens are `wxString` — verify encoding for non-ASCII (see Item 1) → **(P)** [R18]

```cpp
// Good — keep empty tokens
wxStringTokenizer tkz("a,,b,c", ",", wxTOKEN_RET_EMPTY);
while (tkz.HasMoreTokens()) {
    wxString token = tkz.GetNextToken();  // gets "a", "", "b", "c"
```
}

```cpp
// Good — Split (3.1+)
```

```cpp
wxVector<wxString> parts;
```

```cpp
wxString::Split("a,,b,c", ",", parts);  // keeps empty
```

```cpp
// Bad — default tokenizer skips empty tokens
```

```cpp
wxStringTokenizer tkz("a,,b,c", ",");  // gets "a", "b", "c" — empty lost
```

---

### 41. wxHTML Library Limitations  **(P)** [R20]

```cpp
wxHTML is NOT a full HTML browser — the official html.h overview states "it is not intended to be a high-end HTML browser. If you are looking for something like that use wxWebView." Limited CSS support, no JavaScript, limited HTML tag subset.
```

- [ ] wxHTML: use for rich text viewer (About box, help) — NOT for web browsing → **(P)** [R20]

- [ ] CSS: only `text-align`, `width`, `vertical-align`, `background` supported; `SPAN` adds `color`/`font-*`/`text-decoration` → **(P)** [R20]

- [ ] No JavaScript: for interactive web content, use `wxWebView` instead → **(P)** [R20]

- [ ] Custom tags: implement `wxHtmlWinTagHandler` subclass, register via `TAGS_MODULE` macros → **(P)** [R20]

- [ ] `wxHtmlHelpController`: `.hhp` Charset line incompatible with MS HTML Workshop — may be silently removed → **(P)** [R20]

- [ ] HTML help files: can be zipped (`.htb` = zipped `.hhp`+`.hhc`+`.hhk`+HTML) → **(P)** [R20]

- [ ] `SetRelatedFrame()`/`SetRelatedStatusBar()`: link HTML window to frame title and status bar → **(P)** [R20]

### 42. wxMenu and wxMenuBar Bitmap Handling  **(P)** [R20]

```cpp
wxMenuItem bitmap handling has historical issues: disabled item with bitmap looks enabled (#17282), submenu label can't be updated (#16246), bitmap disappears on Windows (#11595), and bitmap must be set before `Append()` on wxMSW (#9388).
```

- [ ] `wxMenuItem::SetBitmap()`: on wxMSW, call BEFORE `Append()` (#9388) — setting after append may not work → **(P)** [R20]

- [ ] Disabled menu item with bitmap: appears enabled (#17282) — verify visual state → **(P)** [R20]

- [ ] Submenu label update: `SetItemLabel()` may not work for submenu items (#16246) → **(P)** [R20]

- [ ] Menu item bitmap disappears on Windows (#11595) — use `wxBitmapBundle` (3.1.6+) for multi-resolution → **(P)** [R20]

- [ ] `wxMenuBar::SetLabelTop()`/`GetLabelTop()`: deprecated, use `SetMenuLabel()`/`GetMenuLabel()` → **(P)** [R20]

- [ ] macOS: menu items with `wxID_ABOUT`/`wxID_PREFERENCES`/`wxID_EXIT` auto-moved to app menu → **(P)** [R20]

### 43. wxSpinCtrl and wxSpinCtrlDouble  **(P)** [R20]

```cpp
wxSpinCtrlDouble has known issues: different size than wxSpinCtrl on MSW (#12767), doesn't wrap around (#10557), and GTK2 assertion failure on hold button (#18695).
```

- [ ] `wxSpinCtrlDouble`: different default size than `wxSpinCtrl` on wxMSW (#12767) — set explicit size → **(P)** [R20]

- [ ] `wxSpinCtrlDouble`: no wrap-around mode (#10557) — handle wrap manually → **(P)** [R20]

- [ ] GTK2: holding spin button up/down may trigger assertion (#18695) — verify on GTK2 → **(P)** [R20]

- [ ] `wxSpinCtrlDouble::SetIncrement()`: floating-point increment may accumulate rounding errors → **(P)** [R20]

- [ ] `wxEVT_SPINCTRL` vs `wxEVT_TEXT`: spin event fires on button, text event fires on typing — choose correct → **(P)** [R20]

- [ ] `wxSpinCtrl::SetRange()`: `min` must be < `max`; `wxSpinCtrlDouble` supports fractional ranges → **(P)** [R20]

### 44. Drag and Drop (wxDropTarget/wxDropSource)  **(P)** [R20]

Drag and drop has platform differences: `ConvertDragEffectToResult` invalid value for multi-column wxListCtrl (#18965), native drag image MSW-only (#14697), and wxDataViewCtrl drag/drop flexibility (#12583).

- [ ] `wxDropTarget::OnData()`/`OnDrop()`/`OnDragOver()`: must return `wxDragResult` — `wxDragCopy`/`wxDragMove`/`wxDragNone` → **(P)** [R20]

- [ ] `wxDropSource::DoDragDrop()`: returns `wxDragResult` — blocking call, do NOT call from event handler with mouse capture → **(P)** [R20]

- [ ] wxMSW: native drag image (`ImageList_BeginDrag`) — other platforms use `wxDragImage` (generic) → **(P)** [R20]

- [ ] `wxDropTarget` ownership: wxWidgets takes ownership — do NOT delete manually → **(P)** [R20]

- [ ] `wxDataViewCtrl` drag/drop: more flexible than `wxListCtrl` (#12583) — prefer for new code → **(P)** [R20]

- [ ] Custom data format: derive from `wxDataObjectSimple`, implement all 4 virtual methods → **(P)** [R20]

### 45. Creating Custom Widgets  **(P)** [R21]

The official customwidgets.h overview documents two approaches: generic (derive from `wxControl`/`wxWindow`) and native (separate implementations per platform). Generic widgets look non-native; native widgets require more work.

- [ ] Generic widget: derive from `wxControl` or `wxWindow` — works on all ports but looks non-native → **(P)** [R21]

- [ ] Native widget: separate header per platform (`wx/gtk/widget.h`, `wx/msw/widget.h`) + common base → **(P)** [R21]

- [ ] `DoGetBestSize()` or `DoGetBestClientSize()`: override for sizer integration → **(P)** [R21]

- [ ] `wxEVT_PAINT` handler: must use `wxPaintDC` — see Item 27 → **(P)** [R21]

- [ ] `wxDECLARE_DYNAMIC_CLASS()` + `wxDECLARE_EVENT_TABLE()`: required for XRC and event table support → **(P)** [R21]

- [ ] `Create()` method with full constructor signature: required for two-step construction → **(P)** [R21]

- [ ] Custom events: use `wxDEFINE_EVENT()` + `Bind()` — do NOT use old `wxNewEventType()` → **(P)** [R21]

### 46. C++ Exceptions in wxWidgets  **(P)** [R21]

The official exceptions.h overview documents that wxWidgets does NOT throw exceptions itself, and pre-2.4 versions were not exception-safe. 3.1.5 is exception-friendly but requires `wxUSE_EXCEPTIONS=1`.

- [ ] wxWidgets itself does NOT throw exceptions — exception safety is your responsibility → **(P)** [R21]

- [ ] `wxUSE_EXCEPTIONS=1` required (default on) — check `setup.h` or `--enable-exceptions` → **(P)** [R21]

- [ ] Override `wxApp::OnExceptionInMainLoop()` to catch exceptions from event handlers → **(P)** [R21]

- [ ] Override `wxApp::OnUnhandledException()` for exceptions outside main loop → **(P)** [R21]

- [ ] Exceptions in `wxYield()`: only safe with C++11 — override `StoreCurrentException()`/`RethrowStoredException()` for C++98 → **(P)** [R21]

- [ ] `--disable-exceptions`: leaner/faster library but no exception safety → **(P)** [R21]

- [ ] Exceptions through system event dispatch: unsafe on non-C++11 — may corrupt stack → **(P)** [R21]

```cpp
// Good — exception handling in wxApp
class MyApp : public wxApp {
    bool OnExceptionInMainLoop() override {
        try { throw; }
        catch (std::exception& e) {
            wxLogError("Unhandled: %s", e.what());
            return false;  // terminate
        }
    }
    void OnUnhandledException() override {
        try { throw; }
        catch (...) { wxLogError("Fatal unhandled exception"); }
    }
```
};

```cpp
// Bad — exception escapes event handler without handler
```

```cpp
void OnButton(wxCommandEvent&) {
```

```cpp
    throw std::runtime_error("oops");  // if no OnExceptionInMainLoop, crash
```

}

### 47. wxMediaCtrl  **(P)** [R20]

```cpp
wxMediaCtrl has platform-specific backends: GStreamer on Linux, DirectShow on Windows, AVFoundation on macOS. Wayland support requires specific backend (#2038 era), and codec availability varies.
```

- [ ] wxGTK: GStreamer backend — must install GStreamer plugins for media formats → **(P)** [R20]

- [ ] wxMSW: DirectShow backend — deprecated, may not support modern formats → **(P)** [R20]

- [ ] wxOSX: AVFoundation backend — requires macOS 10.9+ → **(P)** [R20]

- [ ] Wayland: media playback may require specific backend setup → **(P)** [R20]

- [ ] `wxMediaCtrl::Load()`: asynchronous — use `wxEVT_MEDIA_LOADED` event to know when ready → **(P)** [R20]

- [ ] `wxMediaCtrl::GetState()`: `wxMEDIASTATE_STOPPED`/`PLAYING`/`PAUSED` — check before commands → **(P)** [R20]

- [ ] Volume control: `SetVolume()` 0.0-1.0 — may not work on all backends → **(P)** [R20]

### 48. wxDatePickerCtrl and wxCalendarCtrl  **(P)** [R20]

```cpp
wxDatePickerCtrl has platform differences: `wxDP_ALLOWNONE` best size fixed in 3.1.5, `SetRange()` may assert, and macOS uses native picker with different behavior.
```

- [ ] `wxDP_ALLOWNONE`: best size calculation fixed in 3.1.5 — verify if upgrading from 3.1.4 → **(P)** [R1]

- [ ] `SetRange()`: may trigger bogus assert after `SetRange()` — workaround applied → **(P)** [R1]

- [ ] macOS: `wxDatePickerCtrl` uses native `NSDatePicker` — different appearance/behavior → **(P)** [R20]

- [ ] `wxCalendarCtrl`: native on Windows, generic on GTK/macOS — verify appearance → **(P)** [R20]

- [ ] `wxDatePickerCtrl::GetValue()`: returns `wxDateTime` — check `IsValid()` before using → **(P)** [R20]

- [ ] `SetDate()`/`GetDate()`: use `wxDateTime` — timezone handling matters → **(P)** [R20]

### 49. wxStatusBar and wxToolBar  **(P)** [R20]

```cpp
wxStatusBar fields and wxToolBar tool management have platform-specific behavior and known issues.
```

- [ ] `wxStatusBar::SetFieldsCount()`: call `SetStatusText()` after changing field count → **(P)** [R20]

- [ ] `wxStatusBar::SetStatusWidths()`: negative values = variable width, positive = fixed pixels → **(P)** [R20]

- [ ] wxMSW: `wxToolBar` height adapts to embedded controls (since 3.1) — may make toolbar taller → **(P)** [R1]

- [ ] `wxToolBar::AddTool()`: use `wxBitmapBundle` (3.1.6+) for multi-resolution/HiDPI → **(P)** [R20]

- [ ] `wxToolBar::Realize()`: must call after adding all tools → **(P)** [R20]

- [ ] wxMSW: toolbar tool tooltip ampersand preservation fixed in 3.1.5 → **(P)** [R1]

- [ ] `wxStatusBar` on macOS: may not support all field styles — verify → **(P)** [R20]

### 50. wxBitmapBundle (Multi-Resolution Bitmaps)  **(P)** [R1]

```cpp
wxBitmapBundle provides multi-resolution bitmap support for HiDPI displays. It replaces single wxBitmap for icons/toolbars/menus.
```

> **Version note:** `wxBitmapBundle` was introduced in **3.1.6**, NOT 3.1.5 (`include/wx/bmpbndl.h` does not exist at the v3.1.5 tag). On 3.1.5 use a single `wxBitmap` and accept the HiDPI blurriness, or require 3.1.6+.

- [ ] Use `wxBitmapBundle` for all UI bitmaps — provides automatic multi-resolution bitmap selection for the current DPI → **(P)** [R1]

- [ ] `wxBitmapBundle::FromBitmaps()`: create from multiple resolution bitmaps → **(P)** [R1]

- [ ] `wxBitmapBundle::FromSVG()`: create from SVG data for resolution-independent rendering → **(P)** [R1]

- [ ] `wxToolBar::AddTool()`: accepts `wxBitmapBundle` for automatic scaling → **(P)** [R1]

- [ ] `wxMenuItem::SetBitmap()`: accepts `wxBitmapBundle` for menu icons → **(P)** [R1]

- [ ] Backward compatibility: `wxBitmap` auto-converts to `wxBitmapBundle` → **(P)** [R1]

- [ ] `wxBitmapBundle::GetDefaultSize()`: returns logical (DIP) size → **(P)** [R1]

```cpp
// Good — wxBitmapBundle for HiDPI
wxBitmapBundle bundle = wxBitmapBundle::FromSVG(svgData, wxSize(16, 16));
```
toolBar->AddTool(wxID_OPEN, "Open", bundle);

```cpp
// Good — multiple resolutions
```

```cpp
wxBitmapBundle bundle = wxBitmapBundle::FromBitmaps(
```

```cpp
    wxBitmap("icon_16.png", wxBITMAP_TYPE_PNG),
```

```cpp
    wxBitmap("icon_32.png", wxBITMAP_TYPE_PNG)
```

);

```cpp
// Bad — single bitmap, blurry on HiDPI
```

toolBar->AddTool(wxID_OPEN, "Open", wxBitmap("icon_16.png", wxBITMAP_TYPE_PNG));

---

### 51. wxOSX Cocoa: Native Menu Bar vs In-Window Menu  **(P)** [R22]

On macOS, wxWidgets supports two menu bar modes: the native top-of-screen menu bar (default) and the in-window menu mode (`wxMacPreferencesEditor`). The `SetMenuBar()` behavior differs: on macOS the menu bar is application-global (not per-window), so calling `SetMenuBar()` on a frame replaces the global menu, not a per-window one.

- [ ] Do NOT assume `frame->SetMenuBar()` creates a per-window menu on macOS — it replaces the global application menu bar → **(P)** [R22]

- [ ] Use `wxMenuBar::MacSetCommonMenuBar()` for shared menu bars across all frames on macOS → **(P)** [R22]

- [ ] Test menu bar behavior on all three platforms — wxMSW uses in-window menus, wxGTK uses in-window or global (desktop-dependent), wxOSX uses global → **(P)** [R22]

- [ ] Handle `wxEVT_MENU_OPEN`/`wxEVT_MENU_CLOSE` for dynamic menus — macOS fires these differently than wxMSW → **(P)** [R22]

```cpp
// Good — explicit per-platform menu handling
```
#ifdef __WXOSX__
```cpp
    // macOS: menu bar is global, use common menu bar
    wxMenuBar* commonBar = CreateMenuBar();
    wxMenuBar::MacSetCommonMenuBar(commonBar);
```
#else
```cpp
    // Windows/Linux: per-window menu bar
    frame->SetMenuBar(CreateMenuBar());
```
#endif

- **Consequence:** Menu bar appears wrong or disappears on macOS; per-frame menu logic breaks cross-platform

- **Fix:** Use platform-conditional menu bar management; always test menu behavior on macOS

### 52. wxOSX: App Nap and Timer/Animation Freezing  **(P)** [R22]

macOS App Nap pauses background/occluded windows' timers, animations, and idle events to save energy. wxWidgets timers (`wxTimer`) and idle events may stop firing when the window is occluded or the app is in background, causing UI freezes, stopped animations, or stalled background processing.

- [ ] Do NOT rely on `wxTimer` for time-critical background processing on macOS — App Nap may pause it → **(P)** [R22]

- [ ] If timers must continue in background, disable App Nap via the `LSAppNapDisabled` (`Info.plist`) key or `NSProcessInfo` (`beginActivityWithOptions:reason:`) — wxWidgets 3.1.5 exposes NO API for this → **(P)** [R22]

- [ ] Use `wxEVT_IDLE` for background work that should resume when the app becomes active — App Nap resumes idle processing on activation → **(P)** [R22]

- [ ] Test animations and timers with the app in background (minimized, behind other windows) on macOS → **(P)** [R22]

```cpp
// Good — disable App Nap for time-critical apps
// wxWidgets 3.1.5 has no built-in API; use Info.plist or NSProcessInfo directly
// (1) Info.plist:  <key>LSAppNapDisabled</key>  <true/>
// (2) Runtime (Objective-C++ source), or via wxOSXObjcCType bridge:
//     [[NSProcessInfo processInfo]
//         beginActivityWithOptions:NSActivityUserInitiatedAllowingIdleSystemSleep
//                          reason:@"time-critical work"];
```

- **Consequence:** UI appears frozen, animations stop, timers miss deadlines when app is in background on macOS

- **Fix:** Disable App Nap for time-critical applications, or use idle events for resumable background work

### 53. wxOSX: File Association and Open With on macOS  **(P)** [R22]

On macOS, file type associations use the `CFBundleDocumentTypes` key in `Info.plist`, not registry entries (as on Windows). wxWidgets 3.1.5 does not automatically generate `Info.plist` entries for file associations — you must manually edit the `.plist` or use `wxStandardPaths` + bundle awareness.

- [ ] Do NOT use Windows registry-based file association on macOS — macOS uses `Info.plist` `CFBundleDocumentTypes` → **(P)** [R22]

- [ ] Handle `wxEVT_MENU_OPEN` or macOS open-file event: override `wxApp::MacOpenFile()` or handle `wxEVT_MENU_OPEN` with `wxID_OPEN` — the OS sends file-open requests via this path → **(P)** [R22]

- [ ] Test file double-click in Finder — verify the app receives the file path via `MacOpenFile()` → **(P)** [R22]

- [ ] Use `wxStandardPaths::GetResourcesDir()` to locate bundled resources inside `.app` bundle → **(P)** [R22]

```cpp
// Good — handle macOS file-open-from-Finder
class MyApp : public wxApp {
```
public:
```cpp
    void MacOpenFile(const wxString& fileName) override {
        // Called when user double-clicks a file in Finder
        OpenFileInMainWindow(fileName);
    }
```
};

```cpp
// Bad — assumes command-line args for file opening on macOS
```
// (works only when launched from terminal, not Finder)
```cpp
bool MyApp::OnInit() {
    if (argc > 1) OpenFile(argv[1]); // Fails for Finder-launched files
```
}

- **Consequence:** App cannot open files from Finder; file association appears broken on macOS

- **Fix:** Override `MacOpenFile()`, manually edit `Info.plist` for file types, use bundle resource paths

### 54. wxOSX: Retina/HiDPI Rendering on wxDC and wxGraphicsContext  **(P)** [R22]

On macOS Retina displays, `wxDC` operates in "backing store" coordinates (logical pixels), but `wxGLCanvas` may render in physical pixels depending on context creation flags. `wxGraphicsContext` on macOS uses Core Graphics which is natively HiDPI-aware. Mixing `wxDC` direct drawing with `wxGraphicsContext` on the same surface can cause scaling mismatches.

- [ ] Do NOT mix `wxDC` direct pixel drawing with `wxGraphicsContext` on the same surface on Retina — coordinate systems differ → **(P)** [R22]

- [ ] Use `wxDC::GetContentScaleFactor()` or `wxWindow::GetContentScaleFactor()` to get the scaling ratio for custom drawing → **(P)** [R22]

- [ ] For `wxGLCanvas` on macOS Retina, set `WX_GL_SAMPLE_BUFFER` and verify viewport dimensions match physical pixels → **(P)** [R3]

- [ ] Test custom-drawn controls on both Retina (2x) and non-Retina (1x) macOS displays → **(P)** [R22]

```cpp
// Good — scale-aware drawing
void MyCanvas::OnPaint(wxPaintEvent&) {
    wxPaintDC dc(this);
    double scale = dc.GetContentScaleFactor();
    dc.SetUserScale(scale, scale);
    // Now draw in logical pixels, rendering is crisp on Retina
    dc.DrawRectangle(10, 10, 100, 100);
```
}

- **Consequence:** Blurry rendering, misaligned graphics, or 2x-oversized custom controls on Retina displays

- **Fix:** Use `GetContentScaleFactor()`, avoid mixing DC types, test on Retina and non-Retina

---

### 54b. Platform DPI API Differences: GetContentScaleFactor vs GetDPIScaleFactor  **(P)** [R22][R25][R26][R31]

```cpp
wxWidgets provides multiple DPI query APIs with platform-specific value ranges. Choosing the wrong one can cause blurry rendering on fractional DPI or incorrect font sizes.
```

- [ ] On wxMSW, `GetContentScaleFactor()` returns fractional values (e.g. 1.25 for 125% scaling) — round/cast to integer for GL viewport and bitmap dimensions → **(P)** [R26]

- [ ] On wxOSX/wxGTK, `GetContentScaleFactor()` typically returns integer values (1.0 or 2.0) → **(P)** [R22]

- [ ] `wxWindow::GetDPIScaleFactor()` returns a **`double` ratio** (1.0 for 100%, 2.0 for 200%) — same scale as `GetContentScaleFactor()`, not an integer percentage → **(P)** [R31]

- [ ] `wxDisplay::GetPPI()` (returns `wxSize`) and `wxDisplay::GetScaleFactor()` (returns `double` ratio) query per-monitor DPI — use for multi-monitor DPI heterogeneity → **(P)** [R31]

- [ ] There is NO `MSWGetContentScaleFactor()` in 3.1.5 — use `GetContentScaleFactor()` (or `wxDisplay::GetScaleFactor()` for per-monitor DPI) → **(P)** [R26]

- [ ] Under X11 (non-Wayland wxGTK), `GDK_SCALE` and `GDK_DPI_SCALE` environment variables control HiDPI — test with both set and unset → **(P)** [R25]

```cpp
// Good — fractional DPI-aware GL viewport (round to nearest integer)
const wxSize size = GetClientSize();
double scale = GetContentScaleFactor();
glViewport(0, 0, static_cast<int>(size.x * scale + 0.5),
                    static_cast<int>(size.y * scale + 0.5));
// Good — per-monitor DPI query
int dpi = wxDisplay::GetFromWindow(this).GetPPI().x;       // wxSize::x (px/inch)
double scale = wxDisplay::GetFromWindow(this).GetScaleFactor(); // ratio (1.0/2.0)
```

### 55. wxOSX: Pasteboard Formats and DataObject Translation  **(P)** [R22]

macOS uses `NSPasteboard` with UTI (Uniform Type Identifiers) formats, while wxWidgets wraps this via `wxDataObject`. Custom `wxDataObject` subclasses must correctly map format IDs to macOS pasteboard types. Some standard formats (`wxDF_TEXT`, `wxDF_BITMAP`) have automatic translation, but custom formats require explicit `wxDataObject::GetFormat()` mapping.

- [ ] Do NOT assume custom `wxDataObject` formats work identically on macOS — pasteboard type mapping is required → **(P)** [R22]

- [ ] For custom clipboard formats on macOS, override `wxDataObject::GetFormat()` with the correct UTI → **(P)** [R22]

- [ ] Test drag-and-drop with custom data formats on all platforms — macOS UTI, Windows clipboard format ID, GTK target list differ → **(P)** [R22]

- [ ] Use `wxDataObjectComposite` for multi-format clipboard data — it handles format negotiation per-platform → **(P)** [R16]

- **Consequence:** Custom clipboard/drag data format not recognized on macOS; DnD silently fails

- **Fix:** Map custom formats to UTIs on macOS, use `wxDataObjectComposite` for multi-format

### 56. wxOSX: Modal Dialog Stacking and Sheet Behavior  **(P)** [R22]

On macOS, modal dialogs presented via `wxDialog::ShowModal()` may appear as "sheets" (attached to parent window) or as separate modal windows depending on the macOS version and dialog style flags. Sheet behavior changed across macOS versions (Big Sur, Monterey, Ventura), and `wxDialog` style flags may be interpreted differently.

- [ ] Do NOT assume `wxDialog::ShowModal()` always produces a centered floating dialog on macOS — sheet behavior may attach it to parent → **(P)** [R22]

- [ ] Test modal dialogs on multiple macOS versions (11, 12, 13+) — sheet vs window behavior differs → **(P)** [R22]

- [ ] Avoid `wxSTAY_ON_TOP` with modal dialogs on macOS — it can cause z-order issues with sheets → **(P)** [R22]

- [ ] Use `wxDialog` default styles (not `wxRESIZE_BORDER` unless needed) — macOS sheets ignore resize borders → **(P)** [R22]

- **Consequence:** Dialog appears as sheet (unexpected), z-order issues, dialog not centered, resize handles ignored on macOS

- **Fix:** Test on target macOS versions, avoid conflicting style flags, rely on native dialog behavior

### 57. wxOSX: wxTaskBarIcon and NSStatusItem Limitations  **(P)** [R18][R22]

`wxTaskBarIcon` on macOS uses `NSStatusItem` (menu bar item, right side of screen menu bar). It is NOT a dock icon or notification. Limitations: no custom tooltip on hover in some macOS versions, icon must be `NSImage` (template image for dark mode), and menu items may not fire `wxEVT_MENU` if using non-standard menu construction.

- [ ] Do NOT use `wxTaskBarIcon` for dock badges or notifications on macOS — it is a menu bar status item only → **(P)** [R18]

- [ ] Use template images (monochrome, `isTemplate = YES`) for status bar icons — macOS auto-adapts for dark mode → **(P)** [R22]

- [ ] Verify `wxEVT_MENU` fires from `wxTaskBarIcon` popup menu on macOS — some menu item styles may not fire events → **(P)** [R22]

- [ ] Test status bar icon visibility in both light and dark mode — non-template icons may be invisible in dark mode → **(P)** [R13]

- **Consequence:** Status bar icon invisible in dark mode, menu events not firing, wrong UI paradigm (dock vs menu bar)

- **Fix:** Use template images, verify menu events, understand `wxTaskBarIcon` = NSStatusItem on macOS

### 58. wxOSX: Window Level and Floating Windows (Palette Windows)  **(P)** [R22]

On macOS, "floating" windows (tool palettes, inspector windows that stay above the main window) use `NSPanel` with `floatingWindow` level. wxWidgets maps `wxSTAY_ON_TOP` to this, but behavior differs: the floating window may not receive keyboard focus by default (it becomes "key" only if it has a text field), and it may not participate in window cycling (Cmd+backtick).

- [ ] Do NOT assume `wxSTAY_ON_TOP` windows receive keyboard focus on macOS — `NSPanel` without text fields may be non-key → **(P)** [R22]

- [ ] For floating tool windows on macOS, set `wxWANTS_CHARS` and include at least one focusable control → **(P)** [R22]

- [ ] Test floating window behavior in Expose/Mission Control — `wxSTAY_ON_TOP` windows may not appear correctly → **(P)** [R22]

- [ ] Verify Cmd+backtick (next window) cycling includes/excludes floating windows as expected on macOS → **(P)** [R22]

- **Consequence:** Floating tool windows can't receive keyboard input, missing from window cycling, wrong z-order in Mission Control

- **Fix:** Add focusable controls, use `wxWANTS_CHARS`, test window cycling and Expose

### 59. wxOSX: NSApplication Delegation and wxApp Event Override  **(P)** [R22]

```cpp
wxWidgets on macOS (`wxOSX`) implements `wxApp` as an `NSApplicationDelegate`. Overriding `wxApp` virtual methods like `OnInit()`, `OnExit()` maps to `applicationDidFinishLaunching:`. However, some macOS-specific events (open-file, reopen, dock menu, service menu) require overriding `wxApp` methods: `MacOpenFile()`, `MacOpenURL()`, `MacReopenApp()`, `MacPrintFile()`.
```

- [ ] Override `wxApp::MacReopenApp()` to handle dock-click-when-already-open (re-open main window if minimized) → **(P)** [R22]

- [ ] Override `wxApp::MacOpenFile()` to handle Finder file-open → **(P)** [R22]

- [ ] Do NOT use `wxInitAllImageHandlers()` for macOS-only image types — macOS uses `NSImage` natively, some formats auto-supported → **(P)** [R1]

- [ ] Test app launch via Finder double-click, Dock click, and `open` command — each may trigger different `Mac*` callbacks → **(P)** [R22]

```cpp
// Good — handle dock re-open on macOS
class MyApp : public wxApp {
```
public:
```cpp
    void MacReopenApp() override {
        // User clicked dock icon while app was running
        wxFrame* frame = GetMainFrame();
        if (frame) {
            frame->Show(true);
            frame->Raise();
        }
    }
```
};

- **Consequence:** App doesn't re-open window on dock click, files don't open from Finder, dock menu missing

- **Fix:** Override `Mac*` methods on `wxApp`, test all macOS launch paths

### 60. wxOSX: wxColour and Native Color Panel  **(P)** [R22]

`wxColour` on macOS wraps `NSColor`. The native color panel (`NSColorPanel`) and color well UI elements are not directly exposed by wxWidgets 3.1.5. Using `wxColourDialog` produces a standard color picker, but it may not integrate with macOS system-wide color panel (which syncs across apps). Custom color pickers require platform-specific code.

- [ ] Do NOT expect `wxColourDialog` to sync with the macOS system color panel — wxWidgets uses a standard dialog, not the shared `NSColorPanel` → **(P)** [R22]

- [ ] For `wxColour` to `NSColor` conversion, use `wxColour::OSXGetNSColor()` on macOS — direct RGB may not match color space → **(P)** [R22]

- [ ] Test color display in sRGB and Display P3 color spaces on macOS — default `wxColour` may be sRGB-only → **(P)** [R22]

- [ ] Avoid hardcoded `RGB()` values for UI element colors — use `wxSystemSettings::GetColour()` for theme-adaptive colors → **(P)** [R13]

- **Consequence:** Colors look different across color spaces, custom color picker doesn't sync with system, theme-incompatible colors

- **Fix:** Use `OSXGetNSColor()` for conversion, `wxSystemSettings::GetColour()` for theme colors, test P3 displays

### 61. Cross-Platform Control Native Semantics  **(P)** [R23]

```cpp
wxWidgets maps controls to native widgets on each platform: `wxButton` becomes `HWND` + button on Windows, `GtkButton` on GTK, `NSButton` on macOS. This means visual appearance, default sizes, padding, and font metrics differ per platform. Hardcoded sizes or pixel-perfect layouts that look right on one platform will look wrong on another.
```

- [ ] Do NOT hardcode control dimensions in pixels — use `wxSize::Defaults` or `FromDIP()` for DPI-aware sizing → **(P)** [R23]

- [ ] Use `wxWindow::GetBestSize()` for natural control sizing — it returns the platform's native best size → **(P)** [R23]

- [ ] Avoid absolute positioning (`Move()`/`SetSize()`) for general UI — use sizers for responsive layout → **(P)** [R11]

- [ ] Test on all target platforms — a 80x24 button looks different on wxMSW vs wxGTK vs wxOSX → **(P)** [R23]

```cpp
// Good — DPI-aware, native sizing
wxButton* btn = new wxButton(parent, wxID_OK, "OK");
```
// Let sizer handle sizing, or use FromDIP (member on wxWindow, NOT a static on wxSize)
btn->SetMinSize(btn->FromDIP(wxSize(80, 24)));

- **Consequence:** UI looks broken, controls truncated or oversized on non-development platforms

- **Fix:** Use `BestSize`/`FromDIP`, sizers instead of absolute positioning, test cross-platform

### 62. Layout: Sizer Spacing, Borders, and Platform DPI  **(P)** [R23]

`wxSizer` border values are in device-independent pixels (DIP) on 3.1.5, but `wxSizer::Add()` border parameter interpretation can vary. `wxALL` adds border on all sides, but forgetting it or using `wxLEFT|wxRIGHT` for uniform spacing is less readable. The `wxBORDER` flags on sizer items affect visual appearance differently per platform (GTK adds visible borders, macOS may not).

- [ ] Use `wxSizerFlags().Border(wxALL, FromDIP(5))` for consistent spacing across DPI scales → **(P)** [R23]

- [ ] Do NOT use raw integer border values like `sizer->Add(control, 0, wxALL, 5)` — use `FromDIP(5)` for DPI awareness → **(P)** [R23]

- [ ] Use `wxSizer::SetMinSize()` + `Layout()` after dynamic content changes — sizers do not auto-layout on content change → **(P)** [R11]

- [ ] Call `Fit()` on the parent window after adding/removing sizer items dynamically → **(P)** [R23]

```cpp
// Good — DPI-aware sizer spacing
// FromDIP is a wxWindow member (or static needing a window pointer); there is no
// static wxWindow::FromDIP(int) overload, so call it on a concrete window:
wxSizerFlags flags = wxSizerFlags().Expand().Border(wxALL, parent->FromDIP(5));
```
sizer->Add(control, flags);

- **Consequence:** Inconsistent spacing across DPI scales, layout not updating after dynamic changes, cramped or oversized UI

- **Fix:** Use `SizerFlags().Border()` with `FromDIP`, call `Fit()`/`Layout()` after dynamic changes

### 63. wxNotebook Tab Ordering and Page Lifecycle  **(P)** [R23]

`wxNotebook` tab order is determined by insertion order. On macOS, the tab control uses `NSTabView` which may reorder tabs visually based on overflow handling. Page deletion during event handlers (`wxEVT_NOTEBOOK_PAGE_CHANGED`) can crash on macOS. Also, `wxNotebook::GetSelection()` may return stale values during `wxEVT_PAGE_CHANGING` on some platforms.

- [ ] Do NOT delete notebook pages during `wxEVT_NOTEBOOK_PAGE_CHANGED` — defer deletion via `CallAfter()` → **(P)** [R23]

- [ ] Use `wxEVT_NOTEBOOK_PAGE_CHANGING` (veto-able) vs `PAGE_CHANGED` (post-change) correctly — veto only in CHANGING → **(P)** [R23]

- [ ] Call `wxNotebook::InsertPage()` with correct image list index — image indices are not validated, wrong index = no icon → **(P)** [R23]

- [ ] Test tab overflow behavior — macOS and GTK handle overflow differently (scroll vs squeeze) → **(P)** [R23]

- **Consequence:** Crash on page deletion during event, stale selection value, missing tab icons, inconsistent overflow

- **Fix:** Defer deletion via `CallAfter()`, use correct event types, test tab overflow

### 64. Tooltip Behavior and wxToolTip Cross-Platform Differences  **(P)** [R23]

`wxToolTip` behavior differs across platforms: on macOS, tooltips appear after a delay and use the system tooltip service (which may clip long text); on Windows, `wxToolTip::SetDelay()` affects all tooltips globally; on GTK, tooltips use `GtkTooltip` which supports markup but has different auto-hide timing. Long tooltips may be truncated on macOS.

- [ ] Do NOT rely on tooltips for critical information — they may be truncated on macOS and have platform-specific delays → **(P)** [R23]

- [ ] Keep tooltip text short (under 80 characters) — macOS clips long tooltips → **(P)** [R23]

- [ ] Use `wxToolTip::Enable(false)` to temporarily disable tooltips during drag operations → **(P)** [R23]

- [ ] For rich tooltip content, consider `wxSimpleHelpProvider` or custom help instead of `wxToolTip` → **(P)** [R17]

- **Consequence:** Important info truncated or delayed, tooltips interfere with drag operations, inconsistent UX

- **Fix:** Keep tooltips short, disable during drag, use help provider for rich content

### 65. wxStaticBox Label Position and Layout  **(P)** [R23]

`wxStaticBox` (group box) label positioning differs across platforms: on Windows, the label is in the top-left border; on macOS, it may be bold or in a different position; on GTK, it uses `GtkFrame` which positions the label in the top border. Children must be added to `wxStaticBoxSizer`, not the `wxStaticBox` directly, or layout breaks.

- [ ] Always use `wxStaticBoxSizer` for children inside a `wxStaticBox` — adding children directly to `wxStaticBox` breaks layout → **(P)** [R23]

- [ ] Do NOT rely on label position being consistent — test on all platforms → **(P)** [R23]

- [ ] For empty label `wxStaticBox`, use `wxStaticBoxSizer(wxT(""))` — empty string works on all platforms → **(P)** [R23]

- [ ] Verify `wxStaticBox` border visibility in dark mode — GTK frame border may be invisible → **(P)** [R13]

```cpp
// Good — children in StaticBoxSizer
wxStaticBox* box = new wxStaticBox(parent, wxID_ANY, "Options");
wxStaticBoxSizer* sizer = new wxStaticBoxSizer(box, wxVERTICAL);
```
sizer->Add(new wxStaticText(box, wxID_ANY, "Label")); // parent = box
// NOT: new wxStaticText(parent, ...) — wrong parent breaks layout

- **Consequence:** Children overlap box border, layout breaks, label position unexpected, invisible borders in dark mode

- **Fix:** Use `wxStaticBoxSizer` for children, test label positions, verify dark mode

### 66. wxStatusBar Field Width Measurement  **(P)** [R23]

`wxStatusBar::SetStatusWidths()` uses field widths in pixels, but text rendering width varies by platform and DPI. Negative widths mean "stretch to fill remaining space." Using fixed positive widths for text fields can cause truncation on different platforms or DPI scales. `GetFieldRect()` should be used to get actual rendered field dimensions.

- [ ] Use negative widths for flexible/stretchable status bar fields → **(P)** [R23]

- [ ] Call `wxStatusBar::GetFieldRect()` to get actual field dimensions before drawing custom content → **(P)** [R23]

- [ ] Do NOT assume field width = `SetStatusWidths()` value — DPI scaling and text metrics change it → **(P)** [R23]

- [ ] Use `wxStatusBar::PushStatusText()`/`PopStatusText()` for temporary messages → **(P)** [R23]

```cpp
// Good — flexible last field, fixed first field
int widths[] = { 100, -1 }; // first=100px, second=stretch
```
statusBar->SetStatusWidths(2, widths);

- **Consequence:** Status text truncated, custom-drawn status content misaligned, inconsistent field sizes across DPI

- **Fix:** Use negative widths for stretch fields, `GetFieldRect()` for drawing, `Push/PopStatusText()` for temp messages

### 67. wxStaticText Wrapping and Label Measurement  **(P)** [R23]

`wxStaticText` wrapping behavior differs across platforms. `SetLabel()` with newlines is respected on all platforms, but automatic word wrapping (`wxST_ELLIPSIZE_END`, `wxST_NO_AUTORESIZE`) has different behaviors: wxMSW wraps at window width, wxGTK may not wrap without explicit `Wrap()`, and wxOSX wraps differently. `Wrap()` is the cross-platform way to set wrap width.

- [ ] Use `wxStaticText::Wrap(width)` for explicit wrapping — it works cross-platform, unlike relying on window width → **(P)** [R23]

- [ ] Use `wxST_ELLIPSIZE_END` for single-line labels that may need truncation → **(P)** [R23]

- [ ] Do NOT use `wxST_NO_AUTORESIZE` with dynamic labels — the label may be clipped if text grows → **(P)** [R23]

- [ ] Test multi-line `wxStaticText` on all platforms — wrapping behavior and line height differ → **(P)** [R23]

```cpp
// Good — explicit wrap width
wxStaticText* label = new wxStaticText(parent, wxID_ANY, "Long text...");
```
label->Wrap(300); // wrap at 300 pixels

- **Consequence:** Text not wrapping on GTK, label clipped, inconsistent line breaks, overflow layout

- **Fix:** Use `Wrap()`, `wxST_ELLIPSIZE_END` for truncation, test multi-line on all platforms

### 68. wxChoice vs wxComboBox Selection Semantics  **(P)** [R23]

`wxChoice` (dropdown list, read-only) and `wxComboBox` (dropdown with editable text) have different event semantics: `wxChoice` fires `wxEVT_CHOICE`, `wxComboBox` fires both `wxEVT_TEXT` (on text edit) and `wxEVT_COMBOBOX` (on dropdown selection). On macOS, `wxComboBox` may fire `wxEVT_TEXT` during programmatic selection, causing unexpected handlers.

- [ ] Use `wxChoice` for read-only selection, `wxComboBox` for editable — do NOT use `wxComboBox` with `wxCB_READONLY` if you don't need text editing → **(P)** [R23]

- [ ] Guard `wxEVT_TEXT` handlers in `wxComboBox` against programmatic `SetSelection()` — macOS fires `wxEVT_TEXT` on programmatic change → **(P)** [R16]

- [ ] Use `wxEVT_COMBOBOX` for selection-changed logic, not `wxEVT_TEXT` — `TEXT` fires on every keystroke → **(P)** [R23]

- [ ] Do NOT assume `wxChoice::GetSelection()` returns `wxNOT_FOUND` when empty — verify on all platforms → **(P)** [R23]

- **Consequence:** Event handlers fire unexpectedly, duplicate processing, wrong control for the use case

- **Fix:** Choose correct control type, guard against programmatic events, use `wxEVT_COMBOBOX` for selection

### 69. wxFileDialog and Platform-Specific File Dialog Behavior  **(P)** [R23]

`wxFileDialog` on 3.1.5 uses native file dialogs on each platform. On macOS, it uses `NSOpenPanel`/`NSSavePanel` which may not support all wildcard patterns. On Windows, the dialog can be modern (Vista+) or legacy depending on style flags. `wxFD_MULTIPLE` behavior differs: macOS returns paths via `GetPaths()`, Windows via `GetPath()` for the first and `GetFilenames()`.

- [ ] Use `wxFD_FILE_MUST_EXIST` for open dialogs to enforce file existence → **(P)** [R23]

- [ ] On macOS, wildcard patterns (`*.*`) may not work as expected — use `SetWildcard()` with specific extensions → **(P)** [R23]

- [ ] For multi-file selection, use `GetPaths()` (not `GetPath()`) to get all selected files → **(P)** [R23]

- [ ] Use `wxFD_OVERWRITE_PROMPT` for save dialogs to prompt before overwriting → **(P)** [R23]

```cpp
// Good — proper file dialog usage
wxFileDialog dlg(this, "Open File", "", "", "Text files (*.txt)|*.txt|All files (*.*)|*.*", wxFD_OPEN | wxFD_FILE_MUST_EXIST | wxFD_MULTIPLE);
if (dlg.ShowModal() == wxID_OK) {
    wxArrayString paths;
    dlg.GetPaths(paths); // Use GetPaths for multi-select
    for (const auto& p : paths) { /* ... */ }
```
}

- **Consequence:** Wildcard patterns not working on macOS, only first file retrieved in multi-select, no overwrite warning

- **Fix:** Use `GetPaths()` for multi-file, specific extensions on macOS, `wxFD_OVERWRITE_PROMPT` for save

### 70. wxProgressDialog and Cancel Button Cross-Platform Behavior  **(P)** [R23]

`wxProgressDialog` with `wxPD_CAN_SKIP` and `wxPD_CAN_ABORT` flags has platform-specific behavior: the skip/abort buttons may have different labels and positions on macOS vs Windows. The `Update()` return value indicates skip/abort status, but the timing of when these become true differs. On macOS, the progress dialog may not support `wxPD_APP_MODAL` correctly.

- [ ] Check the return value of `wxProgressDialog::Update()` — it returns `true` if the dialog was not skipped/aborted → **(P)** [R23]

- [ ] Do NOT assume `wxPD_APP_MODAL` blocks all windows on macOS — test modal behavior → **(P)** [R23]

- [ ] Call `Update()` regularly (not too frequently) to keep UI responsive — too infrequent causes frozen UI, too frequent causes flicker → **(P)** [R23]

- [ ] Use `Pulse()` for indeterminate progress (busy mode) → **(P)** [R23]

```cpp
// Good — check Update return value
wxProgressDialog dlg("Progress", "Working...", 100, this, wxPD_CAN_ABORT | wxPD_APP_MODAL);
for (int i = 0; i <= 100; i++) {
    if (!dlg.Update(i)) break; // User pressed Abort
    DoWork(i);
```
}

- **Consequence:** User can't cancel long operations, UI appears frozen, skip/abort not detected

- **Fix:** Check `Update()` return, use `Pulse()` for indeterminate, call regularly but not too frequently

### 71. wxRichTextCtrl Rendering and Performance  **(P)** [R24]

`wxRichTextCtrl` is a complex generic (non-native) control for rich text editing. Known issues in 3.1.5: performance degradation with large documents (>1000 paragraphs), image handling requires explicit `wxRichTextImageHandler` registration, and copy/paste of rich text to external applications (Word, browsers) may lose formatting because the clipboard format is wxWidgets-specific, not RTF/HTML.

- [ ] Register all required `wxRichTextImageHandler` types (`wxBITMAP_TYPE_PNG`, `wxBITMAP_TYPE_JPEG`, etc.) before loading documents → **(P)** [R24]

- [ ] For large documents, use `wxRichTextCtrl::SetEditable(false)` during bulk insertion to avoid per-character re-layout → **(P)** [R24]

- [ ] Do NOT expect clipboard copy to produce RTF/HTML — wxRichTextCtrl uses internal format; implement custom `wxRichTextPlainTextHandler` or `wxRichTextXMLHandler` for interchange → **(P)** [R24]

- [ ] Use `wxRichTextBuffer::ComputeFolding()` carefully — deep nesting can cause stack overflow on 32-bit builds → **(P)** [R24]

```cpp
// Good — register handlers before use
wxRichTextBuffer::AddHandler(new wxRichTextXMLHandler);
wxRichTextBuffer::AddHandler(new wxRichTextHTMLHandler);
wxRichTextBuffer::AddHandler(new wxRichTextPlainTextHandler);
```

- **Consequence:** Images don't display, clipboard paste loses formatting, performance lag with large docs, stack overflow

- **Fix:** Register handlers, disable edit during bulk ops, implement custom clipboard handlers

### 72. wxAnimationCtrl and Animated GIF Handling  **(P)** [R24]

`wxAnimationCtrl` displays animated GIFs. In 3.1.5, it uses a generic implementation that decodes frame-by-frame. Known limitations: only GIF format is supported (no APNG, no WebP animation), the control does not support transparency on all platforms correctly (GTK may render black background), and `SetAnimation()` while an animation is playing causes flicker.

- [ ] Use only GIF format for `wxAnimationCtrl` — APNG and WebP animation are NOT supported → **(P)** [R24]

- [ ] For transparent GIFs, test on GTK — black background may appear instead of transparency → **(P)** [R24]

- [ ] Call `Stop()` before `SetAnimation()` to avoid flicker → **(P)** [R24]

- [ ] Use `wxAnimation::Invalid` to check if animation loaded successfully before display → **(P)** [R24]

- **Consequence:** Unsupported format silently fails, black background on GTK, flicker on animation change

- **Fix:** Use GIF only, test transparency on GTK, stop before SetAnimation, validate loaded animation

### 73. wxHyperlinkCtrl Event Handling  **(P)** [R24]

`wxHyperlinkCtrl` fires `wxEVT_HYPERLINK` when clicked. On 3.1.5, the control uses `wxLaunchDefaultBrowser()` by default if no event handler is bound. Known issues: the link color may not adapt to dark mode (hardcoded blue), the control does not support right-click context menu for "copy link address", and on macOS the hover underline behavior may differ.

- [ ] Bind `wxEVT_HYPERLINK` to handle link clicks yourself — do NOT rely on default browser launch for internal links → **(P)** [R24]

- [ ] Use `SetNormalColour()`/`SetVisitedColour()` with theme-aware colors for dark mode support → **(P)** [R13]

- [ ] Do NOT expect right-click context menu — `wxHyperlinkCtrl` does not provide "copy link" on any platform → **(P)** [R24]

- [ ] Test hover/click behavior on macOS — underline and cursor change may differ from Windows → **(P)** [R24]

```cpp
// Good — custom event handler, theme-aware colors
```
hyperlink->Bind(wxEVT_HYPERLINK, &MyFrame::OnLink, this);
hyperlink->SetNormalColour(wxSystemSettings::GetColour(wxSYS_COLOUR_HOTLIGHT));

- **Consequence:** Links open in browser instead of app, invisible link in dark mode, missing context menu

- **Fix:** Bind event handler, set theme-aware colors, don't expect right-click menu

### 74. wxCollapsiblePane Layout and Event Behavior  **(P)** [R24]

`wxCollapsiblePane` provides a collapsible section with a button. On 3.1.5, known issues: `wxEVT_COLLAPSIBLEPANE_CHANGED` fires BEFORE the layout update, so `GetPane()` size is stale during the event handler. On GTK, the collapse animation may cause visual artifacts. On macOS, the button label alignment differs.

- [ ] Use `CallAfter()` to defer layout-dependent code after `wxEVT_COLLAPSIBLEPANE_CHANGED` — the pane size is stale during the event → **(P)** [R24]

- [ ] Do NOT call `Collapse()` during the `wxEVT_COLLAPSIBLEPANE_CHANGED` handler — recursive event → **(P)** [R24]

- [ ] Use `wxSizer::Fit()` on the parent window after collapse/expand to resize the containing window → **(P)** [R24]

- [ ] Test on GTK for visual artifacts during collapse animation → **(P)** [R24]

```cpp
// Good — defer layout after event
```
pane->Bind(wxEVT_COLLAPSIBLEPANE_CHANGED, [this](wxCommandEvent&) {
```cpp
    CallAfter([this]() {
        this->GetSizer()->Fit(this); // Now pane size is updated
    });
```
});

- **Consequence:** Layout not updated, recursive event, stale pane size, visual artifacts on GTK

- **Fix:** Use `CallAfter()`, call `Fit()` after collapse, avoid `Collapse()` in event handler

### 75. wxSearchCtrl and Cancel Button Behavior  **(P)** [R24]

`wxSearchCtrl` provides a search text field with optional cancel button and search menu. On 3.1.5, the cancel button fires `wxEVT_SEARCH_CANCEL` but the text is NOT automatically cleared — you must clear it yourself. On macOS, the search control uses native `NSSearchField` which has different visual appearance. `wxTE_PROCESS_ENTER` on `wxSearchCtrl` breaks tab traversal on macOS (#12808).

- [ ] Clear the search text manually in the `wxEVT_SEARCH_CANCEL` handler — the control does NOT auto-clear → **(P)** [R24]

- [ ] Do NOT use `wxTE_PROCESS_ENTER` on `wxSearchCtrl` on macOS — it breaks tab traversal (#12808) → **(P)** [R14]

- [ ] Use `wxEVT_SEARCH` (not `wxEVT_TEXT`) for search-triggered actions — `wxEVT_SEARCH` fires on Enter, `TEXT` fires on every keystroke → **(P)** [R24]

- [ ] Test search menu (`SetMenu()`) on macOS — native `NSSearchField` menu behavior differs → **(P)** [R24]

```cpp
// Good — clear on cancel, use correct event
```
searchCtrl->Bind(wxEVT_SEARCH_CANCEL, [searchCtrl](wxCommandEvent&) {
```cpp
    searchCtrl->SetValue(""); // Must clear manually
```
});
searchCtrl->Bind(wxEVT_SEARCH, &MyFrame::OnSearch, this);

- **Consequence:** Search text not cleared on cancel, tab traversal broken on macOS, search fires too frequently

- **Fix:** Clear text in cancel handler, use `wxEVT_SEARCH`, avoid `wxTE_PROCESS_ENTER` on macOS

### 76. wxInfoBar: Dismiss Button and Timeout Behavior  **(P)** [R24]

`wxInfoBar` is a banner-style notification widget. On 3.1.5, it does NOT auto-dismiss after a timeout — the user must click the dismiss button or you must call `Dismiss()` programmatically. The dismiss button may not appear on all platforms. On GTK, the info bar uses `GtkInfoBar` which has native theming but different button layout.

- [ ] Call `infoBar->Dismiss()` programmatically for auto-dismiss behavior — `wxInfoBar` has no built-in timeout → **(P)** [R24]

- [ ] Use `wxTimer` + `CallAfter()` for timed dismissal: show info bar, start timer, dismiss on timeout → **(P)** [R24]

- [ ] Do NOT assume dismiss button is visible on all platforms — test on GTK (uses `GtkInfoBar` native layout) → **(P)** [R24]

- [ ] Use `infoBar->SetShowButton(`wxID_CANCEL`, true)` to explicitly show a dismiss button → **(P)** [R24]

```cpp
// Good — timed info bar dismissal
```
infoBar->ShowMessage("Saved successfully", wxICON_INFORMATION);
```cpp
wxTimer* timer = new wxTimer(this, wxID_ANY);
```
timer->StartOnce(3000);
```cpp
Bind(wxEVT_TIMER, [this, timer](wxTimerEvent&) {
    infoBar->Dismiss();
    delete timer;
```
}, timer->GetId());

- **Consequence:** Info bar stays forever, no auto-dismiss, dismiss button missing on some platforms

- **Fix:** Use timer for auto-dismiss, explicitly set show button, test on GTK

### 77. wxBannerWindow: Usage and Limitations  **(P)** [R24]

`wxBannerWindow` provides a banner with gradient or bitmap background. It is a generic widget (non-native). On 3.1.5, it does not support text wrapping automatically — long titles are truncated. The gradient direction is fixed (top-to-bottom). It is primarily designed for wizard-like dialogs, not general UI.

- [ ] Keep banner title short — `wxBannerWindow` does NOT auto-wrap text → **(P)** [R24]

- [ ] Use `wxBannerWindow` only for wizard/dialog welcome pages — it is not suitable for general UI → **(P)** [R24]

- [ ] Use `SetBitmap()` for custom background — gradient is fixed direction (vertical) and cannot be customized → **(P)** [R24]

- [ ] Test banner appearance in dark mode — gradient colors may need adjustment → **(P)** [R13]

- **Consequence:** Title truncated, banner looks out of place in general UI, gradient direction wrong

- **Fix:** Keep title short, use only for wizard dialogs, use bitmap for custom backgrounds

### 78. wxActivityIndicator: Availability and Cross-Platform Behavior  **(P)** [R24]

`wxActivityIndicator` (added in **3.1.0**, available in 3.1.5) is a spinning indicator for indeterminate progress. On wxOSX it uses `NSProgressIndicator` (native spinner), on wxMSW it uses a generic animation, on wxGTK it uses `GtkSpinner`. Known limitation: the spinner only animates when the window is visible and focused — it may stop in background.

- [ ] `wxActivityIndicator` requires 3.1.0+ — do NOT use in projects targeting 3.0.x → **(P)** [R24]

- [ ] Call `Start()`/`Stop()` explicitly — the spinner does NOT auto-start → **(P)** [R24]

- [ ] Test on macOS — `NSProgressIndicator` may stop when window is in background (App Nap) → **(P)** [R22]

- [ ] For background-visible spinners, consider `wxGauge` with `Pulse()` or custom `wxAnimationCtrl` → **(P)** [R24]

- **Consequence:** Spinner not visible, not animating, stops in background on macOS

- **Fix:** Call `Start()` explicitly, test App Nap behavior, use `wxGauge::Pulse()` as fallback

### 79. wxCommandLinkButton: Platform Availability and Styling  **(P)** [R24]

`wxCommandLinkButton` displays a button with a title, subtitle, and optional default glyph. On wxMSW it uses the native command link button (Vista+). On wxGTK and wxOSX, it falls back to a regular button with multi-line text. The subtitle is NOT displayed on GTK/macOS fallback.

- [ ] Do NOT rely on subtitle being visible on GTK/macOS — the fallback only shows the main label → **(P)** [R24]

- [ ] Test on all platforms — the visual appearance differs significantly (native Vista button vs generic button) → **(P)** [R24]

- [ ] Use `SetMainLabelAndNote()` for setting both title and subtitle → **(P)** [R24]

- [ ] Consider using regular `wxButton` if subtitle is not critical to the UI → **(P)** [R24]

- **Consequence:** Subtitle invisible on GTK/macOS, inconsistent appearance, user misses important info

- **Fix:** Don't rely on subtitle cross-platform, test appearance, consider regular button

### 80. wxRearrangeList and wxEditableListBox  **(P)** [R24]

`wxRearrangeList` allows reordering items via up/down buttons. `wxEditableListBox` allows editing labels. Known issues: drag-to-reorder does not work (only buttons), the control uses `wxCheckListBox` internally which may not render checkboxes on all platforms correctly, and `wxEditableListBox::SetStrings()` replaces all items (no append).

- [ ] Do NOT expect drag-and-drop reordering in `wxRearrangeList` — only button-based reorder is supported → **(P)** [R24]

- [ ] Use `wxRearrangeList::Move()` programmatically for reordering → **(P)** [R24]

- [ ] For `wxEditableListBox`, use `SetStrings()` to replace all items, then `Append()` for individual additions → **(P)** [R24]

- [ ] Test checkbox rendering in `wxRearrangeList` on macOS — native `NSButton` checkbox may look different → **(P)** [R24]

- **Consequence:** Drag doesn't work, unexpected checkbox appearance, items not appended

- **Fix:** Use `Move()` for reorder, `SetStrings()` + `Append()` for editing, test checkboxes

### 81. wxGTK: Themes and CSS-like Styling Limitations  **(P)** [R25]

```cpp
wxGTK maps wxWidgets controls to GTK widgets, which are styled by GTK CSS themes. wxWidgets 3.1.5 does NOT provide direct CSS manipulation — colors set via `wxWindow::SetBackgroundColour()` may be overridden by the GTK theme. Using `SetForegroundColour()` on some widgets (buttons, labels) may not work because GTK theme has priority.
```

- [ ] Do NOT rely on `SetBackgroundColour()`/`SetForegroundColour()` on wxGTK — GTK CSS themes may override → **(P)** [R25]

- [ ] For custom colors on GTK, use `wxPanel` with `wxBG_STYLE_PAINT` and custom painting → **(P)** [R25]

- [ ] Test with multiple GTK themes (Adwaita, Adwaita-dark, custom) — appearance varies significantly → **(P)** [R25]

- [ ] Use `wxSystemSettings::GetColour()` for theme-adaptive colors instead of hardcoded values → **(P)** [R13]

- **Consequence:** Colors not applied, inconsistent appearance across GTK themes, custom styling overridden

- **Fix:** Use `wxSystemSettings::GetColour()`, custom paint for absolute control, test multiple themes

### 82. wxGTK: Dark Mode Detection and Theme Switching  **(P)** [R25]

GTK dark mode is controlled by the `gtk-application-prefer-dark` setting or `color-scheme` (GTK 4). wxWidgets 3.1.5 does NOT provide a native API to detect GTK dark mode. `wxSystemSettings::GetColour(wxSYS_COLOUR_WINDOW)` may return dark values, but this is not reliable for dark mode detection. GTK 3.12+ added `GtkSettings:gtk-application-prefer-dark`.

- [ ] Do NOT use `wxSystemSettings::GetColour(wxSYS_COLOUR_WINDOW)` to reliably detect dark mode on GTK — it is unreliable → **(P)** [R25]

- [ ] For GTK dark mode detection, use `wxSystemSettings::GetAppearance().IsDark()` (3.1.5+) or parse `GtkSettings` directly → **(P)** [R25]

- [ ] Test color scheme switching at runtime — GTK may not fire events to wxWidgets when user toggles dark mode → **(P)** [R25]

- [ ] Use `wxSystemSettings::GetAppearance().IsDark()` (3.1.5+) for cross-platform dark mode detection → **(P)** [R25]

```cpp
// Good — cross-platform dark mode detection (3.1.5+)
bool isDark = wxSystemSettings::GetAppearance().IsDark();
```

- **Consequence:** Dark mode not detected, UI stays wrong theme after user toggles, unreliable color reading

- **Fix:** Use `wxSystemSettings::GetAppearance().IsDark()`, test runtime theme switching

### 83. wxGTK: Window Resize Grip and WM Behavior  **(P)** [R25]

On GTK, window resize behavior depends on the window manager (Mutter, KWin, Xfwm, etc.). `wxRESIZE_BORDER` is the only reliable way to enable resize on GTK. The resize grip (bottom-right corner) is controlled by `wxRESIZE_BOX` on some WMs but not others. Some WMs (GNOME/Mutter) remove the resize grip entirely.

- [ ] Use `wxRESIZE_BORDER` for resize on GTK — do NOT rely on resize grip (`wxRESIZE_BOX`) → **(P)** [R25]

- [ ] Test window resizing on multiple WMs (Mutter, KWin, Xfwm) — behavior differs → **(P)** [R25]

- [ ] Do NOT set `wxMINIMIZE_BOX`/`wxMAXIMIZE_BOX` on child windows — these are top-level window only on GTK → **(P)** [R25]

- [ ] Handle `wxEVT_SIZE` for custom resize behavior — do NOT assume WM will size the window correctly → **(P)** [R25]

- **Consequence:** Can't resize window, resize grip missing, min/max box ignored on child windows

- **Fix:** Use `wxRESIZE_BORDER`, test on multiple WMs, handle `wxEVT_SIZE` for custom behavior

### 84. wxGTK: Overlay/Compositing and Transparency  **(P)** [R25]

GTK compositing (visual transparency, blur) requires a compositing WM (like Mutter with compositing enabled). wxWidgets 3.1.5 does NOT guarantee transparency support on GTK — `SetBackgroundStyle(wxBG_STYLE_TRANSPARENT)` may not work on non-compositing WMs. Result: black background instead of transparency.

- [ ] Verify the WM supports compositing before using transparent backgrounds on GTK → **(P)** [R25]

- [ ] Use `wxWindow::IsTransparentBackgroundSupported()` to check support before applying transparency → **(P)** [R25]

- [ ] For overlay windows, use `wxPopupWindow` (not `wxFrame`) — popup windows are transient and may have different compositing rules → **(P)** [R25]

- [ ] Test transparency on X11 without compositor (e.g., no compton/picom running) — fall back to opaque background → **(P)** [R25]

- **Consequence:** Black background instead of transparent, overlay looks wrong, compositing not available

- **Fix:** Check `IsTransparentBackgroundSupported()`, use `wxPopupWindow`, test without compositor

### 85. wxGTK: ibus/fcitx Input Method Integration  **(P)** [R25]

On GTK/Linux, input methods (ibus, fcitx, fcitx5) are integrated via GTK's `GtkIMContext`. wxWidgets 3.1.5 delegates to GTK for IME support. Known issues: pre-edit text may not display correctly in `wxTextCtrl`, and some IME configurations may cause double input or missing characters.

- [ ] Test with ibus and fcitx input methods on GTK — IME pre-edit and commit behavior may vary → **(P)** [R25]

- [ ] Use `wxTextEntry::IMContextInit()` if available (3.1.5) for explicit IME context setup → **(P)** [R25]

- [ ] Do NOT swallow `wxEVT_CHAR` during IME pre-edit — let the text go through the IME → **(P)** [R25]

- [ ] Handle `wxEVT_KEY_DOWN` and `wxEVT_CHAR` correctly — on GTK, IME may intercept key events → **(P)** [R25]

- **Consequence:** Double input, missing characters, pre-edit not displayed, IME not working

- **Fix:** Test with ibus/fcitx, don't swallow key events during pre-edit, use `IMContextInit()`

### 86. wxGTK: File Dialog and Native File Chooser  **(P)** [R25]

On GTK, `wxFileDialog` uses `GtkFileChooserDialog`. In 3.1.5, the default dialog uses the `GTK_FILE_CHOOSER_ACTION_OPEN` or `SAVE` action. Known issues: the dialog may not respect the initial directory on some GTK versions, and the wildcard filter may not work correctly (GTK uses MIME-type filters, not glob patterns).

- [ ] Use `SetWildcard()` with specific file extensions, not `*.*` — GTK uses MIME-type filters → **(P)** [R25]

- [ ] Use `SetDirectory()` explicitly — do NOT rely on GTK to remember the last directory → **(P)** [R25]

- [ ] For multi-file selection, use `wxFD_MULTIPLE` and `GetPaths()` — `GetFilenames()` does NOT include directory → **(P)** [R25]

- [ ] Test file dialog on different GTK versions (3.22, 3.24) — filter behavior differs → **(P)** [R25]

- **Consequence:** Wildcard doesn't work, wrong initial directory, multi-file missing paths, filter issues

- **Fix:** Use specific extensions, `SetDirectory()` explicitly, `GetPaths()` for multi-file

### 87. wxGTK: High-Resolution Scroll Events and Smooth Scrolling  **(P)** [R25]

On GTK, mouse wheel events (`wxEVT_MOUSEWHEEL`) use `GdkScrollDirection` which may be `GDK_SCROLL_SMOOTH` on modern GTK (3.4+). wxWidgets 3.1.5 maps smooth scroll to `wxEVT_MOUSEWHEEL` but the `GetWheelRotation()` value may be fractional. On touchpads, smooth scrolling produces many small-delta events.

- [ ] Accumulate `GetWheelRotation()` values for smooth scrolling — do NOT scroll by fixed amount per event → **(P)** [R25]

- [ ] Check `GetWheelAxis()` — touchpad horizontal scrolling uses a different axis → **(P)** [R25]

- [ ] Use `wxMouseEvent::GetLinesPerAction()` for line-based scrolling, `GetWheelRotation()` for pixel-based → **(P)** [R25]

- [ ] Test scroll behavior with touchpad (smooth) and mouse wheel (discrete) on GTK → **(P)** [R25]

```cpp
// Good — accumulate smooth scroll deltas
void OnMouseWheel(wxMouseEvent& event) {
    m_scrollAccumulator += event.GetWheelRotation();
    int lines = m_scrollAccumulator / event.GetWheelDelta();
    if (lines != 0) {
        ScrollByLines(lines);
        m_scrollAccumulator %= event.GetWheelDelta();
    }
```
}

- **Consequence:** Over-scrolling or under-scrolling on touchpads, horizontal scroll ignored, choppy scrolling

- **Fix:** Accumulate deltas, check axis, use `GetLinesPerAction()`, test touchpad + mouse wheel

### 88. wxGTK: wxApp::MainLoop and GMainContext  **(P)** [R25]

On GTK, `wxApp::MainLoop()` integrates with the GTK main loop (`gtk_main()`/`g_main_context_iteration()`). This means GTK-internal events (idle, timeout, I/O) are processed in the same loop as wxWidgets events. Known issue: calling `gtk_main_quit()` or `g_main_context_iteration()` manually can desync the wxWidgets event loop.

- [ ] Do NOT call `gtk_main()`/`gtk_main_quit()` directly — let wxWidgets manage the GTK main loop → **(P)** [R25]

- [ ] Use `wxEventLoopBase` for custom event loop behavior — do NOT use `g_main_context_iteration()` → **(P)** [R25]

- [ ] For idle work, use `wxIdleEvent` or `wxTimer` — do NOT use `g_timeout_add()` → **(P)** [R25]

- [ ] Test that `wxApp::Yield()` works correctly with GTK idle sources → **(P)** [R25]

- **Consequence:** Event loop desync, missed events, crash on quit, deadlock

- **Fix:** Let wxWidgets manage the GTK loop, use `wxIdleEvent`/`wxTimer` for idle work

### 89. wxGTK: Clipboard and Wayland/X11 Differences  **(P)** [R25]

On GTK/Wayland, clipboard behavior differs from X11. The clipboard is per-seat, not global. `wxClipboard::GetData()` may fail if the clipboard owner is a different Wayland client. The primary selection (middle-click paste) may not work the same on Wayland.

- [ ] Test clipboard operations on both X11 and Wayland — clipboard behavior differs → **(P)** [R25]

- [ ] Use `wxClipboard::Flush()` to retain clipboard content after the window closes (X11 only; Wayland may not support) → **(P)** [R25]

- [ ] Do NOT rely on primary selection (middle-click paste) on Wayland — it may not work → **(P)** [R25]

- [ ] Handle clipboard failure gracefully on Wayland — `GetData()` may return false → **(P)** [R25]

- **Consequence:** Clipboard doesn't work on Wayland, primary selection missing, data lost after window close

- **Fix:** Test on X11 + Wayland, handle `GetData()` failure gracefully, use `Flush()` on X11

### 90. wxGTK: DnD and Drag Icon Customization  **(P)** [R25]

On GTK, drag-and-drop uses `GtkDragSource`/`GtkDropTarget` (GTK 4) or `gtk_drag_begin` (GTK 3). wxWidgets 3.1.5 uses the GTK 3 API. The drag icon (shown during drag) defaults to the source widget's snapshot. Customizing it requires `wxDropSource::SetIcon()` which maps to `gtk_drag_source_set_icon_`. On Wayland, the drag icon may not appear.

- [ ] Use `wxDropSource::SetIcon()` to customize the drag icon on GTK → **(P)** [R25]

- [ ] Test DnD on Wayland — drag icon may not appear → **(P)** [R25]

- [ ] Do NOT start DnD during `wxEVT_LEFT_DOWN` without checking drag threshold — GTK may not fire `wxEVT_LEFT_UP` → **(P)** [R25]

- [ ] Use `wxDragImage` as alternative for custom drag visuals → **(P)** [R25]

- **Consequence:** Wrong drag icon, no icon on Wayland, DnD stuck, missing mouse-up event

- **Fix:** Use `SetIcon()`, test Wayland, check drag threshold, consider `wxDragImage`

### 91. wxMSW: High DPI and Per-Monitor DPI Awareness  **(P)** [R26]

On Windows 10 1703+, per-monitor DPI awareness allows each monitor to have its own DPI. wxWidgets 3.1.5 exposes `wxWindow::GetDPI()` and `FromDIP()/ToDIP()` for per-monitor DPI queries. NOTE: the `wxEVT_DPI_CHANGED` event / `wxDPIChangedEvent` class and `wxBitmapBundle` were added in **3.1.6** — they do NOT exist in 3.1.5. Known issues: not all controls correctly handle DPI changes at runtime (move window to different monitor), and `wxBitmap` loaded from resources may not scale automatically.

- [ ] Use `wxBitmapBundle` (3.1.6+, NOT 3.1.5) for multi-resolution bitmaps that auto-scale on DPI change → **(P)** [R26]

- [ ] Handle `wxEVT_DPI_CHANGED` (3.1.6+ only; on 3.1.5 you must handle `wxEVT_SIZE`/`wxEVT_DISPLAY_CHANGED` and re-query DPI manually) to re-layout and rescale custom-drawn content → **(P)** [R26]

- [ ] Use `wxWindow::FromDIP()`/`ToDIP()` for all pixel-to-logical conversions (available in 3.1.5) → **(P)** [R26]

- [ ] Test by dragging window between monitors with different DPI (100% and 200%) → **(P)** [R26]

```cpp
// Good — handle DPI change (requires 3.1.6+ for wxEVT_DPI_CHANGED / wxDPIChangedEvent)
Bind(wxEVT_DPI_CHANGED, [this](wxDPIChangedEvent& event) {
    GetSizer()->Fit(this); // Re-layout on DPI change
    Refresh(); // Redraw with new scaling
});
```

- **Consequence:** Blurry UI, controls wrong size after monitor move, pixel-perfect drawing broken

- **Fix:** Use `wxBitmapBundle` (3.1.6+), handle `wxEVT_DPI_CHANGED` (3.1.6+), `FromDIP()`/`ToDIP()` (3.1.5+) for conversions

### 92. wxMSW: wxMSW-specific Control Styles and Visual Themes  **(P)** [R26]

On wxMSW, wxWidgets uses native Win32 controls. Visual styles (XP, Vista, Win10/11) are applied automatically, but only if the manifest enables `Microsoft.Windows.Common-Controls`. Without the manifest, controls render in classic (pre-XP) style. wxWidgets 3.1.5 does not automatically embed the manifest.

- [ ] Embed `Microsoft.Windows.Common-Controls` v6 manifest in the application — otherwise controls appear in classic style → **(P)** [R26]

- [ ] NOTE: `wxApp::MSWEnableDarkMode()` does NOT exist in 3.1.5 (added only in unreleased 3.3/master, with `wxDarkModeSettings`). For 3.1.5 dark mode on Windows, use undocumented Win32 `SetPreferredAppMode`/`AllowDarkModeForWindow` or wait for 3.3+ → **(P)** [R13]

- [ ] Test with visual styles enabled and disabled — appearance differs significantly → **(P)** [R26]

- [ ] Do NOT call `EnableVisualStyles()` (Win32 API) directly — let the manifest handle it → **(P)** [R26]

- **Consequence:** Controls in classic style, no native dark mode in 3.1.5, inconsistent appearance

- **Fix:** Embed common-controls v6 manifest; for Windows dark mode use Win32 APIs directly (no wxWidgets API in 3.1.5) or upgrade to 3.3+

### 93. wxMSW: wxMSW Header Column Click and Sort Indicator  **(P)** [R26]

On wxMSW, `wxListCtrl` in report mode uses `LVM_SETCOLUMN` for header. Setting sort indicator (up/down arrow) requires `LVM_SETCOLUMN` with `fmt` flags (`LVCFMT_IMAGE`). wxWidgets 3.1.5 does not expose this directly — you must use `wxListCtrl::GetHandle()` and send raw Win32 messages.

- [ ] Use `wxListCtrl::GetHandle()` + `ListView_SetColumn()` for sort indicator on wxMSW → **(P)** [R26]

- [ ] Consider `wxDataViewCtrl` for built-in sort indicator support → **(P)** [R4]

- [ ] Do NOT rely on `wxListCtrl::SetColumnWidth()` auto-sizing on wxMSW — use `SetColumnWidth(col, wxLIST_AUTOSIZE)` or `wxLIST_AUTOSIZE_USEHEADER` → **(P)** [R26]

- [ ] Test header click behavior on all platforms — wxMSW, wxGTK, wxOSX differ → **(P)** [R26]

```cpp
// Good — set sort indicator via Win32 API on wxMSW
```
#ifdef __WXMSW__
```cpp
    HWND hwnd = (HWND)listCtrl->GetHWND();
    LVCOLUMN col;
    col.mask = LVCF_FMT;
    col.fmt = LVCFMT_IMAGE | LVCFMT_LEFT | (descending ? LVCFMT_BITMAP_ON_RIGHT : 0);
    ListView_SetColumn(hwnd, colIndex, &col);
```
#endif

- **Consequence:** No sort indicator, columns wrong width, inconsistent header behavior

- **Fix:** Use Win32 messages for sort indicator, consider `wxDataViewCtrl`, use `wxLIST_AUTOSIZE`

### 94. wxMSW: wxTextCtrl RTF and Rich Text Mode  **(P)** [R26]

On wxMSW, `wxTextCtrl` with `wxTE_RICH` or `wxTE_RICH2` uses the Win32 Rich Edit control (`RICHEDIT_CLASS`). `wxTE_RICH2` uses Rich Edit 2.0/3.0 (msftedit.dll). Known issues: `wxTE_RICH` text is limited to 64KB in some configurations, and `GetRange()` on large text in rich mode may be slow. Also, `wxTE_RICH` controls may not handle Unicode correctly in all Windows versions.

- [ ] Use `wxTE_RICH2` (not `wxTE_RICH`) for large text — `wxTE_RICH` has 64KB limit → **(P)** [R26]

- [ ] For Unicode support on wxMSW, use `wxTE_RICH2` — `wxTE_RICH` may corrupt Unicode → **(P)** [R26]

- [ ] Do NOT use `wxTextCtrl::GetRange()` for large text — use `GetValue()` which is optimized → **(P)** [R26]

- [ ] Test with text > 1MB — performance may degrade significantly in rich mode → **(P)** [R26]

- **Consequence:** Text truncated at 64KB, Unicode corruption, performance lag with large text

- **Fix:** Use `wxTE_RICH2`, `GetValue()` for large text, test with > 1MB

### 95. wxMSW: Registry Access and wxRegKey  **(P)** [R26]

`wxRegKey` provides Windows registry access. In 3.1.5, `wxRegKey` uses `RegCreateKeyEx`/`RegOpenKeyEx`. Known issues: 32-bit applications on 64-bit Windows need `KEY_WOW64_64KEY` flag to access the 64-bit registry view. `wxRegKey` does NOT set this flag by default.

- [ ] For 32-bit app accessing 64-bit registry, use `wxRegKey::SetNativeAccess(WOW64_64KEY)` or open with `KEY_WOW64_64KEY` → **(P)** [R26]

- [ ] Do NOT hardcode registry paths — use `wxStandardPaths` for known paths → **(P)** [R26]

- [ ] Handle `wxRegKey` open failure gracefully — registry access may be denied by UAC → **(P)** [R26]

- [ ] For settings storage, prefer `wxConfig`/`wxFileConfig` over direct registry access for portability → **(P)** [R18]

```cpp
// Good — access 64-bit registry from 32-bit app
wxRegKey key(wxRegKey::HKLM, "SOFTWARE\\MyApp");
```
key.SetNativeAccess(WOW64_64KEY); // Access 64-bit view
```cpp
if (key.Exists()) { /* ... */ }
```

- **Consequence:** Registry values not found (wrong view), access denied, non-portable settings

- **Fix:** Use `KEY_WOW64_64KEY` for 64-bit access, `wxStandardPaths` for paths, `wxConfig` for settings

### 96. wxMSW: wxMSW-specific File Dialog and IFileDialog  **(P)** [R26]

On Windows Vista+, the modern file dialog (`IFileDialog`) is used by wxWidgets 3.1.5 by default. Known issues: the modern dialog may not support all `wxFileDialog` features (e.g., `wxFileDialog::SetFilterIndex()` may not work), and the dialog may appear in the taskbar (unexpected for modal dialogs).

- [ ] Use `wxFD_CHANGE_DIR` to change the app working directory on file selection — may not work with IFileDialog → **(P)** [R26]

- [ ] Test `SetFilterIndex()` on Windows 10/11 — may not select the correct filter in modern dialog → **(P)** [R26]

- [ ] NOTE: there is NO `wxFD_USE_LEGACY_DIALOG` style flag in wxWidgets. In 3.1.5 the modern `IFileDialog` is always used on Vista+; to force the legacy `GetOpenFileName` dialog you must build wxWidgets with `wxUSE_IFILEOPENDIALOG=0` or call the Win32 API directly → **(P)** [R26]

- [ ] Do NOT assume the file dialog is modal — on some Windows versions, it may appear in taskbar → **(P)** [R26]

- **Consequence:** Filter index wrong, working directory not changed, dialog in taskbar (looks non-modal)

- **Fix:** Test modern dialog features, disable `IFileDialog` at wxWidgets build time if the legacy dialog is required, don't assume strict modality

### 97. wxMSW: wxMSW Task Dialog and Modern Message Box  **(P)** [R26]

`wxMessageDialog` on Windows uses `MessageBox()` by default. On Vista+, `TaskDialog()` or `TaskDialogIndirect()` provides richer UI (icons, command links, progress bar). wxWidgets 3.1.5 does NOT automatically use `TaskDialog` — it falls back to `MessageBox()` which has limited functionality.

- [ ] Use `wxRichMessageDialog` (3.1.5+) for enhanced message boxes with checkboxes and expandable text → **(P)** [R26]

- [ ] For command-link buttons in dialogs, use `wxRichMessageDialog` with custom buttons → **(P)** [R26]

- [ ] Do NOT expect `wxYES_DEFAULT`/`wxNO_DEFAULT` to work identically across platforms — wxMSW and wxGTK differ → **(P)** [R26]

- [ ] Test message dialog icons on all platforms — some icons may not appear on wxGTK → **(P)** [R26]

- **Consequence:** Limited message box UI, no command links, inconsistent default button behavior

- **Fix:** Use `wxRichMessageDialog`, test icons and defaults cross-platform

### 98. wxMSW: wxMSW Aero/DWM Glass and Custom Frame  **(P)** [R26]

On Windows Vista+, Desktop Window Manager (DWM) provides glass effect (`DwmExtendFrameIntoClientArea`). wxWidgets 3.1.5 does NOT provide a built-in API for DWM glass. Using `SetBackgroundStyle(wxBG_STYLE_PAINT)` and custom painting on the glass area is the workaround, but it requires DWM API calls.

- [ ] For DWM glass effect, call `DwmExtendFrameIntoClientArea()` via `wxDynamicLibrary` → **(P)** [R26]

- [ ] Use `wxBG_STYLE_PAINT` for the glass area — default background erases the glass → **(P)** [R26]

- [ ] Test on Windows 7 (full DWM glass), Windows 10/11 (glass may not work the same) → **(P)** [R26]

- [ ] Do NOT assume glass is available — check `DwmIsCompositionEnabled()` first → **(P)** [R26]

```cpp
// Good — enable DWM glass
wxDynamicLibrary dwm("dwmapi.dll");
```
typedef HRESULT (*DwmExtendFrame_t)(HWND, const MARGINS*);
```cpp
auto pfn = (DwmExtendFrame_t)dwm.GetSymbol("DwmExtendFrameIntoClientArea");
if (pfn) {
    MARGINS m = {0,0,0,1}; // extend to bottom
    pfn((HWND)GetHWND(), &m);
```
}

- **Consequence:** Glass effect not working, default erase destroys glass, inconsistent on Win10/11

- **Fix:** Use `wxDynamicLibrary` for DWM API, `wxBG_STYLE_PAINT`, check composition enabled

### 99. wxMSW: wxMSW Clipboard Format Registration  **(P)** [R26]

On Windows, custom clipboard formats must be registered with `RegisterClipboardFormat()`. wxWidgets 3.1.5 wraps this via `wxCustomDataObject` which auto-registers the format name. However, the format ID may differ between sessions and must be re-registered each time.

- [ ] Use `wxCustomDataObject("MyFormat")` — the format name is persistent, the ID is not → **(P)** [R26]

- [ ] Do NOT cache clipboard format IDs across sessions — re-register each time → **(P)** [R26]

- [ ] Use `wxDataObjectComposite` to provide multiple formats (custom + standard) for maximum compatibility → **(P)** [R16]

- [ ] Test clipboard with apps that use the same format name — format matching is by name, not ID → **(P)** [R26]

- **Consequence:** Clipboard data not recognized, format ID mismatch, DnD fails with external apps

- **Fix:** Use format names (not IDs), `wxCustomDataObject` for auto-registration, `wxDataObjectComposite`

### 100. wxMSW: wxMSW Accessibility (UI Automation)  **(P)** [R26]

`wxAccessible` on wxMSW provides limited UI Automation support via `IAccessible` (legacy). wxWidgets 3.1.5 does NOT support modern UI Automation (UIA) — it uses the older MSAA (`IAccessible`). Modern screen readers (Narrator, NVDA) prefer UIA and may not fully interact with wxWidgets controls.

- [ ] Do NOT rely on `wxAccessible` for modern screen reader support — it uses legacy MSAA → **(P)** [R26]

- [ ] Test with NVDA and Narrator on Windows — some controls may not be announced correctly → **(P)** [R26]

- [ ] Use native control semantics where possible — `wxButton`, `wxTextCtrl` have better default accessibility than custom controls → **(P)** [R26]

- [ ] For custom-drawn controls, implement `wxAccessible` to provide at least name and role → **(P)** [R26]

- **Consequence:** Screen readers don't announce controls, accessibility non-compliant, custom controls invisible to assistive tech

- **Fix:** Use native controls, implement `wxAccessible` for custom controls, test with NVDA/Narrator

### 101. wxThreadHelper and wxThread Join Behavior  **(P)** [R27]

`wxThreadHelper` simplifies worker threads by managing thread lifecycle. Known issue in 3.1.5: `wxThreadHelper::Wait()` may block forever if the thread does not check for `TestDestroy()`. The `wxThread::Delete()` method (graceful shutdown) relies on `TestDestroy()` returning true, which the thread must check.

- [ ] Check `TestDestroy()` in the thread loop and exit promptly when true → **(P)** [R27]

- [ ] Use `wxThreadHelper::Wait()` with a timeout — do NOT wait forever → **(P)** [R27]

- [ ] Do NOT call `wxThread::Kill()` to terminate threads — it leaks resources and may corrupt state → **(P)** [R27]

- [ ] Use `wxQueueEvent`/`wxPostEvent` (not direct GUI calls) from worker threads to communicate results → **(P)** [R5]

```cpp
// Good — check TestDestroy in thread loop
```
void* MyThread::Entry() {
```cpp
    while (!TestDestroy()) {
        DoWork();
        wxThread::This()->Sleep(100);
    }
    return nullptr;
```
}

- **Consequence:** Thread hangs forever, resource leak on Kill, GUI crash from direct access

- **Fix:** Check `TestDestroy()`, use `Wait()` with timeout, use `wxPostEvent` for GUI communication

### 102. wxCriticalSection and wxMutex: RAII and Deadlock  **(P)** [R27]

`wxCriticalLocker` (RAII wrapper for `wxCriticalSection`) is the recommended way to use critical sections. Known issues: `wxCriticalSection::Enter()` without matching `Leave()` causes deadlock, and nested `Enter()` on the same critical section from the same thread is NOT supported (wxCriticalSection is not recursive by default).

- [ ] Use `wxCriticalLocker` (RAII) for critical section — never manual `Enter()`/`Leave()` → **(P)** [R27]

- [ ] Use `wxCriticalSection` with `wxCRIT_RECURSIVE` flag if the same thread needs to re-enter → **(P)** [R27]

- [ ] Do NOT hold `wxCriticalSection` across `wxPostEvent` — the event handler may try to acquire the same lock → **(P)** [R27]

- [ ] Use `wxMutex` for cross-process locking (named mutex), `wxCriticalSection` for single-process → **(P)** [R27]

```cpp
// Good — RAII critical section
wxCriticalLocker locker(m_cs); // Auto-released at scope end
```
// Do work inside critical section

- **Consequence:** Deadlock from unmatched Enter/Leave, non-recursive re-entry crash, lock held during event dispatch

- **Fix:** Use `wxCriticalLocker`, `wxCRIT_RECURSIVE` for re-entrant, don't hold lock across events

### 103. wxCondition and wxSemaphore: Signaling and Spurious Wakeups  **(P)** [R27]

`wxCondition` (condition variable) may have spurious wakeups on some platforms — `Wait()` may return even if no signal was sent. Always use `Wait()` with a predicate loop (check condition after waking). `wxSemaphore` has similar behavior on some platforms.

- [ ] Use `wxCondition::Wait()` with a predicate loop — never assume condition is met after wake → **(P)** [R27]

- [ ] Use `wxCriticalSection` + `wxCondition` together — condition variable requires an associated critical section → **(P)** [R27]

- [ ] Use `wxSemaphore` for resource counting, `wxCondition` for event signaling → **(P)** [R27]

- [ ] Test for spurious wakeups by adding intentional delays — robust code handles them → **(P)** [R27]

```cpp
// Good — predicate loop with condition variable
wxCriticalLocker locker(m_cs);
while (!m_dataReady) {
    m_cond.Wait(); // May spuriously wake
```
}
// m_dataReady is guaranteed true

- **Consequence:** Spurious wakeup causes premature processing, missing condition signaling, race condition

- **Fix:** Use predicate loop, pair with `wxCriticalSection`, test for spurious wakeups

### 104. wxSingleInstanceChecker: Cross-Platform Locking  **(P)** [R27]

`wxSingleInstanceChecker` prevents multiple app instances. On wxMSW it uses a named kernel object (mutex), on wxGTK/wxOSX it uses a lock file. Known issues: the lock file may not be cleaned up on crash, and named mutex on Windows may conflict with other apps using the same name.

- [ ] Use a unique name for `wxSingleInstanceChecker` — include app name and user to avoid conflicts → **(P)** [R27]

- [ ] Handle stale lock files — check process existence before declaring single instance → **(P)** [R27]

- [ ] Create the `wxSingleInstanceChecker` early in `wxApp::OnInit()` and keep it alive for the app lifetime → **(P)** [R27]

- [ ] Test on all platforms — file-based (GTK/macOS) vs kernel-object (Windows) behavior differs → **(P)** [R27]

```cpp
// Good — create early, unique name
bool MyApp::OnInit() {
    const wxString name = wxString::Format("MyApp-%s", wxGetUserId());
    m_instanceChecker = new wxSingleInstanceChecker(name);
    if (m_instanceChecker->IsAnotherRunning()) {
        wxLogError("Another instance is already running.");
        return false;
    }
    // Continue initialization...
```
}

- **Consequence:** Multiple instances start, stale lock prevents app from starting, name conflicts

- **Fix:** Use unique name, handle stale locks, create early, test cross-platform

### 105. wxStopWatch and High-Resolution Timing  **(P)** [R27]

`wxStopWatch` provides millisecond-resolution timing. On 3.1.5, `wxGetLocalTimeMillis()` returns `wxLongLong` (millis since epoch). Known issue: on Windows, the resolution may be 10-16ms (timer tick), not true millisecond. For higher precision, use `wxGetUTCTimeMillis()` or platform-specific `QueryPerformanceCounter()`.

- [ ] Do NOT rely on `wxStopWatch` for sub-millisecond timing — resolution is platform-dependent → **(P)** [R27]

- [ ] Use `wxGetLocalTimeMillis()` for millisecond-precision epoch time → **(P)** [R27]

- [ ] For high-resolution profiling, use platform-specific timers (e.g., `QueryPerformanceCounter` on Windows) → **(P)** [R27]

- [ ] Test timing precision on all target platforms — resolution varies (10ms on Windows, ~1ms on Linux) → **(P)** [R27]

- **Consequence:** Timing too coarse for performance-sensitive code, inconsistent resolution across platforms

- **Fix:** Use `wxGetLocalTimeMillis()` for ms precision, platform-specific timers for sub-ms

### 106. wxStream and wxArchive: Error Handling  **(P)** [R27]

`wxInputStream`/`wxOutputStream` and `wxArchiveInputStream`/`wxArchiveOutputStream` (zip, tar) have limited error reporting. `GetLastError()` returns the last error, but it may be cleared by subsequent operations. Known issue: `wxZipInputStream` may not detect corrupted archives until `Read()` fails.

- [ ] Check `wxStream::GetLastError()` after every `Read()`/`Write()` — it may be cleared by subsequent ops → **(P)** [R27]

- [ ] For `wxZipInputStream`, check the return value of `Read()` — 0 bytes read may indicate corruption → **(P)** [R27]

- [ ] Do NOT assume `wxInputStream::IsOk()` guarantees data integrity — it only checks stream state → **(P)** [R27]

- [ ] Use `wxStreamBuffer` for buffered I/O — reduces error-checking overhead → **(P)** [R27]

- **Consequence:** Corrupt archive not detected, silent data loss, error state cleared before check

- **Fix:** Check `GetLastError()` after every op, verify `Read()` return, use `wxStreamBuffer`

### 107. wxRegEx: Platform-Specific Regex Engine  **(P)** [R27]

`wxRegEx` uses the system regex library on wxMSW (regex.h on wxGTK/wxOSX). On wxMSW, it uses a custom implementation (Henry Spencer's regex). Known differences: `wxRE_ADVANCED` flag enables extended features on wxGTK (POSIX ERE) but may not be supported on wxMSW. Backreferences behave differently across engines.

- [ ] Test `wxRegEx` on all target platforms — regex syntax support varies → **(P)** [R27]

- [ ] Use `wxRE_ADVANCED` for extended regex, but verify support on wxMSW → **(P)** [R27]

- [ ] Do NOT use PCRE-specific syntax (named groups `(?P<name>)`) — wxRegEx does NOT support PCRE → **(P)** [R27]

- [ ] Use `wxRegEx::GetMatch()` with explicit match index — named captures are NOT supported → **(P)** [R27]

- **Consequence:** Regex fails on one platform, unsupported syntax causes error, named captures not working

- **Fix:** Test cross-platform, use `wxRE_ADVANCED` with caution, avoid PCRE syntax, use numeric captures

### 108. wxVariant and wxAny: Type Safety and Conversion  **(P)** [R27]

`wxVariant` (dynamic typing) and `wxAny` (3.0+, lighter) both provide dynamic typing. `wxAny` is preferred for new code — it is more efficient and type-safe. `wxVariant` has known issues with `operator==` comparing different types (e.g., `long` vs `int`), and conversion may silently fail.

- [ ] Use `wxAny` (not `wxVariant`) for new code — it is more efficient and type-safe → **(P)** [R27]

- [ ] Use `wxAny::GetAs<T>()` with explicit type — do NOT rely on implicit conversion → **(P)** [R27]

- [ ] Test `wxVariant::Convert()` for lossy conversions (double to int) — may silently truncate → **(P)** [R27]

- [ ] Use `wxAny::CheckType<T>()` before `GetAs<T>()` — type mismatch throws → **(P)** [R27]

- **Consequence:** Silent type conversion errors, comparison of different types fails, runtime type exception

- **Fix:** Use `wxAny`, explicit `GetAs<T>()`, `CheckType<T>()` before access

### 109. wxDateTime and wxTimeSpan: DST and Timezone Handling  **(P)** [R27]

`wxDateTime` handles date/time with timezone support. Known issues in 3.1.5: DST transitions may cause 1-hour errors when comparing times across DST boundary, `wxDateTime::Now()` uses local time which may change meaning across DST, and `wxDateTime::GetWeekDay()` in ISO mode (Monday=1) vs Sunday mode (Sunday=0) can cause off-by-one errors.

- [ ] Use `wxDateTime::GetUTCTimeMillis()` for unambiguous time storage — UTC has no DST → **(P)** [R27]

- [ ] For date arithmetic across DST boundaries, use `wxDateSpan` (calendar-based) not `wxTimeSpan` (duration-based) → **(P)** [R27]

- [ ] Test DST transitions (spring forward, fall back) — time may be ambiguous or skipped → **(P)** [R27]

- [ ] Use `wxDateTime::FromUTC()` for explicit UTC parsing, `ToUTC()` for UTC output → **(P)** [R27]

```cpp
// Good — use UTC for storage, local for display
wxDateTime utc = wxDateTime::Now().ToUTC(); // Store in UTC
wxDateTime local = utc.FromUTC(); // Convert to local for display
```

- **Consequence:** 1-hour errors across DST, ambiguous time parsing, wrong weekday calculation

- **Fix:** Use UTC for storage, `wxDateSpan` for calendar math, test DST transitions

### 110. wxFileHistory: Menu Integration and Path Handling  **(P)** [R27]

`wxFileHistory` manages a list of recently opened files, typically shown in a File menu. Known issues in 3.1.5: `wxFileHistory::AddFileToHistory()` may exceed the menu's ID range if `SetMenu()` is not called with a menu that has contiguous IDs, and file paths with special characters may display incorrectly.

- [ ] Use `wxFileHistory::SetMenu()` with a menu that has room for `m_fileHistory->GetMaxFiles()` IDs → **(P)** [R27]

- [ ] Use `wxID_FILE1` through `wxID_FILE9` (or `wxID_FILE10`) for file history menu item IDs → **(P)** [R27]

- [ ] Handle `wxEVT_MENU` for `wxID_FILE1`..`wxID_FILE10` to open recent files → **(P)** [R27]

- [ ] Use `wxFileName::GetFullPath()` for display, `wxFileName::GetFullPath()` for storage → **(P)** [R27]

```cpp
// Good — set up file history
```
m_fileHistory = new wxFileHistory(9); // 9 recent files
m_fileHistory->SetMenu(recentFilesMenu); // Menu with wxID_FILE1..9
```cpp
for (size_t i = 0; i < m_fileHistory->GetCount(); i++) {
    // History is managed by wxFileHistory
```
}
```cpp
Bind(wxEVT_MENU, &MyFrame::OnRecentFile, this, wxID_FILE1, wxID_FILE9);
```

- **Consequence:** Menu IDs conflict, recent files not shown, paths display incorrectly

- **Fix:** Use `SetMenu()` with `wxID_FILE1`..`wxID_FILE9`, handle menu events, use `wxFileName`

### 111. wxLocale and Translation Loading: Catalog Path Issues  **(P)** [R28]

`wxLocale` loads translation catalogs (`.mo` files) via `wxFileTranslationsLoader` or `wxResourceTranslationsLoader`. Known issues in 3.1.5: the default search path may not include the app's resource directory, and `.mo` file names must match the locale name exactly (e.g., `zh_CN.mo` not `chinese.mo`).

- [ ] Use `wxFileTranslationsLoader::SetCatalogDir()` or `wxLocale::AddCatalogLookupPathPrefix()` to set the translation search path → **(P)** [R28]

- [ ] Use standard locale names (e.g., `zh_CN`, `ja_JP`, `de_DE`) for `.mo` file names → **(P)** [R28]

- [ ] Call `wxLocale::Init()` before creating any translatable strings — `wxGetTranslation()` uses the global locale → **(P)** [R28]

- [ ] Test translation loading with missing `.mo` files — should fall back to source language → **(P)** [R28]

```cpp
// Good — set catalog path before init
wxFileTranslationsLoader::SetCatalogDir(wxStandardPaths::Get().GetResourcesDir() + "/locale");
```
m_locale = new wxLocale();
m_locale->Init(wxLANGUAGE_CHINESE_SIMPLIFIED);
m_locale->AddCatalog("myapp"); // Loads myapp.mo from zh_CN or zh

- **Consequence:** Translations not loaded, wrong locale name, strings untranslated

- **Fix:** Set catalog path, use standard locale names, init locale before translatable strings

### 112. wxLocale and UTF-8: Source File Encoding  **(P)** [R28]

```cpp
wxWidgets 3.1.5 uses UTF-8 as the internal `wxString` encoding by default. Translation source (`.po`/`.pot`) files must be UTF-8 encoded. Using `_("non-ASCII string")` in source code requires the source file to be UTF-8. Non-UTF-8 source files (e.g., GBK on Windows) will produce garbled translations.
```

- [ ] Save source files as UTF-8 — `_("...")` strings are extracted and compiled into `.mo` files → **(P)** [R28]

- [ ] Use `wxGetTranslation()`/`_()` for ALL translatable strings, including menu items, labels, tooltips → **(P)** [R28]

- [ ] Test translations with non-ASCII characters (Chinese, Japanese, Arabic) — verify encoding is correct → **(P)** [R28]

- [ ] Use `wxString::FromUTF8()` when loading strings from external UTF-8 sources (files, network) → **(P)** [R28]

- **Consequence:** Garbled translations, mojibake, encoding mismatch between source and `.mo`

- **Fix:** UTF-8 source files, `wxGetTranslation()` for all strings, test non-ASCII languages

### 113. wxLocale and Plural Forms  **(P)** [R28]

`wxGetTranslation()` supports plural forms via `ngettext()`. The plural form rules are defined in the `.po` file header (`Plural-Forms`). wxWidgets 3.1.5 uses the GNU gettext plural form syntax. Known issue: some languages (Arabic, Russian, Polish) have complex plural rules that must be correctly specified in the `.po` header.

- [ ] Use `wxPLURAL(msgid, msgid_plural, n)` macro for plurals — it wraps `ngettext` → **(P)** [R28]

- [ ] Verify `Plural-Forms` header in `.po` files for complex-plural languages (Arabic: 6 forms, Russian: 3 forms) → **(P)** [R28]

- [ ] Test plural forms with n=0, n=1, n=2, n=many — verify correct form is selected → **(P)** [R28]

- [ ] Do NOT use `wxGetTranslation()` for plurals — it does not support plural form selection → **(P)** [R28]

```cpp
// Good — use wxPLURAL for plurals
wxString msg = wxPLURAL("1 file", "%d files", count);
```

- **Consequence:** Wrong plural form displayed, grammatically incorrect translations

- **Fix:** Use `wxPLURAL`, verify `Plural-Forms` header, test edge cases

### 114. wxFontMapper and Font Encoding Fallback  **(P)** [R28]

`wxFontMapper` maps logical font encoding (e.g., `wxFONTENCODING_CP1252`) to actual fonts. Known issues in 3.1.5: on systems without the requested font encoding, `wxFontMapper` falls back to a default which may not display all characters. `wxFontEncoding` may be ignored on platforms that use Unicode fonts (macOS, modern Linux).

- [ ] Use `wxFONTENCODING_UTF8` for all new code — modern platforms use Unicode fonts → **(P)** [R28]

- [ ] Do NOT rely on `wxFontMapper` on macOS — all fonts are Unicode, encoding is ignored → **(P)** [R28]

- [ ] For legacy encodings (e.g., `wxFONTENCODING_CP1251` for Cyrillic), test on all platforms — fallback may differ → **(P)** [R28]

- [ ] Use `wxFont::IsOk()` after creation — encoding mismatch may produce an invalid font → **(P)** [R28]

- **Consequence:** Wrong characters displayed, font not found, encoding ignored on modern platforms

- **Fix:** Use `wxFONTENCODING_UTF8`, test legacy encodings, check `IsOk()` after creation

### 115. wxGrid: Cell Editors and Renderers Lifecycle  **(P)** [R28]

`wxGridCellEditor` and `wxGridCellRenderer` are created per-cell and deleted by the grid. Known issues in 3.1.5: custom editors must call `wxGridCellEditor::Create()` to create the editor control, and the editor control's parent must be the grid. Also, `wxGridCellEditor::StartingKey()` may not fire on all platforms.

- [ ] Custom `wxGridCellEditor`: call `Create()` to instantiate the control, set parent to the grid → **(P)** [R28]

- [ ] Override `wxGridCellEditor::HandleReturn()` and `StartingKey()` — key handling differs across platforms → **(P)** [R28]

- [ ] Do NOT delete `wxGridCellEditor`/`wxGridCellRenderer` manually — the grid owns them → **(P)** [R28]

- [ ] Use `wxGridCellAutoWrapStringRenderer` for auto-wrapping text cells, not custom rendering → **(P)** [R28]

- **Consequence:** Editor control not created, key events missing, double-free crash, text not wrapping

- **Fix:** Call `Create()`, override key handlers, let grid own editors/renderers, use auto-wrap renderer

### 116. wxGrid: Table Model (wxGridTableBase) and Virtual Grid  **(P)** [R28]

`wxGridTableBase` provides a virtual grid interface for large datasets. Known issues in 3.1.5: `wxGridTableBase::GetValue()` is called synchronously during paint, so it must be fast. For large datasets, this can cause performance issues. Also, `wxGridTableBase::AppendRows()`/`DeleteRows()` must call `wxGrid::RowNumChanged()` or the view may not update.

- [ ] Make `wxGridTableBase::GetValue()` fast — it is called during paint, blocking the UI → **(P)** [R28]

- [ ] Call `wxGrid::ProcessTableMessage(wxGridTableMessage)` after row/column changes — or the view will not update → **(P)** [R28]

- [ ] Use `wxGridStringTable` for simple string data — do NOT implement `wxGridTableBase` unless you need virtual behavior → **(P)** [R28]

- [ ] For very large grids (> 100K rows), consider `wxDataViewCtrl` with virtual model instead of `wxGrid` → **(P)** [R4]

```cpp
// Good — notify grid after row changes
void MyGridTable::AppendRows(size_t n) {
    m_rows += n;
    if (GetView()) {
        wxGridTableMessage msg(this, wxGRIDTABLE_NOTIFY_ROWS_APPENDED, n);
        GetView()->ProcessTableMessage(msg);
    }
```
}

- **Consequence:** UI lag during paint, view not updating after data change, performance issue with large data

- **Fix:** Fast `GetValue()`, `ProcessTableMessage` after changes, consider `wxDataViewCtrl` for large data

### 117. wxGrid: Selection Model and Multi-select  **(P)** [R28]

`wxGrid` selection modes (`wxGridSelectionModes`) differ across platforms. `wxGridSelectCells` (default) selects individual cells, `wxGridSelectRows` selects entire rows, `wxGridSelectColumns` selects columns. Known issues: `wxGrid::SelectBlock()` may not fire `wxEVT_GRID_RANGE_SELECT` on wxGTK, and `wxGrid::ClearSelection()` may not update the visual state on macOS.

- [ ] Use `wxGrid::SetSelectionMode()` for consistent selection behavior — default is cell selection → **(P)** [R28]

- [ ] Call `wxGrid::Refresh()` after `ClearSelection()` on macOS — visual state may not update → **(P)** [R28]

- [ ] Handle `wxEVT_GRID_RANGE_SELECT` for block selection, `wxEVT_GRID_SELECT_CELL` for cell selection → **(P)** [R28]

- [ ] Test selection behavior on all platforms — wxGTK and wxOSX differ from wxMSW → **(P)** [R28]

- **Consequence:** Wrong selection behavior, stale visual state, missing selection events on GTK

- **Fix:** Set selection mode, `Refresh()` after `ClearSelection()` on macOS, test cross-platform

### 118. wxTimer: OneShot vs. Repeating and Thread Safety  **(P)** [R28]

`wxTimer` fires `wxEVT_TIMER` events. `wxTimer::StartOnce()` fires a single event; `Start(interval)` fires repeatedly. Known issues in 3.1.5: `wxTimer` events are delivered via the main event loop, so they may be delayed if the event loop is busy. `wxTimer` is NOT thread-safe — do NOT create or start timers from worker threads.

- [ ] Use `wxTimer::StartOnce()` for single-fire timers, `Start(interval, false)` for repeating → **(P)** [R28]

- [ ] Do NOT create or start `wxTimer` from worker threads — use `wxPostEvent` to signal the main thread → **(P)** [R5]

- [ ] Be aware that `wxTimer` events may be delayed if the event loop is busy — do NOT use for real-time deadlines → **(P)** [R28]

- [ ] Use `wxTimerEvent::GetInterval()` to verify the timer in multi-timer scenarios → **(P)** [R28]

- **Consequence:** Timer fires from wrong thread, events delayed, missed deadline, wrong timer ID

- **Fix:** `StartOnce` for single-fire, `wxPostEvent` from threads, don't use for real-time

### 119. wxBusyCursor and wxWindowDisabler: Modal-like Behavior  **(P)** [R28]

`wxBusyCursor` (RAII) shows an hourglass cursor. `wxWindowDisabler` (RAII) disables all windows. Known issues: `wxWindowDisabler` disables ALL windows including the one that triggered the action, which can prevent UI updates. Using both together is common but may cause the UI to appear frozen.

- [ ] Use `wxBusyCursor` for short operations (< 1 second) — shows busy without disabling UI → **(P)** [R28]

- [ ] Use `wxWindowDisabler` for long operations — disables input but allows paint events → **(P)** [R28]

- [ ] Call `wxYield()` periodically during long operations if UI updates are needed — but beware reentrancy → **(P)** [R28]

- [ ] Do NOT use `wxWindowDisabler` with modal dialogs — the dialog is already modal → **(P)** [R28]

```cpp
// Good — busy cursor + window disabler for long ops
```
{
```cpp
    wxBusyCursor busy;
    wxWindowDisabler disable;
    for (int i = 0; i < 100; i++) {
        DoWork(i);
        if (i % 10 == 0) wxYield(); // Allow paint
    }
```
}

- **Consequence:** UI appears frozen, input not disabled, reentrancy crash from `wxYield`

- **Fix:** Use `wxBusyCursor` for short ops, `wxWindowDisabler` for long ops, `wxYield` carefully

### 120. wxAcceleratorTable and Platform-Specific Key Handling  **(P)** [R28]

`wxAcceleratorTable` provides keyboard shortcuts (e.g., Ctrl+S). On 3.1.5, accelerator keys are handled before normal key events. Known issues: `wxAcceleratorEntry` uses `wxACCEL_CTRL` for Ctrl, but on macOS, the Command key is the primary modifier — `wxACCEL_CMD` maps to Command. Also, function keys (F1-F12) may conflict with system shortcuts on macOS.

- [ ] Use `wxACCEL_CMD` (not `wxACCEL_CTRL`) on macOS for Command-key shortcuts → **(P)** [R28]

- [ ] Do NOT use F1-F12 on macOS without checking system conflicts — Mission Control, Spotlight use these → **(P)** [R28]

- [ ] Call `wxWindow::SetAcceleratorTable()` on the frame (not child windows) — accelerators are window-level → **(P)** [R28]

- [ ] Test accelerators on all platforms — Ctrl vs Command, function key conflicts differ → **(P)** [R28]

```cpp
// Good — platform-specific accelerator
wxAcceleratorEntry entries[1];
```
#ifdef __WXOSX__
entries[0].Set(wxACCEL_CMD, (int)'S', wxID_SAVE); // Command+S on macOS
#else
entries[0].Set(wxACCEL_CTRL, (int)'S', wxID_SAVE); // Ctrl+S on Windows/Linux
#endif
frame->SetAcceleratorTable(wxAcceleratorTable(1, entries));

- **Consequence:** Wrong modifier key on macOS, system shortcut conflict, accelerators not working on child windows

- **Fix:** Use `wxACCEL_CMD` on macOS, avoid F-keys, set on frame, test cross-platform

### 121. wxWebView: Backend Selection and Platform Differences  **(P)** [R29]

`wxWebView` provides an embedded web view. In 3.1.5, the backend varies by platform: wxMSW uses Edge (Chromium) via `wxWebViewEdge`, wxGTK uses WebKitGTK, wxOSX uses WKWebView. Known issues: `wxWebViewEdge` requires WebView2 runtime (may not be installed on older Windows), WebKitGTK version must be >= 2.14, and WKWebView on macOS may not support all JavaScript APIs.

- [ ] Use `wxWebView::New()` with explicit backend name for platform-specific control → **(P)** [R29]

- [ ] Check `wxWebViewEdge::IsAvailable()` before using Edge backend — requires WebView2 runtime → **(P)** [R29]

- [ ] Test JavaScript execution on all platforms — `wxWebView::RunScript()` behavior may differ → **(P)** [R29]

- [ ] Handle `wxEVT_WEBVIEW_ERROR` for backend-specific errors — network, script, navigation failures → **(P)** [R29]

```cpp
// Good — check backend availability
if (wxWebViewEdge::IsAvailable()) {
    webView = wxWebView::New(this, wxID_ANY, "", wxDefaultPosition, wxDefaultSize, wxWebViewBackendEdge);
```
} else {
```cpp
    webView = wxWebView::New(this, wxID_ANY); // Default backend
```
}

- **Consequence:** WebView not available on older Windows, JavaScript fails, navigation errors unhandled

- **Fix:** Check `IsAvailable()`, explicit backend, handle errors, test cross-platform

### 122. wxWebView: Cookie and Session Handling  **(P)** [R29]

`wxWebView` cookies are handled by the backend (Edge, WebKitGTK, WKWebView). In 3.1.5, there is no unified API for cookie management — each backend handles cookies independently. Session cookies may persist across `wxWebView` instances on the same backend. Known issue: clearing cookies requires backend-specific code.

- [ ] Do NOT assume cookies are isolated per `wxWebView` instance — backend may share them → **(P)** [R29]

- [ ] For private/incognito browsing, use `wxWebViewEdge` with `--incognito` flag or WKWebView `nonPersistentDataStore` → **(P)** [R29]

- [ ] Test cookie behavior across app restarts — persistent cookies may remain → **(P)** [R29]

- [ ] Use `wxWebView::ClearHistory()` (not cookies) for history clearing — cookie clearing is backend-specific → **(P)** [R29]

- **Consequence:** Cookies leak between instances, persistent across restarts, no unified API

- **Fix:** Backend-specific incognito mode, test persistence, use backend-specific cookie clearing

### 123. wxWebView: Print and PDF Export  **(P)** [R29]

`wxWebView` in 3.1.5 has limited print support — `wxWebView::Print()` is not available on all backends. PDF export requires backend-specific JavaScript (`window.print()`) or native API calls. Known issues: print preview is not supported, and the print output may not match the screen rendering.

- [ ] Use JavaScript `window.print()` for printing — native print API is backend-specific → **(P)** [R29]

- [ ] Do NOT rely on `wxWebView::Print()` — it may not exist on all backends → **(P)** [R29]

- [ ] For PDF export, use backend-specific API or a JavaScript library (e.g., `jsPDF`) → **(P)** [R29]

- [ ] Test print output on all backends — rendering may differ from screen → **(P)** [R29]

- **Consequence:** Print not available, PDF export fails, output inconsistent with screen

- **Fix:** Use `window.print()`, backend-specific API for PDF, test output quality

### 124. wxPrintout: Page Setup and Margins Cross-Platform  **(P)** [R29]

`wxPrintout` provides the document-to-printer interface. Known issues in 3.1.5: page size and margins differ by platform — wxMSW uses `DEVMODE`, wxGTK uses `GtkPrintSettings`, wxOSX uses `NSPrintInfo`. The `wxPageSetupDialogData` maps differently to each platform, and `GetPaperRect()` may return different coordinate systems.

- [ ] Use `wxPrintout::GetDC()` for all drawing — do NOT assume pixel coordinates, use `MapScreenSizeToPage()` → **(P)** [R29]

- [ ] Handle `wxPageSetupDialogData::CalcMinMargins()` for consistent margins across platforms → **(P)** [R29]

- [ ] Test printing on all platforms — paper size, orientation, margins may differ → **(P)** [R29]

- [ ] Use `wxPrintout::OnPrintPage()` with page loop — do NOT assume single-page printing → **(P)** [R29]

- **Consequence:** Print output misaligned, wrong paper size, margins inconsistent

- **Fix:** Use `GetDC()` + `MapScreenSizeToPage()`, handle margins, test cross-platform

### 125. wxPrintPreview: Quality and Sync Issues  **(P)** [R29]

`wxPrintPreview` shows a preview of print output. Known issues in 3.1.5: the preview may render at lower quality than the actual print, and the preview's page count may differ from actual pages (due to pagination differences). On macOS, the preview uses the native print preview dialog which is different from the wxWidgets preview.

- [ ] Use `wxPrintPreview` for basic preview — on macOS, it may use native dialog instead → **(P)** [R29]

- [ ] Do NOT assume preview page count equals print page count — pagination may differ → **(P)** [R29]

- [ ] Set `wxPrintPreview::SetZoom()` for user-controlled zoom — default may be too small → **(P)** [R29]

- [ ] Test preview rendering on all platforms — quality and behavior differ → **(P)** [R29]

- **Consequence:** Preview looks different from print, wrong page count, macOS uses native dialog

- **Fix:** Use `wxPrintPreview`, expect page count differences, set zoom, test cross-platform

### 126. wxBitmapType and Image Handler Registration  **(P)** [R29]

`wxImage` uses handler-based loading for different formats (PNG, JPEG, GIF, BMP, etc.). In 3.1.5, handlers must be registered via `wxImage::AddHandler()` before loading. Known issue: `wxInitAllImageHandlers()` registers all built-in handlers, but it may not include handlers for formats loaded from plugins.

- [ ] Call `wxInitAllImageHandlers()` once at app startup — or register specific handlers only → **(P)** [R29]

- [ ] For specific formats, use `wxImage::AddHandler(new wxPNGHandler)` — lighter than registering all → **(P)** [R29]

- [ ] Check `wxImage::FindHandler()` before loading — handler may not be registered → **(P)** [R29]

- [ ] Test image loading with corrupt files — some handlers may crash on malformed input → **(P)** [R29]

```cpp
// Good — register only needed handlers
wxImage::AddHandler(new wxPNGHandler);
wxImage::AddHandler(new wxJPEGHandler);
wxImage::AddHandler(new wxICOHandler);
```
// Or: wxInitAllImageHandlers(); // All built-in handlers

- **Consequence:** Image not loaded, handler not found, crash on corrupt image

- **Fix:** `wxInitAllImageHandlers()` or register specific, `FindHandler()` before load, test corrupt files

### 127. wxImage: Scaling and Quality  **(P)** [R29]

`wxImage::Scale()` uses nearest-neighbor by default (fast but low quality). For better quality, use `wxIMAGE_QUALITY_BICUBIC` or `wxIMAGE_QUALITY_BOX` (3.1.5+). Known issues: scaling down with nearest-neighbor produces jagged edges, and `wxIMAGE_QUALITY_HIGH` may be slow for large images.

- [ ] Use `wxImage::Scale(w, h, wxIMAGE_QUALITY_BICUBIC)` for high-quality scaling → **(P)** [R29]

- [ ] Use `wxIMAGE_QUALITY_NEAREST` for fast, pixelated scaling (retro/gaming) → **(P)** [R29]

- [ ] Avoid scaling in a paint event — pre-scale images during loading or setup → **(P)** [R29]

- [ ] Test image quality on different scaling ratios (2x, 4x, 0.5x) → **(P)** [R29]

```cpp
// Good — high-quality scaling
wxImage img("photo.png");
wxImage scaled = img.Scale(100, 100, wxIMAGE_QUALITY_BICUBIC);
```

- **Consequence:** Jagged images, slow scaling in paint, poor quality thumbnails

- **Fix:** Use `wxIMAGE_QUALITY_BICUBIC`, pre-scale, avoid scaling in paint

### 128. wxCursor and Custom Cursor: Hotspot and Size  **(P)** [R29]

`wxCursor` supports custom cursors from `wxImage`. In 3.1.5, the cursor hotspot is set via `wxImage::SetOption(wxBITMAP_OPTION_CUR_HOTSPOT_X/Y)`. Known issues: cursor size is limited to 32x32 on Windows (classic) but may be larger on macOS and Linux. Monochrome cursors may not work on all platforms.

- [ ] Set cursor hotspot via `wxImage::SetOption()` before creating `wxCursor` → **(P)** [R29]

- [ ] Keep cursor size to 32x32 for Windows compatibility — larger may fail on legacy Windows → **(P)** [R29]

- [ ] Use color cursors (not monochrome) — monochrome may not work on macOS/Linux → **(P)** [R29]

- [ ] Test custom cursors on all platforms — hotspot and size behavior differ → **(P)** [R29]

```cpp
// Good — custom cursor with hotspot
wxImage img(32, 32);
```
// Draw cursor image...
img.SetOption(wxBITMAP_OPTION_CUR_HOTSPOT_X, 0);
img.SetOption(wxBITMAP_OPTION_CUR_HOTSPOT_Y, 0);
```cpp
wxCursor cursor(img);
```
window->SetCursor(cursor);

- **Consequence:** Cursor hotspot wrong, cursor too large on Windows, monochrome fails on macOS

- **Fix:** Set hotspot, 32x32 max, color cursors, test cross-platform

### 129. wxIconBundle and Multi-Resolution Icons  **(P)** [R29]

`wxIconBundle` contains multiple `wxIcon` objects for different sizes. In 3.1.5, `wxIconBundle` is used for window/taskbar icons. On Windows, the bundle is used for taskbar (large) and window title (small) icons. On macOS, the `.icns` file provides multiple resolutions. Known issue: `wxIconBundle::GetIcon(size)` may not return the best match on all platforms.

- [ ] Use `wxIconBundle` with multiple sizes (16x16, 32x32, 48x48, 256x256) for all platforms → **(P)** [R29]

- [ ] On macOS, use `.icns` file — it contains all resolutions natively → **(P)** [R29]

- [ ] Use `wxFrame::SetIcons(bundle)` (not `SetIcon()`) for multi-resolution → **(P)** [R29]

- [ ] Test icon rendering on taskbar, window title, and Alt-Tab — sizes differ → **(P)** [R29]

- **Consequence:** Wrong icon size shown, blurry icons, no high-res icon on Retina

- **Fix:** Use `wxIconBundle` with multiple sizes, `.icns` on macOS, `SetIcons()` not `SetIcon()`

### 130. wxDropTarget and DataObject: Custom Format Registration  **(P)** [R29]

`wxDropTarget` receives drag-and-drop data. Custom formats require `wxDataObject` subclass with `wxDataFormat` registration. In 3.1.5, `wxDataFormat::GetId()` returns the format name (string) which is registered per-session. Known issues: format names must be unique across apps, and `wxDropTarget::OnData()` may be called multiple times for the same drop.

- [ ] Use unique format names (include app name prefix) — format IDs are global per-session → **(P)** [R29]

- [ ] Implement `wxDropTarget::OnData()` to call `wxDataObject::SetData()` — the data is NOT auto-set → **(P)** [R29]

- [ ] Use `wxDropTarget::OnDrop()` for veto-able drop — return false to reject the drop → **(P)** [R29]

- [ ] Test DnD with external apps — custom format may not be recognized by other apps → **(P)** [R29]

```cpp
// Good — custom drop target with format
class MyDropTarget : public wxDropTarget {
```
public:
```cpp
    MyDropTarget() {
        wxDataObjectComposite* data = new wxDataObjectComposite();
        data->Add(new wxCustomDataObject("MyApp.MyFormat"), true); // preferred
        SetDataObject(data);
    }
    wxDragResult OnData(wxCoord x, wxCoord y, wxDragResult def) override {
        GetData(); // Copy data from DnD source to DataObject
        // Process data...
        return def;
    }
```
};

- **Consequence:** DnD not recognized, data not received, drop accepted but data empty

- **Fix:** Unique format names, `GetData()` in `OnData()`, implement `OnDrop()` for veto

## Quick Decision Tree

Using wxGLCanvas?

  ├─ Targeting Wayland/EGL?

  │    ├─ Multiple GL canvases? → Verify independent render, provide X11 fallback

  │    ├─ In wxPopupWindow? → Known positioning bug, restructure UI

  │    └─ Destroying canvas? → Verify no dangling surface

  └─ HiDPI display? → Use physical pixels (GetSize * GetContentScaleFactor)

Using wxDataViewCtrl?

  ├─ Deleting items during edit callback? → Defer via QueueEvent

  ├─ AssociateModel(nullptr) before model destruction? → Required

  ├─ Using wxVSCROLL/wxHSCROLL on macOS? → Remove these styles

  └─ Calling ItemsAdded/Deleted from worker thread? → Move to main thread

Worker thread touching GUI?

  ├─ Direct GUI call? → Use CallAfter or QueueEvent

  ├─ wxPostEvent on wxGTK? → Verify handler runs in main thread

  └─ wxThread::Wait from main on GUI-touching thread? → Deadlock risk, use detached

Migrating from 3.0?

  ├─ wxYield in idle handler? → May fire wxEVT_IDLE unexpectedly

  ├─ Multiline wxTextCtrl wxEVT_TEXT_ENTER? → Add wxTE_PROCESS_ENTER

  ├─ wxFileDialog GetPath with wxFD_MULTIPLE? → Use GetPaths

  └─ wxBitmap(0,0)? → Now fails, handle error

---

### 131. wxString Conversion Buffer Lifetime: ToUTF8()/utf8_str()/mb_str() Temporary Object UB  **(P)** [R30]

```cpp
wxString::utf8_str(), wxString::ToUTF8(), and wxString::mb_str() return a wxScopedCharBuffer / wxCharBuffer **by value**. Calling .data() or .c_str() on that temporary and using the pointer after the full-expression ends is a **dangling pointer** and **undefined behaviour**. This is the #1 wxString lifetime bug in real-world wxWidgets applications.
```

> **Official warning (interface/wx/string.h, utf8_str() doc):** the return type *"is either a temporary wxCharBuffer object or ... a pointer to the internal string contents in UTF-8 build."* The same overview (interface/wx/string.h, around the c_str() docs) warns that vararg calls like `printf("...%s...", s.c_str())` are dangerous because the argument types are not checked — bind the buffer to a named local first.

- [ ] Never call .data() or .c_str() directly on a temporary returned by ToUTF8(), utf8_str(), or mb_str() → **(P)** [R30]

- [ ] Always assign the return value to a local const auto variable before accessing .data() → **(P)** [R30]

- [ ] Prefer wxString::utf8_string() (new in 3.1.5) which returns std::string directly — no buffer lifetime issue → **(P)** [R30]

- [ ] Prefer wxString::ToStdString(wxConvUTF8) as another safe alternative → **(P)** [R30]

- [ ] wc_str() return type is **build-dependent**: in the wchar build (wxMSW default) it returns `const wchar_t*` directly into the internal buffer (no dangling); in the UTF-8 build (wxGTK/wxOSX default) it returns a **temporary wxScopedWCharBuffer** that CAN dangle — bind it to a local first on non-wchar builds → **(P)** [R30]

- [ ] c_str() returns a **wxCStrData** proxy object (implicitly convertible to `const char*`/`const wchar_t*`), NOT a raw pointer; the method that returns the raw internal pointer is **wx_str()** (`const wxStringCharType*`) → **(P)** [R30]

```cpp
// Bad — UB: .data() on temporary wxScopedCharBuffer
std::string file_name = dialog.GetPath().ToUTF8().data();
const char* p = str.utf8_str().data(); // p is dangling as soon as ';' executes
```

```cpp
// Good — assign buffer to local variable first
const auto buf = dialog.GetPath().ToUTF8();
std::string file_name = buf.data();
```

```cpp
// Best — use utf8_string() (3.1.5+), returns std::string directly
std::string file_name = dialog.GetPath().utf8_string();
```

**Rationale:** wxScopedCharBuffer / wxCharBuffer are RAII buffers that free their memory when destroyed. The official wxWidgets 3.1.5 docs (interface/wx/string.h) document the return types as build-conditional temporaries and warn against passing the conversion results through C varargs.

### 132. Freeze()/Thaw() Batch Update and wxWindowUpdateLocker  **(P)** [R30][R37]

```cpp
wxWindow::Freeze() prevents screen updates to a window and all its children. Thaw() re-enables them. They are a critical performance optimization for bulk UI modifications. However, they are **not universally implemented** across all platforms and controls, and misuse can leave a window permanently frozen.
```

- [ ] Always pair Freeze() and Thaw() exactly — they are reference-counted (nested calls require matching number of Thaw() calls) → **(P)** [R30]

- [ ] Prefer wxWindowUpdateLocker for RAII-based Freeze/Thaw — it guarantees Thaw() even on exception/early return → **(P)** [R30]

- [ ] `wxWindowUpdateLocker` is declared in `<wx/wupdlock.h>` (which itself includes `wx/window.h`) — include `wx/wupdlock.h` explicitly; `wx/window.h` does NOT pull it in. Real evidence: OrcaSlicer Flatpak builds failed with `'wxWindowUpdateLocker' was not declared in this scope` (TimelapseDownloadPopup.cpp:492, MixedFilamentBatchDialog.cpp:2715) while the identical code compiled on the ubuntu/macos/windows jobs of the same runs → **(P)** [R37]

- [ ] General include hygiene: include the header that declares the wx class you use — 3.1.5 removed several transitive includes (e.g. `wx/treebook.h` no longer includes `wx/treectrl.h`) → **(P)** [R1]

- [ ] Call Layout() after Thaw() if children were added/removed/shown/hidden while frozen → **(P)** [R30]

- [ ] IsFrozen() to check current state — useful for assertions/debugging → **(N)** [R30]

- [ ] Do NOT rely on Freeze() for thread safety — it only affects visual updates, not data access → **(P)** [R30]

```cpp
// Good — RAII with wxWindowUpdateLocker
void UpdateAllItems(wxListCtrl* list) {
    wxWindowUpdateLocker lock(list);
    list->DeleteAllItems();
    for (auto& item : items)
        list->InsertItem(list->GetItemCount(), item.name);
```
}

```cpp
// Bad — exception between Freeze and Thaw leaves window frozen
```

panel->Freeze();

DoRiskyOperation();  // may throw

panel->Thaw();       // never reached on exception

**Rationale:** interface/wx/window.h documents reference-counting semantics and recommends wxWindowUpdateLocker. The docs note: "This method is useful for visual appearance optimization but is not implemented on all platforms."

### 133. Custom Widget Paint: wxAutoBufferedPaintDC and wxBG_STYLE_PAINT  **(P)** [R21][R30]

When creating custom-painted widgets, proper double-buffering and background style setup are essential to avoid flickering. wxWidgets official customwidgets overview (docs/doxygen/overviews/customwidgets.h) defines the canonical pattern:

- [ ] Call SetBackgroundStyle(wxBG_STYLE_PAINT) in the constructor — prevents default background erase flicker → **(P)** [R30]

- [ ] Use wxAutoBufferedPaintDC (not raw wxPaintDC) in OnPaint() handlers for automatic double-buffering → **(P)** [R30]

- [ ] Implement DoGetBestSize() override for proper sizer integration → **(P)** [R21][R30]

- [ ] Use the Create() two-phase construction pattern → **(P)** [R21][R30]

- [ ] Call Init() from both constructors to share common initialization → **(P)** [R21]

- [ ] Apply FromDIP() to all hardcoded pixel values in paint handlers → **(P)** [R30]

- [ ] Use Refresh() / RefreshRect() to trigger repaint, never call OnPaint() directly → **(P)** [R30]

```cpp
class MyCustomWidget : public wxControl {
```
public:
```cpp
    MyCustomWidget() { Init(); }
    MyCustomWidget(wxWindow* parent, wxWindowID id, ...) { Init(); Create(parent, id, ...); }
    bool Create(wxWindow* parent, wxWindowID id, ...) {
        if (!wxControl::Create(parent, id, ...)) return false;
        SetBackgroundStyle(wxBG_STYLE_PAINT);  // CRITICAL: prevent flicker
        return true;
    }
```
protected:
```cpp
    void Init() { }
    wxSize DoGetBestSize() const override { return FromDIP(wxSize(100, 30)); }
    void OnPaint(wxPaintEvent&) {
        wxAutoBufferedPaintDC dc(this);
        dc.Clear();
    }
```
};

**Rationale:** docs/doxygen/overviews/customwidgets.h provides this template and recommends wxAutoBufferedPaintDC as the standard DC for custom-painted controls.

### 134. wxPopupTransientWindow Lifecycle: Popup/Dismiss Pattern  **(P)** [R30]

```cpp
wxPopupTransientWindow is designed for auto-dismissing popup windows. It adds automatic dismissal when the user clicks outside or focus is lost.
```

- [ ] Use Popup(wxWindow* focus) to show the window — it handles positioning and focus management → **(P)** [R30]

- [ ] Use Dismiss() to programmatically hide — triggers OnDismiss() virtual for cleanup → **(P)** [R30]

- [ ] Override OnDismiss() for cleanup (not Dismiss()) — Dismiss() is a non-virtual hide trigger → **(P)** [R30]

- [ ] Override ProcessLeftDown() and return true to prevent auto-dismiss on specific mouse clicks → **(P)** [R30]

- [ ] Use wxPU_CONTAINS_CONTROLS style on wxMSW when the popup contains focus-needing controls → **(P)** [R30]

- [ ] Call Position() before Popup() for screen-coordinate placement → **(N)** [R30]

- [ ] Do NOT call Show() on wxPopupTransientWindow — use Popup() instead → **(P)** [R30]

**Rationale:** interface/wx/popupwin.h states: "A wxPopupWindow which disappears automatically when the user clicks mouse outside it or if it loses focus in any other way."

### 135. wxWebView MSW Edge Backend: Runtime Detection and Error Handling  **(P)** [R25][R29]

```cpp
wxWebView on wxMSW uses Edge (WebView2) as the modern backend. However, Edge WebView2 may not be installed on all systems.
```

- [ ] Check for Edge WebView2 runtime availability — wxWebView::IsBackendAvailable(wxWebViewBackendEdge) → **(P)** [R25]

- [ ] Provide a fallback error message if Edge is unavailable → **(P)** [R25]

- [ ] Always call wxWebView::New() with explicit backend parameter → **(P)** [R25]

- [ ] Catch exceptions from wxWebView::New() — backend creation can throw → **(P)** [R29]

- [ ] Do NOT call RunScript() before wxEVT_WEBVIEW_LOADED fires → **(P)** [R29]

- [ ] Use AddScriptMessageHandler() + wxEVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED for JS->C++ communication → **(P)** [R29]

- [ ] Handle wxEVT_WEBVIEW_NAVIGATING to intercept navigation → **(N)** [R29]

```cpp
if (!wxWebView::IsBackendAvailable(wxWebViewBackendEdge)) {
    wxMessageBox("Microsoft Edge WebView2 is required.");
    return;
```
}
try {
```cpp
    m_browser = wxWebView::New(this, wxID_ANY, url, wxDefaultPosition, wxDefaultSize, wxWebViewBackendEdge);
```
} catch (const std::exception& e) {
```cpp
    wxLogError("Failed to create WebView: %s", e.what());
    return;
```
}

**Rationale:** interface/wx/webview.h defines the backend selection API. GitHub issues #19814, #16862, #21455 document Edge backend crashes.

### 136. ImGui + wxGLCanvas Integration Patterns  **(P)** [R1][R3][R30]

When integrating Dear ImGui with wxGLCanvas, coordinate spaces, event forwarding, and framebuffer management require careful handling.

- [ ] Use GetClientSize() * GetContentScaleFactor() for ImGui framebuffer size → **(P)** [R1]

- [ ] Convert mouse coordinates from logical to physical using GetContentScaleFactor() → **(P)** [R1]

- [ ] Call wxGLCanvas::SetCurrent() before all ImGui rendering calls and check return value → **(P)** [R1]

- [ ] Call SwapBuffers() only after all ImGui frame rendering is complete → **(P)** [R1]

- [ ] Forwarding key events to ImGui: always call event.Skip() for system keys → **(P)** [R1]

- [ ] Multiple wxGLCanvas with ImGui: verify context sharing on Wayland/EGL (Section 2) → **(P)** [R3]

- [ ] ImGui rendering in main thread only — use CallAfter() from worker threads → **(P)** [R30]

```cpp
void OnPaint(wxPaintEvent&) {
    if (!SetCurrent(*m_context)) return;
    const wxSize size = GetClientSize() * GetContentScaleFactor();
    ImGuiIO& io = ImGui::GetIO();
    io.DisplaySize = ImVec2(size.x, size.y);
    io.DisplayFramebufferScale = ImVec2(GetContentScaleFactor(), GetContentScaleFactor());
    ImGui::NewFrame();
    // ... rendering ...
    ImGui::Render();
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
    SwapBuffers();
```
}

**Rationale:** wxGLCanvas 3.1 uses physical pixels on HiDPI (Section 3). ImGui expects framebuffer coordinates. The SetCurrent->SwapBuffers flow must be atomic within a single paint event.

### 137. Multi-Platform Compilation: wxGTK (Linux) — Build-Time Requirements  **(P)** [R33]

Building wxWidgets 3.1.5 with the wxGTK port requires the GTK development headers (not just the runtime libraries) and GNU make. The official `docs/gtk/install.md` documents the canonical configure+make flow and the feature switches that control which optional backends (EGL, webview, media, OpenGL) are compiled in — backends compiled in **by default** are the ones that surface as runtime instability in Section 2.

- [ ] Install GTK dev headers, not just the runtime library — verify with `pkg-config --modversion gtk+-3.0` → **(P)** [R33]

- [ ] GTK 3 is the default toolkit (`--with-gtk=3`); use `--with-gtk=2` only when GTK2 is explicitly required → **(P)** [R33]

- [ ] Use GNU make (GNU/BSD/Solaris make are supported; other make programs may fail) → **(P)** [R33]

- [ ] Configure failures: read the generated `config.log` for the root cause → **(P)** [R33]

- [ ] EGL backend for wxGLCanvas is enabled **by default** when EGL is available — `--disable-glcanvasegl` to opt out (ties into the Wayland/EGL instability of Section 2) → **(P)** [R33]

- [ ] wxWebView requires `webkit2gtk` dev packages; `--disable-webview` drops the dependency → **(P)** [R33]

- [ ] wxMediaCtrl requires GStreamer dev packages; `--disable-mediactrl` drops the dependency → **(P)** [R33]

- [ ] `--without-opengl` disables wxGLCanvas OpenGL support entirely → **(P)** [R33]

- [ ] Cross-compiling is supported via the `--host` configure option → **(P)** [R33]

- [ ] Static libraries: `--disable-shared`; single monolithic library: `--enable-monolithic` → **(P)** [R33]

- [ ] `--disable-sys-libs` forces the built-in libpng/libjpeg/libtiff/expat to minimize external dependencies → **(P)** [R33]

- [ ] Build in a separate directory from the sources, never inside the source tree → **(P)** [R33]

- [ ] 3.1.5 has known Unix build failures on older Cairo/glibc systems (build fixes landed in 3.2.0) — on legacy distros verify against the 3.2.0 fix list or upgrade → **(P)** [R38]

- [ ] Immediate crashes at app start: the library was compiled with different flags/compiler than the program, or headers/libraries from two different wxWidgets versions are mixed — uninstall stale installs and rebuild → **(P)** [R33]

```sh
# Verify the GTK3 development headers are present
pkg-config --modversion gtk+-3.0

# Build in a separate directory (never inside the source tree)
mkdir buildgtk && cd buildgtk
../configure --with-gtk=3 --disable-glcanvasegl
make -j8
```

**Rationale:** docs/gtk/install.md is the authoritative build reference for the wxGTK port; the GTK3-default and EGL-by-default behaviors directly determine which Section 2 runtime pitfalls can occur on a given machine.

### 138. Multi-Platform Compilation: wxMSW (Windows) — Build-Time Requirements  **(P)** [R32]

The official `docs/msw/install.md` documents the two supported Windows build routes — MSVC `makefile.vc` and MinGW-w64/Cygwin `makefile.gcc` — plus the per-config `setup.h` model that most "no such file" / mismatched-config link errors trace back to.

- [ ] Never extract or build under a path containing spaces (e.g. "C:\Program Files") — breaks makefiles and command-line tools → **(P)** [R32]

- [ ] MSVC: `nmake /f makefile.vc` from a VS command prompt — parameters `BUILD=release`, `SHARED=1`, `TARGET_CPU=X64|ARM64|IA64` (unset = 32-bit x86) → **(P)** [R32]

- [ ] MinGW-w64/Cygwin: `mingw32-make -f makefile.gcc` from `cmd.exe` — the makefile.gcc route does not work under a Unix shell (use configure under MSYS/Cygwin instead) → **(P)** [R32]

- [ ] MinGW parallel build (`-jN`): run the `setup_h` target once first, then the full make — works around a makefile bug → **(P)** [R32]

- [ ] MinGW C++11 builds: use `-std=gnu++11`, NOT `-std=c++11` — wxWidgets relies on GNU extensions that strict `-std=c++11` disables → **(P)** [R32]

- [ ] The master `setup.h` lives at `include/wx/msw/setup.h` and is copied per build config under `lib/` — app include paths must point at the **config-specific** directory, never a hardcoded path (see Section 10) → **(P)** [R32]

- [ ] `RUNTIME_LIBS=static` must NOT be combined with `SHARED=1` (DLL build) → **(P)** [R32]

- [ ] DLL names embed compiler + version + vendor (e.g. `wxmsw311u_core_vc_custom.dll`); keep multiple builds side-by-side with `CFG=` / `COMPILER_PREFIX=` / `VENDOR=` → **(P)** [R32]

- [ ] Multiple MSVC versions on one machine: set `wxCompilerPrefix=vc$(PlatformToolsetVersion)` in `wx_local.props` so build directories do not collide → **(P)** [R32]

- [ ] MSVC apps auto-link via `#pragma comment(lib)`; MinGW/Cygwin apps must link the wx libraries explicitly (e.g. `wxmsw31ud_core.lib wxbase31ud.lib wxpngd.lib ...`) → **(P)** [R32]

- [ ] App-side preprocessor defines: `__WXMSW__`, `_UNICODE`, `NDEBUG` (release), and `WXUSINGDLL` for DLL builds → **(P)** [R32]

- [ ] MSVC: prepend `$WXWIN\include\msvc` to the include paths; other compilers append `<wx-lib-dir>\mswu[d]` → **(P)** [R32]

- [ ] Alternative: `vcpkg install wxwidgets` — the vcpkg port is kept up to date by the Microsoft team and community → **(P)** [R32]

- [ ] Building 3.1.5 with newer MinGW-w64 headers: `wxDECL_FOR_MINGW32_ALWAYS(wcsnlen)` collides with the header's own `wcsnlen` declaration (`redundant redeclaration`) — patch the header or use the provided `makefile.gcc` → **(P)** [R35]

```sh
# MSVC — 64-bit release DLL
cd $WXWIN\build\msw
nmake /f makefile.vc BUILD=release SHARED=1 TARGET_CPU=X64

# MinGW-w64 — release static (from cmd.exe, not bash)
cd $WXWIN\build\msw
mingw32-make -f makefile.gcc BUILD=release
```

**Rationale:** docs/msw/install.md documents all makefile parameters and the setup.h per-config copy model; the wcsnlen conflict is a documented 3.1.5 + new-MinGW-w64 incompatibility (Stack Overflow 67496624).

### 139. Multi-Platform Compilation: wxOSX (macOS) — Build-Time Requirements  **(P)** [R34][R1]

The official `docs/osx/install.md` covers the Cocoa (wxOSX/Cocoa) build; `docs/changes.txt` pins the SDK/toolchain floor. Distributing shared builds on macOS has its own mandatory bundling step.

- [ ] Xcode is required; the canonical flow is a separate build dir: `mkdir build-cocoa-debug && cd build-cocoa-debug && ../configure --enable-debug && make` → **(P)** [R34]

- [ ] Minimum SDK is 10.11 and Xcode must be ≥ 7.2.1; deployment target down to 10.10.5 is supported (see Section 10) → **(P)** [R1]

- [ ] 3.1.5 does not build with Xcode 8.3 for the i386 (32-bit) architecture — `-Wc++11-narrowing` error in `src/osx/carbon/graphics.cpp:917` (`CGSize s = { f, f };` double→CGFloat), and i386 was effectively dropped by the maintainers; build x86_64/ARM64 targets only (#22227) → **(P)** [R35]

- [ ] 3.1.5's wxOSX Xcode project includes i386 by default and has no arm64 target — on Apple Silicon build x86_64 under Rosetta or pass explicit `-arch arm64` to configure; 3.2.0 removed i386 and added arm64 (Xcode 12+) → **(P)** [R38]

- [ ] Shared libraries (default) for distribution: copy the wx dylibs into the app bundle and fix their load paths with `install_name_tool`; static (`--disable-shared`) needs no bundling step → **(P)** [R34]

- [ ] Skip `make install` on macOS — use the full path to `wx-config` under the build directory instead → **(P)** [R34]

- [ ] `build/osx/wxcocoa.xcodeproj` builds the library from Xcode; wxrc has no Xcode project — build it from the command line → **(P)** [R34]

```sh
mkdir build-cocoa-debug && cd build-cocoa-debug
../configure --enable-debug
make
# Distribution with shared libs: copy dylibs into <App>.app/Contents/Frameworks
# and fix load paths, e.g.
# install_name_tool -id @executable_path/../Frameworks/libwx_osx_cocoa-3.1.dylib ...
```

**Rationale:** docs/osx/install.md documents the Cocoa build and the install_name_tool bundling step; changes.txt (3.1.5) sets the SDK 10.11 / Xcode 7.2.1 floor; issue #22227 documents the Xcode 8.3 i386 failure.

### 140. Cross-Platform Build Integration: wx-config, CMake, and ABI/Link Consistency  **(P)** [R1][R32][R33][R35]

Cross-platform compilation fails most often not inside the library build itself but where the consuming application and the library disagree on configuration — toolchain, debug/release, Unicode, static/shared, or which wx-config tree the flags come from.

- [ ] wxMSW 3.1.5 static build with a non-MSVC compiler (e.g. MinGW) **without** wx-config: link `uxtheme.lib`, `shlwapi.lib`, and `version.lib` yourself — only wx-config/MSVC add them automatically → **(P)** [R1]

- [ ] `webview` is not part of the default `wx-config --libs` output — request it explicitly: `wx-config --libs std,webview` (see Sections 8 and 10) → **(P)** [R1]

- [ ] wxGTK: always take `wx-config --cxxflags --libs` from the **same** build tree the library came from — flags from a different build/config produce start-up crashes → **(P)** [R33]

- [ ] Program and library must share the same compiler and debug/optimise/Unicode settings — mismatches cause asserts, link errors, or runtime corruption → **(P)** [R33]

- [ ] CMake `find_package(wxWidgets)` fails to locate a MinGW-w64-built 3.1.5 tree (#19278) — it works for MSVC and Linux GCC; fall back to `find_package(wxWidgets CONFIG)` and adjust `CMAKE_LIBRARY_PATH` for system libraries (#24454) → **(P)** [R35]

- [ ] MinGW-w64 cross builds generate no `wx-config` (#24454) — do not rely on it when cross-compiling → **(P)** [R35]

- [ ] 3.1.5 ships no CMake package config file — `find_package(wxWidgets CONFIG)` works only from 3.2.0; on 3.1.5 use the FindwxWidgets module (with the MinGW-w64 caveats above) → **(P)** [R38]

- [ ] Building 3.1.5 with newer toolchains emits warnings (clang 13, gcc 11, MSVC C++20, `-std=c++20`) that a `-Werror` CI turns into hard failures — fixed in 3.2.0; pin toolchains or add suppressions → **(P)** [R38]

- [ ] Cygwin shared build exports the API via explicit `__declspec(dllexport)` — a missed symbol produces link errors; workaround: `LDFLAGS=-Wl,--export-all-symbols` → **(P)** [R33]

- [ ] MSVS 2019 16.6 changed STL internals and broke pre-3.1.5 builds; 3.1.5 contains the fix — verify the toolset when using VS2019 16.6+ → **(P)** [R1]

- [ ] CMake library targets since 3.1.4 are `wx::core`, `wx::base`, ... — never hardcode `wx/setup.h` paths (see Section 10) → **(P)** [R1]

```sh
# wxGTK — flags must come from the same build tree as the library
g++ myfoo.cpp `wx-config --cxxflags --libs` -o myfoo

# MinGW static wxMSW (no wx-config): add the system libs 3.1.5 requires
g++ myfoo.cpp -lwxmsw31u_core -lwxbase31u -luxtheme -lshlwapi -lversion
```

**Rationale:** changes.txt (3.1.5) documents the uxtheme/shlwapi/version and webview-in-wx-config changes; docs/gtk/install.md documents the same-tree/same-flags rule; issues #19278/#24454 document the CMake+MinGW-w64 find_package gap.

### 141. Real-World CI Compile Failures: wxString ?: Ambiguity and wxMediaState constexpr (Snapmaker/OrcaSlicer)  **(P)** [R36]

Two real production CI failures against wxWidgets 3.1.5 (static, unicode, `-DwxNO_UNSAFE_WXSTRING_CONV`) in the Snapmaker/OrcaSlicer "Build all" workflow demonstrate cross-toolchain compile discrepancies that MSVC-only validation cannot catch.

**Failure 1 — `?:` conditional with mixed `wxEmptyString`/`wxString` operands** (`run #32856432114`, 2026-08-25):

```cpp
// src/slic3r/GUI/Plater.cpp:9462 — compiles on MSVC (windows-2022), FAILS on GCC and AppleClang
diameter_combo->SetValue(diam_str.empty() ? wxEmptyString : wxString(diam_str) + "mm");
```

- GCC 13 (ubuntu-24.04): `error: operands to '?:' have different types 'const wxChar*' {aka 'const wchar_t*'} and 'wxString'`
- AppleClang (macos-14 arm64): `error: conditional expression is ambiguous; 'const wxChar *' (aka 'const wchar_t *') can be converted to 'wxString' and vice versa`
- MSVC (windows-2022): the same translation unit compiles and the build succeeds.

- [ ] Never put a raw `wxEmptyString` (or any `const wxStringCharType*`) and a `wxString` as the two arms of a `?:` — GCC/Clang reject the ambiguous conversion, MSVC silently accepts → **(P)** [R36]

- [ ] Fix: unify both operands to `wxString` — `diam_str.empty() ? wxString(wxEmptyString) : wxString(diam_str) + "mm"` (or `wxString{}`) → **(P)** [R36]

- [ ] MSVC-only CI is insufficient: this exact failure passed Windows and broke Linux + macOS — every wxWidgets CI matrix must build at least one GCC or Clang port → **(P)** [R36]

- [ ] Enforce unsafe wxString-conversion rejection at compile time with `-DwxNO_UNSAFE_WXSTRING_CONV` (as OrcaSlicer does) — turns the §1/§131 runtime hazards into hard build errors on all toolchains → **(P)** [R36]

**Failure 2 — out-of-range value forced into a `constexpr` wx enum** (`run #32696369649`, 2026-08-24, macos-26 / Xcode 26.6):

```cpp
// src/slic3r/GUI/wxMediaCtrl2.h:39 — app-side extension of wxMediaState via C-style cast
static constexpr wxMediaState MEDIASTATE_BUFFERING = (wxMediaState) 6;
```

- AppleClang (Xcode 26.6): `error: constexpr variable 'MEDIASTATE_BUFFERING' must be initialized by a constant expression` — `integer value 6 is outside the valid range of values [0, 3] for the enumeration type 'wxMediaState'`
- The project's `-Wno-error=enum-constexpr-conversion` flag is **GCC-only**: clang reports `warning: unknown warning option '-Werror=enum-constexpr-conversion'` and still emits the error.

- [ ] Do not inject out-of-range values into a wx enum (`wxMediaState`, `wxKeyCode`, etc.) via C-style casts inside `constexpr` — newer AppleClang rejects what older compilers tolerated; store the extension as `static constexpr int` or a non-constexpr variable → **(P)** [R36]

- [ ] `-Wno-error=enum-constexpr-conversion` is a GCC-only flag (GCC 13+): clang does not recognize it and treats the same condition as a hard error — never rely on it for cross-toolchain suppression → **(P)** [R36]

```cpp
// Bad — ambiguous ?: (GCC/Clang reject, MSVC accepts)
diameter_combo->SetValue(diam_str.empty() ? wxEmptyString : wxString(diam_str) + "mm");

// Good — both operands wxString
diameter_combo->SetValue(diam_str.empty() ? wxString(wxEmptyString) : wxString(diam_str) + "mm");

// Bad — out-of-range enum value in constexpr (Xcode 26 clang errors)
static constexpr wxMediaState MEDIASTATE_BUFFERING = (wxMediaState) 6;

// Good — keep the extension out of the enum's value space
static constexpr int MEDIASTATE_BUFFERING = 6;   // compared via static_cast if needed
```

**Rationale:** both failures are reproduced in the public Snapmaker/OrcaSlicer "Build all" workflow logs (runs #32856432114 and #32696369649) against the wxWidgets 3.1.5 deps build (`found suitable version "3.1.5"`), compiled with `-std=gnu++17`, `-DwxNO_UNSAFE_WXSTRING_CONV`, static unicode, on wxGTK3/wxOSX ports. They are direct evidence for the toolchain-divergence warnings of Sections 1 and 140.

---

### 142. Child Window Background Colour Inheritance (wxStaticText / wxPanel / wxStaticBitmap)  **(P)** [R13][R23]

When a wxStaticText, wxStaticBitmap, or wxPanel child is placed inside a coloured container (e.g. a white card StaticBox sitting on a gray dialog), the child does NOT inherit the parent's background colour on wxMSW. On wxOSX the child often picks up the parent bg transparently, so the bug only manifests on Windows — making it easy to miss during macOS-centric development.

- [ ] Always pair `SetForegroundColour()` with `SetBackgroundColour()` for every label placed inside a coloured container → **(P)** [R23]
- [ ] Do NOT assume a child `wxPanel` / `wxStaticText` inherits the card's `SetBackgroundColor()` — set it explicitly on each child → **(P)** [R23]
- [ ] `StaticBox` does NOT propagate its background colour to children — every child window needs its own `SetBackgroundColour()` call → **(P)** [R23]
- [ ] Wrap colours in `StateColor::darkModeColorFor(wxColour("#RRGGBB"))` (Snapmaker_Orca convention) or `wxSystemSettings::GetColour(wxSYS_COLOUR_WINDOW)` so the card stays theme-aware — see §17 → **(P)** [R13]
- [ ] Test card/label rendering on wxMSW explicitly: a bug that looks fine on macOS will leak the dialog bg through on Windows → **(P)** [R13]
- [ ] Audit existing card-building functions when adding a new label row — easy to remember for the title, easy to forget for inline labels ("Plate", "View", row captions, etc.) → **(P)** [R23]

```cpp
// Good — every label in the card gets an explicit bg
auto* card = new StaticBox(parent, ...);
card->SetBackgroundColor(StateColor(std::pair(wxColour("#FFFFFF"), static_cast<int>(StateColor::Normal))));

auto* lbl = new wxStaticText(card, wxID_ANY, _L("Plate"));
lbl->SetFont(Label::Body_12);
lbl->SetForegroundColour(StateColor::darkModeColorFor(wxColour("#4A4A4A")));
lbl->SetBackgroundColour(StateColor::darkModeColorFor(wxColour("#FFFFFF")));  // REQUIRED on wxMSW
```

```cpp
// Bad — label shows the dialog's gray bg through on Windows (looks fine on macOS)
auto* lbl = new wxStaticText(card, wxID_ANY, _L("Plate"));
lbl->SetForegroundColour(StateColor::darkModeColorFor(wxColour("#4A4A4A")));
// missing SetBackgroundColour — leaks #F8F7F7 through on wxMSW
```

**Rationale:** Snapmaker_Orca `MixedFilamentBatchDialog.cpp` (`build_preview_card`, `build_manual_card`, `build_recommended_card`) had this bug — the "Plate" and "View" labels inside the preview card were missing `SetBackgroundColour()` and rendered with the dialog bg (#F8F7F7) showing through on Windows, while looking correct on macOS. The fix pattern (explicit bg on every label, wrapped in `StateColor::darkModeColorFor`) is now applied across all card-building functions in that file. See §17 for dark-mode colour handling and `wxSystemSettings::GetColour()`.

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Implicit wxString -> char* Conversion

- **Appearance:** open(str.c_str(), "r") or std::string s = str;

- **Trap:** Compiles in some build configs; asserts or produces garbage in Unicode-WCHAR builds

- **Consequence:** Runtime assertion failure, corrupted filenames, or silent data loss

- **Fix:** Use str.utf8_string().c_str() (3.1.5+) or str.mb_str(wxConvUTF8).data()

### Anti-Pattern 1b: ToUTF8()/mb_str() Temporary Buffer Dangling Pointer  **(P)** [R30]

- **Appearance:** std::string s = wxstr.ToUTF8().data(); or open(wxstr.mb_str(wxConvUTF8).data(), "r")

- **Trap:** ToUTF8()/utf8_str()/mb_str() return temporary wxScopedCharBuffer; calling .data() on the temporary creates a dangling pointer when the temporary is destroyed at ;

- **Consequence:** Undefined behaviour - corrupted strings, segfault, or silently wrong data

- **Fix:** Assign buffer to local variable first: const auto buf = wxstr.ToUTF8(); std::string s = buf.data(); or use wxstr.utf8_string() (3.1.5+)

### Anti-Pattern 2: Direct GUI Access from Worker Thread

- **Appearance:** `workerThread` calls `m_gauge->SetValue(n)` or `m_list->Append(...)` directly from `Entry()`

- **Trap:** wxWidgets GUI objects are not thread-safe; only the main thread may touch them (see §6, §16). Symptoms are non-deterministic: crashes, corruption, or silent mis-paint — often only under load or on a specific port (wxGTK especially)

- **Consequence:** Race condition, heap corruption, intermittent crash that never reproduces in the debugger, or events delivered to the wrong window

- **Fix:** Communicate via `wxTheApp->CallAfter([](){...})` (lambda runs in main thread) or `wxQueueEvent(handler, new wxThreadEvent(...))`. Never use `wxMutexGuiEnter()`/`wxMutexGuiLeave()` — deprecated and unsafe (#10366)

## See Also

- [Concurrency and Thread Safety](../concurrency/thread-safety.md) — general C++ thread safety rules

- [RAII and Resource Management](../memory/raii.md) — wxObject lifetime patterns

- [C++ Build System and Include Hygiene](../build/cmake-include-hygiene.md) — CMake + wxWidgets integration

- [C++ Toolchain and Compiler Flags](../build/toolchain-and-compiler-flags.md) — compiler matrix, warning policy, reproducible toolchains

- [C++ Const Correctness](../correctness/const-correctness.md) — wxString const correctness

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |

|-------|------|--------|--------|------------|---------------|

| R1 | P | wxWidgets 3.1.5 docs/changes.txt | Incompatible Changes; 3.1.5 Release | verified-2026 | 2026-07 |

| R2 | P | wxWidgets C++ Thread Safety Documentation | wxThread, wxMutexGuiEnter | verified-2026 | 2026-07 |

| R3 | P | wxWidgets GitHub Issues #26248, #26250, #26340, #26410, #24977 | wxGLCanvas EGL/Wayland | verified-2026 | 2026-07 |

| R4 | P | wxWidgets GitHub Issues #25686, #18057, #18167, #18337, #24148, #24382, #17028, #18045 | wxDataViewCtrl crashes | verified-2026 | 2026-07 |

| R5 | P | wxWidgets GitHub Issue #21105 | wxGTK wxPostEvent + threads | verified-2026 | 2026-07 |

| R6 | P | wxWidgets GitHub Issue #26490 | wxPropertyGrid DPI regression | verified-2026 | 2026-07 |

| R7 | P | wxWidgets CMake / wx-config Documentation | Build system integration | verified-2026 | 2026-07 |

| R8 | P | wxWidgets 3.1.5 docs/doxygen/overviews/string.h, cmake.h, unicode.h | wxString encoding, build system, common pitfalls | verified-2026 | 2026-07 |

| R10 | P | wxWidgets 3.1.5 docs/doxygen/overviews/eventhandling.h, thread.h, sizer.h | Official documentation overviews | verified-2026 | 2026-07 |

| R11 | P | wxWidgets GitHub Issues #18964, #12464, #11842, #16088, #4598 | wxSizer layout pitfalls | verified-2026 | 2026-07 |

| R12 | P | wxWidgets GitHub Issue #10366 (ticket) | wxMutexGuiEnter/Leave unsafe | verified-2026 | 2026-07 |

| R13 | P | wxWidgets GitHub Issues #24634, #25681, #25527, #25783, #26198, #26569, #25048 | Dark mode and theme issues | verified-2026 | 2026-07 |

| R14 | P | wxWidgets GitHub Issues #17341, #12808, #23354, #16902, #3449 | Keyboard navigation and tab traversal | verified-2026 | 2026-07 |

| R15 | P | wxWidgets 3.1.5 docs/doxygen/overviews/windowdeletion.h | Window deletion lifecycle | verified-2026 | 2026-07 |

| R16 | P | wxWidgets GitHub Issues #14403, #13110, #12458, #12762, #18014, #13442, #4381, #15243, #19109, #10577, #18492, #15259, #17031, #24649, #12378, #9870, #15647, #12952, #9862, #11404, #25033, #10670 | wxImage/clipboard/XRC/socket/listctrl/combobox/filename pitfalls | verified-2026 | 2026-07 |

| R17 | P | wxWidgets 3.1.5 docs/doxygen/overviews/bitmap.h, dc.h, validator.h, scrolling.h, nonenglish.h, roughguide.h | Official overviews for resource/DC/validator/scrolling/i18n | verified-2026 | 2026-07 |

| R18 | P | wxWidgets GitHub Issues #15417, #4363, #4841, #19210, #10475, #20325, #19048, #17188, #15644, #11831, #10672, #23850, #14033, #11779, #24966, #13381, #13520 | wxAUI/font/taskbar/printing/splitter/richtext issues | verified-2026 | 2026-07 |

| R19 | P | wxWidgets 3.1.5 docs/doxygen/overviews/log.h, aui.h | Logging multithreading, AUI overview | verified-2026 | 2026-07 |

| R20 | P | wxWidgets GitHub Issues #17282, #16246, #11595, #9388, #12767, #10557, #18695, #18965, #14697, #12583, #12037, #12036 | Menu/spinctrl/dnd/html/datepicker/statusbar issues | verified-2026 | 2026-07 |

| R21 | P | wxWidgets 3.1.5 docs/doxygen/overviews/customwidgets.h, exceptions.h, html.h | Custom widgets, exceptions, HTML overview | verified-2026 | 2026-07 |

| R22 | P | wxWidgets GitHub Issues #23367, #18845, #12037, #11567, #24966, #16443, #18625, #19199; wxWidgets 3.1.5 docs/changes.txt (macOS section) | wxOSX macOS platform pitfalls (menu bar, App Nap, file assoc, Retina, pasteboard, sheets, NSStatusItem, panels, NSApp delegation, color panel) | verified-2026 | 2026-07 |

| R23 | P | wxWidgets 3.1.5 docs/doxygen/overviews/sizer.h, roughguide.h; wxWidgets 3.1.5 docs/doxygen/overviews/string.h, cmake.h, unicode.h cross-platform UI best practices; wxWidgets GitHub Issues #18964, #12464, #11842, #16088 | UI/UX best practices (control semantics, layout, notebook, tooltip, static box, status bar, static text, choice/combo, file dialog, progress dialog) | verified-2026 | 2026-07 |

| R24 | P | wxWidgets GitHub Issues #23446, #18845, #19199, #16443; wxWidgets 3.1.5 docs/doxygen/classwx_rich_text_ctrl.h, classwx_animation_ctrl.h, classwx_hyperlink_ctrl.h, classwx_collapsible_pane.h, classwx_search_ctrl.h, classwx_info_bar.h | RichText, Animation, Hyperlink, CollapsiblePane, SearchCtrl, InfoBar, BannerWindow, ActivityIndicator, CommandLinkButton, RearrangeList | verified-2026 | 2026-07 |

| R25 | P | wxWidgets GitHub Issues #22604, #24813, #22085, #21455, #16862, #19814; wxWidgets 3.1.5 docs/wxGTK-overview; GTK CSS theming documentation; Wayland clipboard specification | wxGTK platform-specific pitfalls (themes, dark mode, WM resize, compositing, IME, file dialog, scroll, main loop, clipboard, DnD) | verified-2026 | 2026-07 |

| R26 | P | wxWidgets GitHub Issues #25527, #25681, #26198, #24634, #26490, #23456; wxWidgets 3.1.5 docs/wxMSW-overview; Microsoft Windows DPI awareness documentation; DWM API documentation | wxMSW platform-specific pitfalls (per-monitor DPI, visual themes, list header, rich text, registry, file dialog, task dialog, DWM glass, clipboard format, accessibility) | verified-2026 | 2026-07 |

| R27 | P | wxWidgets GitHub Issues #21105, #10366, #22804, #18856, #17245, #19998; wxWidgets 3.1.5 docs/doxygen/classwx_thread.h, classwx_stop_watch.h, classwx_stream.h, classwx_regex.h, classwx_variant.h, classwx_date_time.h, classwx_file_history.h | Threading/IPC/system pitfalls (wxThreadHelper, critical section, condition, single instance, stopwatch, stream, regex, variant, datetime, file history) | verified-2026 | 2026-07 |

| R28 | P | wxWidgets GitHub Issues #17815, #19456, #22109, #16784; wxWidgets 3.1.5 docs/doxygen/classwx_locale.h, classwx_font_mapper.h, classwx_grid.h, classwx_timer.h, classwx_accelerator.h; GNU gettext documentation | i18n/accessibility/misc pitfalls (locale, encoding, plurals, font mapper, grid editors/table/selection, timer, busy cursor, accelerator) | verified-2026 | 2026-07 |

| R29 | P | wxWidgets GitHub Issues #24967, #23456, #19210, #10475, #20325, #17188; wxWidgets 3.1.5 docs/doxygen/classwx_web_view.h, classwx_printout.h, classwx_print_preview.h, classwx_image.h, classwx_cursor.h, classwx_icon_bundle.h, classwx_drop_target.h | WebView, printing, image, cursor, icon, DnD pitfalls (backend, cookies, print, PDF, scaling, handler, hotspot, bundle, custom format) | verified-2026 | 2026-07 |

| R30 | P | wxWidgets 3.1.5 interface/wx/string.h (utf8_str/ToUTF8/mb_str/wc_str), interface/wx/window.h (Freeze/Thaw/wxWindowUpdateLocker), docs/doxygen/overviews/customwidgets.h, interface/wx/popupwin.h, interface/wx/webview.h; GitHub Issues #19814, #16862, #21455 | String buffer lifetime, batch update, custom widget paint, popup lifecycle, WebView Edge backend, ImGui+wxGLCanvas integration | verified-2026 | 2026-07 |

| R31 | P | wxWidgets 3.1.5 docs/doxygen/classwx_display.h; wxWindow::GetDPIScaleFactor() documentation | wxDisplay::GetPPI(), wxDisplay::GetScaleFactor(), GetDPIScaleFactor() per-monitor DPI queries | verified-2026 | 2026-07 |

| R32 | P | wxWidgets 3.1.5 docs/msw/install.md | wxMSW build: makefile.vc/makefile.gcc, setup.h per-config copy, RUNTIME_LIBS/TARGET_CPU, app-side defines and linking | verified-2026 | 2026-08 |

| R33 | P | wxWidgets 3.1.5 docs/gtk/install.md | wxGTK build: GTK3 default, dev packages, configure options (glcanvasegl/webview/mediactrl/opengl), GNU make, config.log, same-tree wx-config | verified-2026 | 2026-08 |

| R34 | P | wxWidgets 3.1.5 docs/osx/install.md | wxOSX build: Cocoa, Xcode, separate build dir, bundle + install_name_tool for shared libs, wxcocoa.xcodeproj | verified-2026 | 2026-08 |

| R35 | P | wxWidgets GitHub Issues #19278, #24454, #22227; Stack Overflow 67496624 | CMake find_package vs MinGW-w64, missing wx-config on mingw-cross, Xcode 8.3 i386 build failure, wcsnlen redeclaration | verified-2026 | 2026-08 |

| R36 | P | Snapmaker/OrcaSlicer GitHub Actions "Build all" runs #32856432114 (2026-08-25), #32696369649 (2026-08-24) | Real-world wxWidgets 3.1.5 compile failures: Plater.cpp:9462 wxString ?: ambiguity (GCC13/AppleClang vs MSVC); wxMediaCtrl2.h:39 constexpr wxMediaState out-of-range (Xcode 26 clang); wxNO_UNSAFE_WXSTRING_CONV usage | verified-2026 | 2026-08 |

| R37 | P | Snapmaker/OrcaSlicer GitHub Actions "Build all" runs #32143560654, #32025650653, #31679936598 (Flatpak aarch64 jobs, 2026-08); wxWidgets 3.1.5 include/wx/wupdlock.h | 'wxWindowUpdateLocker was not declared in this scope' (TimelapseDownloadPopup.cpp:492, MixedFilamentBatchDialog.cpp:2715) — wxWindowUpdateLocker is declared in <wx/wupdlock.h> (which includes wx/window.h, not vice versa); same code compiles on ubuntu/macos/windows | verified-2026 | 2026-08 |

| R38 | P | wxWidgets 3.2.0 docs/changes.txt (3.2.0 release section, 2022-07-07) | Reverse evidence of 3.1.5 build defects: no CMake package config file (CONFIG mode only from 3.2.0); wxOSX Xcode project targets i386 by default and lacks arm64; warning fixes for clang 13 / gcc 11 / MSVC C++20; Unix build fixes for older Cairo/glibc | verified-2026 | 2026-08 |

---

## Changelog

- 2026.08: Added R38 (3.2.0 changes.txt reverse evidence) — §137 older Cairo/glibc build fixes; §139 wxOSX i386-by-default + no arm64 target (Rosetta or explicit -arch arm64); §140 no CMake CONFIG file before 3.2.0, newer-toolchain warning fixes (clang 13/gcc 11/MSVC C++20).

- 2026.08: Added Section 132 item + R37 — OrcaSlicer Flatpak CI evidence: wxWindowUpdateLocker not declared in scope (TimelapseDownloadPopup.cpp:492, MixedFilamentBatchDialog.cpp:2715); verified via 3.1.5 source that the class is declared in <wx/wupdlock.h> (which includes wx/window.h, not vice versa); added include-hygiene item (3.1.5 removed wx/treebook.h→wx/treectrl.h transitive include).

- 2026.08: Added Section 141 — real-world CI compile-failure evidence from Snapmaker/OrcaSlicer "Build all" runs (wxString ?: ambiguity: GCC 13 + AppleClang reject, MSVC accepts, Plater.cpp:9462; constexpr wxMediaState out-of-range on Xcode 26 clang, wxMediaCtrl2.h:39; GCC-only -Wno-error=enum-constexpr-conversion). Added reference label R36.

- 2026.08: Added Sections 137-140 (multi-platform compilation) covering wxGTK/wxMSW/wxOSX build-time requirements and cross-platform build integration (wx-config/CMake/ABI consistency). Sources: official docs/msw|gtk|osx/install.md, changes.txt build notes, GitHub issues #19278/#24454/#22227, Stack Overflow 67496624. Added reference labels R32-R35 and related link to cpp/build/toolchain-and-compiler-flags.md.

- 2026.07: Added §142 (Child Window Background Colour Inheritance — wxStaticText/wxPanel/wxStaticBitmap do not inherit parent bg on wxMSW) based on a real Snapmaker_Orca bug in `MixedFilamentBatchDialog.cpp` ("Plate"/"View" labels missing `SetBackgroundColour()`, leaked #F8F7F7 through on Windows while looking correct on macOS). References R13 (dark mode) and R23 (control semantics) reused — no new reference added. Renumbered from §137 to §142 on merge to avoid collision with the multi-platform build sections.

- 2026.07: Adversarial audit (Phase 1-4) against wxWidgets v3.1.5 source. Corrected fabricated/nonexistent APIs in §52 (SetAppNapEnabled), §54b (MSWGetContentScaleFactor; GetDPIScaleFactor returns double not int), §61/§62 (FromDIP signatures), §92 (MSWEnableDarkMode — added only in 3.3/master), §96 (wxFD_USE_LEGACY_DIALOG does not exist). Corrected §131 wc_str/c_str build-conditional behavior and removed a fabricated `printf("%s", utf8_str().data())` quote; downgraded two items from (N) to (P). Fixed version attribution: wxBitmapBundle 3.1.5→3.1.6, wxActivityIndicator 3.1.5→3.1.0, wxEVT_DPI_CHANGED 3.1.5→3.1.6. Fixed §1 build option names: wxUSE_STL_BASE_WXSTRING→wxUSE_STL, wxUSE_UTF8_LOCALE→wxUSE_UTF8_LOCALE_ONLY. Filled empty Anti-Pattern 2; §134 tab/typo cleanup.

- 2026.07: Added sections 131-136 (ToUTF8 buffer lifetime UB, Freeze/Thaw batch update, Custom widget paint patterns, wxPopupTransientWindow lifecycle, wxWebView Edge backend, ImGui+wxGLCanvas integration); expanded Anti-Pattern 1; added reference R30. Based on wxWidgets 3.1.5 official interface headers and a production C++ codebase audit (146 ToUTF8().data() UB sites found).

- 2026.07: Initial draft from wxWidgets 3.1.5 changelog, GitHub issues, forum posts, and Stack Overflow
