---
id: index
title: Python SDK
sidebar_position: 1
---

# Kaleidoswap Python SDK

The official Python SDK for Kaleidoswap - a decentralized exchange for Bitcoin and RGB assets on the Lightning Network.

## Overview

The Kaleidoswap Python SDK provides native Python bindings to the Rust core library via PyO3. This means you get the performance of Rust with the convenience of Python, including fully typed Pydantic models for all API responses.

## Key Features

- 🐍 **Native Python** - PyO3 bindings for native performance
- 📊 **Type Safe** - Auto-generated Pydantic models from OpenAPI specs
- 🏗️ **Sub-client Architecture** - Organized API access via `client.market`, `client.orders`, etc.
- 🛡️ **Robust Error Handling** - Comprehensive exception hierarchy
- 📡 **WebSocket Support** - Real-time quote streaming
- 🔧 **Built-in Utilities** - Amount conversion, asset lookup, and validation

## Installation

```bash
pip install kaleidoswap
```

### Requirements

- Python 3.8 or higher
- No additional dependencies required (Rust core is bundled)

## Quick Start

```python
from kaleidoswap import KaleidoClient, KaleidoConfig

# Initialize client
config = KaleidoConfig(
    base_url="https://api.regtest.kaleidoswap.com"
)
client = KaleidoClient(config)

# List available assets
assets = client.list_assets()
print(f"Found {len(assets)} assets")

for asset in assets:
    print(f"  {asset.ticker}: {asset.name}")

# Get a quote for a swap
quote = client.get_quote_by_pair("BTC/USDT", from_amount=1_000_000)
print(f"Quote: {quote.from_asset.amount} {quote.from_asset.ticker}")
print(f"    -> {quote.to_asset.amount} {quote.to_asset.ticker}")
print(f"Price: {quote.price}")
```

## Sub-Client Architecture

The SDK organizes API operations into domain-specific sub-clients:

```python
# Market operations
assets = client.market.list_assets()
pairs = client.market.list_pairs()
quote = client.market.get_quote_by_pair("BTC/USDT", from_amount=1_000_000)

# Order management
history = client.orders.get_order_history()
status = client.orders.get_swap_order_status("order-id")

# Swap operations
result = client.swaps.init_swap(request)

# LSP operations
info = client.lsp.get_lsp_info()

# RGB Node operations (if configured)
if client.node:
    channels = client.node.list_channels()
    balance = client.node.get_btc_balance()
```

## Configuration

```python
from kaleidoswap import KaleidoClient, KaleidoConfig

config = KaleidoConfig(
    # Required: API base URL
    base_url="https://api.regtest.kaleidoswap.com",
    
    # Optional: Your RGB Lightning Node URL (for swap execution)
    node_url="http://localhost:3001",
    
    # Optional: API key for authenticated requests
    api_key=None,
    
    # Optional: Request timeout in seconds (default: 30.0)
    timeout=30.0,
)

client = KaleidoClient(config)
```

## Error Handling

The SDK provides a comprehensive exception hierarchy:

```python
from kaleidoswap import (
    KaleidoError,
    APIError,
    NetworkError,
    ValidationError,
    QuoteExpiredError,
    InsufficientBalanceError,
    NodeNotConfiguredError,
)

try:
    quote = client.get_quote_by_pair("BTC/USDT", from_amount=1_000_000)
except QuoteExpiredError:
    print("Quote has expired, getting a fresh one")
except InsufficientBalanceError as e:
    print(f"Insufficient balance: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
except KaleidoError as e:
    print(f"SDK error: {e}")
```

## Documentation Structure

- **[Getting Started](./getting-started.md)** - Installation and configuration
- **[API Reference](./api-reference.md)** - Complete method documentation
- **[Types](./types.md)** - Pydantic models and type definitions
- **[Examples](./examples.md)** - Complete code examples
- **[Error Handling](./error-handling.md)** - Exception types and patterns
- **[WebSocket](./websocket.md)** - Real-time streaming
- **[Utilities](./utilities.md)** - Helper functions

## Support

- 📚 [API Documentation](./api-reference.md)
- 💬 [Telegram Community](https://t.me/kaleidoswap/)
- 📧 [Contact Support](mailto:support@kaleidoswap.com)
- 🐛 [Report Issues](https://github.com/kaleidoswap/kaleido-sdk/issues)

## License

This SDK is released under the MIT License.
