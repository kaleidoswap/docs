# KaleidoSwap Mintlify Documentation

This directory contains the complete KaleidoSwap documentation migrated to Mintlify format.

## 📁 Structure

```
mintlify-docs/
├── mint.json                    # Mintlify configuration
├── whats-kaleidoswap/           # Product overview + background (7 pages)
├── desktop-app/                 # Desktop App Guide (17 pages)
├── web-app/                     # Coming soon placeholders (6 pages)
├── sdk/
│   ├── python/                  # Python SDK docs (8 pages)
│   └── typescript/              # TypeScript SDK docs (10 pages)
├── api-reference/               # API Reference (6 pages)
├── assets/
│   ├── images/                  # overview/, desktop-app/, extension/
│   └── logos/                   # logo variants + favicon
├── openapi.json                 # Source for API auto-generation
├── README.md                    # Contributor guide
└── RESTRUCTURING.md             # Migration summary
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn

### Installation

```bash
# Install Mintlify CLI globally
npm install -g mintlify

# Or with yarn
yarn global add mintlify
```

### Local Development

```bash
# Navigate to mintlify-docs directory
cd mintlify-docs

# Start the Mintlify dev server
mintlify dev
```

The documentation will be available at `http://localhost:3000`

## 📝 Content Overview

### What's KaleidoSwap (7 pages)
✅ Complete – landing pages for product positioning
- `introduction.mdx` - Product overview
- `quickstart.mdx` - High-level onboarding
- `key-features.mdx` - Feature cards and highlights
- `architecture.mdx` - System diagram and data flow
- `background.mdx` - Context migrated from desktop docs
- `glossary.mdx` - Concepts and terminology
- `troubleshooting.mdx` - Common issues at-a-glance

### Desktop App Guide (17 pages)
✅ Restructured into logical subsections
- Getting Started (installation, verification, node hosting)
- Wallet Management (create, initialize, unlock, deposits, withdrawals)
- Channel Operations (open, order, backup, requests)
- Trading (asset swaps)
- Support (settings, FAQ, additional resources)

### Web App (6 pages)
⚠️ Coming Soon placeholders
- Covers introduction, getting started, wallet connection, trading UI, advanced features, and FAQ
- Communicates timelines and directs users to the Desktop App for now

### Python SDK (8 pages)
✅ Complete – Production-ready with 50+ methods
- `index.mdx` - Overview and features
- `getting-started.mdx` - Installation and quick start
- `api-reference.mdx` - Complete API documentation
- `types.mdx` - Pydantic models and enums
- `examples.mdx` - Real-world code examples
- `error-handling.mdx` - Exception handling guide
- `websocket.mdx` - Real-time data streaming
- `utilities.mdx` - Helper functions

### TypeScript SDK (10 pages)
✅ Complete – Well-documented
- `index.mdx` - Overview and features
- `getting-started.mdx` - Installation and setup
- `api-reference.mdx` - API method documentation
- `types.mdx` - Type definitions
- `utilities.mdx` - Utility classes
- `error-handling.mdx` - Error management
- `examples.mdx` - Code examples
- `websocket.mdx` - WebSocket integration
- `best-practices.mdx` - Best practices guide
- `troubleshooting.mdx` - Common issues

### API Reference (6 pages)
✅ Migrated + expanded with OpenAPI
- `introduction.mdx`, `getting-started.mdx`, `error-handling.mdx`
- `rgb-lsps1-apis.mdx`, `market-apis.mdx`, `swap-apis.mdx`
- Automatic endpoint reference generated from `openapi.json`

## 🎨 Customization

### Branding

Update `docs.json` to customize:

```json
{
  "name": "KaleidoSwap Documentation",
  "favicon": "/assets/logos/kaleidoswap-favicon.ico",
  "logo": {
    "dark": "/assets/logos/kaleidoswap-full-logo-horizontal.svg",
    "light": "/assets/logos/kaleidoswap-full-logo-horizontal-onlight.svg"
  },
  "colors": {
    "primary": "#0D9373",
    "light": "#07C983",
    "dark": "#0D9373"
  }
}
```

### Navigation

Edit the `navigation` array in `mint.json` to modify the sidebar structure.

### Analytics

Add your Google Analytics 4 measurement ID:

