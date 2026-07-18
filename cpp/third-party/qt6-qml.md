---
type: harness
id: "cpp-qt6-qml"
title: "Qt 6 QML Pitfalls, Limitations, and Best Practices Checklist"
language: "cpp"
category: "third-party"
tier: "P"
scope: "Avoid known pitfalls and limitations when using Qt 6 QML across Windows, macOS, Linux, iOS, and Android"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-18"
review_cycle: "12m"
tags: [qt, qml, gui, cross-platform, qt6, declarative]
based_on:
  - "[P] Qt 6.8 Documentation — QML Language Reference"
  - "[P] Qt 6.8 Documentation — Qt Quick Best Practices"
  - "[P] Qt Bug Reports (Jira) — QML engine issues"
  - "[P] Qt 6.8 Documentation — Integrating QML and C++"
  - "[P] Qt 6.8 Documentation — High DPI Support in Qt"
  - "[P] KDAB / ICS blog posts — QML performance and threading"
related:
  - "cpp/third-party/qt6-core.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/memory/raii.md"
supersedes: []
changelog:
  - "2026.07: Initial draft covering QML binding, memory, lifecycle, DPI, ListView, Loader, JS engine, and C++ integration"
---

# Qt 6 QML Pitfalls, Limitations, and Best Practices Checklist

**Based on:** Qt 6.8 official documentation ([P]), Qt Jira bug reports ([P]), KDAB/ICS expert blogs ([P]).
**Scope:** Common pitfalls, platform-specific limitations, and best practices for Qt 6 QML (Qt Quick / Qt Declarative). Covers desktop (Windows/macOS/Linux), mobile (iOS/Android), and embedded. Does NOT cover Qt Quick 3D or Qt for WebAssembly.

---

## Prerequisites

**Version context:** Qt 6.8 LTS (2025). Qt 5.15 LTS is still widely used; key differences from Qt 5 are noted where relevant. QML engine in Qt 6 uses the new QML compiler (qmltc / qmlsc) with stricter type checking.

**Platform matrix:**

| Platform | Backend | Key Risk Areas |
|----------|---------|----------------|
| Windows | Direct3D 11/12 | DPI scaling, text rendering, ANGLE/OpenGL fallback |
| macOS | Metal | Retina rendering, dark mode, sandbox |
| Linux | OpenGL/Vulkan | Wayland/EGL, theming, font differences |
| iOS | Metal | Screen size fragmentation, keyboard handling |
| Android | OpenGL ES | Screen size, background/foreground lifecycle |

**Binding model:** QML uses a JavaScript-based property binding engine. Bindings are re-evaluated when any dependency changes. `property var` defeats the binding engine — prefer typed properties.

---

## Checklist

### 1. Property Binding vs Assignment (The #1 QML Pitfall)  **(P)** [R1]

QML property bindings (`property int x: otherItem.x + 10`) are **live expressions** re-evaluated when dependencies change. JavaScript assignments (`onClicked: { x = 100 }`) **break** the binding permanently. This is the most common and confusing QML bug.

- [ ] Never use JavaScript assignment on a property that has a binding — it breaks the binding permanently → **(P)** [R1]
- [ ] Use `Qt.binding(() => expression)` to create a new binding from JavaScript → **(P)** [R1]
- [ ] Prefer declarative bindings in property declarations over imperative assignments in signal handlers → **(P)** [R1]
- [ ] Use `Binding` element to dynamically create/restore bindings from imperative code → **(P)** [R1]

```qml
// Good — declarative binding
Rectangle {
    width: parent.width / 2  // live binding, updates automatically
}

// Good — restore binding from JS using Qt.binding()
Button {
    onClicked: {
        rect.width = Qt.binding(() => parent.width / 2)
    }
}

// Bad — JavaScript assignment breaks binding permanently
Button {
    onClicked: {
        rect.width = 500  // binding destroyed! rect.width stays 500 forever
    }
}
```

### 2. QML Object Ownership and Memory Management  **(P)** [R1][R3]

