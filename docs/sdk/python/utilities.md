---
id: utilities
title: Utilities
sidebar_position: 8
---

# Utilities

Helper functions and patterns for working with the KaleidoSwap Python SDK.

## Precision Handling

### Converting Between Units

RGB assets use atomic units with varying precision. Here's how to convert:

```python
def atomic_to_decimal(atomic_amount: int, precision: int) -> float:
    """Convert atomic units to decimal representation."""
    return atomic_amount / (10 ** precision)

def decimal_to_atomic(decimal_amount: float, precision: int) -> int:
    """Convert decimal amount to atomic units."""
    return int(decimal_amount * (10 ** precision))

# Usage
btc_atomic = 100000000  # 1 BTC in satoshis
btc_decimal = atomic_to_decimal(btc_atomic, 8)  # 1.0 BTC
print(f"{btc_atomic} sats = {btc_decimal} BTC")

# Convert back
amount = 0.001  # 0.001 BTC
atomic = decimal_to_atomic(amount, 8)  # 100,000 sats
```

### Asset Precision Helper

```python
from kaleidoswap_sdk import KaleidoClient

class AssetPrecisionHelper:
    """Helper for managing asset precision conversions."""

    def __init__(self, assets):
        self.precision_map = {
            asset.ticker: asset.precision
            for asset in assets
        }

    def to_atomic(self, ticker: str, amount: float) -> int:
        """Convert decimal amount to atomic units."""
        precision = self.precision_map.get(ticker, 8)
        return int(amount * (10 ** precision))

    def to_decimal(self, ticker: str, atomic_amount: int) -> float:
        """Convert atomic units to decimal amount."""
        precision = self.precision_map.get(ticker, 8)
        return atomic_amount / (10 ** precision)

# Usage
async def use_precision_helper():
    async with KaleidoClient(...) as client:
        assets = await client.list_assets()
        helper = AssetPrecisionHelper(assets.assets)

        # Convert 1.5 USDT to atomic units
        usdt_atomic = helper.to_atomic("USDT", 1.5)
        print(f"1.5 USDT = {usdt_atomic} atomic units")

        # Convert back
        usdt_decimal = helper.to_decimal("USDT", usdt_atomic)
        print(f"{usdt_atomic} atomic = {usdt_decimal} USDT")
```

## Asset ID Resolution

### Ticker to Asset ID Mapper

```python
from typing import Dict
from kaleidoswap_sdk import KaleidoClient

class AssetMapper:
    """Map between tickers and asset IDs."""

    def __init__(self, assets):
        self.ticker_to_id: Dict[str, str] = {}
        self.id_to_ticker: Dict[str, str] = {}

        for asset in assets:
            self.ticker_to_id[asset.ticker] = asset.asset_id
            self.id_to_ticker[asset.asset_id] = asset.ticker

    def get_asset_id(self, ticker: str) -> str:
        """Get asset ID from ticker."""
        return self.ticker_to_id.get(ticker, ticker)

    def get_ticker(self, asset_id: str) -> str:
        """Get ticker from asset ID."""
        return self.id_to_ticker.get(asset_id, asset_id)

# Usage
async def use_asset_mapper():
    async with KaleidoClient(...) as client:
        assets = await client.list_assets()
        mapper = AssetMapper(assets.assets)

        # Get asset ID from ticker
        usdt_id = mapper.get_asset_id("USDT")
        print(f"USDT asset ID: {usdt_id}")

        # Get ticker from asset ID
        ticker = mapper.get_ticker(usdt_id)
        print(f"Asset ticker: {ticker}")

        # Use in quote request
        quote = await client.get_quote(
            from_asset="BTC",
            to_asset=mapper.get_asset_id("USDT"),
            amount=100000
        )
```

## Retry Utilities

### Simple Retry Decorator

```python
import asyncio
from functools import wraps
from typing import Type, Tuple

def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Retry decorator for async functions."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise

                    print(f"Attempt {attempt} failed: {e}")
                    print(f"Retrying in {current_delay}s...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

# Usage
from kaleidoswap_sdk.exceptions import NetworkError, TimeoutError

@async_retry(max_attempts=3, delay=2.0, exceptions=(NetworkError, TimeoutError))
async def get_quote_with_retry(client):
    """Get quote with automatic retry."""
    return await client.get_quote("BTC", "USDT", 100000)
```

## Context Managers

### Custom Context Manager for Operations

