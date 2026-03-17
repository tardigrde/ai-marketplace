---
name: generate-tests
description: Generate unit tests for specified source files
argument-hint: <file-path> [--framework <name>]
---

# Generate Tests Command

Generate comprehensive unit tests for the specified source file(s).

## Usage

```
/generate-tests <file-path>
/generate-tests <file-path> --framework jest
/generate-tests src/**/*.ts --framework vitest
```

## Steps

1. Read the specified source file(s)
2. Analyze all exported functions, classes, and interfaces
3. Detect the project's test framework from package.json or config files
4. Generate test files with appropriate imports and setup
5. Write tests to the corresponding `__tests__/` or `test/` directory
6. Report what was generated with a summary of coverage

## Options

- `--framework <name>` — Override detected test framework
- `--coverage` — Aim for maximum branch coverage
- `--integration` — Generate integration tests instead of unit tests
