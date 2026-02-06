---
id: error-handling
title: Error Handling
sidebar_position: 6
---

# Error Handling

The Kaleidoswap Python SDK provides a comprehensive exception hierarchy for handling various error conditions.

## Exception Hierarchy

```
KaleidoError (base)
├── APIError
│   ├── ValidationError
│   ├── AuthenticationError
│   └── RateLimitError
├── NetworkError
├── ResourceNotFoundError
│   ├── AssetNotFoundError
│   ├── TradingPairNotFoundError
│   ├── OrderNotFoundError
│   └── ChannelNotFoundError
├── QuoteExpiredError
├── InsufficientBalanceError
├── NodeNotConfiguredError
├── NodeLockedError
└── LspError
```

## Importing Exceptions

```python
from kaleidoswap import (
    # Base exception
    KaleidoError,
    
    # API errors
    APIError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    
    # Network errors
    NetworkError,
    
    # Resource not found errors
    AssetNotFoundError,
    TradingPairNotFoundError,
    OrderNotFoundError,
    ChannelNotFoundError,
    
    # Business logic errors
    QuoteExpiredError,
    InsufficientBalanceError,
    
    # Node errors
    NodeNotConfiguredError,
    NodeLockedError,
    
    # LSP errors
    LspError,
)
```

## Exception Details

### KaleidoError

Base exception for all SDK errors.

```python
class KaleidoError(Exception):
    """Base exception for all Kaleidoswap SDK errors."""
    pass
```

**Usage:**
```python
try:
    result = client.list_assets()
except KaleidoError as e:
    print(f"SDK error: {e}")
```

---

### APIError

Represents HTTP API errors with status codes.

```python
class APIError(KaleidoError):
    """API request failed with an error response."""
    
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")
```

**Properties:**
- `status_code`: HTTP status code (e.g., 400, 500)
- `message`: Error message from the API

**Usage:**
```python
try:
    quote = client.get_quote_by_pair("BTC/USDT", from_amount=100)
except APIError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
```

---

### ValidationError

Raised when request parameters are invalid.

```python
class ValidationError(APIError):
    """Request validation failed."""
    pass
```

**Common causes:**
- Invalid asset ID or ticker
- Amount outside allowed range
- Missing required parameters

**Example:**
```python
try:
    # Amount too small
    quote = client.get_quote_by_pair("BTC/USDT", from_amount=1)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

### AuthenticationError

Raised when authentication fails.

```python
class AuthenticationError(APIError):
    """Authentication or authorization failed."""
    pass
```

**Common causes:**
- Invalid API key
- Expired credentials
- Insufficient permissions

---

### RateLimitError

Raised when rate limits are exceeded.

```python
class RateLimitError(APIError):
    """Rate limit exceeded."""
    
    def __init__(self, retry_after: Optional[int] = None):
        self.retry_after = retry_after
        message = f"Rate limit exceeded"
        if retry_after:
            message += f", retry after {retry_after}s"
        super().__init__(429, message)
```

**Properties:**
- `retry_after`: Seconds to wait before retrying (if provided)

**Usage:**
```python
import time

try:
    result = client.list_assets()
except RateLimitError as e:
    if e.retry_after:
        print(f"Rate limited, waiting {e.retry_after}s...")
        time.sleep(e.retry_after)
    else:
        time.sleep(60)  # Default wait
```

---

### NetworkError

Raised for network connectivity issues.

```python
class NetworkError(KaleidoError):
    """Network connectivity or request failed."""
    pass
```

**Common causes:**
- Connection refused
- DNS resolution failure
- Request timeout
- SSL/TLS errors

---

### AssetNotFoundError

Raised when a requested asset doesn't exist.

```python
class AssetNotFoundError(ResourceNotFoundError):
    """Asset not found."""
    pass
```

**Usage:**
```python
try:
    asset = client.get_asset_by_ticker("NONEXISTENT")
except AssetNotFoundError:
    print("Asset does not exist")
