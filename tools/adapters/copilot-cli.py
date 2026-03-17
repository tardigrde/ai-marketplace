#!/usr/bin/env python3
"""Generate Copilot CLI marketplace.json from Claude Code marketplace."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CLAUDE_MARKETPLACE = PROJECT_ROOT / ".claude-plugin" / "marketplace.json"
OUTPUT_DIR = PROJECT_ROOT / "dist" / "copilot-cli"


def main() -> None:
    if not CLAUDE_MARKETPLACE.exists():
        print("ERROR: .claude-plugin/marketplace.json not found.", file=sys.stderr)
        sys.exit(1)

    claude = json.loads(CLAUDE_MARKETPLACE.read_text())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copilot_plugins = []
    for entry in claude.get("plugins", []):
        plugin_dir = (PROJECT_ROOT / entry["source"]).resolve()
        skills_dir = plugin_dir / "skills"

        skill_paths = []
        if skills_dir.exists():
            for skill_dir in sorted(skills_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skill_paths.append(f"./skills/{skill_dir.name}")

        copilot_plugins.append({
            "name": entry["name"],
            "source": entry["source"],
            "description": entry.get("description", ""),
            "version": entry.get("version", "1.0.0"),
            "skills": skill_paths,
        })

    copilot_marketplace = {
        "name": claude["name"],
        "metadata": {
            "description": claude.get("metadata", {}).get("description", ""),
            "version": claude.get("metadata", {}).get("version", "1.0.0"),
        },
        "owner": claude.get("owner", {}),
        "plugins": copilot_plugins,
    }

    out_path = OUTPUT_DIR / "marketplace.json"
    out_path.write_text(json.dumps(copilot_marketplace, indent=2) + "\n")
    print(f"Generated: dist/copilot-cli/marketplace.json")
    print(f"  {len(copilot_plugins)} plugin(s) for Copilot CLI")


if __name__ == "__main__":
    main()