QML engine owns objects created in QML. Objects created via `Qt.createComponent()` / `createObject()` are **not** garbage-collected — they must be explicitly destroyed. JavaScript objects referenced by QML properties may prevent GC. C++ objects exposed to QML have C++ ownership semantics (parent-child).

- [ ] Objects from `createObject()` — call `destroy()` when no longer needed, or set parent to manage lifecycle → **(P)** [R1]
- [ ] `Loader` with `active: true/false` — inactive items are destroyed unless `Loader.asynchronous` is set → **(P)** [R1]
- [ ] C++ objects exposed to QML: QML does NOT own them — ensure C++ side manages lifetime → **(P)** [R3]
- [ ] Avoid circular references in QML parent-child trees — prevents GC and causes leaks → **(P)** [R1]

```qml
// Good — explicit destruction
Component.onDestruction: {
    if (dynamicItem) dynamicItem.destroy()
}

// Good — parent management
let comp = Qt.createComponent("MyItem.qml")
let obj = comp.createObject(parentContainer)  // parent owns it

// Bad — orphaned object never destroyed
let obj = comp.createObject()  // no parent, never destroyed = leak
```

### 3. Component Lifecycle: onCompleted vs onDestruction  **(P)** [R1]

`Component.onCompleted` fires after all bindings are set up — safe to read properties. `Component.onDestruction` fires during destruction but children may already be destroyed. `Item.visible` false vs `Loader.active` false have different lifecycle implications.

- [ ] Use `Component.onCompleted` for initialization — all properties and children are ready → **(P)** [R1]
- [ ] Do NOT access children in `Component.onDestruction` — they may already be destroyed → **(P)** [R1]
- [ ] `Loader.active: false` destroys the loaded item; `Item.visible: false` keeps it alive → **(P)** [R1]
- [ ] `Timer` with `running: true` and no parent — continues after item destruction unless explicitly stopped → **(P)** [R1]

```qml
// Good — safe init and cleanup
Item {
    Component.onCompleted: {
        // All children exist, bindings active
        console.log("Ready:", childItem.width)
    }
    Component.onDestruction: {
        timer.stop()  // stop timers before destruction
    }
}

// Bad — accessing destroyed children
Component.onDestruction: {
    childItem.doSomething()  // UB: child may already be destroyed
}
```

### 4. ListView / TableView Performance and Delegate Pitfalls  **(P)** [R1][R2]

`ListView` and `TableView` use delegate pooling for performance. Delegates are **reused**, not recreated. Caching delegates breaks reuse. `cacheBuffer` and `displayMargin` control pre-rendering area. `Repeater` does NOT pool — use `ListView` for large datasets.

- [ ] Never store state in delegate root item — use `model` roles or external storage; delegates are reused → **(P)** [R1]
- [ ] Use `required property` for model roles in delegates for compile-time checking → **(P)** [R1]
- [ ] `ListView.cacheBuffer`: set to visible area height for smooth scrolling; too large wastes memory → **(P)** [R2]
- [ ] For >1000 items: use `DelegateModel` with incremental loading, not `Repeater` → **(P)** [R2]
- [ ] `TableView` with large models: implement `QAbstractItemModel::canFetchMore()` on C++ side → **(P)** [R2]

```qml
// Good — correct delegate with required properties
ListView {
    model: myModel
    delegate: Rectangle {
        required property string name
        required property int value
        Text { text: name + ": " + value }
    }
}

// Bad — storing state in delegate (lost on reuse)
ListView {
    model: myModel
    delegate: Rectangle {
        property bool selected: false  // WRONG: lost on delegate reuse
        MouseArea { onClicked: selected = !selected }
    }
}
```

### 5. Loader and Dynamic Component Creation  **(P)** [R1][R3]

`Loader` asynchronously loads QML components. Accessing `Loader.item` before loading completes returns `null`. Setting `Loader.source` triggers async loading — use `Loader.status` or `onLoaded` signal. Multiple `Loader` instances with the same source share component cache.

