---
id: error-handling
title: Error Handling
sidebar_position: 6
---

# Error Handling

Comprehensive guide to exception handling in the KaleidoSwap Python SDK.

## Overview

The Python SDK provides a rich exception hierarchy for precise error handling. All SDK exceptions inherit from the base `KaleidoError` class, making it easy to catch all SDK-related errors or handle specific cases.

## Exception Hierarchy

```
Exception
└── KaleidoError (base SDK exception)
    ├── NetworkError
    ├── AuthenticationError
    ├── RateLimitError
    ├── ValidationError
    ├── SwapError
    ├── TimeoutError
    ├── WebSocketError
    ├── AssetError
    ├── PairError
    ├── QuoteError
    └── NodeError
```

## Importing Exceptions

```python
from kaleidoswap_sdk.exceptions import (
    KaleidoError,          # Base exception
    NetworkError,          # Network issues
    AuthenticationError,   # Auth problems
    RateLimitError,        # Rate limiting
    ValidationError,       # Invalid input
    SwapError,             # Swap failures
    TimeoutError,          # Operation timeout
    WebSocketError,        # WebSocket issues
    AssetError,            # Asset operations
    PairError,             # Pair operations
    QuoteError,            # Quote operations
    NodeError,             # Node operations
)
```

---

## Exception Reference

### KaleidoError

Base exception for all SDK errors.

**Attributes**:
- `message: str` - Error description
- `status_code: Optional[int]` - HTTP status code (if applicable)
- `response: Optional[Dict[str, Any]]` - API response data (if available)

**Usage**:
```python
try:
    # SDK operation
    pass
except KaleidoError as e:
    print(f"SDK Error: {e.message}")
    if e.status_code:
        print(f"Status code: {e.status_code}")
    if e.response:
        print(f"Response: {e.response}")
```

---

### NetworkError

Raised when network-related issues occur.

**Common Causes**:
- Connection timeout
- DNS resolution failure
- Server unreachable
- SSL/TLS errors

**Example**:
```python
from kaleidoswap_sdk import KaleidoClient
from kaleidoswap_sdk.exceptions import NetworkError

async def handle_network_errors():
    client = KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    )

    try:
        pairs = await client.list_pairs()
    except NetworkError as e:
        print(f"Network error: {e.message}")
        print("Please check your internet connection")
        # Implement retry logic or fallback
    finally:
        await client.close()
```

---

### AuthenticationError

Raised when authentication fails.

**Common Causes**:
- Invalid API key
- Expired credentials
- Missing authentication header

**Example**:
```python
from kaleidoswap_sdk.exceptions import AuthenticationError

try:
    client = KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>",
        api_key="invalid_key"
    )
    await client.list_assets()
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print("Please check your API credentials")
```

---

### RateLimitError

Raised when API rate limits are exceeded.

**Common Causes**:
- Too many requests in short time
- Quota exceeded

**Example**:
```python
import asyncio
from kaleidoswap_sdk.exceptions import RateLimitError

try:
    for i in range(100):
        quote = await client.get_quote("BTC", "USDT", 100000)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    print("Waiting before retry...")
    await asyncio.sleep(60)  # Wait 1 minute
    # Retry operation
```

---

### ValidationError

Raised when input validation fails.

**Common Causes**:
- Invalid parameter format
- Missing required fields
- Out-of-range values

**Example**:
```python
from kaleidoswap_sdk import CreateOrderRequest
from kaleidoswap_sdk.exceptions import ValidationError

try:
    order = await client.create_order(
        CreateOrderRequest(
            rfq_id="",  # Empty string - invalid
            from_amount=-100  # Negative amount - invalid
        )
    )
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print("Please check your input parameters")
```

---

### SwapError

Raised when swap operations fail.

**Common Causes**:
- Insufficient balance
- Expired quote
- Swap already executed
- Invalid swap state

