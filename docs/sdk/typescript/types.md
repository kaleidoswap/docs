# Types Reference

Complete reference for TypeScript interfaces, types, and enums used in the KaleidoSwap SDK.

## Overview

The SDK provides comprehensive TypeScript definitions for all data structures, configuration options, and response types. This ensures type safety and excellent IDE support with autocompletion and inline documentation.

```typescript
import { 
  KaleidoConfig,
  SwapRequest,
  PairQuoteResponse,
  AssetResponse,
  ErrorCode
} from '@kaleidoswap/sdk';
```

## Core Interfaces

### Client Configuration

| Interface | Description | Usage |
|-----------|-------------|-------|
| `KaleidoConfig` | Main client configuration options | `new KaleidoClient(config)` |
| `HttpClientConfig` | HTTP client specific settings | Extended by KaleidoConfig |
| `WebSocketConfig` | WebSocket connection configuration | Used internally for real-time features |
| `RetryConfig` | Retry behavior configuration | Used with retry utilities |

#### KaleidoConfig

```typescript
interface KaleidoConfig extends Omit<HttpClientConfig, 'baseUrl'> {
  baseUrl?: string;        // API base URL
  nodeUrl?: string;        // Lightning node URL  
  wsUrl?: string;          // WebSocket URL
  timeout?: number;        // Request timeout (ms)
  retries?: number;        // Max retry attempts
  apiKey?: string;         // API authentication key
  userAgent?: string;      // Custom User-Agent header
}
```

#### HttpClientConfig

```typescript
interface HttpClientConfig {
  baseUrl: string;         // Required base URL
  timeout?: number;        // Request timeout in milliseconds
  retries?: number;        // Number of retry attempts
  headers?: Record<string, string>; // Custom headers
  apiKey?: string;         // API key for authentication
}
```

#### WebSocketConfig

```typescript
interface WebSocketConfig {
  baseUrl: string;         // WebSocket URL
  timeout?: number;        // Connection timeout
  reconnect?: boolean;     // Auto-reconnect on disconnect
  maxReconnectAttempts?: number; // Max reconnection attempts
}
```

### Asset Types

| Interface | Description | Usage |
|-----------|-------------|-------|
| `ClientAsset` | Individual asset information | Asset listings and metadata |
| `AssetResponse` | Asset list API response | Response from `assetList()` |
| `Pair` | Trading pair definition | Pair information and configuration |
| `PairResponse` | Trading pairs API response | Response from `pairList()` |
| `MappedAsset` | Enhanced asset with trading info | Used by AssetPairMapper utility |

#### ClientAsset

```typescript
interface ClientAsset {
  asset_id: string;        // Unique asset identifier
  ticker: string;          // Asset ticker symbol (e.g., "BTC")
  name: string;            // Human-readable asset name
  precision: number;       // Decimal precision for amounts
  is_active: boolean;      // Whether asset is available for trading
  min_order_size: number;  // Minimum order size (atomic units)
  max_order_size: number;  // Maximum order size (atomic units)
  icon_url?: string;       // Asset icon URL
  description?: string;    // Asset description
}
```

#### Pair

```typescript
interface Pair {
  pair_id: string;         // Unique pair identifier
  base_asset: string;      // Base asset ticker
  base_asset_id: string;   // Base asset ID
  quote_asset: string;     // Quote asset ticker  
  quote_asset_id: string;  // Quote asset ID
  is_active: boolean;      // Trading availability
  base_precision: number;  // Base asset precision
  quote_precision: number; // Quote asset precision
  min_base_order_size: number;   // Min base amount
  max_base_order_size: number;   // Max base amount
  min_quote_order_size: number;  // Min quote amount
  max_quote_order_size: number;  // Max quote amount
  fee_rate: number;        // Trading fee rate
}
```

#### MappedAsset

```typescript
interface MappedAsset {
  asset_id: string;        // Asset identifier
  ticker: string;          // Asset ticker
  name: string;            // Asset name
  precision: number;       // Decimal precision
  is_active: boolean;      // Active status
  min_order_size: number;  // Minimum order size
  max_order_size: number;  // Maximum order size
  trading_pairs: string[]; // Compatible asset IDs for trading
}
```

## Request and Response Types

### Quote and Trading

