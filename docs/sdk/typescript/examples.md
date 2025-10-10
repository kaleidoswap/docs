# Examples

This guide provides working examples for common use cases with the KaleidoSwap SDK.

## Basic Quote Example

<details>
  <summary>Get a price quote for swapping assets</summary>

  ```ts
  import { KaleidoClient, createAssetPairMapper } from 'kaleidoswap-sdk';

  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
  });

  // Get available pairs
  const pairs = await client.pairList();
  ```

  ```ts
  const btc = assetMapper.findByTicker('BTC');
  const usdt = assetMapper.findByTicker('USDT');

  // BTC has a precision of 8, so remove 8 zeros manually or use our precision utility 
  if (!btc || !usdt) {
    throw new Error('BTC or USDT asset not found.');
  }

  const quote = await client.quoteRequest(
    btc.asset_id,
    usdt.asset_id,
    100000000
  );
  ```

  <details>
    <summary>View Response</summary>
    ```json
    Quote: {
      rfq_id: '79fe223c-6242-4014-b56d-ed0d226e6236',
      from_asset: 'BTC',
      from_amount: 100000000,
      to_asset: 'rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg',
      to_amount: 119112540,
      price: 120315696187,
      fee: {
        base_fee: 0,
        variable_fee: 1203156,
        fee_rate: 0.01,
        final_fee: 1203156,
        fee_asset: 'rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg',
        fee_asset_precision: 6
      },
      timestamp: 1760077778,
      expires_at: 1760077838
    }
    ```
  </details>
</details>

## Swap From USDT to BTC

<details>
  <summary>Complete swap workflow from USDT to BTC</summary>

```ts
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
} from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
});

// Get trading pairs
const pairs = await client.pairList();
```

<details>
  <summary>View Response</summary>

```json

```
</details>

```ts
// Create utilities
const assetMapper = createAssetPairMapper(pairs);
const allAssets = assetMapper.getAllAssets();
const precisionHandler = createPrecisionHandler(allAssets);

// Find assets
const usdt = assetMapper.findByTicker('USDT');
const btc = assetMapper.findByTicker('BTC');
```

<details>
  <summary>View Assets</summary>

```json

```
</details>

```ts
// Validate amount (100 USDT)
const decimalAmount = 100;
const validation = precisionHandler.validateOrderSize(decimalAmount, usdt);
```

<details>
  <summary>View Validation</summary>

```json

```
</details>

```ts
// Get quote
const quote = await client.quoteRequest(
  usdt.asset_id, 
  btc.asset_id, 
  validation.atomicAmount
);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

```ts
// Create order
const orderRequest = {
  rfq_id: quote.rfq_id,
  from_type: 'ONCHAIN',
  to_type: 'ONCHAIN',
  min_onchain_conf: 1,
  dest_onchain_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
  refund_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
};

const order = await client.createOrder(orderRequest);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

```ts
// Check order status
const orderId = order.order_id || order.rfq_id;
const status = await client.swapOrderStatus(orderId);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

</details>


## Market Analysis

<details>
  <summary>Discover and analyze available assets and trading pairs</summary>

```ts
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler
} from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});

// Get market data
const pairs = await client.pairList();
```

<details>
  <summary>View Response</summary>

```json

```
</details>

```ts
const assetMapper = createAssetPairMapper(pairs);
const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

// Get all assets
const allAssets = assetMapper.getAllAssets();
const activeAssets = allAssets.filter(asset => asset.is_active);
```

<details>
  <summary>View Assets</summary>

```json

```
</details>

```ts
// Get asset details
const btc = assetMapper.findByTicker('BTC');
const limits = precisionHandler.getOrderSizeLimits(btc);
const partners = assetMapper.getTradingPartners(btc.asset_id);
```

<details>
  <summary>View BTC Details</summary>

```json

```
</details>

```ts
// Get active trading pairs
const activePairs = assetMapper.getActivePairs();
```

<details>
  <summary>View Response</summary>

```json

```
</details>

</details>

## Order Monitoring

<details>
  <summary>Monitor swap order status and handle state changes</summary>

```ts
import { KaleidoClient } from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});

// Check order status
const orderId = 'your_order_id';
const status = await client.swapOrderStatus(orderId);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

```ts
// Monitor order with polling
async function monitorOrder(orderId: string) {
  const maxAttempts = 30;
  let attempts = 0;

  while (attempts < maxAttempts) {
    const status = await client.swapOrderStatus(orderId);
    
    if (status.order_state === 'COMPLETED') {
      return status;
    }
    
    if (status.order_state === 'FAILED' || status.order_state === 'EXPIRED') {
      throw new Error(`Order ${status.order_state}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 10000));
    attempts++;
  }
  
  throw new Error('Monitoring timeout');
}

const finalStatus = await monitorOrder(orderId);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

</details>

## Batch Quote Requests

<details>
  <summary>Get multiple quotes efficiently</summary>

```ts
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler
} from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});

// Initialize
const pairs = await client.pairList();
const assetMapper = createAssetPairMapper(pairs);
const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

// Define quote requests
const requests = [
  { fromTicker: 'BTC', toTicker: 'USDT', amount: 0.001 },
  { fromTicker: 'ETH', toTicker: 'USDT', amount: 0.1 },
  { fromTicker: 'USDT', toTicker: 'BTC', amount: 1000 }
];

// Get quotes with delay to avoid rate limiting
const quotes = [];
for (const req of requests) {
  const fromAsset = assetMapper.findByTicker(req.fromTicker);
  const toAsset = assetMapper.findByTicker(req.toTicker);
  
  const validation = precisionHandler.validateOrderSize(req.amount, fromAsset);
  
  const quote = await client.quoteRequest(
    fromAsset.asset_id,
    toAsset.asset_id,
    validation.atomicAmount
  );
  
  quotes.push(quote);
  
  // Wait 200ms between requests
  await new Promise(resolve => setTimeout(resolve, 200));
}
```

<details>
  <summary>View Response</summary>

```json

```
</details>

</details>

## Rate Comparison

<details>
  <summary>Compare exchange rates across multiple trading pairs</summary>

```ts
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler
} from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});

// Initialize
const pairs = await client.pairList();
const assetMapper = createAssetPairMapper(pairs);
const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

// Compare BTC rates against multiple assets
const baseTicker = 'BTC';
const targetTickers = ['USDT', 'ETH', 'LTC'];
const amount = 0.001;

const baseAsset = assetMapper.findByTicker(baseTicker);
const validation = precisionHandler.validateOrderSize(amount, baseAsset);

const rates = [];
for (const targetTicker of targetTickers) {
  const targetAsset = assetMapper.findByTicker(targetTicker);
  
  const quote = await client.quoteRequest(
    baseAsset.asset_id,
    targetAsset.asset_id,
    validation.atomicAmount
  );
  
  rates.push({
    pair: `${baseTicker}/${targetTicker}`,
    price: quote.price,
    output: precisionHandler.toDecimalAmount(quote.to_amount, targetAsset.asset_id)
  });
  
  await new Promise(resolve => setTimeout(resolve, 200));
}

// Sort by best output
rates.sort((a, b) => b.output - a.output);
```

<details>
  <summary>View Response</summary>

```json

```
</details>

</details>
