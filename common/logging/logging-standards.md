---
type: harness
id: "common-logging-standards"
title: "Logging Standards Checklist"
language: "common"
category: "logging"
tier: "N"
scope: "Establish log levels, structured format, PII protection, correlation, and retention policies"
version: "2026.09.1"
status: "draft"
stable_since: ""
last_validated: "2026-09-10"
review_cycle: "12m"
tags: [logging, observability, security, pii]
based_on:
  - "[N] OWASP ASVS V7 — Logging Requirements"
  - "[C] NIST SP 800-92 — Log Management"
  - "[C] OpenTelemetry Logging Specification"
  - "[A] 12-Factor App — Logs as Event Streams"
  - "[A] Google SRE Book Ch.16"
related:
  - "common/ai/prompt-injection-and-llm-security.md"
  - "common/ai/tool-calling-and-agent-control.md"
  - "cpp/runtime/observability-and-diagnostics.md"
  - "common/security/input-validation.md"
  - "python/security/input-deserialization.md"
  - "common/error-handling/error-handling-strategy.md"
supersedes: []
changelog:
  - "2026.09.10: Corrected item-3 bullet and anti-pattern 3's mechanism — Dart's inherited default `toString()` prints only `Instance of '<ClassName>'` and never dumps fields; a field-dumping string (and the PII it carries into log lines) comes from an overridden or code-generated full-field `toString()` (e.g. freezed). Fact-checked against the Dart API docs (Object.toString) in the C29/C30 documentation audit."
  - "2026.06: Initial draft"
  - "2026.09: Item 3 and anti-pattern 3 extended — whole-object logging via default entity `toString()` in Dart/Flutter carries PII implicitly, and raising a line's level (debug→warning) changes retention/upload policy and must be re-reviewed. Distilled from the lava monorepo dual-diff review."
---

# Logging Standards Checklist

**Based on:** OWASP ASVS V7 ([N]), NIST SP 800-92 ([C]), OpenTelemetry Logging ([C]), 12-Factor App ([A]), Google SRE Book Ch.16 ([A]).
**Scope:** What, how, and when to log. Covers security, format, and operational concerns.

---

## Concepts

| Level | Purpose |
|-------|---------|
| DEBUG | Trace/diagnose; disabled in prod by default |
| INFO | Key state transitions, milestones |
| WARN | Recoverable anomalies, approaching limits |
| ERROR | Operation failure, user-impacting |
| FATAL | Unrecoverable, imminent shutdown |

---

## Checklist

### 1. Log Level Selection  **(C)** [R1][R2]

- [ ] DEBUG: trace/diagnose, off in production → **(C)** [R2]
- [ ] INFO: state transitions, milestones → **(C)** [R2]
- [ ] WARN: recoverable anomalies → **(C)** [R2]
- [ ] ERROR: operation failure → **(C)** [R2]
- [ ] FATAL: unrecoverable shutdown → **(C)** [R2]

### 2. Structured Format  **(C)** [R3]

- [ ] JSON with canonical schema → **(C)** [R3]
- [ ] Every line: `timestamp`, `level`, `message`, `context` → **(C)** [R3]
- [ ] Context fields use consistent naming → **(C)** [R3]

### 3. What NOT to Log  **(N)** [R1]

- [ ] NEVER credentials, passwords, tokens, API keys → **(N)** [R1]
- [ ] NEVER PII (names, emails, phones, SSNs) in plaintext → **(N)** [R1]
- [ ] NEVER session IDs, credit card numbers → **(N)** [R1]
- [ ] An entity with a full-field `toString()` is interpolated into a log line as a whole object → **(N)** log explicit safe fields or a redacted projection; never the whole object. In Dart/Flutter the inherited default prints only `Instance of '<ClassName>'` — a field-dumping string (email, phone) comes from an overridden or code-generated `toString()`, so check what that override emits before logging the object. [R1]
- [ ] A log line's level is raised (debug→warning/error) on a message that may carry PII → **(C)** re-review the line under this section before promotion; raising the level changes retention and upload policy and expands the PII exposure surface. [R1][R2]
- [ ] Mask/redact sensitive values before emission → **(C)** [R1]

### 4. Correlation IDs  **(C)** [R3]

- [ ] Generate at ingress → **(C)** [R3]
- [ ] Propagate across all service calls → **(C)** [R3]
- [ ] Attach to every log line in scope → **(C)** [R3]

### 5. Log Protection  **(N)** [R1]