| Interface | Description | Usage |
|-----------|-------------|-------|
| `PairQuoteRequest` | Quote request parameters | Used with `quoteRequest()` |
| `PairQuoteResponse` | Quote response data | Returned by quote methods |
| `SwapRequest` | Swap initialization parameters | Used with `initMakerSwap()` |
| `SwapResponse` | Swap initialization response | Returned by `initMakerSwap()` |
| `ConfirmSwapRequest` | Swap execution parameters | Used with `executeMakerSwap()` |
| `ConfirmSwapResponse` | Swap execution response | Returned by `executeMakerSwap()` |

#### PairQuoteRequest

```typescript
interface PairQuoteRequest {
  from_asset: string;      // Source asset ID
  to_asset: string;        // Destination asset ID
  from_amount?: number;    // Amount to send (atomic units)
  to_amount?: number;      // Amount to receive (atomic units)
  timestamp?: number;      // Request timestamp
}
```

#### PairQuoteResponse

```typescript
interface PairQuoteResponse {
  rfq_id: string;          // Request for Quote ID
  from_asset: string;      // Source asset ID
  to_asset: string;        // Destination asset ID
  from_amount: number;     // Source amount (atomic units)
  to_amount: number;       // Destination amount (atomic units)
  price: number;           // Exchange rate
  fee: number;             // Trading fee (atomic units)
  expires_at: number;      // Quote expiration timestamp
  slippage?: number;       // Price slippage percentage
}
```

#### SwapRequest

```typescript
interface SwapRequest {
  rfq_id: string;          // Quote ID from PairQuoteResponse
  from_asset: string;      // Source asset ID
  to_asset: string;        // Destination asset ID
  from_amount: number;     // Amount to send (atomic units)
  to_amount: number;       // Amount to receive (atomic units)
}
```

#### SwapResponse

```typescript
interface SwapResponse {
  payment_hash: string;    // Unique payment identifier
  swapstring: string;      // Swap execution data
  expires_at: number;      // Swap expiration time
  lightning_invoice?: string; // Lightning payment invoice
}
```

#### ConfirmSwapRequest

```typescript
interface ConfirmSwapRequest {
  swapstring: string;      // Swap data from SwapResponse
  payment_hash: string;    // Payment hash from SwapResponse
  taker_pubkey: string;    // Taker's Lightning node public key
}
```

#### ConfirmSwapResponse

```typescript
interface ConfirmSwapResponse {
  success: boolean;        // Execution success status
  transaction_id?: string; // Transaction identifier
  message?: string;        // Status message
}
```

### Swap Status and Orders

| Interface | Description | Usage |
|-----------|-------------|-------|
| `Swap` | Swap status information | Status tracking and monitoring |
| `SwapStatus` | Swap state enumeration | Current swap state |
| `CreateOrderRequest` | Order creation parameters | Order management |
| `PaymentState` | Payment status enumeration | Payment tracking |

#### Swap

```typescript
interface Swap {
  order_id: string;        // Order identifier
  payment_hash: string;    // Payment hash
  status: SwapStatus;      // Current swap status
  from_asset: string;      // Source asset
  to_asset: string;        // Destination asset
  from_amount: number;     // Source amount
  to_amount: number;       // Destination amount
  created_at: number;      // Creation timestamp
  updated_at: number;      // Last update timestamp
  expires_at?: number;     // Expiration timestamp
  error_message?: string;  // Error description if failed
}
```

#### SwapStatus

```typescript
enum SwapStatus {
  PENDING = "Pending",         // Swap initiated, awaiting execution
  IN_PROGRESS = "InProgress",  // Currently executing
  SUCCEEDED = "Succeeded",     // Successfully completed
  FAILED = "Failed",           // Failed to execute
  EXPIRED = "Expired",         // Expired before completion
  CANCELLED = "Cancelled"      // Manually cancelled
}
```

#### CreateOrderRequest

```typescript
interface CreateOrderRequest {
  from_asset: string;      // Source asset ID
  to_asset: string;        // Destination asset ID
  from_amount: number;     // Amount to trade
  order_type: OrderType;   // Order type (market, limit, etc.)
  settlement: OrderSettlement; // Settlement method
  expires_at?: number;     // Order expiration
}
```

#### OrderSettlement

```typescript
enum OrderSettlement {
  LIGHTNING = "LIGHTNING",   // Lightning Network settlement
  ONCHAIN = "ONCHAIN"        // On-chain settlement
}
```

