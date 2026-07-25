"""Configuration helpers for {{ project_name }}."""

from __future__ import annotations

from pathlib import Path


def load_config(path: str | Path | None = None) -> dict[str, object]:
    """Load configuration from a YAML-like file path when available."""
    if path is None:
        return {"name": "{{ project_name }}"}

    config_path = Path(path)
    if not config_path.exists():
        return {"name": "{{ project_name }}", "path": str(config_path)}

    return {"name": "{{ project_name }}", "path": str(config_path)}
