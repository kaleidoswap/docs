# Error Handling

The KaleidoSwap SDK provides a comprehensive error handling system designed to help you build robust applications. This guide covers error types, handling strategies, and best practices for dealing with various failure scenarios.

## Introduction

The SDK features a hierarchical error system with enhanced metadata, automatic retry strategies, and user-friendly error messages. All errors extend from `KaleidoSDKError` and include detailed context for debugging and recovery.

```typescript
import { 
  KaleidoClient,
  NetworkError,
  AuthenticationError,
  ValidationError,
  SwapError,
  ErrorFactory
} from '@kaleidoswap/sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});
```

## Error Types

### Error Hierarchy

The SDK uses a structured error hierarchy with specific error classes for different scenarios:

| Error Class | Purpose | Category | Retryable |
|-------------|---------|----------|-----------|
| `KaleidoSDKError` | Base error class | - | Varies |
| `NetworkError` | Network connectivity issues | Network | Yes |
| `AuthenticationError` | API key and auth problems | Authentication | No |
| `ValidationError` | Invalid request data | Validation | No |
| `SwapError` | Trading and swap failures | Trading | Varies |
| `AssetError` | Asset-related issues | Business Logic | No |
| `PairError` | Trading pair problems | Business Logic | No |
| `QuoteError` | Quote generation failures | Business Logic | Varies |
| `TimeoutError` | Operation timeouts | Network | Yes |
| `WebSocketError` | WebSocket connection issues | Network | Yes |
| `HttpError` | HTTP response errors | HTTP | Varies |
| `ConfigurationError` | Client configuration issues | Configuration | No |
| `NodeError` | Lightning node problems | Lightning Network | Varies |
| `RateLimitError` | Rate limiting violations | Rate Limiting | Yes |

### Error Codes

Each error includes a specific error code for programmatic handling:

```typescript
import { ErrorCode } from '@kaleidoswap/sdk';

// Network errors (1000-1099)
ErrorCode.NETWORK_UNREACHABLE
ErrorCode.CONNECTION_TIMEOUT
ErrorCode.WEBSOCKET_CONNECTION_FAILED

// HTTP errors (1100-1199)
ErrorCode.HTTP_UNAUTHORIZED
ErrorCode.HTTP_NOT_FOUND
ErrorCode.HTTP_INTERNAL_SERVER_ERROR

// Validation errors (1300-1399)
ErrorCode.VALIDATION_INVALID_AMOUNT
ErrorCode.VALIDATION_INVALID_ASSET_ID

// Trading errors (1500-1599)
ErrorCode.SWAP_FAILED
ErrorCode.SWAP_INSUFFICIENT_BALANCE
ErrorCode.INSUFFICIENT_LIQUIDITY
```

## Error Response Format

All SDK errors follow a consistent structure with enhanced metadata:

```typescript
interface KaleidoSDKError {
  name: string;           // Error class name
  message: string;        // Human-readable description
  code: ErrorCode;        // Specific error code
  category: ErrorCategory; // Error category
  severity: ErrorSeverity; // Error severity level
  metadata: {
    statusCode?: number;     // HTTP status code
    response?: any;          // Raw server response
    requestData?: any;       // Original request data
    timestamp: Date;         // Error occurrence time
    requestId?: string;      // Request tracking ID
    retryable: boolean;      // Whether retry is recommended
    retryStrategy: string;   // Suggested retry approach
    retryDelay?: number;     // Recommended retry delay
    maxRetries?: number;     // Maximum retry attempts
    recoveryActions?: string[]; // Suggested recovery steps
  };
  cause?: Error;          // Original underlying error
}
```

## Common Error Scenarios

### Network Connectivity Issues

```typescript
try {
  const pairs = await client.pairList();
} catch (error) {
  if (error instanceof NetworkError) {
    console.error('Network issue:', error.getUserMessage());
    
    // Check if retryable
    if (error.isRetryable()) {
      console.log('Retry strategy:', error.getRetryStrategy());
      console.log('Retry delay:', error.metadata.retryDelay);
    }
    
    // Handle specific network codes
    switch (error.code) {
      case ErrorCode.NETWORK_UNREACHABLE:
        showOfflineMessage();
        break;
      case ErrorCode.CONNECTION_TIMEOUT:
        retryWithBackoff();
        break;
    }
  }
}
```

### Authentication Failures

```typescript
try {
  const quote = await client.quoteRequest('BTC', 'USDT', 100000);
} catch (error) {
  if (error instanceof AuthenticationError) {
    switch (error.code) {
      case ErrorCode.AUTH_INVALID_API_KEY:
        redirectToLogin();
        break;
      case ErrorCode.AUTH_EXPIRED_API_KEY:
        refreshApiKey();
        break;
      case ErrorCode.AUTH_INSUFFICIENT_PERMISSIONS:
        showPermissionError();
        break;
    }
  }
}
```

