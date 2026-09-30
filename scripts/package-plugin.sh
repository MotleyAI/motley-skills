#!/bin/bash
# Package the plugin as a zip.
#   ./scripts/package-plugin.sh          Claude Code / Cowork plugin
#   ./scripts/package-plugin.sh openai   OpenAI plugin directory submission
set -e
cd "$(dirname "$0")/.."
TARGET="${1:-claude}"

case "$TARGET" in
  claude)
    VERSION=$(jq -r '.version' .claude-plugin/plugin.json)
    OUT="motley-plugin-${VERSION}.zip"
    rm -f "$OUT"
    zip -r "$OUT" \
      .claude-plugin \
      .mcp.json \
      skills \
      LICENSE \
      README.md
    ;;
  openai)
    VERSION=$(jq -r '.version' plugin.json)
    CLAUDE_VERSION=$(jq -r '.version' .claude-plugin/plugin.json)
    if [ "$VERSION" != "$CLAUDE_VERSION" ]; then
      echo "Version mismatch: plugin.json=$VERSION, .claude-plugin/plugin.json=$CLAUDE_VERSION" >&2
      exit 1
    fi
    OUT="motley-openai-plugin-${VERSION}.zip"
    rm -f "$OUT"
    # frontend-slides depends on Claude Code tools, so the OpenAI package leaves it out.
    zip -r "$OUT" \
      plugin.json \
      mcp.json \
      assets \
      skills/create-report \
      skills/semantic-layer-bootstrap \
      LICENSE \
      README.md
    ;;
  *)
    echo "Unknown target: $TARGET (expected: claude or openai)" >&2
    exit 1
    ;;
esac
echo "Created plugin package: $OUT"
