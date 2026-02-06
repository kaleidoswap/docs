---
id: overview
title: SDK Overview
sidebar_position: 0
---

# Kaleidoswap SDK

The official multi-language SDK for interacting with [Kaleidoswap](https://kaleidoswap.com) - a decentralized exchange for Bitcoin and RGB assets on the Lightning Network.

## Architecture

The SDK is built with a **Rust-first architecture**, providing a unified core library with native bindings for multiple languages:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Language Bindings                         │
├───────────────────────┬───────────────────────┬─────────────────┤
│    Python (PyO3)      │   TypeScript (NAPI)   │     Swift       │
│      kaleidoswap      │   @kaleidoswap/sdk    │   (planned)     │
└───────────────────────┴───────────────────────┴─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Rust Library                          │
│                     kaleidoswap-core                            │
├─────────────────────────────────────────────────────────────────┤
│  • 191 auto-generated models from OpenAPI specs                 │
│  • HTTP client with retry and caching                           │
│  • WebSocket client for real-time updates                       │
│  • Comprehensive error handling                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Language Support

| Language | Status | Package | Requirements |
|----------|--------|---------|--------------|
| **Python** | ✅ Ready | `kaleidoswap` | Python 3.8+ |
| **TypeScript** | ✅ Ready | `@kaleidoswap/sdk` | Node.js 18+ |
| **Swift** | 🚧 Planned | - | - |

## Key Features

- 📊 **Market Data** - Assets, trading pairs, and real-time quotes
- 🔄 **Swap Operations** - Atomic swaps on Lightning and on-chain
- 📦 **Order Management** - Order creation, history, and analytics
- ⚡ **LSPS1 Channels** - Lightning channel creation via LSP
- 🔗 **RGB Lightning Node** - Full RGB node integration
- 🛡️ **Type Safe** - Auto-generated models from OpenAPI specs
- 🔧 **Built-in Retry** - Exponential backoff for reliability
- 📡 **WebSocket** - Real-time updates with auto-reconnection

## Sub-Client Architecture

The SDK organizes API operations into sub-clients for better code organization:

```python
# Python
client.market.list_assets()      # Market operations
client.orders.get_order_history() # Order management
client.swaps.init_swap(...)      # Swap execution
client.lsp.get_lsp_info()        # LSP operations
client.node.list_channels()      # RGB Node operations
```

```typescript
// TypeScript
client.market.listAssets();      // Market operations
client.orders.getOrderHistory(); // Order management
client.swaps.initSwap(...);      // Swap execution
client.lsp.getLspInfo();         // LSP operations
client.node.listChannels();      // RGB Node operations
```

## Quick Start

### Python

```bash
pip install kaleidoswap
```

```python
from kaleidoswap import KaleidoClient, KaleidoConfig

config = KaleidoConfig(
    base_url="https://api.regtest.kaleidoswap.com",
    node_url=None,  # Optional: Your RGB Lightning node
)
client = KaleidoClient(config)

# List available assets
assets = client.list_assets()
for asset in assets:
    print(f"{asset.ticker}: {asset.name}")

# Get a quote
quote = client.get_quote_by_pair("BTC/USDT", from_amount=1_000_000)
print(f"Price: {quote.price}")
```

### TypeScript

```bash
pnpm add @kaleidoswap/sdk
```

```typescript
import { KaleidoClient } from '@kaleidoswap/sdk';

const client = new KaleidoClient({
    baseUrl: 'https://api.regtest.kaleidoswap.com',
    nodeUrl: undefined, // Optional: Your RGB Lightning node
});

// List available assets
const assets = await client.listAssets();
assets.forEach(asset => {
    console.log(`${asset.ticker}: ${asset.name}`);
});

// Get a quote
const quote = await client.getQuoteByPair('BTC/USDT', 1_000_000);
console.log(`Price: ${quote.price}`);
```

## API Coverage

| API | Description | Status |
|-----|-------------|--------|
| Market | Assets, pairs, quotes | ✅ Complete |
| Swaps | Atomic swap operations | ✅ Complete |
| Orders | Order creation and management | ✅ Complete |
| LSPS1 | Lightning channel service | ✅ Complete |
| RGB Node | Full RGB Lightning Node API | ✅ Complete |

## Documentation

- **[Python SDK](./python/index.md)** - Full Python documentation
- **[TypeScript SDK](./typescript/index.md)** - Full TypeScript documentation

## Resources

- **[GitHub Repository](https://github.com/kaleidoswap/kaleido-sdk)** - Source code and issues
- **[Telegram Community](https://t.me/kaleidoswap)** - Community support
- **[Website](https://kaleidoswap.com)** - Official website
