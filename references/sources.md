# Authoritative Source Registry

Central registry of all sources cited across harnesses. Harness reference tables reference entries here by Source ID. **Single source of truth for tier classification, review cycles, and verification status.**

**Last updated:** 2026-06-01

---

## N-Tier: Normative (Standards)

| ID | Source | Coverage | Maintainer | Edition Cycle |
|----|--------|----------|------------|---------------|
| N1 | ISO/IEC 14882 (C++ Standard) | C++ language, library | ISO/IEC JTC1/SC22/WG21 | ~3 years |
| N2 | WG21 Adopted Papers (PxxxxRxx) | New feature design, rationale | WG21 | Per standard cycle |
| N3 | IETF RFC (Standards Track / BCP) | Network protocols, TLS, HTTP | IETF | On demand |
| N4 | IEEE 754 | Floating-point arithmetic | IEEE | Infrequent (latest 2019) |
| N5 | OWASP Top 10 | Web application security risks | OWASP Foundation | ~3 years |
| N6 | NIST SP 800-53 | Security and privacy controls | NIST | Periodic revision |
| N7 | ISO 26262 / IEC 61508 | Functional safety | ISO/TC22, IEC | Infrequent |
| N8 | Conventional Commits 1.0.0 | Commit message specification | Community | Stable |

## C-Tier: Consensus (Industry Guidelines)

| ID | Source | Coverage | Maintainer | Update Rhythm |
|----|--------|----------|------------|---------------|
| C1 | C++ Core Guidelines | C++ coding rules | Stroustrup / Sutter | Continuous; per-standard |
| C2 | SEI/CERT C++ Coding Standard | Secure C++ coding | CMU SEI | On demand (v2025 latest) |
| C3 | CWE Top 25 | Software weakness ranking | MITRE | Annual |
| C4 | MISRA C++:2023 | Safety-critical C++ | MISRA Consortium | Versioned |
| C5 | Bloomberg BDE | Contracts, defensive programming | Bloomberg | Whitepapers + GitHub |
| C6 | NIST SP 800-218 (SSDF) | Secure software development | NIST | Periodic |
| C7 | OpenSSF Scorecard | Open-source security practices | OpenSSF / Linux Foundation | Continuous |
| C8 | OWASP ASVS | Application security verification | OWASP Foundation | ~3 years |
| C9 | Google API Design Guide | API design conventions | Google | On demand |
| C10 | IETF RFC 7807 (Problem Details) | API error response format | IETF | Stable |
| C11 | GitHub Actions Documentation | CI/CD workflow syntax, caching, matrices | GitHub | Continuous |
| C12 | Google Testing Blog | Test sizes, best practices, flaky test management | Google | Continuous |
| C13 | Microsoft vcpkg Documentation | C++ package management via manifest mode | Microsoft | Continuous |
| C14 | Conan Documentation | Cross-platform C++ package management | JFrog | Continuous |
| C15 | CMake FetchContent / CPM.cmake | Fetch-based C++ dependency acquisition | Kitware / Community | Continuous |

## A-Tier: Advisory (Expert Literature & Org Standards)

| ID | Source | Coverage | Author/Org | Published | Obsolescence Risk |
|----|--------|----------|------------|-----------|-------------------|
| A1 | Effective C++ (3/e) | C++98/03 best practices | Scott Meyers | 2005 | High — C++11+ obsolete items |
| A2 | Effective Modern C++ | C++11/14 best practices | Scott Meyers | 2014 | Medium |
| A3 | C++ Concurrency in Action (2/e) | C++11-17 concurrency | Anthony Williams | 2019 | Low |
| A4 | C++ Templates: Complete Guide (2/e) | Template programming | Vandevoorde, Josuttis, Gregor | 2017 | Medium |
| A5 | A Tour of C++ (3/e) | C++ overview | Bjarne Stroustrup | 2022 | Low |
| A6 | Exceptional C++ | Exception safety, RAII | Herb Sutter | 2000 | Medium |
| A7 | Release It! (2/e) | Production stability | Michael Nygard | 2018 | Low |
| A8 | The Pragmatic Programmer (20th) | Software craftsmanship | Hunt & Thomas | 2019 | Low |
| A9 | Google C++ Style Guide | C++ coding conventions | Google | Continuous | Low |
| A10 | LLVM Coding Standards | C++ coding conventions | LLVM Project | Continuous | Low |
| A11 | Abseil C++ Tips of the Week | C++ idioms | Google | Weekly | Low |
| A12 | Continuous Delivery (Humble/Farley, 2010) | CI/CD build pipeline, fast feedback | Humble & Farley | 2010 | Low |
| A13 | Effective STL | STL algorithms, containers, iterators best practices | Scott Meyers | 2001 | High — pre-C++11 |
| A14 | xUnit Test Patterns | Test organization, fixtures, test doubles taxonomy | Gerard Meszaros | 2007 | Medium |
| A15 | Mocks Aren't Stubs (Fowler) | Test double definitions article | Martin Fowler | 2007 | Low — principles timeless |

## Deprecated Sources

| ID | Source | Reason | Superseded By | When |
|----|--------|--------|---------------|------|
| D1 | `std::auto_ptr` patterns | Removed in C++17 | `std::unique_ptr` (N1, C1) | 2017 |
| D2 | C++03 standard references | 3+ standard versions behind | Current ISO 14882 edition | — |
| D3 | Pre-C++11 Meyers Items | Language features replaced | Per-item assessment | — |

## Usage

Harness reference tables reference this registry by Source ID:

```markdown
| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO C++ Standard | [class.dtor] | verified-2026 | 2026-06 |
| R2 | C | [C1] C++ Core Guidelines | R.1-R.5 | verified-2026 | 2026-06 |
```

When adding or reclassifying a source: update this registry first, then update affected harnesses.