**Example**:
```python
from kaleidoswap_sdk import InitMakerSwapRequest
from kaleidoswap_sdk.exceptions import SwapError

try:
    swap = await client.init_maker_swap(
        InitMakerSwapRequest(
            rfq_id=quote.rfq_id,
            from_asset="BTC",
            to_asset="USDT",
            from_amount=100000,
            to_amount=quote.to_amount
        )
    )
except SwapError as e:
    print(f"Swap failed: {e.message}")
    if "balance" in e.message.lower():
        print("Insufficient balance for swap")
    elif "expired" in e.message.lower():
        print("Quote has expired, request a new one")
```

---

### TimeoutError

Raised when operations take too long.

**Common Causes**:
- Slow network connection
- Server processing delay
- Client timeout configuration

**Example**:
```python
from kaleidoswap_sdk.exceptions import TimeoutError

try:
    # Operation with custom timeout
    final_status = await client.wait_for_swap_completion(
        payment_hash=swap.payment_hash,
        timeout_seconds=60  # Short timeout
    )
except TimeoutError as e:
    print(f"Operation timed out: {e.message}")
    print("You can check the status manually later")
```

---

### WebSocketError

Raised when WebSocket operations fail.

**Common Causes**:
- Connection dropped
- Invalid message format
- WebSocket not connected

**Example**:
```python
from kaleidoswap_sdk.exceptions import WebSocketError

try:
    # Try to use WebSocket before connecting
    await client.get_quote_websocket(
        from_asset="BTC",
        to_asset="USDT",
        amount=100000,
        callback=handler
    )
except WebSocketError as e:
    print(f"WebSocket error: {e.message}")
    print("Connecting to WebSocket...")
    await client.connect()
    # Retry operation
```

---

### AssetError

Raised when asset operations fail.

**Common Causes**:
- Asset not found
- Asset not supported
- Invalid asset ID

**Example**:
```python
from kaleidoswap_sdk.exceptions import AssetError

try:
    assets = await client.list_assets()
except AssetError as e:
    print(f"Asset error: {e.message}")
```

---

### PairError

Raised when trading pair operations fail.

**Common Causes**:
- Pair not found
- Pair not active
- Invalid pair combination

**Example**:
```python
from kaleidoswap_sdk.exceptions import PairError

try:
    pair = await client.get_pair_by_assets("BTC", "INVALID_ASSET")
except PairError as e:
    print(f"Pair error: {e.message}")
    print("This trading pair is not available")
```

---

### QuoteError

Raised when quote operations fail.

**Common Causes**:
- Invalid quote parameters
- Quote expired
- Market conditions changed

**Example**:
```python
from kaleidoswap_sdk.exceptions import QuoteError

try:
    quote = await client.get_quote(
        from_asset="BTC",
        to_asset="USDT",
        amount=0  # Invalid amount
    )
except QuoteError as e:
    print(f"Quote error: {e.message}")
```

---

### NodeError

Raised when node operations fail.

**Common Causes**:
- Node offline
- Node not synchronized
- Invalid node configuration

**Example**:
```python
from kaleidoswap_sdk.exceptions import NodeError

try:
    node_info = await client.get_node_info()
except NodeError as e:
    print(f"Node error: {e.message}")
    print("Please check your node connection")
```

---

## Error Handling Patterns

### Basic Pattern

Catch specific exceptions for precise error handling:

```python
import asyncio
from kaleidoswap_sdk import KaleidoClient
from kaleidoswap_sdk.exceptions import (
    NetworkError,
    ValidationError,
    SwapError,
    KaleidoError,
)

async def safe_swap_operation():
    client = KaleidoClient(
        api_url="https://api.staging.kaleidoswap.com/api/v1",
        node_url="<Your node URL>"
    )

    try:
        # Get quote
        quote = await client.get_quote("BTC", "USDT", 100000)

        # Execute swap
        # ... swap logic

    except NetworkError as e:
        print(f"Network issue: {e.message}")
        # Retry logic
    except ValidationError as e:
        print(f"Invalid input: {e.message}")
        # Fix parameters
    except SwapError as e:
        print(f"Swap failed: {e.message}")
        # Handle swap failure
    except KaleidoError as e:
        print(f"SDK error: {e.message}")
        # Generic error handling
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await client.close()

asyncio.run(safe_swap_operation())
```

