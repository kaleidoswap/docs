---
id: getting-started
title: Getting Started
sidebar_position: 2
---

# Getting Started

This guide will help you get up and running with the KaleidoSwap Python SDK.

## Installation

Install the SDK using pip:

```bash
pip install kaleidoswap-sdk
```

Or with Poetry:

```bash
poetry add kaleidoswap-sdk
```

### Requirements

- Python 3.11 or higher
- Dependencies will be automatically installed:
  - `httpx` - Modern HTTP client
  - `websockets` - WebSocket support
  - `aiohttp` - Async HTTP operations
  - `pydantic` - Data validation and type safety

## Understanding RGB Assets

Before you start, it's helpful to understand how RGB assets work:

- **name**: The full name of the asset (e.g., "Bitcoin", "Tether USD")
- **ticker**: Abbreviated symbol (e.g., "BTC", "USDT")
- **asset_id**: Unique identifier for verification, usually starts with `rgb:x...`

> **Note**: BTC is not an RGB asset - it's the native Bitcoin blockchain coin, so its asset_id remains as `BTC`.

## Basic Setup

### 1. Import the SDK

```python
import asyncio
from kaleidoswap_sdk import KaleidoClient
```

### 2. Initialize the Client

```python
# Basic initialization
client = KaleidoClient(
    api_url="https://api.staging.kaleidoswap.com/api/v1",
    node_url="<Address of your RGB Lightning node>"
)
```

> **Important**: The Python SDK requires both `api_url` and `node_url` parameters. More configuration options are covered later in this page.

### 3. Make Your First API Call

```python
async def main():
    # Get available trading pairs
    pairs = await client.list_pairs()
    print(f"Found {len(pairs.pairs)} trading pairs")

    # Remember to close the client when done
    await client.close()

# Run the async function
asyncio.run(main())
```

<details>
  <summary>
    Available Pairs:
  </summary>

  ```json
  {
    "pairs": [
      {
        "id": "30302cec-6a8e-4951-ba0a-2f5bf451979e",
        "base_asset": "BTC",
        "base_asset_id": "BTC",
        "base_precision": 11,
        "quote_asset": "USDT",
        "quote_asset_id": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
        "quote_precision": 6,
        "is_active": true,
        "min_base_order_size": 1000000,
        "max_base_order_size": 1000000000,
        "min_quote_order_size": 2000000,
        "max_quote_order_size": 1000000000
      },
      {
        "id": "47b20cf2-1268-4866-bf54-4556e6f49b37",
        "base_asset": "BTC",
        "base_asset_id": "BTC",
        "base_precision": 11,
        "quote_asset": "XAUT",
        "quote_asset_id": "rgb:7r5InPtB-PpkGVrA-h3vW_tB-bN3NVki-Nrj4trt-rlG42ng",
        "quote_precision": 9,
        "is_active": true,
        "min_base_order_size": 1000000,
        "max_base_order_size": 1000000000,
        "min_quote_order_size": 1000000,
        "max_quote_order_size": 1000000000
      }
    ]
  }
  ```
</details>

```python
async def main():
    client = KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    )

    try:
        # Get available assets
        assets = await client.list_assets()
        print(f"Found {len(assets.assets)} assets")
    finally:
        await client.close()

asyncio.run(main())
```

<details>
  <summary>
    Available Assets:
  </summary>

  ```json
  {
    "assets": [
      {
        "asset_id": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
        "ticker": "USDT",
        "name": "Tether USD",
        "details": null,
        "precision": 6,
        "issued_supply": 1000000000000000,
        "timestamp": 1759944618,
        "added_at": 1759944618,
        "balance": {
          "settled": 999999979729794,
          "future": 999999979729794,
          "spendable": 999999979729794,
          "offchain_outbound": 0,
          "offchain_inbound": 0
        },
        "media": null,
        "asset_iface": null,
        "is_active": true
      },
      {
        "asset_id": "rgb:7r5InPtB-PpkGVrA-h3vW_tB-bN3NVki-Nrj4trt-rlG42ng",
        "ticker": "XAUT",
        "name": "Tether Gold",
        "details": null,
        "precision": 9,
        "issued_supply": 1000000000000000,
        "timestamp": 1759944619,
        "added_at": 1759944619,
        "balance": {
          "settled": 999999750000000,
          "future": 999999750000000,
          "spendable": 999999750000000,
          "offchain_outbound": 249411646,
          "offchain_inbound": 588354
        },
        "media": null,
        "asset_iface": null,
        "is_active": true
      }
    ],
    "network": "regtest",
    "timestamp": 1760053210
  }
  ```
</details>

## Configuration Options

The `KaleidoClient` class accepts several configuration parameters:

