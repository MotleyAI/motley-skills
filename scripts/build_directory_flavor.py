"""Build the directory flavor of this plugin.

This repository is the full flavor. The Claude and ChatGPT directories list the
directory flavor, which CI generates from it. The directory flavor connects to
the directory endpoint, and that endpoint never prompts agents for feedback.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FULL_MCP_URL = "https://app.motley.ai/api/v1/mcp"
DIRECTORY_MCP_URL = "https://app.motley.ai/api/v1/mcp-directory"
DIRECTORY_REPO = "MotleyAI/motley-skills-directory"
DIRECTORY_MARKETPLACE = "motley-directory"

EXCLUDED_PREFIXES = (".github/", "scripts/")
MCP_CONFIGS = (".mcp.json", "mcp.json")
MARKETPLACE = ".claude-plugin/marketplace.json"
VERSIONED_MANIFESTS = ("plugin.json", ".claude-plugin/plugin.json")
OPENAI_BUNDLE = ("plugin.json", "mcp.json", "assets", "skills", "LICENSE", "README.md")
TEXT_SUFFIXES = (".md", ".json")

# The lookahead keeps the directory URL from matching.
FULL_URL_PATTERN = re.compile(re.escape(FULL_MCP_URL) + r"(?![\w-])")
SOURCE_REPO_PATTERN = re.compile(r"MotleyAI/motley-skills(?![\w-])")
# Directory users install from the directory, so the install steps only confuse them.
INSTALL_SECTION = re.compile(r"^## Install\n.*?(?=^## )", flags=re.MULTILINE | re.DOTALL)
FORBIDDEN_SKILL_TEXT = "report_feedback"


class FlavorError(Exception):
    pass


def tracked_files() -> list[str]:
    output = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO_ROOT, check=True, capture_output=True, text=True
    ).stdout
    return [path for path in output.split("\0") if path and not path.startswith(EXCLUDED_PREFIXES)]


def mcp_url(*, config_path: Path) -> str:
    return json.loads(config_path.read_text())["mcpServers"]["motley"]["url"]


def check_source() -> None:
    for name in MCP_CONFIGS:
        url = mcp_url(config_path=REPO_ROOT / name)
        if url != FULL_MCP_URL:
            raise FlavorError(f"{name} in the full flavor must use {FULL_MCP_URL}, not {url}")


def copy_tree(*, out_dir: Path) -> None:
    for relative in tracked_files():
        target = out_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / relative, target)


def rewrite_text(*, out_dir: Path) -> None:
    for path in out_dir.rglob("*"):
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = FULL_URL_PATTERN.sub(DIRECTORY_MCP_URL, path.read_text())
        path.write_text(SOURCE_REPO_PATTERN.sub(DIRECTORY_REPO, text))

    readme = out_dir / "README.md"
    text, count = INSTALL_SECTION.subn("", readme.read_text())
    if count != 1:
        raise FlavorError("README.md must have exactly one '## Install' section followed by another section")
    readme.write_text(text)

    # Another name keeps the marketplace apart from the full one when a user adds both.
    marketplace = out_dir / MARKETPLACE
    data = json.loads(marketplace.read_text())
    data["name"] = DIRECTORY_MARKETPLACE
    marketplace.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def plugin_versions(*, root: Path) -> set[str]:
    versions = {json.loads((root / name).read_text())["version"] for name in VERSIONED_MANIFESTS}
    versions.update(plugin["version"] for plugin in json.loads((root / MARKETPLACE).read_text())["plugins"])
    return versions


def check_flavor(*, out_dir: Path, expected_version: str | None) -> None:
    for name in MCP_CONFIGS:
        url = mcp_url(config_path=out_dir / name)
        if url != DIRECTORY_MCP_URL:
            raise FlavorError(f"{name} in the directory flavor must use {DIRECTORY_MCP_URL}, not {url}")

    for path in out_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if FULL_URL_PATTERN.search(text):
            raise FlavorError(f"{path.relative_to(out_dir)} still contains {FULL_MCP_URL}")
        if path.suffix == ".json":
            json.loads(text)

    for skill in (out_dir / "skills").rglob("*"):
        if skill.is_file() and FORBIDDEN_SKILL_TEXT in skill.read_text():
            raise FlavorError(
                f"{skill.relative_to(out_dir)} mentions {FORBIDDEN_SKILL_TEXT}. "
                "Directory policy forbids skills that make agents report feedback."
            )

    versions = plugin_versions(root=out_dir)
    if len(versions) != 1:
        raise FlavorError(f"Manifests disagree on the version: {sorted(versions)}")
    if expected_version is not None and versions != {expected_version}:
        raise FlavorError(f"Manifests have version {versions.pop()}, but the tag says {expected_version}")


def build_openai_zip(*, out_dir: Path, zip_path: Path) -> None:
    files = []
    for entry in OPENAI_BUNDLE:
        path = out_dir / entry
        files.extend(sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path])

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            # A fixed timestamp makes rebuilds byte-identical.
            info = zipfile.ZipInfo(filename=str(path.relative_to(out_dir)), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, path.read_bytes())

    with zipfile.ZipFile(zip_path) as bundle:
        if bundle.testzip() is not None:
            raise FlavorError(f"{zip_path} is corrupt")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Empty or missing directory for the flavor.")
    parser.add_argument("--zip", type=Path, help="Also write the OpenAI plugin bundle to this path.")
    parser.add_argument("--expect-version", help="Fail unless every manifest has this version.")
    args = parser.parse_args()

    out_dir: Path = args.out.resolve()
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FlavorError(f"{out_dir} is not empty")

    check_source()
    copy_tree(out_dir=out_dir)
    rewrite_text(out_dir=out_dir)
    check_flavor(out_dir=out_dir, expected_version=args.expect_version)
    if args.zip is not None:
        build_openai_zip(out_dir=out_dir, zip_path=args.zip.resolve())
    print(f"Built the directory flavor in {out_dir}")


if __name__ == "__main__":
    try:
        main()
    except FlavorError as error:
        sys.exit(f"error: {error}")
