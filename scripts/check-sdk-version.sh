#!/usr/bin/env bash
#
# Compares the SDK version documented in mintlify-docs/snippets/versions.mdx
# against the latest kaleido-sdk published on npm.
#
# This check WARNS, it never fails. A mismatch is not necessarily wrong: npm may
# carry a release we have deliberately not documented yet. The point is to make
# the gap visible on the PR rather than let it go unnoticed.
#
# Usage: bash scripts/check-sdk-version.sh

set -uo pipefail

SNIPPET="mintlify-docs/snippets/versions.mdx"
REGISTRY="https://registry.npmjs.org/kaleido-sdk/latest"

# GitHub Actions annotations degrade to plain text when run locally.
warn()   { echo "::warning file=${SNIPPET}::$*"; }
notice() { echo "::notice file=${SNIPPET}::$*"; }
summary() { [[ -n "${GITHUB_STEP_SUMMARY:-}" ]] && echo "$*" >> "$GITHUB_STEP_SUMMARY"; echo "$*"; }

if [[ ! -f "$SNIPPET" ]]; then
  warn "Not found: ${SNIPPET}. Cannot check the documented SDK version."
  summary "### SDK version check — skipped"
  summary "\`${SNIPPET}\` is missing, so there is nothing to compare."
  exit 0
fi

documented="$(grep -oE 'sdkVersion[[:space:]]*=[[:space:]]*"[^"]+"' "$SNIPPET" \
  | head -1 | grep -oE '"[^"]+"' | tr -d '"')"

if [[ -z "$documented" ]]; then
  warn "Could not parse sdkVersion from ${SNIPPET}."
  summary "### SDK version check — skipped"
  summary "No \`sdkVersion\` export found in \`${SNIPPET}\`."
  exit 0
fi

# Parsed with grep rather than jq so the script runs the same locally on any
# platform as it does on a runner, without an extra dependency.
response="$(curl -fsSL --max-time 20 "$REGISTRY" 2>/dev/null)"
curl_status=$?

if [[ $curl_status -ne 0 || -z "$response" ]]; then
  warn "Could not reach the npm registry. Skipping the version comparison."
  summary "### SDK version check — skipped"
  summary "npm registry unreachable. Documented version: \`${documented}\`."
  exit 0
fi

published="$(printf '%s' "$response" \
  | grep -oE '"version"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 \
  | grep -oE '"[^"]+"[[:space:]]*$' | tr -d '"[:space:]')"

if [[ -z "$published" ]]; then
  warn "Reached the npm registry but could not parse a version from its response."
  summary "### SDK version check — skipped"
  summary "Unexpected registry response shape. Documented version: \`${documented}\`."
  exit 0
fi

if [[ "$documented" == "$published" ]]; then
  notice "Documented SDK version ${documented} matches the latest on npm."
  summary "### SDK version check — up to date"
  summary "Documented and published SDK version: \`${documented}\`."
else
  warn "Docs document SDK v${documented}, but npm's latest is v${published}. Update ${SNIPPET} if the new release should be documented."
  summary "### SDK version check — mismatch"
  summary ""
  summary "| | Version |"
  summary "|---|---|"
  summary "| Documented (\`${SNIPPET}\`) | \`${documented}\` |"
  summary "| Latest on npm | \`${published}\` |"
  summary ""
  summary "This is a warning, not a failure. Update the snippet if \`${published}\` is meant to be documented, or ignore it if that release is not ready to announce."
fi

exit 0
