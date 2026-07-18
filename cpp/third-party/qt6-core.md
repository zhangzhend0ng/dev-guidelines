---
type: harness
id: "cpp-qt6-core"
title: "Qt 6 C++ Core Pitfalls, Limitations, and Best Practices Checklist"
language: "cpp"
category: "third-party"
tier: "P"
scope: "Avoid known pitfalls and limitations when using Qt 6 C++ across Windows, macOS, Linux, iOS, and Android"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-18"
review_cycle: "12m"
tags: [qt, qt6, cpp, cross-platform, signal-slot, model-view, dpi]
based_on:
  - "[P] Qt 6.8 Documentation — Core APIs and Framework"
  - "[P] Qt 6.8 Documentation — Best Practices for Qt Development"
  - "[P] Qt Bug Reports (Jira) — Qt 6.x known issues"
  - "[P] Qt 6.8 Documentation — Threading and Concurrency"
  - "[P] Qt 6.8 Documentation — Model/View Programming"
  - "[P] Qt 6.8 Documentation — High DPI Support"
  - "[P] KDAB / ICS blog posts — Qt threading and memory management"
related:
  - "cpp/third-party/qt6-qml.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/memory/raii.md"
  - "cpp/build/cmake-include-hygiene.md"
supersedes: []
changelog:
  - "2026.07: Initial draft covering ownership, signal/slot, threading, model/view, DPI, CMake, containers, and encoding"
---

# Qt 6 C++ Core Pitfalls, Limitations, and Best Practices Checklist

**Based on:** Qt 6.8 official documentation ([P]), Qt Jira bug reports ([P]), KDAB/ICS expert blogs ([P]).
**Scope:** Common pitfalls, platform-specific limitations, and best practices for Qt 6 C++ (Qt Core, Qt GUI, Qt Widgets, Qt Quick). Covers desktop (Windows/macOS/Linux), mobile (iOS/Android). Does NOT cover Qt WebEngine, Qt Network, or Qt SQL in detail.

---

## Prerequisites

**Version context:** Qt 6.8 LTS (2025). Qt 5.15 LTS is still widely used. Key Qt 5→6 changes: `QTextCodec` removed, `QRegExp` replaced by `QRegularExpression`, CMake is the primary build system (qmake deprecated), `QPair`/`QMultiMap` API changes.

**Ownership model:** Qt uses parent-child ownership for `QObject`-derived classes. Parent deletes children on destruction. Objects created with `new` without a parent must be explicitly deleted. This is NOT garbage collection — it"s deterministic.

**Signal/Slot connection types:**

| Type | Behavior |
|------|----------|
| `Qt::AutoConnection` (default) | Direct if same thread, queued if different |
| `Qt::DirectConnection` | Slot executes in emitter"s thread immediately |
| `Qt::QueuedConnection` | Slot executes in receiver"s thread event loop |
| `Qt::BlockingQueuedConnection` | Emitter blocks until slot returns (cross-thread only) |

---

## Checklist

### 1. QObject Parent-Child Ownership and Memory Management  **(P)** [R1]

Qt parent-child ownership is deterministic: parent deletes children in its destructor. Objects created with `new` without a parent leak. Stack-allocated `QObject` with parent causes double-delete. `deleteLater()` defers deletion to the event loop — safe for cross-thread use.

- [ ] Every `QObject*` created with `new` must have a parent or explicit `delete`/`deleteLater()` → **(P)** [R1]
- [ ] Never stack-allocate `QObject` with a parent — parent destructor calls `delete` on stack object → **(P)** [R1]
- [ ] Use `deleteLater()` instead of `delete` in signal handlers — prevents deletion during signal emission → **(P)** [R1]
- [ ] `QObject::setParent()` transfers ownership: old parent releases, new parent takes ownership → **(P)** [R1]

```cpp
// Good — parent manages lifetime
auto* button = new QPushButton("Click", parentWidget);  // deleted with parentWidget

// Good — explicit management without parent
auto* worker = new QObject;  // no parent
connect(worker, &QObject::destroyed, []{ /* cleanup */ });
worker->deleteLater();  // safe deferred deletion

// Bad — stack object with parent = double delete
QPushButton button("Click", parentWidget);  // parent will delete it, then stack unwinds = crash
```

### 2. Signal/Slot Connection Types and Thread Safety  **(P)** [R1][R2]

