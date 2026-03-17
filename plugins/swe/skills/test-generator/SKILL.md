---
name: test-generator
description: Generate unit tests for source code. Use when writing tests, improving coverage, or setting up TDD.
---

# Test Generator Skill

When generating tests:

1. **Analyze the source** — Understand functions, inputs, outputs, side effects
2. **Identify test cases** — Happy paths, edge cases, error conditions, boundary values
3. **Follow patterns** — Arrange/Act/Assert, test doubles, parameterized tests

Test quality standards:
- Each test verifies one behavior
- Descriptive test names explaining expected behavior
- Mock external dependencies appropriately
- Test both positive and negative cases

Adapt to detected framework: Jest/Vitest/Mocha, pytest, Go testing, Rust #[test], JUnit 5.

Generate tests that are immediately runnable and follow existing project patterns.
