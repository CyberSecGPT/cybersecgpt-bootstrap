from pathlib import Path

import pytest

from csgpt.bootstrap import Bootstrapper
from csgpt.github import GitHubClient
from csgpt.templates import TemplateManager
from csgpt import cli


def test_template_manager_discovers_and_renders_templates(tmp_path: Path) -> None:
    templates_dir = tmp_path / "templates"
    template_dir = templates_dir / "bootstrap"
    template_dir.mkdir(parents=True)
    (template_dir / "README.md").write_text("# {project_name}\n", encoding="utf-8")
    (template_dir / "src").mkdir()
    (template_dir / "src" / "__init__.py").write_text(
        "# generated for {project_name}\n", encoding="utf-8"
    )

    manager = TemplateManager(templates_dir=templates_dir)

    assert manager.list() == ["bootstrap"]

    destination = tmp_path / "output"
    manager.render("bootstrap", destination, replacements={"project_name": "demo"})

    assert (destination / "README.md").read_text(encoding="utf-8") == "# demo\n"
    assert (destination / "src" / "__init__.py").read_text(
        encoding="utf-8"
    ) == "# generated for demo\n"


def test_template_manager_renders_double_brace_placeholder(tmp_path: Path) -> None:
    template = tmp_path / "templates" / "bootstrap"
    template.mkdir(parents=True)
    (template / "README.md").write_text("# {{ project_name }}\n", encoding="utf-8")

    destination = tmp_path / "output"
    TemplateManager(template.parent).render(
        "bootstrap", destination, {"project_name": "demo"}
    )

    assert (destination / "README.md").read_text(encoding="utf-8") == "# demo\n"


def test_template_manager_renders_package_name_in_path(tmp_path: Path) -> None:
    template = tmp_path / "templates" / "bootstrap"
    package_dir = template / "src" / "{{ package_name }}"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text("", encoding="utf-8")

    destination = tmp_path / "output"
    TemplateManager(template.parent).render(
        "bootstrap", destination, {"project_name": "My Project"}
    )

    assert (destination / "src" / "my_project" / "__init__.py").is_file()


def test_template_manager_rejects_unresolved_placeholder(tmp_path: Path) -> None:
    template = tmp_path / "templates" / "bootstrap"
    template.mkdir(parents=True)
    (template / "README.md").write_text(
        "# {{ project_name }} by {{ author }}\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match=r"Unresolved required placeholder.*author"):
        TemplateManager(template.parent).render(
            "bootstrap", tmp_path / "output", {"project_name": "demo"}
        )


def test_template_manager_copies_binary_file_unchanged(tmp_path: Path) -> None:
    template = tmp_path / "templates" / "bootstrap"
    template.mkdir(parents=True)
    binary_content = b"\x89PNG\r\n\x1a\n\xff{project_name}\x00"
    (template / "logo.png").write_bytes(binary_content)

    destination = tmp_path / "output"
    TemplateManager(template.parent).render(
        "bootstrap", destination, {"project_name": "demo"}
    )

    assert (destination / "logo.png").read_bytes() == binary_content


def test_template_manager_validates_template_directory(tmp_path: Path) -> None:
    templates_dir = tmp_path / "templates"
    template_dir = templates_dir / "bootstrap"
    template_dir.mkdir(parents=True)
    (template_dir / "README.md").write_text("# template\n", encoding="utf-8")

    manager = TemplateManager(templates_dir=templates_dir)

    assert manager.validate("bootstrap") is True

    with pytest.raises(ValueError):
        manager.validate("missing")


def test_template_list_cli_command_prints_discovered_templates(
    tmp_path: Path, capsys
) -> None:
    templates_dir = tmp_path / "templates"
    (templates_dir / "bootstrap").mkdir(parents=True)
    (templates_dir / "bootstrap" / "README.md").write_text(
        "# template\n", encoding="utf-8"
    )

    parser = cli.build_parser()
    args = parser.parse_args(
        ["template", "list", "--templates-dir", str(templates_dir)]
    )

    assert args.func(args) == 0
    captured = capsys.readouterr()
    assert "bootstrap" in captured.out


def test_template_apply_cli_command_renders_template(tmp_path: Path, capsys) -> None:
    templates_dir = tmp_path / "templates"
    template_dir = templates_dir / "bootstrap"
    template_dir.mkdir(parents=True)
    (template_dir / "README.md").write_text("# {project_name}\n", encoding="utf-8")

    destination = tmp_path / "generated"
    parser = cli.build_parser()
    args = parser.parse_args(
        [
            "template",
            "apply",
            "bootstrap",
            "--destination",
            str(destination),
            "--templates-dir",
            str(templates_dir),
            "--project-name",
            "demo",
        ]
    )

    assert args.func(args) == 0
    assert (destination / "README.md").read_text(encoding="utf-8") == "# demo\n"
    captured = capsys.readouterr()
    assert "Applied template" in captured.out


def test_template_show_and_validate_cli_commands(tmp_path: Path, capsys) -> None:
    templates_dir = tmp_path / "templates"
    template_dir = templates_dir / "bootstrap"
    template_dir.mkdir(parents=True)
    (template_dir / "README.md").write_text("# template\n", encoding="utf-8")
    (template_dir / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (template_dir / "requirements.txt").write_text("", encoding="utf-8")
    (template_dir / "configs").mkdir()
    (template_dir / "docs").mkdir()
    (template_dir / "scripts").mkdir()
    (template_dir / "src").mkdir()
    (template_dir / "tests").mkdir()
    (template_dir / "assets").mkdir()

    parser = cli.build_parser()
    show_args = parser.parse_args(
        ["template", "show", "bootstrap", "--templates-dir", str(templates_dir)]
    )
    validate_args = parser.parse_args(
        ["template", "validate", "bootstrap", "--templates-dir", str(templates_dir)]
    )

    assert show_args.func(show_args) == 0
    assert validate_args.func(validate_args) == 0
    captured = capsys.readouterr()
    assert "Template: bootstrap" in captured.out
    assert "is valid" in captured.out


def test_github_client_returns_basic_metadata() -> None:
    client = GitHubClient()

    metadata = client.get_repository("octocat", "Hello-World")

    assert metadata["full_name"] == "octocat/Hello-World"
    assert metadata["name"] == "Hello-World"


def test_bootstrapper_creates_expected_directories(tmp_path: Path) -> None:
    bootstrapper = Bootstrapper(project_root=tmp_path)

    bootstrapper.run()

    for directory_name in ("src", "tests", "docs", "configs", "templates"):
        assert (tmp_path / directory_name).is_dir()
