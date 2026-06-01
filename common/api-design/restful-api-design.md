---
type: harness
id: "common-api-design"
title: "API Design Principles Checklist"
language: "common"
category: "design"
tier: "N"
scope: "Design consistent, versionable, and idempotent HTTP APIs with standard error reporting"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [api-design, rest, versioning, idempotency, error-handling]
based_on:
  - "[C] IETF RFC 7807 — Problem Details for HTTP APIs"
  - "[C] Google API Design Guide"
  - "[C] Microsoft REST API Guidelines"
  - "[A] API Design Patterns (Geewax, 2021)"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# API Design Principles Checklist

**Based on:** RFC 7807 ([C]), Google API Design Guide ([C]), Microsoft REST API Guidelines ([C]), API Design Patterns ([A]).
**Scope:** HTTP API design decisions for public/internal services.

---

## Concepts

| Principle | Standard |
|-----------|----------|
| Error format | RFC 7807: `type`, `title`, `status`, `detail` required |
| Versioning | URL path or header; breaking = new version |
| Pagination | Cursor-based preferred; page-based acceptable |
| Idempotency | `Idempotency-Key` header for POST/PATCH/DELETE |

---

## Checklist

### 1. Error Response Format  **(C)** [R1]

- [ ] Every error response uses RFC 7807 problem detail → **(C)** [R1]
- [ ] Content-Type `application/problem+json` → **(C)** [R1]
- [ ] Multiple errors returned as array with per-error `source` → **(C)** [R2]

### 2. Idempotency  **(C)** [R2]

- [ ] POST/PATCH/DELETE support `Idempotency-Key` header → **(C)** [R2]
- [ ] Retry with same key + payload = same result → **(C)** [R2]

### 3. Pagination  **(C)** [R1][R2]

- [ ] All list endpoints paginate → **(C)** [R1]
- [ ] Response includes `next` link when more results exist → **(C)** [R1]
- [ ] Default page size documented; max enforced server-side → **(C)** [R2]

### 4. Versioning  **(C)** [R2][R3]

- [ ] Breaking changes gated behind new API version → **(C)** [R2]
- [ ] Backward-compatible additions within same version → **(C)** [R2]
- [ ] Deprecated fields/endpoints have sunset date → **(C)** [R3]

### 5. Naming Consistency  **(C)** [R2][R3]

- [ ] One naming convention for all JSON fields, documented → **(C)** [R2]
- [ ] Resource names use noun plurals → **(C)** [R2]
- [ ] Convention enforced via linting → **(C)** [R2]

### 6. Rate Limiting  **(C)** [R3]

- [ ] Rate-limited endpoints return HTTP 429 + `Retry-After` → **(C)** [R3]
- [ ] Error body follows RFC 7807 → **(C)** [R3]

### 7. Security Baseline  **(C)** [R3]

- [ ] All endpoints use TLS (HTTPS only) → **(C)** [R3]
- [ ] Authentication on all non-public endpoints → **(C)** [R3]
- [ ] Input validation on every endpoint → **(C)** [R3]

---

## Decision Tree

```
New endpoint?
  → Error format: RFC 7807 [1]
  → Mutating? → Idempotency-Key [2]
  → List? → Pagination [3]
  → Breaking existing? → New version [4]
  → Naming consistent? [5]
  → Rate limit? → 429 + Retry-After [6]
  → HTTPS + auth + validation [7]
```

---

## Anti-Patterns

### 1. 200 OK with Error Body

- **Appearance:** HTTP 200 with `{"error": "not found"}` in body.
- **Trap:** Simpler to always return 200; avoids handling different status codes in clients.
- **Consequence:** Monitoring tools, CDNs, and HTTP clients cannot distinguish success from failure. Caching layers cache error responses. Retry logic cannot know which requests are safe to retry.
- **Fix:** Use correct HTTP status codes. Error bodies follow RFC 7807.

### 2. Breaking Change Without Version

- **Appearance:** Rename a field or change its type in a minor release.
- **Trap:** "It's a small change, nobody uses that field."
- **Consequence:** Client breaks without warning. Production incident. Trust in API stability evaporates. Downstream teams add defensive workarounds that compound over time.
- **Fix:** Never remove or rename published fields. Deprecate old fields with sunset dates. Gate breaking changes behind new API version.

---

## See Also

- [Input Validation](../security/input-validation.md) — Security-focused input validation
- [Error Handling Strategy](../error-handling/error-handling-strategy.md) — Consistent error handling patterns

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | IETF RFC 7807 | Sections 3-3.2 | verified-2026 | 2026-06 |
| R2 | C | Google API Design Guide | Naming, Pagination, Idempotency | verified-2026 | 2026-06 |
| R3 | C | Microsoft REST API Guidelines | Versioning, Rate Limiting | verified-2026 | 2026-06 |
| R4 | A | API Design Patterns (Geewax) | Ch.3,5,7,17 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