New-style connect syntax (`connect(sender, &Sender::signal, receiver, &Receiver::slot)`) is type-safe and preferred. Old-style (`SIGNAL()`/`SLOT()` macros) compiles even with typos. `Qt::AutoConnection` (default) chooses direct or queued based on thread affinity.

- [ ] Always use new-style `connect(&sender, &Sender::sig, &receiver, &Receiver::slot)` — type-checked at compile time → **(P)** [R1]
- [ ] Cross-thread signals: use `Qt::QueuedConnection` explicitly for clarity; default auto-detection works but is implicit → **(P)** [R2]
- [ ] Disconnect signals in destructors to avoid calls on partially destroyed objects → **(P)** [R1]
- [ ] `connect()` with lambda: pass context object as third argument to auto-disconnect on destruction → **(P)** [R1]
- [ ] Never call `processEvents()` inside a slot — causes re-entrancy and stack corruption → **(P)** [R2]

```cpp
// Good — new-style connect with context object (auto-disconnect)
connect(sender, &Sender::dataReady, receiver,
        [receiver](const Data& d) { receiver->process(d); });

// Good — explicit cross-thread connection
connect(worker, &Worker::finished, ui, &UI::update,
        Qt::QueuedConnection);

// Bad — old-style, no compile-time check
connect(sender, SIGNAL(dataReady(Data)), receiver, SLOT(process(Data)));
// typo in signal/slot name not detected until runtime
```

### 3. QObject Thread Affinity and Worker Threads  **(P)** [R2]

`QObject` has thread affinity — it belongs to the thread where it was created. GUI objects must live in the main thread. Moving an object with `moveToThread()` transfers all children. Signals across threads use queued connections automatically. Never access GUI from worker threads.

- [ ] All QWidget/QQuickItem objects must stay in the main thread — never `moveToThread()` a widget → **(P)** [R2]
- [ ] `QObject::moveToThread()` moves the object AND all children to the target thread → **(P)** [R2]
- [ ] Use `QThread` with `moveToThread()` not `QThread::run()` override — modern Qt worker pattern → **(P)** [R2]
- [ ] `QMetaObject::invokeMethod(obj, "method", Qt::QueuedConnection, ...)` for thread-safe method invocation → **(P)** [R2]
- [ ] Use `QThreadPool` + `QRunnable` for fire-and-forget tasks; `QtConcurrent::run()` for simple async → **(P)** [R2]

```cpp
// Good — modern worker thread pattern
auto* worker = new WorkerObject;  // no parent, will be moved
auto* thread = new QThread;
worker->moveToThread(thread);
connect(thread, &QThread::started, worker, &WorkerObject::doWork);
connect(worker, &WorkerObject::finished, thread, &QThread::quit);
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
thread->start();

// Bad — direct GUI access from worker
void WorkerThread::run() override {
    ui->label->setText("done");  // CRASH: not main thread
}
```

### 4. Model/View Architecture Pitfalls  **(P)** [R4]

Qt"s Model/View framework separates data (model) from presentation (view). `beginInsertRows()`/`endInsertRows()` must bracket every structural change. Model indexes become invalid after model changes. `QAbstractItemModel::data()` is called frequently — must be fast.

- [ ] Every `insertRows()`/`removeRows()` must be wrapped in `beginInsertRows()`/`endInsertRows()` or equivalent → **(P)** [R4]
- [ ] Model indexes are invalid after model structural changes — never store `QModelIndex` across model updates → **(P)** [R4]
- [ ] `QAbstractItemModel::data()` is called frequently — cache expensive computations → **(P)** [R4]
- [ ] For large models (>10000 rows): use `canFetchMore()`/`fetchMore()` for incremental loading → **(P)** [R4]
- [ ] Use `QIdentityProxyModel` for column injection, `QSortFilterProxyModel` for filtering — don"t subclass base model → **(P)** [R4]

```cpp
// Good — safe model insertion
bool MyModel::insertRows(int row, int count, const QModelIndex& parent) {
    beginInsertRows(parent, row, row + count - 1);
    // ... insert data ...
    endInsertRows();
    return true;
}

// Bad — structural change without begin/end
void MyModel::addRow() {
    m_data.append(newRow);  // view not notified, crashes on access
}
```

### 5. Qt Build System: CMake Integration  **(P)** [R5][R6]

Qt 6 requires CMake (qmake deprecated). `find_package(Qt6 REQUIRED COMPONENTS ...)` is mandatory. `AUTOMOC`, `AUTOUIC`, `AUTORCC` handle moc/uic/rcc automatically. Missing `set(CMAKE_AUTOMOC ON)` causes linker errors for QObject subclasses.

