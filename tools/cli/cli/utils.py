from __future__ import annotations

import json
import os
import re
from pathlib import Path


def read_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def find_project_root(start: Path | None = None) -> Path:
    d = start or Path.cwd()
    while d != d.parent:
        if (d / ".git").exists():
            return d
        d = d.parent
    return start or Path.cwd()


def parse_frontmatter(content: str) -> dict | None:
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        idx = line.find(":")
        if idx == -1:
            continue
        fm[line[:idx].strip()] = line[idx + 1 :].strip()
    return fm if "name" in fm and "description" in fm else None


def resolve_marketplace_path(path: str | None = None) -> Path:
    if path:
        return Path(path).resolve()
    root = find_project_root()
    return root / ".github" / "plugin" / "marketplace.json"
