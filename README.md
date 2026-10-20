# KaleidoSwap Documentation

This repository contains the documentation for KaleidoSwap, built using [Mintlify](https://mintlify.com/).

**Live docs:** [docs.kaleidoswap.com](https://docs.kaleidoswap.com)

## Documentation Structure

All documentation lives in the `mintlify-docs/` directory. Each section below maps to a tab in the docs navigation:

- `whats-kaleidoswap/` - Overview: introduction, quickstart, key features, architecture, glossary
- `desktop-app/` - Desktop App guides: getting started, wallet, channels, trading, KaleidoMind, support
- `extensions/` - Browser extensions (multi-layer wallet for Spark, Arkade and Liquid)
- `sdk/` - KaleidoSDK documentation (`kaleido-sdk`, TypeScript and Python clients)
- `cli/` - KaleidoCLI: local multi-asset Lightning nodes, channels, market and swaps from the terminal
- `ai-tools/` - AI tools: MCP servers, skills, KaleidoAgent and KaleidoMind
- `api-reference/` - API reference and integration guides
- `wallet-engine/` - Multi-protocol wallet engine: concepts and adding a protocol
- `cn/` - Simplified Chinese translation (see [Translations](#translations))
- `snippets/` - Shared MDX snippets, including `versions.mdx` (documented SDK and RLN API versions)
- `assets/` - Images (`assets/images/`) and logos/favicon (`assets/logos/`)

## Configuration

- `mintlify-docs/docs.json` - Mintlify configuration (navigation for both languages, theme, navbar, redirects, API settings)
- `mintlify-docs/openapi.json` - OpenAPI specification for the interactive API playground (shared across languages)

## Translations

English is the default language and lives at the root of `mintlify-docs/`. The Simplified Chinese translation mirrors that tree one-to-one under `mintlify-docs/cn/`, and both are declared under `navigation.languages` in `docs.json`. Adding or removing a page means updating both trees. The Wallet Engine section is currently English-only.

Read [TRANSLATION-GUIDE.md](TRANSLATION-GUIDE.md) before touching `cn/`, and run the parity checks after any change:

```bash
python scripts/check-cn-parity.py
python scripts/pin-cn-anchors.py      # add --apply to write
```

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mint) to preview changes locally:

```bash
npm i -g mint
cd mintlify-docs
mint dev
```

## Version checks

SDK and API versions quoted in the docs are defined once in `mintlify-docs/snippets/versions.mdx`. On every pull request, the `Check SDK version` workflow (`scripts/check-sdk-version.sh`) compares the documented SDK version against the latest `kaleido-sdk` on npm and warns if they have drifted. It never blocks a merge.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes in `mintlify-docs/` (and mirror them in `mintlify-docs/cn/` where relevant)
4. Preview locally with `mint dev`
5. Submit a pull request

## License

[MIT License](LICENSE)
