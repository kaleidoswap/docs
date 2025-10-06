# Getting Started

This guide will help you get up and running with the KaleidoSwap TypeScript SDK.

## Installation

Install the SDK using npm or yarn:

```bash
npm install @kaleidoswap/kaleidoswap-sdk
```

```bash
yarn add @kaleidoswap/kaleidoswap-sdk
```

A little information about how RGB assets are:
- name: the name of the asset, for example Bitcoin, Tether, etc.
- ticker: ticker symbol is an abbreviation of the asset name, for example BTC, USDT, etc.
- asset_id: a unique id of the asset that is used for verification, usually starts with `rgb:x...`
> Remember that BTC is not an asset on rgb and is the native coin on Bitcoin network, that's why the asset_id for BTC remians `BTC`

## Basic Setup

### 1. Import the SDK

```typescript
import { KaleidoClient } from '@kaleidoswap/kaleidoswap-sdk';
```

### 2. Initialize the Client

```typescript
const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
  // nodeUrl: '<Address of your RGB node>', 
});
```

> More information about the configuration of `KaleidoClient` class later in this guide.

### 3. Make Your First API Call

```typescript
// Get available trading pairs
const pairs = await client.pairList();
console.log('Available pairs:', pairs.length);

// Get available assets
const assets = await client.assetList();
console.log('Available assets:', assets.length);
```

## Configuration Options

The `KaleidoClient` class accepts a configuration object with the following options:

```typescript
import { KaleidoClient, KaleidoConfig } from '@kaleidoswap/kaleidoswap-sdk';

const config: KaleidoConfig = {
  // Required: API base URL (if skipped, it defaults to using our staging node below)
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
  
  // Optional: Your RGB Lightning Node (required for some node operations)
  nodeUrl: '',
  
  // Optional: API key for authenticated requests (has not been implemented yet)
  apiKey: '',
};

const client = new KaleidoClient(config);
```

## Environment Variables

You can also use environment variables for configuration:

```bash
# Set the API URL
export KALEIDO_API_URL=https://api.staging.kaleidoswap.com/api/v1
```

The SDK will automatically use `KALEIDO_API_URL` if no `baseUrl` is provided in the configuration.

## Example Swap From USDT to BTC

### Importing

```ts
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
} from '@kaleidoswap/kaleidoswap-sdk`;
```

```ts
const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
})

// Step 1: Get trading paris data
const pairs = await client.pairList();

// Step 2: Create asset pair mapper
const assetMapper = createAssetPairMapper(pairs);

// Step 3: Create precision handler
    const allAssets = assetMapper.getAllAssets();
    const precisionHandler = createPrecisionHandler(allAssets);

    allAssets.forEach(asset => {
      console.log(`- ${asset.ticker} (${asset.asset_id})`);
      console.log(`  Precision: ${asset.precision}`);
      const limits = precisionHandler.getOrderSizeLimits(asset);
      console.log(`  Order limits: ${limits.minDecimal} - ${limits.maxDecimal} ${asset.ticker}`);
    });
```

Before proceeding with this example, have a look at our utility function [here](./utilities.md). Make sure to understand what `findByTicker` method does, as it should not be use for production and is only created for abstracting the following example.

```ts
// Step 4: Find USDT and BTC assets
const usdt = assetMapper.findByTicker('USDT');
const btc = assetMapper.findByTicker('BTC');

console.log(`Found: ${usdt.ticker} (${usdt.asset_id}) and ${btc.ticker} (${btc.asset_id})`);

// Step 5: Check if trading pair exists
if (!assetMapper.canTrade(usdt.asset_id, btc.asset_id)) {
  throw new Error('No trading pair between USDT and BTC');
}

// Step 6: Validate and prepare amount
const decimalAmount = 100; // 100 USDT
console.log(`\nPreparing to swap ${decimalAmount} ${usdt.ticker}...`);

// Validate order size
const validation = precisionHandler.validateOrderSize(decimalAmount, usdt);
if (!validation.valid) {
  throw new Error(validation.error);
}

console.log(`Amount validation passed:`);
console.log(`- Decimal amount: ${decimalAmount} ${usdt.ticker}`);
console.log(`- Atomic amount: ${validation.atomicAmount} units`);

// Step 7: Get quote with atomic amount
console.log('\nGetting quote...');
const quote = await client.quoteRequest(
  usdt.asset_id, 
  btc.asset_id, 
  validation.atomicAmount, // Use atomic amount for API
);