- [ ] Always set `set(CMAKE_AUTOMOC ON)` — otherwise Q_OBJECT macros are not processed → **(P)** [R6]
- [ ] Use `qt_add_executable()` not `add_executable()` for Qt applications (handles platform setup) → **(P)** [R6]
- [ ] `find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick)` — list all used modules → **(P)** [R6]
- [ ] `target_link_libraries(myapp PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)` — use namespaced targets → **(P)** [R6]
- [ ] Qt resource files (.qrc): use `qt_add_resources()` instead of `CMAKE_AUTORCC` for Qt 6.2+ → **(P)** [R5]

```cmake
# Good — CMake Qt 6 setup
cmake_minimum_required(VERSION 3.16)
project(MyApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)
qt_add_executable(MyApp main.cpp mainwindow.cpp mainwindow.h resources.qrc)
target_link_libraries(MyApp PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
```

### 6. High-DPI and Per-Monitor DPI Awareness  **(P)** [R7]

Qt 6 enables high-DPI scaling by default (`Qt::AA_EnableHighDpiScaling`). On Windows, per-monitor DPI v2 requires `Qt::AA_DisableHighDpiScaling` to be NOT set. Fractional scaling (125%, 150%) requires explicit rounding policy. `devicePixelRatioF()` returns fractional, `devicePixelRatio()` rounds.

- [ ] Do NOT set `Qt::AA_EnableHighDpiScaling` in Qt 6 — it"s already the default and duplicates scaling → **(P)** [R7]
- [ ] On Windows: set `QGuiApplication::setHighDpiScaleFactorRoundingPolicy(RoundPreferFloor)` for fractional DPI → **(P)** [R7]
- [ ] Use `devicePixelRatioF()` (returns `qreal`) for fractional scaling; `devicePixelRatio()` rounds to integer → **(P)** [R7]
- [ ] QPixmap with `devicePixelRatio()`: set explicitly after loading for correct physical pixel density → **(P)** [R7]
- [ ] Test at 100%, 125%, 150%, 200% on Windows and Retina macOS → **(P)** [R7]

```cpp
// Good — main.cpp DPI setup for Qt 6
int main(int argc, char* argv[]) {
    QGuiApplication::setHighDpiScaleFactorRoundingPolicy(
        Qt::HighDpiScaleFactorRoundingPolicy::RoundPreferFloor);
    QApplication app(argc, argv);
    // ... create windows ...
    return app.exec();
}

// Bad — double-scaling in Qt 6
QApplication app(argc, argv);
app.setAttribute(Qt::AA_EnableHighDpiScaling);  // already default in Qt 6 = double scaling
```

### 7. QString Encoding and Conversion  **(P)** [R1][R3]

`QString` is UTF-16 internally. `QTextCodec` removed in Qt 6 — use `QStringConverter` instead. `QString::toUtf8()` returns `QByteArray` (UTF-8). `QString::toLocal8Bit()` depends on locale — avoid for portable code. `QLatin1String` is efficient for ASCII literals.

- [ ] `QString::toUtf8()` for all data interchange; `toLocal8Bit()` only for OS APIs that require it → **(P)** [R1]
- [ ] Use `QStringConverter` instead of removed `QTextCodec` for legacy encodings → **(P)** [R3]
- [ ] `QLatin1String("literal")` avoids UTF-16 conversion for compile-time ASCII strings → **(P)** [R1]
- [ ] `QString::fromStdString()` expects UTF-8; `QString::fromStdWString()` expects UTF-16 (Windows) or UTF-32 (Unix) → **(P)** [R1]

```cpp
// Good — proper encoding conversion
QString str = "Hello";
QByteArray utf8 = str.toUtf8();  // for network, file I/O, JSON
std::string stdStr = str.toStdString();  // UTF-8

// Good — efficient literal
QLatin1String label("OK");  // no heap allocation for short ASCII

// Bad — locale-dependent
QByteArray data = str.toLocal8Bit();  // different results on different OS locales
```

### 8. Qt Container Classes vs STL  **(P)** [R1]

Qt containers (`QList`, `QVector`, `QMap`) have implicit sharing (copy-on-write). `QList` is the default — it"s an array list, not a linked list (Qt 6 unified QList/QVector). Use `qAsConst()` in C++17 range-for to prevent detach. Qt 6 deprecates `QPair`, `QMultiMap` — use `std::pair`, `QMultiHash`.