- [ ] Always check `Loader.status === Loader.Ready` before accessing `Loader.item` → **(P)** [R1]
- [ ] Use `Loader.setSource(source, props)` for parameterized loading instead of post-load property setting → **(P)** [R1]
- [ ] `Loader.asynchronous: true` prevents UI freeze for heavy components; use `onLoaded` for post-load setup → **(P)** [R1]
- [ ] `Loader.active: false` destroys the item; toggling active causes destroy/create cycles — cache state externally → **(P)** [R3]

```qml
// Good — safe Loader with status check
Loader {
    id: loader
    source: "HeavyComponent.qml"
    asynchronous: true
    onLoaded: {
        loader.item.initialize(data)  // item is ready here
    }
}

// Bad — accessing item before loaded
Loader { id: loader; source: "Page.qml" }
// loader.item.width  // null reference if not loaded yet
```

### 6. DPI Scaling and High-DPI in QML  **(P)** [R5]

Qt 6 enables high-DPI scaling by default. QML uses logical pixels. `Screen.devicePixelRatio` returns the current scale factor. On Windows with fractional scaling (125%, 150%), rounding policy affects QML rendering. `Qt::AA_EnableHighDpiScaling` is default in Qt 6.

- [ ] QML coordinates are in logical pixels (device-independent) — do NOT multiply by `devicePixelRatio` → **(P)** [R5]
- [ ] Set `QT_SCALE_FACTOR_ROUNDING_POLICY=RoundPreferFloor` for fractional DPI on Windows → **(P)** [R5]
- [ ] `Screen.devicePixelRatio` returns **integer** on Qt < 6.5; use `QWindow::devicePixelRatio()` from C++ for fractional → **(P)** [R5]
- [ ] PNG images with `sourceSize` set render at native resolution; omit `sourceSize` for automatic DPI scaling → **(P)** [R5]
- [ ] Test on 100%, 125%, 150%, 200% scaling on Windows and Retina macOS → **(P)** [R5]

```qml
// Good — correct DPI-aware Image
Image {
    source: "icon.png"
    width: 48  // logical pixels, automatically scaled
    // do NOT set sourceSize unless you need a specific resolution
}

// Good — check fractional DPI from C++ side
// In main.cpp: QGuiApplication::setHighDpiScaleFactorRoundingPolicy(
//     Qt::HighDpiScaleFactorRoundingPolicy::RoundPreferFloor)

// Bad — manual DPI multiplication defeats auto-scaling
Rectangle {
    width: 100 * Screen.devicePixelRatio  // WRONG: double-scaling
}
```

### 7. C++ / QML Integration: Context Properties and Type Registration  **(P)** [R4]

QML engine accesses C++ objects via `QQmlContext::setContextProperty()` or `qmlRegisterType()`. Context properties are **not** QML-owned — C++ manages their lifetime. Exposing raw pointers risks dangling references. `Q_PROPERTY` NOTIFY signals are required for QML bindings to work.

- [ ] Every `Q_PROPERTY` exposed to QML must have a NOTIFY signal — bindings break silently without it → **(P)** [R4]
- [ ] Prefer `qmlRegisterSingletonInstance()` over `setContextProperty()` for global objects (type-safe) → **(P)** [R4]
- [ ] Use `QQmlApplicationEngine` not `QQuickView` for production apps — supports QML module imports → **(P)** [R4]
- [ ] Call `qmlRegisterUncreatableType()` for types exposed only for property access (enums, helpers) → **(P)** [R4]
- [ ] QML can only access `Q_INVOKABLE` methods and `Q_PROPERTY` — regular C++ methods are invisible → **(P)** [R4]

```cpp
// Good — NOTIFY signal for QML binding
class MyData : public QObject {
    Q_OBJECT
    Q_PROPERTY(int count READ count WRITE setCount NOTIFY countChanged)
public:
    int count() const { return m_count; }
    void setCount(int c) { if (m_count != c) { m_count = c; emit countChanged(); } }
signals:
    void countChanged();
private:
    int m_count = 0;
};

// Bad — missing NOTIFY: QML bindings to "count" silently fail
Q_PROPERTY(int count READ count WRITE setCount)  // no NOTIFY
```