```python
from kaleidoswap_sdk import KaleidoClient

client = KaleidoClient(
    # Required: API base URL
    api_url="https://api.staging.kaleidoswap.com/api/v1",

    # Required: Your RGB Lightning Node URL
    node_url="<Your node URL>",

    # Optional: API key for authenticated requests (future use)
    api_key=None,

    # Optional: WebSocket configuration
    ping_interval=30,        # WebSocket ping interval in seconds
    ping_timeout=10,          # WebSocket ping timeout in seconds
    close_timeout=10,         # WebSocket close timeout in seconds
    max_size=2**20,           # Maximum message size (1MB)
    max_queue=32,             # Maximum message queue size
    compression=None          # Optional compression method
)
```

## Environment Variables

You can use environment variables for configuration:

```bash
# Set the API URL
export KALEIDO_API_URL=https://api.staging.kaleidoswap.com/api/v1

# Set the node URL
export KALEIDO_NODE_URL=<Your node URL>

# Optional: Set API key
export KALEIDO_API_KEY=your_api_key_here
```

Then use them in your code:

```python
import os
from kaleidoswap_sdk import KaleidoClient

client = KaleidoClient(
    api_url=os.getenv("KALEIDO_API_URL"),
    node_url=os.getenv("KALEIDO_NODE_URL"),
    api_key=os.getenv("KALEIDO_API_KEY")
)
```

## Available Nodes

KaleidoSwap provides different environments for testing and production:

- **Staging**: `https://api.staging.kaleidoswap.com/api/v1`
- **Regtest**: `https://api.regtest.kaleidoswap.com/api/v1`
- **Signet**: `https://api.signet.kaleidoswap.com/api/v1`

## Using Async Context Manager

The recommended way to use the client is with an async context manager, which automatically handles cleanup:

```python
import asyncio
from kaleidoswap_sdk import KaleidoClient

async def main():
    async with KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    ) as client:
        # Client is automatically closed when exiting this block
        pairs = await client.list_pairs()
        print(f"Found {len(pairs.pairs)} trading pairs")

asyncio.run(main())
```

## Error Handling

Always wrap your API calls in try-except blocks to handle errors gracefully:

```python
from kaleidoswap_sdk import KaleidoClient
from kaleidoswap_sdk.exceptions import (
    KaleidoException,
    NetworkError,
    ValidationError
)

async def main():
    client = KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    )

    try:
        pairs = await client.list_pairs()
        print(f"Success: {len(pairs.pairs)} pairs found")
    except NetworkError as e:
        print(f"Network error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except KaleidoException as e:
        print(f"API error: {e}")
    finally:
        await client.close()

asyncio.run(main())
```

See the [Error Handling](./error-handling.md) guide for comprehensive error management patterns.

## Complete Example

Here's a complete example that demonstrates initialization, making API calls, and proper cleanup:

```python
import asyncio
import os
from kaleidoswap_sdk import KaleidoClient
from kaleidoswap_sdk.exceptions import KaleidoException

async def get_market_overview():
    """Get an overview of the KaleidoSwap market."""

    client = KaleidoClient(
        api_url=os.getenv("KALEIDO_API_URL", "https://api.staging.kaleidoswap.com/api/v1"),
        node_url=os.getenv("KALEIDO_NODE_URL")
    )

    try:
        # Fetch market data
        print("Fetching market data...")

        pairs = await client.list_pairs()
        assets = await client.list_assets()

        print(f"\n📊 Market Overview")
        print(f"Trading Pairs: {len(pairs.pairs)}")
        print(f"Available Assets: {len(assets.assets)}")

        # Display trading pairs
        print(f"\n💱 Active Trading Pairs:")
        for pair in pairs.pairs:
            if pair.is_active:
                print(f"  - {pair.base_asset}/{pair.quote_asset}")

        # Get a sample quote
        if pairs.pairs:
            pair = pairs.pairs[0]
            quote = await client.get_quote(
                from_asset=pair.base_asset_id,
                to_asset=pair.quote_asset_id,
                amount=pair.min_base_order_size
            )
            print(f"\n💰 Sample Quote:")
            print(f"  {pair.base_asset} → {pair.quote_asset}")
            print(f"  Rate: {quote.exchange_rate}")

    except KaleidoException as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(get_market_overview())
```

## Next Steps

Now that you have the basics, explore these guides:

- **[API Reference](./api-reference.md)** - Complete method documentation
- **[Types](./types.md)** - Pydantic models and type definitions
- **[Examples](./examples.md)** - Full swap workflows and use cases
- **[Error Handling](./error-handling.md)** - Comprehensive error management
- **[WebSocket](./websocket.md)** - Real-time market data streaming

You're now ready to start building with the KaleidoSwap Python SDK!
