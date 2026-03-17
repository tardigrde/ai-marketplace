---
name: code-review
description: Review code for bugs, security, and best practices. Use when reviewing code, checking PRs, or analyzing code quality.
---

# Code Review Skill

When reviewing code, follow these steps:

1. **Security Analysis** — Check for SQL injection, XSS, CSRF, hardcoded secrets, unsafe deserialization
2. **Code Quality** — Evaluate readability, naming conventions, DRY principle, proper abstractions
3. **Performance** — Identify bottlenecks, unnecessary allocations, algorithmic inefficiencies
4. **Error Handling** — Ensure proper error handling, edge cases, graceful degradation

Provide your review as:
- **Summary**: Brief overall assessment
- **Issues** (critical/warning/info): Specific findings with line references
- **Suggestions**: Improvement recommendations

Be constructive and specific. Reference language idioms and conventions. Suggest concrete fixes.