### 8. JavaScript Engine Quirks in QML  **(P)** [R1][R2]

QML uses Qt's V4 JavaScript engine (not V8/SpiderMonkey). It has limitations: no `let`/`const` in Qt 5 (available in Qt 6.4+), limited ES6 support, `for...in` behavior differs from browser JS. `property var` is a QML type, not a JS variable — it participates in the binding engine.

- [ ] Avoid complex computation in QML JS — move to C++ for performance-critical logic → **(P)** [R2]
- [ ] `property var` stores JavaScript objects but triggers binding re-evaluation — use `property var` only when necessary → **(P)** [R1]
- [ ] `Array.includes()` and other ES7 features unavailable before Qt 6.4 — polyfill or use C++ → **(P)** [R1]
- [ ] JSON parsing is synchronous and blocks the UI thread — parse in C++ worker thread for large payloads → **(P)** [R2]

```qml
// Good — move heavy computation to C++
function processData(data) {
    backend.processAsync(data)  // C++ side, non-blocking
}

// Bad — blocking JSON parse in UI thread
Component.onCompleted: {
    let parsed = JSON.parse(hugeString)  // blocks UI for large data
}
```

### 9. QML Signal/Handler Naming Conventions  **(P)** [R1]

Signal handlers use `on<SignalName>` convention (capitalize first letter of signal). Custom signals defined with `signal mySignal(type arg)` are handled with `onMySignal: { ... }`. Property change signals auto-generate `on<Property>Changed` handlers.

- [ ] Signal handler naming: `on + CapitalizedSignalName` — e.g., `signal clicked()` → `onClicked:` → **(P)** [R1]
- [ ] Connect signals to C++ slots using `Connections` element with `target` → **(P)** [R1]
- [ ] `Connections` with function syntax (Qt 5.15+): `function onSignal(args) { }` — cleaner than `target.onSignal:` → **(P)** [R1]
- [ ] Disconnect in `Component.onDestruction` to avoid accessing destroyed objects → **(P)** [R1]

```qml
// Good — modern Connections syntax (Qt 5.15+/6.x)
Connections {
    target: backend
    function onDataReady(data) {
        displayData(data)
    }
}

// Bad — old syntax, verbose
Connections {
    target: backend
    onDataReady: { displayData(data) }
}
```

### 10. States, Transitions, and Animation Performance  **(P)** [R1][R2]

QML states and transitions are powerful but misuse causes performance issues. `Behavior` on `width`/`height` triggers layout recalculations every animation frame. `Animator` types run on the render thread (Qt Quick 2) for smoother animations. Avoid animating `anchors` — animate `x`/`y`/`width`/`height` directly.

- [ ] Use `Animator` types (`OpacityAnimator`, `XAnimator`) instead of `Animation` types for GPU-accelerated animations → **(P)** [R2]
- [ ] Animate `x`/`y`/`scale` instead of `anchors` — anchor changes trigger expensive layout passes → **(P)** [R2]
- [ ] `Behavior` on layout properties (`width`, `height`, `anchors`) causes per-frame relayout — use only when necessary → **(P)** [R1]
- [ ] Set `SmoothedAnimation` for fluid transitions; avoid `NumberAnimation` on layout properties → **(P)** [R2]

```qml
// Good — GPU-accelerated opacity animation
OpacityAnimator on opacity {
    from: 0; to: 1; duration: 300
}

// Bad — Behavior on width triggers per-frame layout
Behavior on width {
    NumberAnimation { duration: 300 }  // expensive: triggers layout each frame
}
// Better: Behavior on scale (transform, no layout)
Behavior on scale {
    NumberAnimation { duration: 300 }
}
```

### 11. Text Rendering and Font Handling  **(P)** [R1][R5]

QML text rendering differs by platform. `Text.RichText` uses a different code path than `Text.PlainText`. `Text.elide` and `Text.wrapMode` interact with layout. `font.pixelSize` vs `font.pointSize` — use `pixelSize` for consistent cross-platform sizing.

