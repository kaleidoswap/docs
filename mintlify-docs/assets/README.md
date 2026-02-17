# Assets Directory

Place your branding assets here.

## Required Assets

### Logos
- `logo-dark.svg` - Logo for dark mode (recommended: SVG format)
- `logo-light.svg` - Logo for light mode (recommended: SVG format)
- `favicon.png` - Favicon (recommended: 32x32 or 64x64 PNG)

### Optional Assets
- Images referenced in documentation
- Icons for custom components
- Diagrams and charts

## Specifications

### Logo Requirements
- **Format**: SVG preferred (PNG/JPG also supported)
- **Size**: Height should be 32-40px for best results
- **Background**: Transparent
- **Color**: Ensure good contrast with background

### Favicon Requirements
- **Format**: PNG or ICO
- **Size**: 32x32px or 64x64px
- **Background**: Transparent or solid color

## Usage

Reference assets in documentation:

```mdx
![Architecture Diagram](/assets/architecture.png)
```

Or in mint.json:

```json
{
  "logo": {
    "dark": "/assets/logo-dark.svg",
    "light": "/assets/logo-light.svg"
  },
  "favicon": "/assets/favicon.png"
}
```

## Current Assets

- [ ] logo-dark.svg - **TODO: Add KaleidoSwap dark logo**
- [ ] logo-light.svg - **TODO: Add KaleidoSwap light logo**
- [ ] favicon.png - **TODO: Add KaleidoSwap favicon**