- [ ] `QList<T>` is an array list (like `std::vector`) — O(1) index, O(n) prepend → **(P)** [R1]
- [ ] Use `qAsConst(container)` in `for (auto& x : container)` to avoid implicit detach → **(P)** [R1]
- [ ] Qt 6: prefer `std::pair` over deprecated `QPair` → **(P)** [R1]
- [ ] For large data: `QList` with copy-on-write is cheap to pass by value; `std::vector` better for mutating → **(P)** [R1]

```cpp
// Good — prevent detach in range-for
for (auto& item : qAsConst(myList)) {
    process(item);
}

// Bad — implicit detach in range-for
for (auto& item : myList) {  // detach if myList is shared (from const reference)
    process(item);
}
```

### 9. Event Handling and Event Filters  **(P)** [R1][R2]

Qt processes events through `QObject::event()` virtual method and event filters. `installEventFilter()` installs a filter; filters receive events before the target. Returning `true` from `eventFilter()` consumes the event. `QCoreApplication::sendEvent()` is synchronous, `postEvent()` is asynchronous.

- [ ] `eventFilter(QObject* obj, QEvent* event)` — return `true` to consume, return `QObject::eventFilter(obj, event)` to pass through → **(P)** [R1]
- [ ] `QCoreApplication::postEvent()` — event is owned by Qt after posting, do not delete → **(P)** [R1]
- [ ] `QCoreApplication::sendEvent()` — synchronous, may cause recursion if event creates new events → **(P)** [R1]
- [ ] Override `event()` not individual handlers when intercepting multiple event types → **(P)** [R2]

```cpp
// Good — event filter that passes through
bool MyWidget::eventFilter(QObject* obj, QEvent* event) {
    if (event->type() == QEvent::KeyPress) {
        handleKey(static_cast<QKeyEvent*>(event));
        return true;  // consumed
    }
    return QWidget::eventFilter(obj, event);  // pass through
}

// Bad — consuming all events accidentally
bool MyWidget::eventFilter(QObject*, QEvent*) {
    doSomething();
    return true;  // ALL events consumed, widget stops responding
}
```

### 10. QML/C++ Integration: Registration and Data Binding  **(P)** [R3][R8]

C++ types exposed to QML need `QML_ELEMENT` (Qt 6.2+) or `qmlRegisterType()`. `Q_PROPERTY` must have NOTIFY for QML bindings. `Q_INVOKABLE` for methods callable from QML. `QQmlApplicationEngine` is the standard QML engine in Qt 6.

- [ ] Use `QML_ELEMENT` / `QML_NAMED_ELEMENT(name)` macros for auto-registration (Qt 6.2+) → **(P)** [R3]
- [ ] Every `Q_PROPERTY` for QML must have NOTIFY → bindings silently break without it → **(P)** [R3]
- [ ] `Q_INVOKABLE` on all methods callable from QML → **(P)** [R3]
- [ ] C++ objects exposed to QML: manage lifetime on C++ side; QML does NOT own them → **(P)** [R3]
- [ ] `qmlRegisterSingletonInstance()` for global application objects → **(P)** [R8]

```cpp
// Good — QML-ready C++ class (Qt 6.2+)
class Backend : public QObject {
    Q_OBJECT
    QML_ELEMENT  // auto-registers with QML
    Q_PROPERTY(int count READ count WRITE setCount NOTIFY countChanged)
public:
    int count() const { return m_count; }
    void setCount(int c) { if (m_count != c) { m_count = c; emit countChanged(); } }
    Q_INVOKABLE void refresh() { /* ... */ }
signals:
    void countChanged();
private:
    int m_count = 0;
};
```

### 11. Platform-Specific Code: Windows, macOS, Linux  **(P)** [R1][R7]

Qt provides `Q_OS_WIN`, `Q_OS_MACOS`, `Q_OS_LINUX` preprocessor macros. `QSysInfo::productType()` for runtime platform detection. macOS requires `NSApplication` integration for menus; Windows requires `WinMain` or proper manifest for DPI. Use `#ifdef` sparingly — prefer Qt abstractions.

- [ ] Use `#ifdef Q_OS_WIN` / `Q_OS_MACOS` / `Q_OS_LINUX` for compile-time platform branching → **(P)** [R1]
- [ ] macOS: `setQuitOnLastWindowClosed(false)` for apps that run in menu bar → **(P)** [R7]
- [ ] Windows: set DPI awareness in manifest or `qputenv("QT_ENABLE_HIGHDPI_SCALING", "0")` for manual control → **(P)** [R7]
- [ ] Prefer Qt abstractions (`QStandardPaths`, `QFileDialog`) over platform APIs where available → **(P)** [R1]

