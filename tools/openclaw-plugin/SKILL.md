---
name: openclaw-plugin
description: Create, package, and deploy a native OpenClaw plugin with agent tools. Use when building a new OpenClaw plugin, wiring it into a Docker-based deployment, or debugging plugin load failures.
compatibility: Requires Docker, Node.js/TypeScript, and an OpenClaw gateway deployment. Designed for self-hosted OpenClaw setups using openclaw-infra or similar IaC repos.
metadata:
  author: tardigrde
  version: "1.0"
---

# OpenClaw Plugin Development & Deployment

## Plugin structure

A native plugin lives in `plugins/<id>/` at the repo root:

```
plugins/dropbox/
├── package.json           # Required by openclaw plugins install
├── openclaw.plugin.json   # Plugin manifest (id, configSchema, uiHints)
├── index.ts               # Entry point — exports default function(api)
└── src/
    └── client.ts          # Supporting modules
```

## Plugin API

The entry point receives an `api` object. Use the real OpenClaw SDK types:

```typescript
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

export default function (api: OpenClawPluginApi) {
  // Access plugin config (from openclaw.json plugins.entries.<id>.config)
  const config = (api.pluginConfig ?? {}) as MyConfig;

  // Register a tool
  api.registerTool({
    name: "my_tool",
    description: "...",
    input: Type.Object({ ... }),
    async run(ctx, params) { ... }
  }, { optional: true });
}
```

**Common mistake:** `api.getConfig()` does not exist. Plugin config is at `api.pluginConfig` (a plain object, not a method).

## package.json requirements

`openclaw plugins install` requires a `package.json`. Minimum viable:

```json
{
  "name": "<plugin-id>",
  "version": "1.0.0",
  "type": "module",
  "main": "index.ts",
  "openclaw": { "extensions": ["./index.ts"] },
  "dependencies": {
    "@sinclair/typebox": "0.34.48"
  },
  "peerDependencies": { "openclaw": "*" }
}
```

- `name` must match the `id` in `openclaw.plugin.json` to avoid id-mismatch warnings.
- TypeBox (`@sinclair/typebox`) is needed for `Type.Object(...)` tool schemas.

## openclaw.plugin.json

```json
{
  "id": "dropbox",
  "name": "Dropbox",
  "description": "...",
  "configSchema": {
    "type": "object",
    "properties": {
      "myOption": { "type": "number", "default": 100 }
    }
  }
}
```

## Docker wiring

### Dockerfile — copy plugins and install their deps at build time

```dockerfile
COPY plugins/ /opt/plugins/
RUN for dir in /opt/plugins/*/; do \
      [ -f "$dir/package.json" ] && npm install --prefix "$dir" --omit=dev --no-package-lock; \
    done
```

**Build context must be repo root** (not `docker/`) so `plugins/` is reachable:

```yaml
# docker-compose.yml
build:
  context: .
  dockerfile: docker/Dockerfile
```

```yaml
# .github/workflows/docker-build.yml
- uses: docker/build-push-action@v7
  with:
    context: .
    file: docker/Dockerfile
```

### entrypoint.sh — install and refresh plugins on every container start

```bash
if [[ -d "/opt/plugins" ]]; then
  for plugin_dir in /opt/plugins/*/; do
    plugin_id=$(basename "$plugin_dir")
    # Force-remove stale install from persistent volume before reinstalling
    rm -rf "/home/node/.openclaw/extensions/$plugin_id"
    openclaw plugins install "$plugin_dir" 2>&1 || true
    # Install deps (openclaw plugins install does not run npm install)
    ext_dir="/home/node/.openclaw/extensions/$plugin_id"
    if [[ -f "$ext_dir/package.json" ]]; then
      npm install --prefix "$ext_dir" --omit=dev --no-package-lock --silent 2>&1 || true
    fi
  done
fi
```

**Why force-remove:** plugin extensions are in a Docker volume (persisted across restarts). Without `rm -rf`, `openclaw plugins install` fails with "plugin already exists" and the old source code is never updated.

**Why npm install after:** `openclaw plugins install` copies source files but does not install npm dependencies in the extensions directory.

## Enable in openclaw.json

```json
{
  "plugins": {
    "entries": {
      "dropbox": {
        "enabled": true,
        "config": { "myOption": 102400 }
      }
    }
  }
}
```

## Verify

```bash
docker exec <gateway-container> openclaw plugins list
# Expect: | MyPlugin | my-id | loaded | global:my-id/index.ts | 1.0.0 |
```

Common error states and causes:

| Status | Cause | Fix |
|---|---|---|
| `error: Cannot find module 'X'` | npm deps not installed in extensions dir | Add npm install step to entrypoint after plugin install |
| `error: api.getConfig is not a function` | Wrong plugin API usage | Use `api.pluginConfig` instead |
| `error: plugin already exists` | Stale volume install, reinstall blocked | `rm -rf extensions/<id>` before `openclaw plugins install` |
| `plugin not found: X (stale config)` | Plugin in `openclaw.json` but not yet installed | Normal during entrypoint before install completes |