```python
from contextlib import asynccontextmanager
from kaleidoswap_sdk import KaleidoClient

@asynccontextmanager
async def kaleido_session(api_url: str, node_url: str):
    """Context manager for KaleidoSwap operations."""
    client = KaleidoClient(api_url=api_url, node_url=node_url)

    try:
        yield client
    finally:
        await client.close()

# Usage
async def main():
    async with kaleido_session(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    ) as client:
        pairs = await client.list_pairs()
        print(f"Found {len(pairs.pairs)} pairs")
```

## Validation Helpers

### Amount Validation

```python
def validate_swap_amount(
    amount: int,
    min_amount: int,
    max_amount: int,
    asset_name: str = "asset"
) -> None:
    """Validate swap amount is within limits."""
    if amount < min_amount:
        raise ValueError(
            f"{asset_name} amount {amount} below minimum {min_amount}"
        )
    if amount > max_amount:
        raise ValueError(
            f"{asset_name} amount {amount} exceeds maximum {max_amount}"
        )

# Usage
async def create_validated_order(client, pair):
    amount = 100000

    # Validate amount
    validate_swap_amount(
        amount=amount,
        min_amount=pair.min_base_order_size,
        max_amount=pair.max_base_order_size,
        asset_name=pair.base_asset
    )

    # Proceed with order
    quote = await client.get_quote(
        from_asset=pair.base_asset,
        to_asset=pair.quote_asset,
        amount=amount
    )
```

## Data Formatting

### Format Asset Balance

```python
def format_balance(balance: int, precision: int, ticker: str) -> str:
    """Format asset balance for display."""
    decimal_balance = balance / (10 ** precision)
    return f"{decimal_balance:,.{precision}f} {ticker}"

# Usage
async def display_balances(client):
    assets = await client.list_assets()

    print("Asset Balances:")
    for asset in assets.assets:
        if asset.balance.spendable > 0:
            formatted = format_balance(
                balance=asset.balance.spendable,
                precision=asset.precision,
                ticker=asset.ticker
            )
            print(f"  {formatted}")
```

### Format Quote Output

```python
from datetime import datetime

def format_quote(quote, from_ticker: str, to_ticker: str) -> str:
    """Format quote for human-readable display."""
    from_amount = quote.from_amount
    to_amount = quote.to_amount
    rate = quote.exchange_rate

    return (
        f"Quote:\n"
        f"  From: {from_amount} {from_ticker}\n"
        f"  To: {to_amount} {to_ticker}\n"
        f"  Rate: {rate:,.2f}\n"
        f"  Expires: {datetime.fromtimestamp(quote.expires_at)}"
    )

# Usage
async def get_and_display_quote(client):
    quote = await client.get_quote("BTC", "USDT", 100000)
    print(format_quote(quote, "BTC", "USDT"))
```

## Environment Configuration

### Configuration Manager

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class KaleidoConfig:
    """Configuration for KaleidoSwap SDK."""

    api_url: str
    node_url: str
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'KaleidoConfig':
        """Load configuration from environment variables."""
        return cls(
            api_url=os.getenv(
                "KALEIDO_API_URL",
                "https://api.staging.kaleidoswap.com/api/v1"
            ),
            node_url=os.getenv("KALEIDO_NODE_URL", ""),
            api_key=os.getenv("KALEIDO_API_KEY")
        )

# Usage
from kaleidoswap_sdk import KaleidoClient

async def main():
    config = KaleidoConfig.from_env()

    async with KaleidoClient(
        api_url=config.api_url,
        node_url=config.node_url,
        api_key=config.api_key
    ) as client:
        # Operations
        pass
```

## Logging Utilities

### Structured Logging

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logger for KaleidoSwap operations."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log_quote(self, quote, level=logging.INFO):
        """Log quote with structured data."""
        self.logger.log(
            level,
            json.dumps({
                "event": "quote_received",
                "timestamp": datetime.utcnow().isoformat(),
                "rfq_id": quote.rfq_id,
                "rate": quote.exchange_rate,
                "from_asset": quote.from_asset,
                "to_asset": quote.to_asset,
            })
        )

    def log_swap(self, swap_status, level=logging.INFO):
        """Log swap status with structured data."""
        self.logger.log(
            level,
            json.dumps({
                "event": "swap_status",
                "timestamp": datetime.utcnow().isoformat(),
                "payment_hash": swap_status.payment_hash,
                "status": swap_status.status,
            })
        )

# Usage
logger = StructuredLogger(__name__)

async def monitored_swap(client):
    quote = await client.get_quote("BTC", "USDT", 100000)
    logger.log_quote(quote)

    # Execute swap
    # ...

    logger.log_swap(swap_status)
```

## Next Steps

- **[Examples](./examples.md)** - See utilities in action
- **[API Reference](./api-reference.md)** - Complete method documentation
- **[Types](./types.md)** - Understanding data models
