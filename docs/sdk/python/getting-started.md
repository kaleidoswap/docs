---
id: getting-started
title: Getting Started
sidebar_position: 2
---

# Getting Started

This guide will help you get up and running with the Kaleidoswap Python SDK.

## Installation

Install the SDK using pip:

```bash
pip install kaleidoswap
```

Or with Poetry:

```bash
poetry add kaleidoswap
```

Or with uv:

```bash
uv add kaleidoswap
```

### Requirements

- Python 3.8 or higher
- No additional dependencies required (the Rust core library is bundled)

## Understanding RGB Assets

Before you start, it's helpful to understand how RGB assets work:

- **name**: The full name of the asset (e.g., "Bitcoin", "Tether USD")
- **ticker**: Abbreviated symbol (e.g., "BTC", "USDT")
- **asset_id**: Unique identifier, usually starts with `rgb:...` for RGB assets

> **Note**: BTC is not an RGB asset - it's the native Bitcoin blockchain coin, so its asset_id is simply `BTC`.

## Basic Setup

### 1. Import the SDK

```python
from kaleidoswap import KaleidoClient, KaleidoConfig
```

### 2. Initialize the Client

```python
# Basic initialization (for market data only)
config = KaleidoConfig(
    base_url="https://api.regtest.kaleidoswap.com"
)
client = KaleidoClient(config)

# Full initialization (for swaps and node operations)
config = KaleidoConfig(
    base_url="https://api.regtest.kaleidoswap.com",
    node_url="http://localhost:3001"  # Your RGB Lightning node
)
client = KaleidoClient(config)
```

### 3. Make Your First API Call

```python
# Get available trading pairs
pairs = client.list_pairs()
print(f"Found {len(pairs)} trading pairs")

for pair in pairs:
    base = pair.base.ticker if pair.base else "?"
    quote = pair.quote.ticker if pair.quote else "?"
    print(f"  {base}/{quote} - Price: {pair.price}")
```

### 4. Get Available Assets

```python
# Get all available assets
assets = client.list_assets()
print(f"Found {len(assets)} assets")

for asset in assets:
    print(f"  {asset.ticker}: {asset.name}")
    print(f"    Precision: {asset.precision}")
    print(f"    Active: {asset.is_active}")
```

## Configuration Options

The `KaleidoConfig` class accepts several parameters:

```python
from kaleidoswap import KaleidoConfig

config = KaleidoConfig(
    # Required: API base URL
    base_url="https://api.regtest.kaleidoswap.com",

    # Optional: Your RGB Lightning Node URL
    # Required for swap execution and node operations
    node_url="http://localhost:3001",

    # Optional: API key for authenticated requests
    api_key=None,

    # Optional: Request timeout in seconds (default: 30.0)
    timeout=30.0,
)
```

## Environment Variables

You can use environment variables for configuration:

```bash
export KALEIDO_API_URL=https://api.regtest.kaleidoswap.com
export KALEIDO_NODE_URL=http://localhost:3001
export KALEIDO_API_KEY=your_api_key_here
```

Then use them in your code:

```python
import os
from kaleidoswap import KaleidoClient, KaleidoConfig

config = KaleidoConfig(
    base_url=os.getenv("KALEIDO_API_URL", "https://api.regtest.kaleidoswap.com"),
    node_url=os.getenv("KALEIDO_NODE_URL"),
    api_key=os.getenv("KALEIDO_API_KEY"),
)
client = KaleidoClient(config)
```

## Available Environments

Kaleidoswap provides different environments for testing and production:

| Environment | API URL |
|-------------|---------|
| **Regtest** | `https://api.regtest.kaleidoswap.com` |
| **Signet** | `https://api.signet.kaleidoswap.com` |
| **Mainnet** | `https://api.kaleidoswap.com` |

## Checking Node Configuration

Before executing swaps, verify that your node is configured:

```python
from kaleidoswap import KaleidoClient, KaleidoConfig

config = KaleidoConfig(
    base_url="https://api.regtest.kaleidoswap.com",
    node_url="http://localhost:3001"
)
client = KaleidoClient(config)

# Check if node is configured
if client.has_node():
    print("✅ Node is configured - can execute swaps")
    
    # Access node operations
    if client.node:
        node_info = client.get_rgb_node_info()
        print(f"Node info: {node_info}")
else:
    print("⚠️  Node not configured - limited to market data only")
```

## Error Handling

Always wrap your API calls in try-except blocks:

```python
from kaleidoswap import KaleidoClient, KaleidoConfig
from kaleidoswap import (
    KaleidoError,
    NetworkError,
    ValidationError,
    APIError,
)

config = KaleidoConfig(base_url="https://api.regtest.kaleidoswap.com")
client = KaleidoClient(config)

try:
    pairs = client.list_pairs()
    print(f"Success: {len(pairs)} pairs found")
except NetworkError as e:
    print(f"Network error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except APIError as e:
    print(f"API error (status {e.status_code}): {e}")
except KaleidoError as e:
    print(f"SDK error: {e}")
```

See the [Error Handling](./error-handling.md) guide for comprehensive error management patterns.

## Complete Example

Here's a complete example that demonstrates initialization, making API calls, and getting a quote:

```python
import os
from kaleidoswap import KaleidoClient, KaleidoConfig
from kaleidoswap import KaleidoError

def get_market_overview():
    """Get an overview of the Kaleidoswap market."""
    
    config = KaleidoConfig(
        base_url=os.getenv("KALEIDO_API_URL", "https://api.regtest.kaleidoswap.com"),
        node_url=os.getenv("KALEIDO_NODE_URL"),
    )
    client = KaleidoClient(config)

    try:
        # Fetch market data
        print("Fetching market data...\n")
        
        pairs = client.list_pairs()
        assets = client.list_assets()

        print(f"📊 Market Overview")
        print(f"   Trading Pairs: {len(pairs)}")
        print(f"   Available Assets: {len(assets)}")

        # Display trading pairs
        print(f"\n💱 Active Trading Pairs:")
        for pair in pairs:
            base = pair.base.ticker if pair.base else "?"
            quote = pair.quote.ticker if pair.quote else "?"
            print(f"   {base}/{quote} - Price: {pair.price}")

        # Get a sample quote
        if pairs:
            pair = pairs[0]
            base_ticker = pair.base.ticker if pair.base else None
            quote_ticker = pair.quote.ticker if pair.quote else None
            
            if base_ticker and quote_ticker:
                pair_ticker = f"{base_ticker}/{quote_ticker}"
                
                # Use a reasonable amount based on limits
                from_amount = 10_000_000  # 10M smallest units
                
                quote = client.get_quote_by_pair(pair_ticker, from_amount=from_amount)
                
                print(f"\n💰 Sample Quote for {pair_ticker}:")
                print(f"   From: {quote.from_asset.amount} {quote.from_asset.ticker}")
                print(f"   To: {quote.to_asset.amount} {quote.to_asset.ticker}")
                print(f"   Price: {quote.price}")
                print(f"   Fee: {quote.fee.final_fee}")

    except KaleidoError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_market_overview()
```

## Next Steps

Now that you have the basics, explore these guides:

- **[API Reference](./api-reference.md)** - Complete method documentation
- **[Types](./types.md)** - Pydantic models and type definitions
- **[Examples](./examples.md)** - Full swap workflows and use cases
- **[Error Handling](./error-handling.md)** - Comprehensive error management
- **[WebSocket](./websocket.md)** - Real-time market data streaming
- **[Utilities](./utilities.md)** - Amount conversion and validation helpers

You're now ready to start building with the Kaleidoswap Python SDK!
