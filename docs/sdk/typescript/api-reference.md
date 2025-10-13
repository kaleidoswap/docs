# API Reference

Complete reference for the KaleidoSwap TypeScript SDK client methods, configuration options, and response types.

## Overview

The `KaleidoClient` is the main entry point for interacting with the KaleidoSwap API. It provides methods for asset discovery, quote generation, swap execution, and Lightning Network operations.

```typescript
import { KaleidoClient } from '@kaleidoswap/sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
  nodeUrl: 'https://your-lightning-node.com', // Optional
  wsUrl: 'wss://api.staging.kaleidoswap.com/api/v1', // Optional
  timeout: 30000,
  retries: 3
});
```

## Client Configuration

### KaleidoConfig Interface

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `baseUrl` | `string` | No | `process.env.KALEIDO_API_URL` or staging URL | KaleidoSwap API base URL |
| `nodeUrl` | `string` | No | `null` | Lightning node URL for node operations |
| `wsUrl` | `string` | No | Auto-derived from baseUrl | WebSocket URL for real-time features |
| `timeout` | `number` | No | `30000` | Request timeout in milliseconds |
| `retries` | `number` | No | `3` | Number of automatic retries |
| `apiKey` | `string` | No | `undefined` | API key for authenticated requests |
| `userAgent` | `string` | No | SDK default | Custom User-Agent header |

### Configuration Example

```typescript
const client = new KaleidoClient({
  baseUrl: 'https://api.kaleidoswap.com/api/v1',
  nodeUrl: 'https://lightning.example.com',
  timeout: 60000,
  retries: 5,
  apiKey: process.env.KALEIDO_API_KEY
});
```

## API Methods

### Asset and Market Data

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `assetList()` | List all available assets | None | `Promise<AssetResponse>` | `const assets = await client.assetList();` |
| `pairList()` | List all trading pairs | None | `Promise<PairResponse>` | `const pairs = await client.pairList();` |
| `quoteRequest()` | Get price quote for a trade | `fromAsset`, `toAsset`, `fromAmount?`, `toAmount?` | `Promise<PairQuoteResponse>` | `const quote = await client.quoteRequest('BTC', 'USDT', 100000);` |
| `quoteRequestWS()` | Get real-time quote via WebSocket | `fromAsset`, `toAsset`, `fromAmount?`, `toAmount?` | `Promise<PairQuoteResponse>` | `const quote = await client.quoteRequestWS('BTC', 'USDT', 100000);` |

### Swap Operations

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `initMakerSwap()` | Initialize a new swap as maker | `SwapRequest` | `Promise<SwapResponse>` | `const swap = await client.initMakerSwap(request);` |
| `executeMakerSwap()` | Execute an initialized swap | `ConfirmSwapRequest` | `Promise<ConfirmSwapResponse>` | `const result = await client.executeMakerSwap(confirm);` |
| `atomicSwapStatus()` | Get swap status by order ID | `orderId: any` | `Promise<Swap>` | `const status = await client.atomicSwapStatus('order123');` |
| `waitForSwapCompletion()` | Wait for swap to complete with polling | `paymentHash`, `timeoutSeconds?`, `pollIntervalSeconds?` | `Promise<Swap>` | `const final = await client.waitForSwapCompletion('hash123');` |
| `whitelistTrade()` | Whitelist a trade on Lightning node | `swapstring: string` | `Promise<Record<string, never>>` | `await client.whitelistTrade(swapstring);` |

### Order Management

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `createOrder()` | Create a new swap order | `CreateOrderRequest` | `Promise<OrderResponse>` | `const order = await client.createOrder(orderRequest);` |
| `swapOrderStatus()` | Get order status | `orderId: string` | `Promise<OrderStatusResponse>` | `const status = await client.swapOrderStatus(order.id);` |
| `swapOrderAnalytic()` | Get order analytics | None | `Promise<any>` | `const analytics = await client.swapOrderAnalytic();` |

**Order Response Structure:**
```typescript
interface OrderResponse {
  id: string;                    // Unique order ID
  rfq_id: string;                // Quote request ID
  pay_in: string;                // Payment method (ONCHAIN/LIGHTNING)
  onchain_address: string;       // Payment address (for onchain)
  ln_invoice: string | null;     // Lightning invoice (if applicable)
  rgb_recipient_id: string | null;
  rgb_invoice: string | null;
  status: 'PENDING_PAYMENT' | 'COMPLETED' | 'FAILED';
}
```

### Lightning Network Operations

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `getLspInfo()` | Get Lightning Service Provider info | None | `Promise<GetInfoResponseModel>` | `const info = await client.getLspInfo();` |
| `getLspConnectionUrl()` | Get LSP connection URL | None | `Promise<string>` | `const url = await client.getLspConnectionUrl();` |
| `getLspNetworkInfo()` | Get LSP network information | None | `Promise<NetworkInfoResponse>` | `const netInfo = await client.getLspNetworkInfo();` |
| `connectPeer()` | Connect to a Lightning peer | `connectionUrl: string` | `Promise<any>` | `await client.connectPeer(connectionUrl);` |
| `getNodeInfo()` | Get Lightning node information | None | `Promise<{ pubkey: string }>` | `const info = await client.getNodeInfo();` |
| `getNodePubkey()` | Get node public key | None | `Promise<string>` | `const pubkey = await client.getNodePubkey();` |
| `getAssetMetadata()` | Get RGB asset metadata | `assetId: string` | `Promise<any>` | `const metadata = await client.getAssetMetadata(assetId);` |