## Lightning Network Types

### LSP and Network Information

| Interface | Description | Usage |
|-----------|-------------|-------|
| `GetInfoResponseModel` | LSP information response | Lightning service provider details |
| `NetworkInfoResponse` | Network status information | Lightning network status |

#### GetInfoResponseModel

```typescript
interface GetInfoResponseModel {
  lsp_connection_url: string;    // LSP connection string
  node_pubkey: string;           // LSP node public key
  features: number[];            // Supported Lightning features
  min_channel_size: number;      // Minimum channel size
  max_channel_size: number;      // Maximum channel size
  fee_rate: number;              // Channel opening fee rate
}
```

#### NetworkInfoResponse

```typescript
interface NetworkInfoResponse {
  block_height: number;          // Current block height
  block_hash: string;            // Latest block hash
  network: string;               // Network name (mainnet, testnet)
  synced_to_chain: boolean;      // Chain synchronization status
  num_peers: number;             // Connected peer count
  num_channels: number;          // Active channel count
}
```

## Error System Types (Experimentory)

### Error Enumerations

| Enum | Description | Usage |
|------|-------------|-------|
| `ErrorCode` | Specific error identifiers | Error identification and handling |
| `ErrorSeverity` | Error severity levels | Error prioritization |
| `ErrorCategory` | Error classification | Error grouping and handling strategies |
| `RetryStrategy` | Retry behavior types | Automatic retry configuration |

#### ErrorCode

```typescript
enum ErrorCode {
  // Network errors (1000-1099)
  NETWORK_UNREACHABLE = 'NETWORK_UNREACHABLE',
  CONNECTION_TIMEOUT = 'CONNECTION_TIMEOUT',
  WEBSOCKET_CONNECTION_FAILED = 'WEBSOCKET_CONNECTION_FAILED',
  
  // HTTP errors (1100-1199)
  HTTP_UNAUTHORIZED = 'HTTP_UNAUTHORIZED',
  HTTP_NOT_FOUND = 'HTTP_NOT_FOUND',
  HTTP_INTERNAL_SERVER_ERROR = 'HTTP_INTERNAL_SERVER_ERROR',
  
  // Validation errors (1300-1399)
  VALIDATION_INVALID_AMOUNT = 'VALIDATION_INVALID_AMOUNT',
  VALIDATION_INVALID_ASSET_ID = 'VALIDATION_INVALID_ASSET_ID',
  
  // Trading errors (1500-1599)
  SWAP_FAILED = 'SWAP_FAILED',
  INSUFFICIENT_LIQUIDITY = 'INSUFFICIENT_LIQUIDITY',
  SWAP_SLIPPAGE_EXCEEDED = 'SWAP_SLIPPAGE_EXCEEDED',
  
  // Lightning errors (1600-1699)
  LN_NODE_UNREACHABLE = 'LN_NODE_UNREACHABLE',
  LN_PAYMENT_FAILED = 'LN_PAYMENT_FAILED'
}
```

#### ErrorSeverity

```typescript
enum ErrorSeverity {
  LOW = 'low',           // Minor issues, app can continue
  MEDIUM = 'medium',     // Moderate issues, feature degradation
  HIGH = 'high',         // Serious issues, major functionality affected
  CRITICAL = 'critical'  // Critical issues, app unusable
}
```

#### ErrorCategory

```typescript
enum ErrorCategory {
  NETWORK = 'network',                    // Network connectivity
  HTTP = 'http',                         // HTTP protocol issues
  AUTHENTICATION = 'authentication',     // Auth and authorization
  VALIDATION = 'validation',             // Input validation
  BUSINESS_LOGIC = 'business_logic',     // Business rule violations
  TRADING = 'trading',                   // Trading operations
  LIGHTNING_NETWORK = 'lightning_network', // Lightning Network
  CONFIGURATION = 'configuration'        // Client configuration
}
```

### Error Metadata

| Interface | Description | Usage |
|-----------|-------------|-------|
| `ErrorMetadata` | Additional error context | Error debugging and recovery |

#### ErrorMetadata