### Validation Errors

```typescript
try {
  const swap = await client.initMakerSwap({
    rfq_id: 'invalid-id',
    from_asset: 'BTC',
    to_asset: 'USDT',
    from_amount: -100, // Invalid negative amount
    to_amount: 45000
  });
} catch (error) {
  if (error instanceof ValidationError) {
    // Show specific validation messages
    const field = extractFieldFromError(error.message);
    showFieldError(field, error.getUserMessage());
    
    // Get recovery suggestions
    if (error.metadata.recoveryActions) {
      showRecoverySuggestions(error.metadata.recoveryActions);
    }
  }
}
```

### Trading and Swap Errors

```typescript
try {
  const swapResult = await client.executeMakerSwap({
    swapstring: 'swap-data...',
    payment_hash: 'hash123',
    taker_pubkey: 'pubkey456'
  });
} catch (error) {
  if (error instanceof SwapError) {
    switch (error.code) {
      case ErrorCode.SWAP_INSUFFICIENT_BALANCE:
        showInsufficientBalanceError();
        break;
      case ErrorCode.SWAP_SLIPPAGE_EXCEEDED:
        offerSlippageAdjustment();
        break;
      case ErrorCode.INSUFFICIENT_LIQUIDITY:
        suggestAlternativePairs();
        break;
      case ErrorCode.SWAP_TIMEOUT:
        // This is retryable
        if (error.isRetryable()) {
          scheduleRetry();
        }
        break;
    }
  }
}
```

## Error Handling Best Practices

### 1. Use Type-Safe Error Handling

Always check error types using `instanceof` for proper TypeScript support:

```typescript
try {
  await performTradingOperation();
} catch (error) {
  if (error instanceof NetworkError) {
    handleNetworkError(error);
  } else if (error instanceof SwapError) {
    handleSwapError(error);
  } else if (error instanceof KaleidoSDKError) {
    handleGenericSDKError(error);
  } else {
    handleUnknownError(error);
  }
}
```

### 2. Implement Graceful Degradation

```typescript
async function getAssetData(assetId: string) {
  try {
    return await client.getAssetMetadata(assetId);
  } catch (error) {
    if (error instanceof AssetError) {
      // Fallback to basic asset info
      console.warn('Asset metadata unavailable, using basic info');
      return getBasicAssetInfo(assetId);
    }
    throw error; // Re-throw unexpected errors
  }
}
```

### 3. Use Error Context for Debugging

```typescript
try {
  await client.initMakerSwap(swapRequest);
} catch (error) {
  if (error instanceof KaleidoSDKError) {
    // Log detailed error context
    console.error('Swap failed:', {
      code: error.code,
      category: error.category,
      severity: error.severity,
      requestData: error.metadata.requestData,
      requestId: error.metadata.requestId,
      timestamp: error.metadata.timestamp
    });
    
    // Send to error reporting service
    errorReporter.captureError(error.toJSON());
  }
}
```

### 4. Handle Rate Limiting Appropriately

```typescript
async function handleRateLimit(operation: () => Promise<any>) {
  try {
    return await operation();
  } catch (error) {
    if (error instanceof RateLimitError) {
      const retryAfter = error.metadata.retryDelay || 1000;
      console.warn(`Rate limited, retrying in ${retryAfter}ms`);
      
      await new Promise(resolve => setTimeout(resolve, retryAfter));
      return await operation(); // Retry once
    }
    throw error;
  }
}
```

## Retry Strategies

### Automatic Retry with SDK Utilities

The SDK provides built-in retry functionality that respects error metadata:

```typescript
import { retry, withRetry } from '@kaleidoswap/sdk';

// Basic retry wrapper
const retryableOperation = withRetry(async () => {
  return await client.pairList();
}, {
  maxRetries: 3,
  respectErrorRetryConfig: true // Use error's own retry settings
});

// Manual retry with custom config
async function robustQuoteRequest() {
  return await retry(async () => {
    return await client.quoteRequest('BTC', 'USDT', 100000);
  }, {
    maxRetries: 5,
    initialDelay: 1000,
    exponentialBase: 2,
    retryOnExceptions: [NetworkError, TimeoutError, RateLimitError]
  });
}
```

### Custom Retry Logic

