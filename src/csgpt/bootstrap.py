"""Bootstrap orchestration helpers for initializing a project skeleton."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Bootstrapper:
    """Coordinates bootstrap operations.

    Attributes:
        project_root: Path - root path of the project
    """

    project_root: Path

    def run(self) -> None:
        """Create the standard project directories for a new workspace."""
        logger.debug("Bootstrapping project at %s", self.project_root)

        directories = ["src", "tests", "docs", "configs", "templates", "scripts"]
        for directory_name in directories:
            directory = self.project_root / directory_name
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Bootstrap directories created under %s", self.project_root)
