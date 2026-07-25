"""Command line interface for {{ project_name }}."""

from __future__ import annotations

import argparse

from .version import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="{{ package_name }}")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main() -> int:
    """Run the CLI entry point."""
    parser = build_parser()
    parser.parse_args()
    return 0
