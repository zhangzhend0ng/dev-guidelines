# Prompt: Code Review with a Harness

Use this template with an AI agent to review code against any dev-guidelines harness.

## Template

```
Review this code against the {HARNESS_NAME} harness ({HARNESS_PATH}).

Process each checklist item:
1. State the condition
2. Check if the code satisfies it; cite specific lines
3. For failures: suggest a fix with code example

Priority by authority tier:
- (N) = blocking (objectively wrong)
- (C) = requires justification if bypassed
- (A) = suggestion

Also check the anti-patterns section.
Reference the decision tree for orientation.

Code:
```{LANGUAGE}
{CODE}
```
```

## Example: RAII Review

```
Review this code against the RAII harness (cpp/memory/raii.md).

Process each checklist item; cite lines; suggest fixes.
(N) = blocking, (C) = requires justification, (A) = suggestion.

Code:
```cpp
class FileHandler {
    FILE* f_;
public:
    FileHandler(const char* path) { f_ = fopen(path, "r"); }
    ~FileHandler() { if (f_) fclose(f_); }
    FILE* get() { return f_; }
};
```
```

Expected output: item-by-item pass/fail with line citations and fix suggestions.
