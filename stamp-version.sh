#!/bin/sh
# Regenerates version.json with the current branch, short commit hash, and
# build time. Run this right before committing/pushing (to either origin
# or staging) so the footer always shows what's actually deployed.
branch=$(git rev-parse --abbrev-ref HEAD)
commit=$(git rev-parse --short HEAD)
built=$(date -u +"%Y-%m-%d %H:%M UTC")
cat > version.json <<EOF
{"branch":"$branch","commit":"$commit","built":"$built"}
EOF
echo "version.json -> $branch · $commit · $built"
