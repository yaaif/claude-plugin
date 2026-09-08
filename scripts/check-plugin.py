#!/usr/bin/env python3
"""Inventory and skill-sync checks for the YAAIF Claude Code plugin."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PLUGIN_VERSION = "1.3.0"
MCP_PACKAGE = "@yaaif/platform-mcp@1.3.1"

EXPECTED_SKILLS = (
    "yaaif-auth",
    "yaaif-create-ambient",
    "yaaif-create-mcp",
    "yaaif-create-skill",
    "yaaif-doctor",
    "yaaif-ops-support",
    "yaaif-plan-usecase",
    "yaaif-platform-tools",
    "yaaif-scenario",
)

EXPECTED_COMMANDS = (
    "yaaif-doctor",
    "yaaif-login",
    "yaaif-new-mcp",
    "yaaif-new-skill",
    "yaaif-new-workflow",
    "yaaif-ops",
    "yaaif-plan",
    "yaaif-platform-tools",
    "yaaif-scenario",
    "yaaif-sync-scenario",
)

USER_CONFIG_KEYS = (
    "YAAIF_PLATFORM_PROFILE",
    "YAAIF_OIDC_AUTHORITY",
    "YAAIF_API_BASE_URL",
    "YAAIF_AGENT_BASE_URL",
    "YAAIF_CONTROL_PLANE_BASE_URL",
    "YAAIF_APPROVAL_BASE_URL",
    "YAAIF_DEFAULT_TENANT_ID",
    "YAAIF_OIDC_CLIENT_ID",
    "YAAIF_EXTRA_CA_FILE",
    "YAAIF_CLIENT_CERT_FILE",
    "YAAIF_CLIENT_KEY_FILE",
)

_PROTECT = "cursor-plugin"


def canonicalize_skill_text(text: str) -> str:
    """Normalize IDE-specific tokens so Cursor and Claude skill copies can be compared."""
    protected = "\0CURSOR_PLUGIN\0"
    text = text.replace(_PROTECT, protected)
    text = text.replace("/yaaif-platform:", "/")
    text = text.replace("~/.yaaif/claude", "{{STATE}}")
    text = text.replace("~/.yaaif/cursor", "{{STATE}}")
    text = text.replace("~/.yaaif/codex", "{{STATE}}")
    text = text.replace("yaaif-claude", "{{OIDC}}")
    text = text.replace("yaaif-cursor", "{{OIDC}}")
    text = text.replace("yaaif-codex", "{{OIDC}}")
    text = text.replace("--client claude", "--client {{CLIENT}}")
    text = text.replace("--client cursor", "--client {{CLIENT}}")
    text = text.replace("--client codex", "--client {{CLIENT}}")
    text = text.replace("Claude Code", "{{IDE}}")
    text = text.replace("Cursor", "{{IDE}}")
    text = text.replace("Codex", "{{IDE}}")
    text = text.replace("MCP REST", "{{REST}}")
    text = text.replace("{{IDE}} REST", "{{REST}}")
    text = text.replace("The bridge discovers", "{{DISCOVERS}}")
    text = text.replace("{{IDE}} discovers", "{{DISCOVERS}}")
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    return text.replace(protected, _PROTECT)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_inventory(root: Path) -> list[str]:
    errors: list[str] = []
    plugin_path = root / ".claude-plugin" / "plugin.json"
    mcp_path = root / ".mcp.json"
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    logo = root / "assets" / "logo.svg"

    if not plugin_path.is_file():
        return [f"missing {plugin_path}"]
    plugin = _load_json(plugin_path)
    if plugin.get("version") != PLUGIN_VERSION:
        errors.append(f"plugin.json version {plugin.get('version')!r} != {PLUGIN_VERSION}")
    if plugin.get("name") != "yaaif-platform":
        errors.append(f"plugin.json name {plugin.get('name')!r} != 'yaaif-platform'")
    user_config = plugin.get("userConfig") or {}
    missing = [k for k in USER_CONFIG_KEYS if k not in user_config]
    if missing:
        errors.append(f"plugin.json userConfig missing {missing}")

    if not mcp_path.is_file():
        errors.append(f"missing {mcp_path}")
    else:
        mcp = _load_json(mcp_path)
        args = mcp.get("mcpServers", {}).get("yaaif", {}).get("args") or []
        if MCP_PACKAGE not in args:
            errors.append(f".mcp.json does not pin {MCP_PACKAGE}: {args}")
        if "--client" not in args or "claude" not in args:
            errors.append(f".mcp.json missing --client claude: {args}")
        env = mcp.get("mcpServers", {}).get("yaaif", {}).get("env") or {}
        for key in USER_CONFIG_KEYS:
            expected = f"${{user_config.{key}}}"
            if env.get(key) != expected:
                errors.append(f".mcp.json env.{key} != {expected}")

    if marketplace_path.is_file():
        market = _load_json(marketplace_path)
        plugins = market.get("plugins") or []
        if not plugins or plugins[0].get("version") != PLUGIN_VERSION:
            errors.append(f"marketplace.json plugin version != {PLUGIN_VERSION}")

    if not logo.is_file():
        errors.append("missing assets/logo.svg")

    skills_dir = root / "skills"
    for name in EXPECTED_SKILLS:
        skill = skills_dir / name / "SKILL.md"
        if not skill.is_file():
            errors.append(f"missing skill {skill}")

    extra_skills = sorted(
        p.name for p in skills_dir.iterdir() if p.is_dir() and p.name not in EXPECTED_SKILLS
    )
    if extra_skills:
        errors.append(f"unexpected skills: {extra_skills}")

    commands_dir = root / "commands"
    for name in EXPECTED_COMMANDS:
        cmd = commands_dir / f"{name}.md"
        if not cmd.is_file():
            errors.append(f"missing command {cmd}")

    extra_cmds = sorted(
        p.stem
        for p in commands_dir.glob("*.md")
        if p.stem not in EXPECTED_COMMANDS
    )
    if extra_cmds:
        errors.append(f"unexpected commands: {extra_cmds}")

    return errors


def _iter_skill_files(skills_root: Path) -> list[Path]:
    return sorted(p for p in skills_root.rglob("*") if p.is_file() and not p.name.startswith("."))


def check_skill_sync(claude_root: Path, cursor_root: Path) -> list[str]:
    errors: list[str] = []
    cursor_skills = cursor_root / "skills"
    claude_skills = claude_root / "skills"
    if not cursor_skills.is_dir():
        return [f"cursor skills dir missing: {cursor_skills}"]

    cursor_files = {p.relative_to(cursor_skills): p for p in _iter_skill_files(cursor_skills)}
    claude_files = {p.relative_to(claude_skills): p for p in _iter_skill_files(claude_skills)}

    missing = sorted(cursor_files.keys() - claude_files.keys())
    extra = sorted(claude_files.keys() - cursor_files.keys())
    if missing:
        errors.append(f"claude skills missing vs cursor: {missing}")
    if extra:
        errors.append(f"claude skills extra vs cursor: {extra}")

    for rel in sorted(cursor_files.keys() & claude_files.keys()):
        expected = canonicalize_skill_text(cursor_files[rel].read_text(encoding="utf-8"))
        actual = canonicalize_skill_text(claude_files[rel].read_text(encoding="utf-8"))
        if expected != actual:
            errors.append(f"skill drift after IDE substitutions: skills/{rel}")
    return errors


def resolve_cursor_root(explicit: str | None, claude_root: Path) -> Path | None:
    if explicit:
        return Path(explicit).expanduser().resolve()
    sibling = (claude_root / ".." / "cursor-plugin").resolve()
    if sibling.is_dir() and (sibling / "skills").is_dir():
        return sibling
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="claude-plugin root",
    )
    parser.add_argument(
        "--cursor-root",
        default=None,
        help="cursor-plugin root (defaults to ../cursor-plugin or CURSOR_PLUGIN_ROOT)",
    )
    parser.add_argument(
        "--require-skill-sync",
        action="store_true",
        help="fail if cursor-plugin skills are not available to compare",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    errors = check_inventory(root)

    cursor_root = resolve_cursor_root(args.cursor_root or os.environ.get("CURSOR_PLUGIN_ROOT"), root)
    if cursor_root is None:
        msg = "cursor-plugin skills not found (set --cursor-root or CURSOR_PLUGIN_ROOT)"
        if args.require_skill_sync:
            errors.append(msg)
        else:
            print(f"skip skill-sync: {msg}", file=sys.stderr)
    else:
        errors.extend(check_skill_sync(root, cursor_root))

    if errors:
        print("check-plugin failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("check-plugin ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