```cpp
// Good — platform-specific code
void setupApplication(QApplication& app) {
#ifdef Q_OS_MACOS
    app.setQuitOnLastWindowClosed(false);  // macOS menu bar apps
    app.setAttribute(Qt::AA_DontShowIconsInMenus, false);
#endif
#ifdef Q_OS_WIN
    app.setStyle("fusion");  // consistent look on Windows
#endif
}

// Bad — avoid when Qt provides abstraction
#ifdef Q_OS_WIN
    std::string path = getenv("APPDATA");  // use QStandardPaths instead
#else
    std::string path = getenv("HOME");
#endif
```

### 12. QSettings and Application Data Storage  **(P)** [R1]

`QSettings` stores application settings. On Windows: registry by default; macOS: plist; Linux: INI file. `QSettings` is not thread-safe — use from main thread. Organization name and application name must be set before first use.

- [ ] Set `QCoreApplication::setOrganizationName()` and `setApplicationName()` before using `QSettings` → **(P)** [R1]
- [ ] `QSettings` defaults to registry on Windows — explicitly use `QSettings::IniFormat` for portable INI files → **(P)** [R1]
- [ ] `QSettings::sync()` to flush to disk — called automatically on destruction but not on crash → **(P)** [R1]
- [ ] Use `QSettings` from main thread only — not thread-safe → **(P)** [R1]

```cpp
// Good — proper QSettings setup
int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setOrganizationName("MyCompany");
    app.setApplicationName("MyApp");
    // QSettings now works anywhere
    QSettings settings;
    settings.setValue("window/geometry", saveGeometry());
    return app.exec();
}

// Bad — using QSettings without org/app name (empty path)
QSettings settings;  // defaults to system registry root or unknown file
```

### 13. qobject_cast and RTTI  **(P)** [R1]

`qobject_cast<T*>()` is Qt"s RTTI mechanism for QObject hierarchies. It"s faster than `dynamic_cast` but only works for QObject subclasses with `Q_OBJECT` macro. Returns `nullptr` on failure (no exception). Missing `Q_OBJECT` macro causes `qobject_cast` to silently return `nullptr`.

- [ ] Always use `qobject_cast` for QObject hierarchies — faster and doesn"t require C++ RTTI → **(P)** [R1]
- [ ] Check `qobject_cast` return value for `nullptr` — failed cast returns null, not exception → **(P)** [R1]
- [ ] Missing `Q_OBJECT` macro: `qobject_cast` silently fails — ensure all classes in hierarchy have it → **(P)** [R1]
- [ ] Use `dynamic_cast` for non-QObject classes; `qobject_cast` only works with QObject → **(P)** [R1]

```cpp
// Good — safe qobject_cast with null check
void handleEvent(QObject* obj) {
    if (auto* button = qobject_cast<QPushButton*>(obj)) {
        button->setText("Clicked");
    }
}

// Bad — unchecked qobject_cast
auto* button = qobject_cast<QPushButton*>(obj);
button->setText("Clicked");  // crash if obj is not QPushButton
```

### 14. Qt Resource System (.qrc)  **(P)** [R5]

Qt resources are compiled into the binary via `.qrc` files. Resources are read-only. Path prefix is set in `.qrc` file. Resource aliases can override file paths. Large resources increase binary size significantly — consider external files for >10MB assets.

- [ ] Use `:/prefix/filename` to access compiled-in resources → **(P)** [R5]
- [ ] Set resource prefix in `.qrc` file to avoid path collisions: `<qresource prefix="/icons">` → **(P)** [R5]
- [ ] Large assets (>10MB): keep as external files, fall back to resources only for essential assets → **(P)** [R5]
- [ ] `QDirIterator(":/")` can iterate compiled resources for discovery → **(P)** [R5]

```xml
<!-- Good — qrc with prefix -->
<RCC>
    <qresource prefix="/icons">
        <file alias="save">images/save_32.png</file>
        <file alias="open">images/open_32.png</file>
    </qresource>
</RCC>
<!-- Access: QIcon(":/icons/save") -->
```

### 15. Qt Quick vs Qt Widgets: Choosing the Right Framework  **(P)** [R1][R8]