## Method Details

### assetList()

Lists all available assets on the platform.

**Purpose**: Retrieve comprehensive asset information including supported cryptocurrencies and their properties.

**Parameters**: None

**Returns**: `Promise<AssetResponse>`

**Error Conditions**:
- `AssetError` - Failed to fetch assets
- `NetworkError` - Connection issues

**Example**:
```typescript
try {
  const assets = await client.assetList();
  console.log('Available assets:', assets.assets);
} catch (error) {
  if (error instanceof AssetError) {
    console.error('Failed to load assets:', error.message);
  }
}
```

### pairList()

Retrieves all available trading pairs with their configuration.

**Purpose**: Get trading pair information including precision, order limits, and active status.

**Parameters**: None

**Returns**: `Promise<PairResponse>`

**Example**:
```typescript
const pairs = await client.pairList();
console.log('Trading pairs:', pairs.pairs.length);

// Find specific pair
const btcUsdtPair = pairs.pairs.find(p => 
  p.base_asset === 'BTC' && p.quote_asset === 'USDT'
);
```

### quoteRequest()

Generates a price quote for a potential trade.

**Purpose**: Get current pricing and trade parameters before executing a swap.

**Parameters**:
- `fromAsset: string` - Source asset ID or ticker
- `toAsset: string` - Destination asset ID or ticker  
- `fromAmount?: number` - Amount to trade (atomic units) - use this OR toAmount
- `toAmount?: number` - Amount to receive (atomic units) - use this OR fromAmount

**Returns**: `Promise<PairQuoteResponse>`

**Error Conditions**:
- `QuoteError` - Quote generation failed
- `ValidationError` - Invalid parameters
- `PairError` - Trading pair not available

**Example**:
```typescript
// Quote selling 0.001 BTC (100000 atomic units with precision 11)
const quote = await client.quoteRequest('BTC', 'USDT', 100000);
console.log('Price:', quote.price);
console.log('You will receive:', quote.to_amount, 'atomic USDT');

// Quote buying specific amount of USDT
const buyQuote = await client.quoteRequest('BTC', 'USDT', undefined, 45000000);
console.log('BTC required:', buyQuote.from_amount);
```

### initMakerSwap()

Initializes a swap transaction as the maker (liquidity provider).

**Purpose**: Start a swap process using an RFQ (Request for Quote) ID.

**Parameters**: `SwapRequest`
- `rfq_id: string` - Quote ID from previous quote request
- `from_asset: string` - Source asset
- `to_asset: string` - Destination asset
- `from_amount: number` - Amount to send (atomic units)
- `to_amount: number` - Amount to receive (atomic units)

**Returns**: `Promise<SwapResponse>`

**Error Conditions**:
- `SwapError` - Swap initialization failed
- `ValidationError` - Invalid swap parameters

**Example**:
```typescript
const quote = await client.quoteRequest('BTC', 'USDT', 100000);

const swap = await client.initMakerSwap({
  rfq_id: quote.rfq_id,
  from_asset: 'BTC',
  to_asset: 'USDT', 
  from_amount: 100000,
  to_amount: quote.to_amount
});

console.log('Swap initialized:', swap.payment_hash);
console.log('Swapstring:', swap.swapstring);
```

### executeMakerSwap()

Executes a previously initialized swap.

**Purpose**: Complete the swap transaction by providing execution parameters.

**Parameters**: `ConfirmSwapRequest`
- `swapstring: string` - Swap data from initMakerSwap
- `payment_hash: string` - Payment hash from initMakerSwap  
- `taker_pubkey: string` - Taker's Lightning node public key

**Returns**: `Promise<ConfirmSwapResponse>`

**Example**:
```typescript
const result = await client.executeMakerSwap({
  swapstring: swap.swapstring,
  payment_hash: swap.payment_hash,
  taker_pubkey: await client.getNodePubkey()
});

console.log('Swap executed successfully:', result);
```

### waitForSwapCompletion()

Polls for swap completion with configurable timeout and interval.

**Purpose**: Monitor swap status until it reaches a terminal state (Succeeded, Failed, or Expired).

**Parameters**:
- `paymentHash: string` - Payment hash to monitor
- `timeoutSeconds?: number` - Maximum wait time (default: 300)
- `pollIntervalSeconds?: number` - Polling frequency (default: 5)

**Returns**: `Promise<Swap>`

**Error Conditions**:
- `TimeoutError` - Swap didn't complete within timeout
- `SwapError` - Status check failed

