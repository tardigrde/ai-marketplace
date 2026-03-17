from __future__ import annotations

from pydantic import BaseModel


class Owner(BaseModel):
    name: str
    email: str | None = None


class Metadata(BaseModel):
    description: str | None = None
    version: str | None = None


class MarketplacePluginEntry(BaseModel):
    name: str
    source: str
    description: str | None = None
    version: str | None = None
    category: str | None = None
    keywords: list[str] | None = None


class MarketplaceManifest(BaseModel):
    name: str
    owner: Owner
    metadata: Metadata | None = None
    plugins: list[MarketplacePluginEntry]


class PluginManifest(BaseModel):
    name: str
    description: str
    version: str


class SkillFrontmatter(BaseModel):
    name: str
    description: str
