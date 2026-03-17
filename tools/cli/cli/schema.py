from __future__ import annotations

from pydantic import BaseModel, Field


class Compatibility(BaseModel):
    copilot_cli: str | None = Field(None, alias="copilot-cli")
    claude_code: str | None = Field(None, alias="claude-code")
    cursor: bool | None = None
    windsurf: bool | None = None

    model_config = {"populate_by_name": True}


class PluginManifest(BaseModel):
    name: str
    version: str
    description: str
    author: str
    category: str
    keywords: list[str]
    skills: list[str]
    commands: list[str] | None = None
    agents: list[str] | None = None
    mcp_servers: dict | None = Field(None, alias="mcpServers")
    compatibility: Compatibility | None = None

    model_config = {"populate_by_name": True}


class MarketplaceEntry(BaseModel):
    name: str
    version: str
    description: str
    author: str
    category: str
    keywords: list[str]
    entry: str


class MarketplaceManifest(BaseModel):
    name: str
    version: str
    description: str
    plugins: list[MarketplaceEntry]


class SkillFrontmatter(BaseModel):
    name: str
    description: str