```typescript
async function customRetrySwap(swapRequest: SwapRequest): Promise<SwapResponse> {
  let lastError: Error;
  
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await client.initMakerSwap(swapRequest);
    } catch (error) {
      lastError = error;
      
      if (error instanceof SwapError) {
        // Check if error is retryable
        if (!error.isRetryable()) {
          throw error; // Don't retry non-retryable errors
        }
        
        // Use error's suggested retry strategy
        const strategy = error.getRetryStrategy();
        const delay = error.metadata.retryDelay || (1000 * Math.pow(2, attempt));
        
        console.log(`Swap attempt ${attempt + 1} failed, retrying in ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error; // Don't retry unexpected errors
      }
    }
  }
  
  throw lastError;
}
```

## Code Examples

### Complete Error Handling Example

```typescript
import { 
  KaleidoClient,
  NetworkError,
  SwapError,
  ValidationError,
  ErrorCode,
  withRetry
} from '@kaleidoswap/sdk';

class TradingService {
  private client: KaleidoClient;
  
  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
    });
  }
  
  async executeSwap(fromAsset: string, toAsset: string, amount: number) {
    try {
      // Step 1: Get quote with retry
      const quote = await withRetry(async () => {
        return await this.client.quoteRequest(fromAsset, toAsset, amount);
      });
      
      // Step 2: Initialize swap
      const swapResponse = await this.client.initMakerSwap({
        rfq_id: quote.rfq_id,
        from_asset: fromAsset,
        to_asset: toAsset,
        from_amount: amount,
        to_amount: quote.to_amount
      });
      
      // Step 3: Execute swap
      const result = await this.client.executeMakerSwap({
        swapstring: swapResponse.swapstring,
        payment_hash: swapResponse.payment_hash,
        taker_pubkey: await this.client.getNodePubkey()
      });
      
      return result;
      
    } catch (error) {
      return this.handleSwapError(error, { fromAsset, toAsset, amount });
    }
  }
  
  private handleSwapError(error: unknown, context: any) {
    if (error instanceof ValidationError) {
      throw new Error(`Invalid swap parameters: ${error.getUserMessage()}`);
    }
    
    if (error instanceof NetworkError) {
      // Log and retry or show offline message
      console.error('Network error during swap:', error.toJSON());
      throw new Error('Network connection issue. Please try again.');
    }
    
    if (error instanceof SwapError) {
      switch (error.code) {
        case ErrorCode.INSUFFICIENT_LIQUIDITY:
          throw new Error(`Insufficient liquidity for ${context.fromAsset}/${context.toAsset} pair`);
        case ErrorCode.SWAP_SLIPPAGE_EXCEEDED:
          throw new Error('Price moved too much. Please try again with higher slippage tolerance.');
        case ErrorCode.SWAP_INSUFFICIENT_BALANCE:
          throw new Error(`Insufficient ${context.fromAsset} balance`);
        default:
          throw new Error(`Swap failed: ${error.getUserMessage()}`);
      }
    }
    
    // Unknown error
    console.error('Unexpected error during swap:', error);
    throw new Error('An unexpected error occurred. Please try again later.');
  }
}
```

### Error Recovery with Fallback

```typescript
async function robustPairListing() {
  try {
    // Primary method
    return await client.pairList();
  } catch (error) {
    if (error instanceof NetworkError) {
      // Try WebSocket fallback
      try {
        console.warn('HTTP request failed, trying WebSocket...');
        return await getPairsViaWebSocket();
      } catch (wsError) {
        // Both methods failed
        console.error('Both HTTP and WebSocket failed');
        throw new Error('Unable to fetch trading pairs. Please check your connection.');
      }
    }
    
    if (error instanceof RateLimitError) {
      // Wait and retry
      const delay = error.metadata.retryDelay || 5000;
      console.warn(`Rate limited, waiting ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
      return await client.pairList();
    }
    
    throw error;
  }
}
```

### Logging and Monitoring

```typescript
function setupErrorMonitoring() {
  // Global error handler for unhandled SDK errors
  process.on('unhandledRejection', (error) => {
    if (error instanceof KaleidoSDKError) {
      // Send to monitoring service
      errorMonitor.captureSDKError({
        error: error.toJSON(),
        severity: error.severity,
        category: error.category,
        retryable: error.isRetryable()
      });
    }
  });
}

// Error logging utility
function logError(error: unknown, operation: string) {
  if (error instanceof KaleidoSDKError) {
    console.error(`[${operation}] SDK Error:`, {
      code: error.code,
      message: error.message,
      category: error.category,
      severity: error.severity,
      requestId: error.metadata.requestId,
      retryable: error.isRetryable()
    });
  } else {
    console.error(`[${operation}] Unknown Error:`, error);
  }
}
```

> **Warning**: Always handle errors appropriately in production applications. Network errors should typically be retried, while validation errors should be shown to users with clear guidance on how to fix the input.

> **Note**: The SDK automatically includes request IDs in error metadata when available, which can be helpful for support and debugging purposes.
