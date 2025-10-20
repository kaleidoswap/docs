# Utilities

The KaleidoSwap SDK includes utility functions to make your life easier when working with assets and amounts. Think of these as your helpers for the common stuff you'll be doing.

## AssetPairMapper

The asset mapper helps you work with trading pairs without having to juggle asset IDs manually. It builds a map of all available assets and their trading relationships from the pairs data.

One handy method is `findByTicker('BTC')`, which lets you search for an asset by its ticker symbol instead of remembering cryptic asset IDs.

> **Note:** This works best when you're connecting to our maker node, where each ticker maps to one asset ID.

### Getting Started

```typescript
import { createAssetPairMapper } from 'kaleidoswap-sdk';

// Fetch pairs and create the mapper
const pairs = await client.pairList();
const assetMapper = createAssetPairMapper(pairs);
```

### Finding Assets

The most common thing you'll do is find assets by their ticker:

```typescript
const btc = assetMapper.findByTicker('BTC');
const usdt = assetMapper.findByTicker('USDT');

if (!btc || !usdt) {
  throw new Error('Assets not found');
}

console.log(`BTC asset ID: ${btc.asset_id}`);
console.log(`Precision: ${btc.precision} decimal places`);
```

You can also search by asset ID if you already have it:

```typescript
const asset = assetMapper.findById('some_asset_id');
```

### Checking Trading Pairs

Before requesting a quote, you might want to check if two assets can be traded:

```typescript
const canSwap = assetMapper.canTrade(usdt.asset_id, btc.asset_id);
if (!canSwap) {
  console.log('This pair cannot be traded directly');
}
```

### Getting All Assets

Need to show a list of available assets? Easy:

```typescript
const allAssets = assetMapper.getAllAssets();

allAssets.forEach(asset => {
  console.log(`${asset.ticker}: ${asset.min_order_size} - ${asset.max_order_size} units`);
});
```

## PrecisionHandler

Here's the thing: users think in "0.5 BTC" but APIs work with "50000000 satoshis". The precision handler converts between these two worlds so you don't have to do the math yourself.

### Setting It Up

```typescript
import { createPrecisionHandler } from 'kaleidoswap-sdk';

const assets = assetMapper.getAllAssets();
const precisionHandler = createPrecisionHandler(assets);
```

### Converting Amounts

**From decimal to atomic units (for API calls):**

```typescript
// User wants to swap 100 USDT
const amountToSwap = 100;
const atomicAmount = precisionHandler.toAssetAmount(amountToSwap, usdt.asset_id);

// Now use this in your API call
const quote = await client.quoteRequest(btc.asset_id, usdt.asset_id, atomicAmount);
```

**From atomic units back to decimal (for display):**

```typescript
// Show the user how much BTC they'll receive
const receiveBTC = precisionHandler.toAssetDecimalAmount(quote.to_amount, btc.asset_id);
console.log(`You will receive ${receiveBTC} BTC`);
```

### Validating Order Sizes

Before making an API call, validate that the amount is within the allowed limits:

```typescript
const validation = precisionHandler.validateOrderSize(100, usdt);

if (!validation.valid) {
  throw new Error(validation.error);
}

// If valid, use the atomic amount
const quote = await client.quoteRequest(btc.asset_id, usdt.asset_id, validation.asset_amount);
```

### Getting Order Limits

Want to show users the min/max they can swap?

```typescript
const limits = precisionHandler.getOrderSizeLimits(btc);

console.log(`You can swap between ${limits.asset_min_decimal_amount} and ${limits.asset_max_decimal_amount} BTC`);
```

## Retry Logic

Network hiccups happen. The retry utilities help you handle temporary failures gracefully.

### Basic Usage

```typescript
import { retry } from 'kaleidoswap-sdk';

// Automatically retry on network failures
const quote = await retry(async () => {
  return await client.quoteRequest(btc.asset_id, usdt.asset_id, amount);
});
```

### Custom Configuration

Need more control? You can customize the retry behavior:

```typescript
const quote = await retry(
  async () => client.quoteRequest(btc.asset_id, usdt.asset_id, amount),
  {
    maxRetries: 5,        // Try up to 5 times
    initialDelay: 2000,   // Wait 2 seconds between retries
    maxDelay: 30000,      // Never wait more than 30 seconds
  }
);
```

The retry logic uses exponential backoff with jitter by default, so it won't hammer the API if something's wrong.

## Complete Utility Example

Here's a comprehensive example showing how to use all utilities together:

```typescript
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
  retry
} from 'kaleidoswap-sdk';

async function swapExample() {
  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
  });

  // Step 1: Setup utilities (do this once)
  const pairs = await retry(() => client.pairList());
  const assetMapper = createAssetPairMapper(pairs);
  const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

  // Step 2: Find your assets
  const usdt = assetMapper.findByTicker('USDT');
  const btc = assetMapper.findByTicker('BTC');

  if (!usdt || !btc) {
    throw new Error('Assets not found');
  }

  // Step 3: Check if they can be traded
  if (!assetMapper.canTrade(usdt.asset_id, btc.asset_id)) {
    throw new Error('This pair cannot be traded');
  }

  // Step 4: Validate the amount
  const amountToSwap = 100; // 100 USDT
  const validation = precisionHandler.validateOrderSize(amountToSwap, usdt);

  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Step 5: Get a quote with retry logic
  const quote = await retry(
    () => client.quoteRequest(
      btc.asset_id,
      usdt.asset_id,
      validation.asset_amount
    )
  );

  // Step 6: Show the user what they'll get
  const receiveBTC = precisionHandler.toAssetDecimalAmount(quote.to_amount, btc.asset_id);
  console.log(`Swapping ${amountToSwap} USDT for ${receiveBTC} BTC`);

  // Step 7: Create the order
  const order = await client.createOrder({
    rfq_id: quote.rfq_id,
    from_type: 'ONCHAIN',
    to_type: 'ONCHAIN',
    min_onchain_conf: 1,
    dest_rgb_invoice: 'your_btc_address',
    refund_address: 'your_refund_address',
  });

  console.log('Order created! Pay to:', order.onchain_address);
}
```

## Quick Tips

**Initialize once, use everywhere:** Create your asset mapper and precision handler once when your app starts, then reuse them.

**Always validate:** Use `validateOrderSize()` before making API calls. It'll save you from errors.

**Check assets exist:** Always verify that `findByTicker()` actually found the asset before using it.

**Use retry for network calls:** Wrap your API calls in `retry()` to handle temporary network issues gracefully.
