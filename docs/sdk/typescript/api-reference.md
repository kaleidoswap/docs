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
  apiKey: process.env.KALEIDO_API_KEY, // leave empty for now
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

## API Methods

### Asset and Market Data

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `assetList()` | List all available assets | None | `Promise<AssetResponse>` | `const assets = await client.assetList();` |
| `pairList()` | List all trading pairs | None | `Promise<PairResponse>` | `const pairs = await client.pairList();` |
| `quoteRequest()` | Get price quote for a trade | `fromAsset`, `toAsset`, `fromAmount?`, `toAmount?` | `Promise<PairQuoteResponse>` | `const quote = await client.quoteRequest('BTC', 'USDT', 100000);` |
| `quoteRequestWS()` | Get real-time quote via WebSocket | `fromAsset`, `toAsset`, `fromAmount?`, `toAmount?` | `Promise<PairQuoteResponse>` | `const quote = await client.quoteRequestWS('BTC', 'USDT', 100000);` |

### Atomic Swap Operations

| Method | Description | Parameters | Return Type | Example Usage |
|--------|-------------|------------|-------------|---------------|
| `initMakerSwap()` | Initialize a new swap as maker | `SwapRequest` | `Promise<SwapResponse>` | `const swap = await client.initMakerSwap(request);` |
| `executeMakerSwap()` | Execute an initialized swap | `ConfirmSwapRequest` | `Promise<ConfirmSwapResponse>` | `const result = await client.executeMakerSwap(confirm);` |
| `atomicSwapStatus()` | Get swap status by order ID | `orderId: any` | `Promise<Swap>` | `const status = await client.atomicSwapStatus('order123');` |
| `waitForSwapCompletion()` | Wait for swap to complete with polling | `paymentHash`, `timeoutSeconds?`, `pollIntervalSeconds?` | `Promise<Swap>` | `const final = await client.waitForSwapCompletion('hash123');` |
| `whitelistTrade()` | Whitelist a trade on Lightning node | `swapstring: string` | `Promise<Record<string, never>>` | `await client.whitelistTrade(swapstring);` |

### On-Chain Order Management

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

> You can also verify these types from our node Swagger documentation: `https://api.regtest.kaleidoswap.com/docs`

### LSP Operations

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

### - `assetList()`

Lists all available assets on the platform.

**Purpose**: Retrieve comprehensive asset information including supported cryptocurrencies and their properties.

**Parameters**: None

**Returns**: `Promise<AssetResponse>`

**Error Conditions**:
- `AssetError` - Failed to fetch assets
- `NetworkError` - Connection issues

### - `pairList()`

Retrieves all available trading pairs with their configuration.

**Purpose**: Get trading pair information including precision, order limits, and active status.

**Parameters**: None

**Returns**: `Promise<PairResponse>`

### - `quoteRequest()`

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

**Note:** `quoteRequest` accepts a single object parameter. The request shape is:

Example — quoting a sell (0.001 BTC = 100000 atomic units with precision):
```typescript
const quote = await client.quoteRequest({
  from_asset: 'BTC',
  from_amount: 100000,
  to_asset: 'USDT'
});
console.log('Price:', quote.price);
console.log('You will receive:', quote.to_amount, 'atomic USDT');
```

Example — quoting a buy (specific USDT amount with precision):
```typescript
const buyQuote = await client.quoteRequest({
  to_asset: 'USDT',
  to_amount: 45000000,
  from_asset: 'BTC' // property order can differ
});
console.log('BTC required:', buyQuote.from_amount);
```

### - `initMakerSwap()`

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

### - `executeMakerSwap()`

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

### - `waitForSwapCompletion()`

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

### - `getLspInfo()`

Retrieves our Lightning Service Provider information.

**Purpose**: Get LSP capabilities and connection details for Lightning operations.

**Parameters**: None

**Returns**: `Promise<GetInfoResponseModel>`

**Example**:
```typescript
const lspInfo = await client.getLspInfo();
console.log('LSP connection URL:', lspInfo.lsp_connection_url);
console.log('Supported features:', lspInfo.features);
```

> A complete guide for atomic swaps will be added to the docs soon.