- [ ] Use `font.pixelSize` for cross-platform consistency; `pointSize` depends on screen DPI → **(P)** [R5]
- [ ] `Text.RichText` with `<img>` tags is asynchronous and may not render in `onCompleted` — use `onImageLoaded` → **(P)** [R1]
- [ ] `Text.MarkdownText` (Qt 6.4+) for rich text; `Text.StyledText` is limited and platform-dependent → **(P)** [R1]
- [ ] `Text.elide: Text.ElideRight` requires explicit `width` — text collapses to nothing without it → **(P)** [R1]

```qml
// Good — platform-consistent text
Text {
    text: "Hello World"
    font.pixelSize: 14  // consistent across platforms
    width: parent.width
    elide: Text.ElideRight
    wrapMode: Text.WordWrap
}

// Bad — pointSize varies by DPI
Text {
    font.pointSize: 12  // different physical sizes on different screens
}
```

### 12. Image Caching and Asynchronous Loading  **(P)** [R1][R2]

QML images load asynchronously by default (`Image.asynchronous: true`). Large images block the UI thread on synchronous load. `Image.sourceSize` decodes to a specific resolution. `Image.cache` defaults to `true` — memory accumulates for many images.

- [ ] Set `Image.asynchronous: true` for all non-trivial images → **(P)** [R1]
- [ ] `Image.sourceSize` should match display size to avoid memory waste → **(P)** [R2]
- [ ] For large image sets (photo gallery): set `cache: false` to prevent unbounded memory growth → **(P)** [R2]
- [ ] `Image.status === Image.Ready` before accessing `Image.sourceSize` or `Image.paintedWidth` → **(P)** [R1]

```qml
// Good — optimized image loading
Image {
    asynchronous: true
    source: "large_photo.jpg"
    sourceSize.width: 256
    cache: false  // photo gallery, don"t cache
}

// Bad — synchronous loading blocks UI
Image {
    asynchronous: false  // blocks UI until image decoded
    source: "huge_image.png"
}
```

### 13. QML Module Versioning and Imports  **(P)** [R1][R4]

QML modules use versioned imports (`import QtQuick 6.8`). Mixing Qt 5 and Qt 6 imports causes compatibility issues. Custom QML modules need `qmldir` files and proper CMake configuration. Singleton types need `pragma Singleton` in `qmldir`.

- [ ] Always specify explicit version in QML imports — `import QtQuick 6.8` not `import QtQuick` → **(P)** [R1]
- [ ] For Qt 6: use `qt_add_qml_module()` in CMake, not the old `qt6_add_resources()` → **(P)** [R4]
- [ ] Custom C++ types: `QML_ELEMENT` macro for automatic registration (Qt 6.2+) → **(P)** [R4]
- [ ] `qmldir` file required alongside QML files for module resolution → **(P)** [R1]

```cmake
# Good — CMake Qt 6 QML module
qt_add_qml_module(myapp
    URI "com.example.myapp"
    VERSION 1.0
    QML_FILES Main.qml Page1.qml
    SOURCES backend.cpp backend.h
)
```

### 14. Platform-Specific QML: Mobile vs Desktop  **(P)** [R1][R5]

QML runs on mobile (iOS/Android) and desktop. `ApplicationWindow` vs `Window` — `ApplicationWindow` provides platform menus and status bar. Mobile requires handling software keyboard, safe areas, and background/foreground transitions.

- [ ] Use `ApplicationWindow` not `Window` for platform integration (menu bar, status bar, system palette) → **(P)** [R1]
- [ ] iOS safe area: wrap content in `Item { anchors.fill: parent; anchors.margins: Qt.application.screens[0].safeAreaMargins }` → **(P)** [R5]
- [ ] Handle `Qt.application.state === Qt.ApplicationActive` for background/foreground on mobile → **(P)** [R1]
- [ ] Test with software keyboard open on mobile — layout may shift unexpectedly → **(P)** [R5]