```typescript
interface ErrorMetadata {
  statusCode?: number;           // HTTP status code
  response?: any;                // Raw server response
  requestData?: any;             // Original request data
  timestamp?: Date;              // Error occurrence time
  requestId?: string;            // Request tracking ID
  context?: Record<string, any>; // Additional context
  recoveryActions?: string[];    // Suggested recovery steps
  retryable?: boolean;          // Whether retry is recommended
  retryStrategy?: RetryStrategy; // Suggested retry approach
  retryDelay?: number;          // Recommended retry delay (ms)
  maxRetries?: number;          // Maximum retry attempts
}
```

## Utility Types

### Asset Mapping and Precision

| Interface | Description | Usage |
|-----------|-------------|-------|
| `RetryConfig` | Retry behavior configuration | Automatic retry utilities |

#### RetryConfig

```typescript
interface RetryConfig {
  maxRetries: number;              // Maximum retry attempts
  initialDelay: number;            // Initial delay in milliseconds
  maxDelay: number;                // Maximum delay in milliseconds
  exponentialBase: number;         // Exponential backoff base
  jitter: boolean;                 // Add random jitter to delays
  retryOnExceptions: Array<new (...args: any[]) => Error>; // Exception types to retry
  respectErrorRetryConfig?: boolean; // Use error's own retry settings
  customRetryStrategy?: RetryStrategy; // Override retry strategy
}
```

## WebSocket Message Types

### Real-time Communication

| Interface | Description | Usage |
|-----------|-------------|-------|
| `WebSocketMessage` | WebSocket message format | Real-time data exchange |
| `MessageHandler` | Message handler function type | Event handling |

#### WebSocketMessage

```typescript
interface WebSocketMessage {
  action: string;              // Message type/action
  data?: any;                  // Message payload
  error?: {                    // Error information
    code: string;
    message: string;
  };
  request_id?: string;         // Request correlation ID
  timestamp?: number;          // Message timestamp
}
```

#### MessageHandler

```typescript
type MessageHandler = (message: WebSocketMessage) => void;
```

## Type Guards and Utilities

### Runtime Type Checking

```typescript
// Check if error is SDK error
function isKaleidoSDKError(error: unknown): error is KaleidoSDKError {
  return error instanceof KaleidoSDKError;
}

// Check if error is retryable
function isRetryableError(error: unknown): boolean {
  return isKaleidoSDKError(error) && error.isRetryable();
}

// Extract error category
function getErrorCategory(error: unknown): ErrorCategory | null {
  return isKaleidoSDKError(error) ? error.category : null;
}
```

## Complete Type Usage Example

```typescript
import {
  KaleidoClient,
  KaleidoConfig,
  PairQuoteResponse,
  SwapRequest,
  SwapResponse,
  ErrorCode,
  NetworkError,
  MappedAsset
} from '@kaleidoswap/sdk';

// Type-safe client configuration
const config: KaleidoConfig = {
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
  nodeUrl: 'https://lightning.example.com',
  timeout: 30000,
  retries: 3
};

const client = new KaleidoClient(config);

// Type-safe trading function
async function executeTypedSwap(
  fromAsset: string,
  toAsset: string,
  amount: number
): Promise<SwapResponse> {
  try {
    // Get quote with proper typing
    const quote: PairQuoteResponse = await client.quoteRequest(
      fromAsset,
      toAsset,
      amount
    );

    // Create typed swap request
    const swapRequest: SwapRequest = {
      rfq_id: quote.rfq_id,
      from_asset: fromAsset,
      to_asset: toAsset,
      from_amount: amount,
      to_amount: quote.to_amount
    };

    // Execute swap with typed response
    const swapResponse: SwapResponse = await client.initMakerSwap(swapRequest);
    
    return swapResponse;
    
  } catch (error) {
    // Type-safe error handling
    if (error instanceof NetworkError) {
      if (error.code === ErrorCode.NETWORK_UNREACHABLE) {
        throw new Error('Network is unreachable');
      }
    }
    throw error;
  }
}

// Using utility types with proper generics
function processAssets(assets: MappedAsset[]): Record<string, MappedAsset> {
  return assets.reduce((acc, asset) => {
    acc[asset.ticker] = asset;
    return acc;
  }, {} as Record<string, MappedAsset>);
}
```

> **Note**: All amounts in the API use atomic units (smallest divisible unit for each asset). Use the PrecisionHandler utility to convert between decimal and atomic amounts.

> **Warning**: Always validate input types at runtime when dealing with external data, even with TypeScript. The SDK provides comprehensive error handling for invalid inputs.
