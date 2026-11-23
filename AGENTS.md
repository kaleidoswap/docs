# AGENTS.md

Guidance for coding agents working in this repository. Human contributors: see [README.md](README.md).

## What this is

Source of [docs.kaleidoswap.com](https://docs.kaleidoswap.com), built with Mintlify. Everything published lives in `mintlify-docs/`. Merging to `main` publishes.

## Layout

| Path | Contents |
|---|---|
| `mintlify-docs/docs.json` | Navigation for both languages, theme, navbar, redirects |
| `mintlify-docs/openapi.json` | Public `/v2` API spec of the maker. Shared by both languages, never translated |
| `mintlify-docs/sdk/` | `@kaleidorg/swap-sdk`, the SDK integrators use against the maker |
| `mintlify-docs/cli/` | KaleidoCLI, plus `cli/node-sdk/` for `kaleido-sdk` (the Node SDK the CLI, MCP server and Desktop app use) |
| `mintlify-docs/api-reference/` | API overview and integration guides; endpoint pages come from `openapi.json` |
| `mintlify-docs/{whats-kaleidoswap,desktop-app,extensions,ai-tools,wallet-engine}/` | Product sections, one per navigation tab |
| `mintlify-docs/cn/` | Simplified Chinese, a one-to-one mirror of the English tree |
| `mintlify-docs/snippets/` | Shared MDX: `versions.mdx`, `feature-video.mdx`, `swap-sdk-setup.mdx` |
| `mintlify-docs/assets/` | Images, logos, and feature videos (`videos/<name>.mp4` + `<name>.jpg` poster) |
| `scripts/` | `check-cn-parity.py`, `pin-cn-anchors.py`, `check-sdk-version.sh` |

## Commands

```bash
cd mintlify-docs && mint dev           # local preview on :3000 (npm i -g mint)
cd mintlify-docs && mint broken-links  # internal link check
python scripts/check-cn-parity.py      # en/cn structure, links, anchors
python scripts/pin-cn-anchors.py       # add --apply to write
bash scripts/check-sdk-version.sh      # documented versions vs npm (warns only)
```

Run one `mint dev` at a time: two instances share a cache and serve stale 500s.

## Rules

- **English is the source.** Write the English page first; mirror the change in `cn/` following [TRANSLATION-GUIDE.md](TRANSLATION-GUIDE.md). If the Chinese update is left for later, say so in the PR.
- **Navigation is in `docs.json`, per language.** Adding, moving or removing a page means editing both the `en` and `cn` trees. Moving a page also needs a redirect.
- **Versions live in `snippets/versions.mdx`.** Import them; never hardcode a version number in a page.
- **Describe the current behaviour only.** No "since vX" notes or version matrices in pages; what changed between versions goes in `sdk/changelog.mdx`.
- **`openapi.json` is public.** It is generated from the maker's spec with `/v2/admin/*`, metrics and readiness routes removed. Never add internal routes, hostnames or operator details.
- **Videos** use `<FeatureVideo name="..." />`; the name maps to `assets/videos/<name>.mp4` and its `.jpg` poster. Delete an asset in the same PR that stops referencing it.
- **No secrets, internal hostnames, IPs or private repo links.** This repository is public.
- Commits follow `docs(<section>): <what changed>` or `docs: ...`, written in English.