```

---

### TradingPairNotFoundError

Raised when a trading pair doesn't exist.

```python
class TradingPairNotFoundError(ResourceNotFoundError):
    """Trading pair not found."""
    pass
```

**Usage:**
```python
try:
    pair = client.get_pair_by_ticker("BTC/UNKNOWN")
except TradingPairNotFoundError:
    print("Trading pair does not exist")
```

---

### OrderNotFoundError

Raised when an order doesn't exist.

```python
class OrderNotFoundError(ResourceNotFoundError):
    """Order not found."""
    pass
```

---

### ChannelNotFoundError

Raised when a Lightning channel doesn't exist.

```python
class ChannelNotFoundError(ResourceNotFoundError):
    """Channel not found."""
    pass
```

---

### QuoteExpiredError

Raised when a quote has expired.

```python
class QuoteExpiredError(KaleidoError):
    """Quote has expired and is no longer valid."""
    pass
```

**Common causes:**
- Too much time between getting quote and executing swap
- Market conditions changed

**Usage:**
```python
try:
    result = client.init_swap(old_quote)
except QuoteExpiredError:
    # Get a fresh quote
    new_quote = client.get_quote_by_pair("BTC/USDT", from_amount=amount)
    result = client.init_swap(new_quote)
```

---

### InsufficientBalanceError

Raised when there's not enough balance for an operation.

```python
class InsufficientBalanceError(KaleidoError):
    """Insufficient balance for the operation."""
    
    def __init__(
        self,
        required: int,
        available: int,
        message: Optional[str] = None
    ):
        self.required = required
        self.available = available
        msg = message or f"Insufficient balance: required {required}, available {available}"
        super().__init__(msg)
```

**Properties:**
- `required`: Amount required for the operation
- `available`: Currently available balance

**Usage:**
```python
try:
    result = client.execute_swap(swap_request)
except InsufficientBalanceError as e:
    shortfall = e.required - e.available
    print(f"Need {shortfall} more units")
```

---

### NodeNotConfiguredError

Raised when node operations are attempted without configuration.

```python
class NodeNotConfiguredError(KaleidoError):
    """Node URL not configured."""
    pass
```

**Usage:**
```python
# Always check before node operations
if client.has_node():
    channels = client.list_channels()
else:
    print("Configure node_url to use node operations")
```

---

### NodeLockedError

Raised when the node wallet is locked.

```python
class NodeLockedError(KaleidoError):
    """Node wallet is locked."""
    pass
```

**Usage:**
```python
try:
    balance = client.get_btc_balance()
except NodeLockedError:
    client.unlock_wallet("your_password")
    balance = client.get_btc_balance()
```

---

### LspError

Raised for Lightning Service Provider errors.

```python
class LspError(KaleidoError):
    """LSP operation failed."""
    pass
```

**Common causes:**
- Channel parameters rejected
- Option mismatch with LSP
- LSP unavailable

---

## Error Handling Patterns

### Basic Error Handling

```python
from kaleidoswap import KaleidoClient, KaleidoConfig, KaleidoError

config = KaleidoConfig(base_url="https://api.regtest.kaleidoswap.com")
client = KaleidoClient(config)

try:
    assets = client.list_assets()
except KaleidoError as e:
    print(f"Error: {e}")
```

### Comprehensive Error Handling

```python
from kaleidoswap import (
    KaleidoClient,
    KaleidoConfig,
    KaleidoError,
    APIError,
    NetworkError,
    ValidationError,
    QuoteExpiredError,
    InsufficientBalanceError,
    AssetNotFoundError,
)

def get_quote_safely(client, pair: str, amount: int):
    """Get a quote with comprehensive error handling."""
    
    try:
        return client.get_quote_by_pair(pair, from_amount=amount)
        
    except AssetNotFoundError as e:
        print(f"Asset not found: {e}")
        return None
        
    except ValidationError as e:
        print(f"Invalid parameters: {e}")
        return None
        
    except QuoteExpiredError:
        print("Quote expired, this shouldn't happen for a new quote")
        return None
        
    except NetworkError as e:
        print(f"Network error: {e}")
        # Could implement retry logic here
        return None
        
    except APIError as e:
        print(f"API error ({e.status_code}): {e.message}")
        return None
        
    except KaleidoError as e:
        print(f"SDK error: {e}")
        return None
