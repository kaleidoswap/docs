# KaleidoSwap Documentation

This repository contains the documentation for KaleidoSwap, built using [Mintlify](https://mintlify.com/).

## Documentation Structure

All documentation lives in the `mintlify-docs/` directory:

- `whats-kaleidoswap/` - Introduction, architecture, and core concepts
- `desktop-app/` - Desktop application guides and tutorials
- `web-app/` - Web application documentation
- `sdk/` - SDK documentation (Python & TypeScript)
- `api-reference/` - API reference and integration guides
- `images/` - Screenshot and diagram assets
- `assets/` - Logos and favicon

## Configuration

- `docs.json` - Mintlify configuration (navigation, theme, analytics, API settings)
- `openapi.json` - OpenAPI specification for interactive API playground

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mintlify) to preview changes locally:

```bash
npm i -g mintlify
cd mintlify-docs
mintlify dev
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes in `mintlify-docs/`
4. Preview locally with `mintlify dev`
5. Submit a pull request

## License

[MIT License](LICENSE)