**Example**:
```typescript
try {
  const finalSwap = await client.waitForSwapCompletion(
    swap.payment_hash,
    600, // 10 minutes
    2    // Poll every 2 seconds
  );
  
  if (finalSwap.status === 'Succeeded') {
    console.log('Swap completed successfully!');
  } else {
    console.error('Swap failed:', finalSwap.status);
  }
} catch (error) {
  if (error instanceof TimeoutError) {
    console.error('Swap timed out');
  }
}
```

### getLspInfo()

Retrieves Lightning Service Provider information.

**Purpose**: Get LSP capabilities and connection details for Lightning operations.

**Parameters**: None

**Returns**: `Promise<GetInfoResponseModel>`

**Example**:
```typescript
const lspInfo = await client.getLspInfo();
console.log('LSP connection URL:', lspInfo.lsp_connection_url);
console.log('Supported features:', lspInfo.features);
```

### getNodePubkey()

Gets the Lightning node's public key.

**Purpose**: Retrieve the node's public key for use in swap operations.

**Parameters**: None

**Returns**: `Promise<string>`

**Error Conditions**:
- `NodeError` - Node operation failed
- `ConfigurationError` - Node URL not configured

**Example**:
```typescript
try {
  const pubkey = await client.getNodePubkey();
  console.log('Node public key:', pubkey);
} catch (error) {
  if (error instanceof ConfigurationError) {
    console.error('Node URL not configured in client');
  }
}
```

### quoteRequestWS()

Real-time quote generation using WebSocket connection.

**Purpose**: Get live pricing with lower latency than HTTP requests.

**Parameters**: Same as `quoteRequest()`

**Returns**: `Promise<PairQuoteResponse>`

**Error Conditions**:
- `WebSocketError` - WebSocket connection failed
- `TimeoutError` - Quote request timed out (30s default)

**Example**:
```typescript
// WebSocket connection is automatically managed
const liveQuote = await client.quoteRequestWS('BTC', 'USDT', 100000);
console.log('Live price:', liveQuote.price);
```

## Complete Usage Example

```typescript
import { 
  KaleidoClient, 
  createAssetPairMapper, 
  createPrecisionHandler 
} from '@kaleidoswap/sdk';

async function performSwap() {
  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
    nodeUrl: 'https://your-lightning-node.com'
  });

  try {
    // 1. Get trading pairs and create utilities
    const pairs = await client.pairList();
    const assetMapper = createAssetPairMapper(pairs);
    const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

    // 2. Find assets
    const btc = assetMapper.findByTicker('BTC');
    const usdt = assetMapper.findByTicker('USDT');

    // 3. Validate and convert amount
    const decimalAmount = 0.001; // 0.001 BTC
    const validation = precisionHandler.validateOrderSize(decimalAmount, btc);
    
    if (!validation.valid) {
      throw new Error(`Invalid order size: ${validation.error}`);
    }

    // 4. Get quote
    const quote = await client.quoteRequest(
      btc.asset_id, 
      usdt.asset_id, 
      validation.atomicAmount
    );

    console.log('Quote received:', {
      price: quote.price,
      fromAmount: precisionHandler.toDecimalAmount(quote.from_amount, btc.asset_id),
      toAmount: precisionHandler.toDecimalAmount(quote.to_amount, usdt.asset_id),
      fee: quote.fee
    });

    // 5. Initialize swap
    const swap = await client.initMakerSwap({
      rfq_id: quote.rfq_id,
      from_asset: btc.asset_id,
      to_asset: usdt.asset_id,
      from_amount: quote.from_amount,
      to_amount: quote.to_amount
    });

    // 6. Execute swap  
    const result = await client.executeMakerSwap({
      swapstring: swap.swapstring,
      payment_hash: swap.payment_hash,
      taker_pubkey: await client.getNodePubkey()
    });

    // 7. Wait for completion
    const finalSwap = await client.waitForSwapCompletion(swap.payment_hash);
    
    console.log('Swap completed:', finalSwap.status);
    return finalSwap;

  } catch (error) {
    console.error('Swap failed:', error);
    throw error;
  }
}
```

## Authentication

Most API methods work without authentication, but some advanced features may require API keys:

```typescript
const client = new KaleidoClient({
  baseUrl: 'https://api.kaleidoswap.com/api/v1',
  apiKey: process.env.KALEIDO_API_KEY
});
```

## Rate Limiting

The API implements rate limiting. The SDK automatically handles rate limit responses with appropriate retry delays:

```typescript
try {
  const quote = await client.quoteRequest('BTC', 'USDT', 100000);
} catch (error) {
  if (error instanceof RateLimitError) {
    // SDK will automatically retry with proper delay
    console.log('Rate limited, retrying...');
  }
}
```

> **Warning**: Always configure `nodeUrl` in the client configuration when using Lightning Network operations like `getNodePubkey()`, `connectPeer()`, or `getAssetMetadata()`.

> **Note**: WebSocket connections are automatically managed by the client. The connection is established on first use and reused for subsequent requests.