```json
{
  "analytics": {
    "ga4": {
      "measurementId": "G-YOUR-ID-HERE"
    }
  }
}
```

## 🚢 Deployment

### Deploy to Mintlify

1. Sign up at [https://mintlify.com](https://mintlify.com)
2. Connect your GitHub repository
3. Select the `mintlify-docs` directory as the docs folder
4. Deploy!

### Custom Domain

Configure your custom domain in the Mintlify dashboard:
- `docs.kaleidoswap.com` → Mintlify documentation

### Environment Variables

Set these in your deployment platform:
- `MINTLIFY_API_KEY` - Your Mintlify API key (if using custom deployment)

## 📋 Migration Notes

### From Docusaurus

This documentation was migrated from Docusaurus with the following changes:

1. **File Format**: Changed from `.md` to `.mdx`
2. **Frontmatter**: Simplified to use only `title` and `description`
3. **Navigation**: Moved from `sidebars.js` to `mint.json`
4. **Components**: Enhanced with Mintlify-specific components:
   - `<Card>` and `<CardGroup>` for better visuals
   - `<Steps>` for step-by-step guides
   - `<Accordion>` for collapsible content
   - `<Tabs>` for multi-option content

### Frontmatter Cleanup

Some files may still have old Docusaurus frontmatter fields. To clean up:

```bash
# Remove old fields like 'id' and 'sidebar_position'
find . -name "*.mdx" -exec sed -i '' '/^id:/d; /^sidebar_position:/d' {} \;
```

## 🎯 Best Practices

### Writing Documentation

1. **Use Descriptive Titles**: Clear, concise titles in frontmatter
2. **Add Descriptions**: SEO-friendly descriptions for all pages
3. **Use Components**: Leverage Mintlify components for better UX
4. **Code Examples**: Include runnable code with syntax highlighting
5. **Navigation**: Keep the structure intuitive and logical

### Component Examples

```mdx
<Card title="Quick Start" icon="rocket" href="/quickstart">
  Get started in 5 minutes
</Card>

<Steps>
  <Step title="Install">
    Install the SDK
  </Step>
  <Step title="Configure">
    Set up your configuration
  </Step>
</Steps>

<Accordion title="Advanced Options">
  Additional configuration options...
</Accordion>
```

## 🔧 Troubleshooting

### Build Errors

```bash
# Clear cache and rebuild
mintlify dev --clear-cache
```

### Missing Assets

Ensure logos and images are in the `assets/` directory and referenced correctly in `mint.json`.

### Broken Links

Use relative paths for internal links:
```mdx
[Python SDK](/sdk/python/index)
```

## 📚 Resources

- [Mintlify Documentation](https://mintlify.com/docs)
- [Mintlify Components](https://mintlify.com/docs/components)
- [MDX Documentation](https://mdxjs.com/)

## 🤝 Contributing

To contribute to the documentation:

1. Edit the relevant `.mdx` file
2. Test locally with `mintlify dev`
3. Submit a pull request

## 📞 Support

- **Mintlify Support**: support@mintlify.com
- **KaleidoSwap Team**: support@kaleidoswap.com
- **Community**: [Telegram](https://t.me/kaleidoswap)

## 📄 License

Documentation is licensed under the MIT License, same as KaleidoSwap.

---

**Migration Date**: 2025-11-16
**Total Pages**: 54
**Status**: ✅ Complete

---

## ✨ Recent Updates (2025-11-16)

### Documentation Restructured

The documentation has been completely reorganized into 5 main sections:

1. **What's KaleidoSwap** - Product overview, architecture, features
2. **Desktop App** - Organized into 5 logical subsections
3. **Web App** - Placeholder documentation (Coming Soon)
4. **SDK** - Python and TypeScript SDKs
5. **API Reference** - Enhanced with OpenAPI auto-generation

**Key Improvements**:
- ✅ Better navigation with hierarchical structure
- ✅ OpenAPI integration for automatic API documentation
- ✅ 11 new pages added (5 What's KaleidoSwap + 6 Web App)
- ✅ Desktop App organized into logical subsections
- ✅ Cleaner, more professional structure

See [RESTRUCTURING.md](./RESTRUCTURING.md) for detailed changes.