```qml
// Good — mobile-aware ApplicationWindow
ApplicationWindow {
    visible: true
    Item {
        anchors.fill: parent
        anchors.margins: Screen.virtualKeyboardHeight > 0 ? 10 : 0
    }
    onClosing: {
        if (Qt.platform.os === "android") {
            close.accepted = false  // minimize, don"t close
        }
    }
}

// Bad — plain Window, no platform integration
Window {
    visible: true  // no menu bar, no status bar on macOS
}
```

### 15. Debugging and Profiling QML  **(P)** [R1][R2]

QML debugging requires enabling in project settings. `console.log()` is synchronous and affects performance. `QML_DEBUG` enables the QML debugger but has a performance cost. Qt Creator's QML profiler shows binding evaluations and paint times.

- [ ] Remove `console.log()` calls in production — they are synchronous and slow → **(P)** [R2]
- [ ] Enable QML debugging only in debug builds: `QT_QML_DEBUG` → **(P)** [R1]
- [ ] Use `QML_PROFILER` environment variable with Qt Creator's QML Profiler for binding analysis → **(P)** [R2]
- [ ] `Renderer` > `FramesPerSecond` overlay in `qtquickcontrols2.conf` for FPS monitoring → **(P)** [R2]

---

## Quick Decision Tree

```
Binding update after JS assignment?
  ├─ Use Qt.binding() → re-enables binding
  └─ Use Binding element → from imperative context

Dynamic component needed?
  ├─ Single item, load once → Loader
  ├─ Many items, reusable → createComponent + incubateObject
  └─ Very many items → ListView/TableView with model

Animation smooth but blocks UI?
  ├─ Animating opacity/scale/rotation → Animator (render thread)
  └─ Animating layout properties → Behavior (may relayout)

High-DPI rendering wrong?
  ├─ Double-scale issue → remove manual devicePixelRatio multiplication
  ├─ Fractional scaling (125%) → set RoundPreferFloor in main.cpp
  └─ Image blurry → set sourceSize or use SVG
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: JavaScript Assignment Breaking Bindings

- **Appearance:** `onClicked: { width = 200 }`
- **Trap:** Looks like setting a value; actually destroys the binding permanently
- **Consequence:** Property stops updating, UI becomes stale
- **Fix:** Use `Qt.binding()` or `Binding` element, or restructure to use declarative bindings

### Anti-Pattern 2: Property var for Everything

- **Appearance:** `property var data: ({})` used for all data storage
- **Trap:** `var` bypasses QML typing and prevents binding optimization
- **Consequence:** Slower bindings, harder to debug, no compile-time checks
- **Fix:** Use typed properties (`property int`, `property string`, custom QObject types) wherever possible

### Anti-Pattern 3: Synchronous Image Loading

- **Appearance:** `Image { asynchronous: false; source: "large.jpg" }`
- **Trap:** Default `asynchronous: true` may be overridden
- **Consequence:** UI freezes while image decodes
- **Fix:** Always use `asynchronous: true` for images > 64x64

---

## See Also

- [Qt6 Core C++ Harness](qt6-core.md) — Qt 6 C++ pitfalls and best practices
- [Concurrency and Thread Safety](../concurrency/thread-safety.md) — general thread safety rules
- [RAII and Resource Management](../memory/raii.md) — C++ ownership patterns

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | P | Qt 6.8 Documentation — QML Language Reference | Properties, Signals, Loader, Component | verified-2026 | 2026-07 |
| R2 | P | Qt 6.8 Documentation — Qt Quick Performance Best Practices | ListView, Animator, Image, JavaScript | verified-2026 | 2026-07 |
| R3 | P | Qt 6.8 Documentation — Integrating QML and C++ | QQmlEngine, Context Properties, Type Registration | verified-2026 | 2026-07 |
| R4 | P | Qt 6.8 Documentation — QML Modules and CMake | qt_add_qml_module, QML_ELEMENT, qmldir | verified-2026 | 2026-07 |
| R5 | P | Qt 6.8 Documentation — High DPI Support | devicePixelRatio, ScaleFactorRoundingPolicy | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft covering QML binding, memory, lifecycle, DPI, ListView, Loader, JS engine, and C++ integration
