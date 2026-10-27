#!/usr/bin/env bash
#
# Compares the SDK versions documented in mintlify-docs/snippets/versions.mdx
# against the latest releases published on npm:
#
#   swapSdkVersion  -> @kaleidorg/swap-sdk
#   nodeSdkVersion  -> kaleido-sdk
#
# This check WARNS, it never fails. A mismatch is not necessarily wrong: npm may
# carry a release we have deliberately not documented yet. The point is to make
# the gap visible on the PR rather than let it go unnoticed.
#
# Usage: bash scripts/check-sdk-version.sh

set -uo pipefail

SNIPPET="mintlify-docs/snippets/versions.mdx"

CHECKS=(
  "swapSdkVersion|@kaleidorg/swap-sdk|https://registry.npmjs.org/@kaleidorg%2Fswap-sdk/latest"
  "nodeSdkVersion|kaleido-sdk|https://registry.npmjs.org/kaleido-sdk/latest"
)

# GitHub Actions annotations degrade to plain text when run locally.
warn()   { echo "::warning file=${SNIPPET}::$*"; }
notice() { echo "::notice file=${SNIPPET}::$*"; }
summary() { [[ -n "${GITHUB_STEP_SUMMARY:-}" ]] && echo "$*" >> "$GITHUB_STEP_SUMMARY"; echo "$*"; }

if [[ ! -f "$SNIPPET" ]]; then
  warn "Not found: ${SNIPPET}. Cannot check the documented SDK versions."
  summary "### SDK version check — skipped"
  summary "\`${SNIPPET}\` is missing, so there is nothing to compare."
  exit 0
fi

check() {
  local var="$1" package="$2" registry="$3"

  local documented
  documented="$(grep -oE "export const ${var}[[:space:]]*=[[:space:]]*\"[^\"]+\"" "$SNIPPET" \
    | head -1 | grep -oE '"[^"]+"' | tr -d '"')"

  if [[ -z "$documented" ]]; then
    warn "Could not parse ${var} from ${SNIPPET}."
    summary "### ${package} — skipped"
    summary "No \`${var}\` export found in \`${SNIPPET}\`."
    return
  fi

  # Parsed with grep rather than jq so the script runs the same locally on any
  # platform as it does on a runner, without an extra dependency.
  local response curl_status
  response="$(curl -fsSL --max-time 20 "$registry" 2>/dev/null)"
  curl_status=$?

  if [[ $curl_status -ne 0 || -z "$response" ]]; then
    warn "Could not reach the npm registry for ${package}. Skipping the comparison."
    summary "### ${package} — skipped"
    summary "npm registry unreachable. Documented version: \`${documented}\`."
    return
  fi

  local published
  published="$(printf '%s' "$response" \
    | grep -oE '"version"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 \
    | grep -oE '"[^"]+"[[:space:]]*$' | tr -d '"[:space:]')"

  if [[ -z "$published" ]]; then
    warn "Reached the npm registry but could not parse a version for ${package}."
    summary "### ${package} — skipped"
    summary "Unexpected registry response shape. Documented version: \`${documented}\`."
    return
  fi

  if [[ "$documented" == "$published" ]]; then
    notice "Documented ${package} version ${documented} matches the latest on npm."
    summary "### ${package} — up to date"
    summary "Documented and published version: \`${documented}\`."
  else
    warn "Docs document ${package} v${documented}, but npm's latest is v${published}. Update ${var} in ${SNIPPET} if the new release should be documented."
    summary "### ${package} — mismatch"
    summary ""
    summary "| | Version |"
    summary "|---|---|"
    summary "| Documented (\`${var}\`) | \`${documented}\` |"
    summary "| Latest on npm | \`${published}\` |"
    summary ""
    summary "This is a warning, not a failure. Update the snippet if \`${published}\` is meant to be documented, or ignore it if that release is not ready to announce."
  fi
}

for entry in "${CHECKS[@]}"; do
  IFS='|' read -r var package registry <<< "$entry"
  check "$var" "$package" "$registry"
done

exit 0