```

### Retry Pattern

```python
import time
from kaleidoswap import NetworkError, APIError, RateLimitError

def with_retry(func, max_retries=3, base_delay=1.0):
    """Execute with exponential backoff retry."""
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return func()
            
        except RateLimitError as e:
            # Respect rate limit
            wait_time = e.retry_after or (base_delay * 2 ** attempt)
            print(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)
            last_error = e
            
        except NetworkError as e:
            # Retry on network errors
            delay = base_delay * (2 ** attempt)
            print(f"Network error, retry in {delay}s: {e}")
            time.sleep(delay)
            last_error = e
            
        except APIError as e:
            if e.status_code >= 500:
                # Retry on server errors
                delay = base_delay * (2 ** attempt)
                print(f"Server error, retry in {delay}s: {e}")
                time.sleep(delay)
                last_error = e
            else:
                # Don't retry client errors
                raise
    
    # All retries exhausted
    if last_error:
        raise last_error
    return None

# Usage
try:
    result = with_retry(lambda: client.list_assets())
except KaleidoError as e:
    print(f"Failed after retries: {e}")
```

### Context-Specific Error Messages

```python
from kaleidoswap import (
    APIError,
    ValidationError,
    InsufficientBalanceError,
    QuoteExpiredError,
)

def execute_swap_with_feedback(client, quote):
    """Execute swap with user-friendly error messages."""
    
    try:
        return client.complete_swap_from_quote(quote)
        
    except QuoteExpiredError:
        return {
            "success": False,
            "error": "quote_expired",
            "message": "The quote has expired. Please get a new quote.",
            "action": "refresh_quote",
        }
        
    except InsufficientBalanceError as e:
        return {
            "success": False,
            "error": "insufficient_balance",
            "message": f"You need {e.required - e.available} more units.",
            "required": e.required,
            "available": e.available,
            "action": "add_funds",
        }
        
    except ValidationError as e:
        return {
            "success": False,
            "error": "validation_error",
            "message": str(e),
            "action": "check_parameters",
        }
        
    except APIError as e:
        return {
            "success": False,
            "error": "api_error",
            "message": f"An error occurred: {e.message}",
            "status_code": e.status_code,
            "action": "contact_support" if e.status_code >= 500 else "retry",
        }
```

### Logging Errors

```python
import logging
from kaleidoswap import KaleidoError, APIError, NetworkError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kaleidoswap")

def logged_operation(client, operation_name: str, func):
    """Execute operation with logging."""
    
    logger.info(f"Starting {operation_name}")
    
    try:
        result = func()
        logger.info(f"Completed {operation_name}")
        return result
        
    except NetworkError as e:
        logger.error(f"Network error in {operation_name}: {e}")
        raise
        
    except APIError as e:
        logger.error(f"API error in {operation_name}: {e.status_code} - {e.message}")
        raise
        
    except KaleidoError as e:
        logger.error(f"SDK error in {operation_name}: {e}")
        raise

# Usage
try:
    assets = logged_operation(
        client,
        "list_assets",
        client.list_assets
    )
except KaleidoError:
    logger.warning("Operation failed, using cached data")
    assets = cached_assets
```

## Best Practices

1. **Always catch `KaleidoError`** as a fallback to handle unexpected errors
2. **Check `has_node()` before node operations** to avoid `NodeNotConfiguredError`
3. **Handle `QuoteExpiredError`** by getting a fresh quote
4. **Implement retry logic** for `NetworkError` and server errors
5. **Log errors** for debugging and monitoring
6. **Provide user-friendly messages** based on error types
7. **Don't swallow errors silently** - at minimum, log them