// Convert quote amounts back to decimal for display
const fromAmountDecimal = precisionHandler.toDecimalAmount(quote.from_amount, usdt.asset_id);
const toAmountDecimal = precisionHandler.toDecimalAmount(quote.to_amount, btc.asset_id);
const feeDecimal = quote.fee && typeof quote.fee === 'object' && 'final_fee' in quote.fee
  ? precisionHandler.toDecimalAmount((quote.fee as any).final_fee, btc.asset_id)
  : 0;

console.log(`Quote received:`);
console.log(`- From: ${fromAmountDecimal} ${usdt.ticker}`);
console.log(`- To: ${toAmountDecimal} ${btc.ticker}`);
console.log(`- Fee: ${feeDecimal} ${btc.ticker}`);
console.log(`- Price: ${quote.price}`);
console.log(`- RFQ ID: ${quote.rfq_id}`);

// Step 8: Create order using createOrder (correct for RFQ-based swaps)
const orderRequest = {
  rfq_id: quote.rfq_id,
  from_type: 'ONCHAIN',
  to_type: 'ONCHAIN',
  min_onchain_conf: 1,
  dest_onchain_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh', // BTC destination address
  refund_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh', // BTC refund address
};

console.log('\nCreating swap order...');
const order = await client.createOrder(orderRequest);

console.log(`Order created:`);
console.log(`- Order ID: ${order.order_id || order.rfq_id}`);
console.log(`- Status: ${order.order_state || order.status}`);

// Step 9: Monitor order status
console.log('\nMonitoring order status...');
let attempts = 0;
const maxAttempts = 1;

while (attempts < maxAttempts) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  try {
    const orderId = order.order_id || order.rfq_id;
    const status = await client.swapOrderStatus(orderId);
    console.log(`[${attempts + 1}/${maxAttempts}] Order Status: ${status.order_state || 'Unknown'}`);
    
    if (status.order_state === 'COMPLETED') {
      console.log('\n✅ Swap completed successfully!');
      console.log(`Final result: Swapped ${fromAmountDecimal} ${usdt.ticker} for ${toAmountDecimal} ${btc.ticker}`);
      break;
    } else if (status.order_state === 'FAILED') {
      console.log(`\n❌ Swap failed`);
      break;
    }
  } catch (error) {
    console.log(`[${attempts + 1}/${maxAttempts}] Status check failed: ${error}`);
  }
  
  attempts++;
}

if (attempts >= maxAttempts) {
  console.log('\n⏳ Order monitoring timed out. Check status manually with:');
  console.log(`client.getOrderStatus("${order.order_id || order.rfq_id}")`);
}

```

## Working with Asset Precision

Different assets have different precision levels. The SDK provides utilities to handle this:

```typescript
import { createAssetPairMapper, createPrecisionHandler } from 'kaleidoswap-sdk';

async function handlePrecision() {
  // Get pairs and create utilities
  const pairs = await client.pairList();
  const assetMapper = createAssetPairMapper(pairs);
  const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());
  
  // Find BTC asset
  const btc = assetMapper.findByTicker('BTC');
  if (!btc) return;
  
  // Convert decimal amount to atomic units
  const decimalAmount = 0.001; // 0.001 BTC
  const atomicAmount = precisionHandler.toAtomicAmount(decimalAmount, btc.asset_id);
  console.log(`${decimalAmount} BTC = ${atomicAmount} satoshis`);
  
  // Convert back to decimal
  const backToDecimal = precisionHandler.toDecimalAmount(atomicAmount, btc.asset_id);
  console.log(`${atomicAmount} satoshis = ${backToDecimal} BTC`);
  
  // Validate order size
  const validation = precisionHandler.validateOrderSize(decimalAmount, btc);
  if (validation.valid) {
    console.log('Order size is valid');
  } else {
    console.log('Invalid order size:', validation.error);
  }
}
```

## Available Nodes

- 'https://api.staging.kaleidoswap.com/docs'
- 'https://api.regtest.kaleidoswap.com/docs'
- 'https://api.signet.kaleidoswap.com/docs'

## Next Steps

Now that you have the basics, explore these guides:

- **[API Reference](./api-reference.md)** - Complete method documentation
- **[Examples](./examples.md)** - Full swap workflows and use cases
- **[WebSocket Guide](./websocket.md)** - Real-time data streaming
- **[Utilities](./utilities.md)** - Helper classes for common operations
- **[Error Handling](./error-handling.md)** - Comprehensive error management

You're now ready to start building with the KaleidoSwap SDK!