Qt Widgets (`QWidget`) is mature, stable, and provides native look on all platforms. Qt Quick (`QQuickItem` + QML) is GPU-accelerated, modern, and better for animations and mobile. Mixing both is possible (`QQuickWidget`, `QWidget::createWindowContainer`) but has limitations.

- [ ] For desktop apps with standard controls: prefer Qt Widgets — mature, stable, native look → **(P)** [R1]
- [ ] For touch/mobile/modern UI with animations: prefer Qt Quick — GPU-accelerated, flexible → **(P)** [R8]
- [ ] `QQuickWidget` embeds QML in Widgets — has performance cost (renders to offscreen surface) → **(P)** [R8]
- [ ] Mixing Widgets and Quick: never embed a `QWidget` inside QML; use `QQuickWidget` to embed QML in Widgets → **(P)** [R8]

---

## Quick Decision Tree

```
Thread safety for QObject?
  ├─ GUI object (QWidget/QQuickItem) → main thread ONLY
  ├─ Worker object → create in worker thread or use moveToThread()
  └─ Cross-thread communication → QueuedConnection signals or QMetaObject::invokeMethod

Model performance issue?
  ├─ <1000 rows → QStandardItemModel or custom model
  ├─ 1000-10000 rows → custom model with cached data()
  └─ >10000 rows → custom model + canFetchMore() + fetchMore()

Build system?
  ├─ New Qt 6 project → CMake + find_package(Qt6)
  ├─ Qt 5 → CMake preferred, qmake for legacy
  └─ Mixed C++/QML → qt_add_qml_module() in CMake

UI framework choice?
  ├─ Desktop, standard controls → Qt Widgets
  ├─ Mobile, animations, modern → Qt Quick (QML)
  └─ Both → QQuickWidget to embed QML in Widgets
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Deleting QObject During Signal Emission

- **Appearance:** `delete sender` inside a slot connected to `sender`"s signal
- **Trap:** The signal emission loop still references the destroyed object
- **Consequence:** Undefined behavior, crash
- **Fix:** Use `sender->deleteLater()` instead of `delete sender`

### Anti-Pattern 2: Forgetting NOTIFY in Q_PROPERTY

- **Appearance:** `Q_PROPERTY(int count READ count WRITE setCount)` — no NOTIFY
- **Trap:** QML bindings compile but never update
- **Consequence:** Stale UI, mysterious "binding not updating" bugs
- **Fix:** Always add `NOTIFY countChanged` and emit the signal in the setter

### Anti-Pattern 3: Stack QObject with Parent

- **Appearance:** `QPushButton btn("OK", this)` inside a function
- **Trap:** Appears to work until parent is destroyed
- **Consequence:** Double-delete: parent destructor calls `delete`, then stack unwinding
- **Fix:** Always allocate QObjects on heap when they have parents

---

## See Also

- [Qt6 QML Harness](qt6-qml.md) — Qt 6 QML pitfalls and best practices
- [Concurrency and Thread Safety](../concurrency/thread-safety.md) — general thread safety rules
- [RAII and Resource Management](../memory/raii.md) — C++ ownership patterns
- [CMake Include Hygiene](../build/cmake-include-hygiene.md) — CMake integration rules

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | P | Qt 6.8 Documentation — Core APIs | QObject, QString, QSettings, QList, qobject_cast | verified-2026 | 2026-07 |
| R2 | P | Qt 6.8 Documentation — Threading and Concurrency | QThread, moveToThread, signal-slot connections | verified-2026 | 2026-07 |
| R3 | P | Qt 6.8 Documentation — Integrating QML and C++ | QML_ELEMENT, qmlRegisterType, Q_PROPERTY | verified-2026 | 2026-07 |
| R4 | P | Qt 6.8 Documentation — Model/View Programming | beginInsertRows, QAbstractItemModel, index invalidation | verified-2026 | 2026-07 |
| R5 | P | Qt 6.8 Documentation — Qt Resource System | .qrc, CMake qt_add_resources, rcc | verified-2026 | 2026-07 |
| R6 | P | Qt 6.8 Documentation — Build System (CMake) | find_package, AUTOMOC, CMake integration | verified-2026 | 2026-07 |
| R7 | P | Qt 6.8 Documentation — High DPI Support | devicePixelRatioF, ScaleFactorRoundingPolicy | verified-2026 | 2026-07 |
| R8 | P | Qt 6.8 Documentation — Qt Quick / Qt Widgets | QQuickWidget, createWindowContainer, framework choice | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft covering ownership, signal/slot, threading, model/view, DPI, CMake, containers, and encoding
