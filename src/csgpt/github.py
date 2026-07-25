"""Minimal GitHub client helpers for repository metadata lookups."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class GitHubClient:
    """Simple GitHub client stub with deterministic metadata responses.

    Attributes:
        token: Optional[str] - authentication token
    """

    token: Optional[str] = None

    def get_repository(self, owner: str, name: str) -> dict[str, Any]:
        """Return basic repository metadata for the requested repository."""
        normalized_owner = owner.strip()
        normalized_name = name.strip()

        if not normalized_owner or not normalized_name:
            raise ValueError("owner and name must be non-empty")

        return {
            "owner": normalized_owner,
            "name": normalized_name,
            "full_name": f"{normalized_owner}/{normalized_name}",
            "private": False,
            "default_branch": "main",
            "description": f"Repository {normalized_name}",
        }
