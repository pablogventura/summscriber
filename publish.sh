#!/usr/bin/env bash
# Publish summscriber to PyPI.
# Usage: ./publish.sh [--tag-only]
#   --tag-only  Skip build and upload; only create and push the version tag (via SSH).
#               Use to test tag/push or when you already published but didn't tag.
# Prerequisites:
#   pip install build twine
#   PyPI account and token (https://pypi.org/manage/account/token/)
#   For first upload: twine upload will prompt for username __token__ and password (pypi-...)
#   Or set: export TWINE_USERNAME=__token__  export TWINE_PASSWORD=pypi-your-token

set -e
cd "$(dirname "$0")"

TAG_ONLY=false
[[ "${1:-}" == "--tag-only" ]] && TAG_ONLY=true

if ! $TAG_ONLY; then
  echo "Cleaning old build artifacts..."
  rm -rf build/ dist/ *.egg-info

  echo "Building package..."
  python -m build

  echo "Uploading to PyPI..."
  twine upload dist/*
fi

VERSION=$(sed -n 's/^version = "\(.*\)"$/\1/p' pyproject.toml)
if [ -z "$VERSION" ]; then
  echo "Could not read version from pyproject.toml"
  exit 1
fi
TAG="v${VERSION}"
echo "Creating tag ${TAG}..."
git tag "$TAG"
echo "Pushing tag ${TAG} (via SSH)..."
ORIGIN_URL=$(git remote get-url origin)
case "$ORIGIN_URL" in
  https://github.com/*) PUSH_URL="git@github.com:${ORIGIN_URL#https://github.com/}"; PUSH_URL="${PUSH_URL%.git}.git"; ;;
  *) PUSH_URL="$ORIGIN_URL"; ;;
esac
git push "$PUSH_URL" "$TAG"

echo "Done. Check https://pypi.org/project/summscriber/"