- [ ] Append-only; no application delete/modify → **(N)** [R1]
- [ ] Access-controlled storage; read access audited → **(N)** [R1]
- [ ] Integrity protection (hash chain, write-once) → **(C)** [R1]

### 6. Retention and Rotation  **(C)** [R2]

- [ ] Classified by sensitivity: hot 7d, warm 90d, cold 1y+ → **(C)** [R2]
- [ ] Rotate on size or time → **(C)** [R2]

### 7. Production Standard  **(A)** [R4][R5]

- [ ] Write to stdout; environment routes → **(A)** [R4]
- [ ] Sampling for high-volume paths → **(A)** [R5]

---

## Decision Tree

```
Event to log?
  → PII/credential? → MASK or SKIP [3]
  → Severity? DEBUG/INFO/WARN/ERROR/FATAL [1]
  → Structured JSON [2] + Correlation ID [4]
  → Protection: append-only, access-controlled [5]
  → Retention + rotation [6]
  → stdout → env router [7]
```

---

## Anti-Patterns

### 1. Logging Credentials

- **Appearance:** `logger.info("auth with token=%s", apiKey)`.
- **Trap:** Helpful for debugging auth failures.
- **Consequence:** Token leaks to logs, monitoring, error aggregators. Security incident.
- **Fix:** Log `"authenticating user id=42"`. Never the token.

### 2. Unstructured Free-Text

- **Appearance:** `logger.info("user " + name + " did thing at " + now)`.
- **Trap:** Simple, human-readable, no tools needed.
- **Consequence:** Impossible to search/aggregate/alert. Volume explodes, signal lost.
- **Fix:** `logger.info("action=login user_id=42")` or structured JSON.

### 3. Logging the Whole Entity Through a Field-Dumping `toString()`

- **Appearance:** A Dart/Flutter client logs `log.info('session updated: $user')` where `User` **overrides** `toString()` — code-generated (e.g. freezed emits every field) or hand-written as `User(email: …, phone: …)` — so `$user` dumps the whole entity, including `email` and `phone`, into the log line. The inherited `Object.toString()` is not the risk: with no override it prints only `Instance of 'User'` and no fields.
- **Trap:** `$user` is one interpolation token and reads as "logging the user for context"; the field-dumping `toString()` was written or generated for debugging, so the field list is invisible at the call site. Because no code names a PII field, the line never looks like a PII leak, and the full-field output even looks intentional.
- **Consequence:** Emails/phones land in logs and flow into retention, upload, and error-aggregation pipelines. Later, raising that line from debug to warning moves it into always-on retention — the PII exposure surface expands silently, driven by a log-level change nobody reviewed as a data-protection decision.
- **Fix:** Item 3 — log an explicit projection (`userId=42`, redacted fields) or an overridden safe `toString()`; never interpolate an unvetted whole object. Treat any level promotion of a log line as a trigger to re-review it under item 3.

---

## See Also

- [Input Validation](../security/input-validation.md) — Validate before logging
- [Error Handling](../error-handling/error-handling-strategy.md) — Log once at outermost handler; message text is not a contractual error identifier
- [Dart Asynchronous Error and Exception Safety Checklist](../../dart/error-handling.md) — the client-side rule that the single log line at the edge is the *only* log line

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | OWASP ASVS V7 | V7.1-V7.4 | verified-2026 | 2026-06 |
| R2 | C | NIST SP 800-92 | Sections 3-5 | verified-2026 | 2026-06 |
| R3 | C | OpenTelemetry Logging | Data model | verified-2026 | 2026-06 |
| R4 | A | 12-Factor App | Section XI | verified-2026 | 2026-06 |
| R5 | A | Google SRE Book | Ch.16 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.09.10: Corrected the item-3 bullet and anti-pattern 3 mechanism — Dart's inherited default `toString()` prints only `Instance of '<ClassName>'` and never dumps fields; a field-dumping string (and the PII it carries into log lines) comes from an overridden or code-generated full-field `toString()` (e.g. freezed). Fact-checked against the Dart API docs (Object.toString) in the C29/C30 documentation audit.
- 2026.06: Initial draft
- 2026.09: Item 3 and anti-pattern 3 extended with the Dart/Flutter client form — whole-object logging through default entity `toString()` carries PII implicitly (email/phone), and promoting a log line's level (debug→warning) changes retention/upload policy and expands the PII exposure surface. Distilled from the lava monorepo dual-diff review.
