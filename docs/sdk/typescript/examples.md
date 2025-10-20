# Examples

Quick examples to get you started with the KaleidoSwap SDK.

## Getting a Quote

Here's how to get a price quote for swapping assets:

<details>
  <summary>View Example</summary>

```typescript
import { KaleidoClient, createAssetPairMapper, createPrecisionHandler } from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
});

// Get available trading pairs
const pairs = await client.pairList();
const assetMapper = createAssetPairMapper(pairs);

// Find the assets
const btc = assetMapper.findByTicker('BTC');
const usdt = assetMapper.findByTicker('USDT');

if (!btc || !usdt) {
  throw new Error('Assets not found');
}

// Convert 1 BTC to atomic units and get quote
const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());
const atomicAmount = precisionHandler.toAssetAmount(1, btc.asset_id);

const quote = await client.quoteRequest(
  btc.asset_id,
  usdt.asset_id,
  atomicAmount
);

// Display the quote
const receiveUSDT = precisionHandler.toAssetDecimalAmount(quote.to_amount, usdt.asset_id);
console.log(`1 BTC = ${receiveUSDT} USDT`);
```

<details>
<summary>Response Example</summary>

```json
{
  "rfq_id": "9c5ef628-811f-4c27-bf4f-d79da5ab1767",
  "from_asset": "BTC",
  "from_amount": 100000000,
  "to_asset": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
  "to_amount": 113118488,
  "price": 114261098118,
  "timestamp": 1760340000,
  "expires_at": 1760340060
}
```

</details>

</details>


## Complete Swap: USDT to BTC

This example shows the complete flow of swapping USDT for BTC, including payment monitoring.

<details>
  <summary>View Full Example</summary>

```typescript
import { KaleidoClient, createAssetPairMapper, createPrecisionHandler } from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
});

// Step 1: Get trading pairs and setup helpers
const pairs = await client.pairList();
const assetMapper = createAssetPairMapper(pairs);
const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

// Step 2: Find your assets
const usdt = assetMapper.findByTicker('USDT');
const btc = assetMapper.findByTicker('BTC');

if (!usdt || !btc) {
  throw new Error('Assets not found');
}

// Step 3: Prepare and validate the amount
const amountToSwap = 100; // 100 USDT
const validation = precisionHandler.validateOrderSize(amountToSwap, usdt);

if (!validation.valid) {
  throw new Error(validation.error);
}
```

<details>
  <summary>View Validation Result</summary>

```json
{
  "valid": true,
  "asset_amount": 100000000,
  "asset_min_amount": 1000000,
  "asset_max_amount": 1000000000000
}
```
</details>

```ts
// Step 4: Get a quote
const quote = await client.quoteRequest(
  btc.asset_id,
  usdt.asset_id,
  validation.asset_amount
);

console.log('Quote:', {
  from: `${precisionHandler.toAssetDecimalAmount(quote.from_amount, btc.asset_id)} BTC`,
  to: `${precisionHandler.toAssetDecimalAmount(quote.to_amount, usdt.asset_id)} USDT`,
  price: quote.price
});
```

<details>
  <summary>View Quote Response</summary>

```json
{
  "from": "0.001 BTC",
  "to": "113.084759 USDT",
  "price": "114227029743"
}
```
</details>

```ts
// Step 5: Create the swap order
const order = await client.createOrder({
  rfq_id: quote.rfq_id,
  from_type: 'ONCHAIN',
  to_type: 'ONCHAIN',
  min_onchain_conf: 1,
  dest_rgb_invoice: 'rgb:2whK8s5O-b1LG4rR-OhXpDq1-SjyHvKx-OhTEFjQ-aba0V_o/...',
  refund_address: 'rgb:2whK8s5O-b1LG4rR-OhXpDq1-SjyHvKx-OhTEFjQ-aba0V_o/...',
});

// Step 6: Display payment information
console.log('Order ID:', order.id);
console.log('Payment Address:', order.onchain_address);
console.log('Status:', order.status);
console.log(`Send ${precisionHandler.toAssetDecimalAmount(quote.from_amount, btc.asset_id)} BTC to complete the swap`);
```

<details>
  <summary>View Order Response</summary>

```json
{
  "id": "36f1a715-89a3-4af8-888a-af095b3275f6",
  "rfq_id": "9c5ef628-811f-4c27-bf4f-d79da5ab1767",
  "pay_in": "ONCHAIN",
  "ln_invoice": null,
  "onchain_address": "bcrt1pdhd3g2v3v58r6k2z0pr54kevs8nk2yjjskweeaw4v3f9m993rwasdu4cww",
  "rgb_recipient_id": null,
  "rgb_invoice": null,
  "status": "PENDING_PAYMENT"
}
```
</details>

```ts
// Step 7: Monitor order status
const status = await client.swapOrderStatus(order.id);
console.log('Current status:', status.status);

// Poll until completed (example with timeout)
const maxAttempts = 60;
for (let i = 0; i < maxAttempts; i++) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  const status = await client.swapOrderStatus(order.id);
  
  if (status.status === 'COMPLETED') {
    console.log('✅ Swap completed!');
    break;
  } else if (status.status === 'FAILED') {
    console.log('❌ Swap failed');
    break;
  }
}
```

<details>
  <summary>View Status Response</summary>

```json
{
  "id": "36f1a715-89a3-4af8-888a-af095b3275f6",
  "status": "PENDING_PAYMENT"
}
```
</details>

</details>