### Retry Pattern

Implement automatic retries for transient errors:

```python
import asyncio
from kaleidoswap_sdk.exceptions import NetworkError, TimeoutError

async def get_quote_with_retry(client, max_retries=3):
    """Get quote with automatic retry on network errors."""

    for attempt in range(max_retries):
        try:
            quote = await client.get_quote("BTC", "USDT", 100000)
            return quote

        except (NetworkError, TimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts")
                raise

    return None
```

### Context Manager Pattern

Use context managers for automatic cleanup:

```python
from kaleidoswap_sdk import KaleidoClient
from kaleidoswap_sdk.exceptions import KaleidoError

async def safe_operation():
    """Operation with automatic cleanup."""

    try:
        async with KaleidoClient(
            api_url="https://api.staging.kaleidoswap.com/api/v1",
            node_url="<Your node URL>"
        ) as client:
            # Client automatically closes even if errors occur
            pairs = await client.list_pairs()
            return pairs

    except KaleidoError as e:
        print(f"Error: {e.message}")
        return None
```

### Logging Pattern

Log errors for debugging and monitoring:

```python
import logging
from kaleidoswap_sdk.exceptions import KaleidoError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def operation_with_logging():
    try:
        # SDK operation
        pass
    except KaleidoError as e:
        logger.error(
            "SDK error occurred",
            extra={
                "error_type": type(e).__name__,
                "message": e.message,
                "status_code": e.status_code,
                "response": e.response,
            }
        )
        raise
```

### Graceful Degradation Pattern

Provide fallback behavior when operations fail:

```python
from kaleidoswap_sdk.exceptions import QuoteError

async def get_quote_or_estimate(client):
    """Try to get quote, fall back to estimation if unavailable."""

    try:
        quote = await client.get_quote("BTC", "USDT", 100000)
        return quote.exchange_rate

    except QuoteError:
        # Fallback to historical rate or estimation
        print("Live quote unavailable, using estimated rate")
        return 50000.0  # Fallback rate
```

## Best Practices

### 1. Always Use Specific Exceptions

```python
# Good - catches specific errors
try:
    quote = await client.get_quote("BTC", "USDT", 100000)
except QuoteError as e:
    # Handle quote-specific error
    pass

# Avoid - too broad
try:
    quote = await client.get_quote("BTC", "USDT", 100000)
except Exception as e:
    # Catches everything, hard to debug
    pass
```

### 2. Log Error Details

```python
import logging

logger = logging.getLogger(__name__)

try:
    swap = await client.init_maker_swap(request)
except SwapError as e:
    logger.error(f"Swap initialization failed: {e.message}")
    logger.debug(f"Status code: {e.status_code}")
    logger.debug(f"Response: {e.response}")
```

### 3. Clean Up Resources

```python
client = KaleidoClient(api_url="...", node_url="...")

try:
    # Operations
    pass
except KaleidoError as e:
    # Handle error
    pass
finally:
    # Always close the client
    await client.close()
```

### 4. Provide User-Friendly Messages

```python
try:
    order = await client.create_order(request)
except ValidationError as e:
    # Convert technical error to user-friendly message
    user_message = "Please check your order details and try again"
    print(user_message)
    logger.error(f"Technical details: {e.message}")
```

## Next Steps

- **[Examples](./examples.md)** - See error handling in complete workflows
- **[API Reference](./api-reference.md)** - Learn which exceptions each method can raise
- **[WebSocket](./websocket.md)** - Handle WebSocket-specific errors
