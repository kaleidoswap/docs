# Market APIs

The Market APIs provide endpoints to access information about available assets and trading pairs. These APIs are essential for users who want to explore the market data or set up trading operations.

---

## List Assets

### Endpoint
**`GET /api/v1/market/assets`**

### Description
Fetch the list of assets available for trading on the RGB Lightning Node.

### Response Structure
- **`assets`**: Array of supported assets.
  - **`asset_id`**: The unique identifier of the asset.
  - **`asset_iface`**: The interface type (e.g., `RGB20`).
  - **`ticker`**: Short name or symbol of the asset (e.g., `USDT`).
  - **`name`**: Full name of the asset (e.g., `Tether USD`).
  - **`precision`**: Decimal precision for the asset.
  - **`issued_supply`**: Total issued supply of the asset.
  - **`media`**: Additional media or metadata about the asset (optional).
  - **`is_active`**: Boolean indicating if the asset is currently active.
- **`network`**: Indicates whether the response pertains to the mainnet, testnet, or regtest.
- **`timestamp`**: The server-side timestamp when the response was generated.

### Example Response
```json
{
  "assets": [
    {
      "asset_id": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB",
      "asset_iface": "RGB20",
      "ticker": "USDT",
      "name": "Tether USD",
      "precision": 6,
      "issued_supply": 100000000000,
      "media": null,
      "is_active": true
    },
    {
      "asset_id": "rgb:2AqCRS7-BAchKZra7-nmyQz7z68-itsY6o85v-z8gQJAXMD-evdFnKz",
      "asset_iface": "RGB20",
      "ticker": "ETH",
      "name": "Ethereum",
      "precision": 8,
      "issued_supply": 100000000000,
      "media": null,
      "is_active": true
    }
  ],
  "network": "regtest",
  "timestamp": 1724676126
}
```

---

## List Trading Pairs

### Endpoint

`GET /api/v1/market/pairs`

### Description

Retrieve the list of supported trading pairs for swap operations.

### Response Structure

- `pairs`: Array of supported trading pairs.
  - `base_asset`: The base asset in the trading pair (e.g., `BTC`).
  - `base_asset_id`: The unique identifier of the base asset.
  - `quote_asset`: The quote asset in the trading pair (e.g., `USDT`).
  - `quote_asset_id`: The unique identifier of the quote asset.
  - `is_active`: Boolean indicating if the trading pair is currently active.
  - `min_order_size`: The minimum order size for this trading pair.
  - `max_order_size`: The maximum order size for this trading pair.
  - `price_precision`: Decimal precision for prices in this trading pair.
  - `quantity_precision`: Decimal precision for quantities in this trading pair.

### Example Response

```json
{
  "pairs": [
    {
      "base_asset": "BTC",
      "base_asset_id": "BTC",
      "quote_asset": "USDT",
      "quote_asset_id": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB",
      "is_active": true,
      "min_order_size": 1000,
      "max_order_size": 1000000,
      "price_precision": 2,
      "quantity_precision": 0
    },
    {
      "base_asset": "ETH",
      "base_asset_id": "rgb:2AqCRS7-BAchKZra7-nmyQz7z68-itsY6o85v-z8gQJAXMD-evdFnKz",
      "quote_asset": "BTC",
      "quote_asset_id": "BTC",
      "is_active": true,
      "min_order_size": 0.001,
      "max_order_size": 1,
      "price_precision": 0,
      "quantity_precision": 8
    },
    {
      "base_asset": "ETH",
      "base_asset_id": "rgb:2AqCRS7-BAchKZra7-nmyQz7z68-itsY6o85v-z8gQJAXMD-evdFnKz",
      "quote_asset": "USDT",
      "quote_asset_id": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB",
      "is_active": true,
      "min_order_size": 0.001,
      "max_order_size": 1,
      "price_precision": 2,
      "quantity_precision": 8
    }
  ]
}
```
---

## Request Quote for a Pair

### Endpoint
**`POST /api/v1/market/quote`**

### Description
Request a quote for a specific trading pair and amount. The response includes detailed information about the quote, including prices, fees, and expiration time.

### Request Structure

- **`pair_id`**: The unique identifier of the trading pair (obtained from the `/api/v1/market/pairs endpoint`).
- **`from_asset`**: The asset ID of the asset to swap from.
- **`from_amount`**: The amount of the base asset to swap from.
- **`to_asset`**: The asset ID of the asset to swap to.

### Example Request

```json
{
  "pair_id": "BTC_USDT",
  "from_asset": "BTC",
  "from_amount": 100000000,
  "to_asset": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB"
}
```

### Response Structure

- `rfq_id`: A unique identifier for this quote request.
- `pair_id`: The ID of the trading pair.
- `from_asset`: The asset ID being swapped from.
- `to_asset`: The asset ID being swapped to.
- `from_amount`: The amount of the base asset to be swapped.
- `to_amount`: The amount of the quote asset to be received after fees.
- `price`: The exchange rate between the base and quote assets.
- `fee`: The fee applied to the transaction, denominated in the quote asset.
- `fee_rate`: The fee rate as a percentage.
- `price_precision`: The number of decimal places for the price.
- `base_precision`: The number of decimal places for the base asset.
- `quote_precision`: The number of decimal places for the quote asset.
- `timestamp`: The server-side timestamp when the quote was generated.
- `expires_at`: The timestamp when this quote will expire.

### Example Response

```json
{
  "rfq_id": "13d4777c-ae96-4858-9c7c-3ca730c5039a",
  "pair_id": "BTC_USDT",
  "from_asset": "BTC",
  "to_asset": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB",
  "from_amount": 100000000,
  "to_amount": 5877000000,
  "price": 59507000000,
  "fee": 53000000,
  "fee_rate": 0.001,
  "price_precision": 2,
  "base_precision": 8,
  "quote_precision": 6,
  "timestamp": 1630296243,
  "expires_at": 1630296543
}
```

### Additional Notes
- The `pair_id` in the request should match an ID returned from the `/api/v1/market/pairs` endpoint.
- The `from_amount` should adhere to the `min_order_size` and `max_order_size` defined in the trading pair details.
- The `expires_at` field indicates when this quote will no longer be valid for initiating a swap.
- The `fee` is already included in the `to_amount`.
- Precision fields help clients format and display values correctly.
- The `rfq_id` can be used in subsequent swap initiation requests if the client decides to proceed with the trade.

---

## Estimate Bitcoin Fee

### Endpoint
**`GET /api/v1/market/bitcoin_fee_estimate`**

### Description
Estimate the Bitcoin fee required to include a transaction in a specified number of target blocks.

### Query Parameters
- `target_blocks` (integer, required): The number of blocks within which you aim to have the transaction confirmed.

### Example Request
```bash
GET /api/v1/market/bitcoin_fee_estimate?target_blocks=3
```

### Response Structure
- `estimated_fee_sat`: The estimated fee in satoshis required for the transaction to be confirmed within the target number of blocks.
- `target_blocks`: The number of blocks within which the fee estimate is applicable.
- `timestamp`: The server-side timestamp when the estimate was generated.

### Example Response
```json
{
  "estimated_fee_sat": 253,
  "target_blocks": 3,
  "timestamp": 1691160765
}
```

### Field Descriptions

- **`estimated_fee_sat`**: The estimated fee in satoshis needed for the transaction to be included in the next target_blocks blocks.
- **`target_blocks`**: The user-specified number of blocks within which the transaction should be confirmed.
- **`timestamp`**: The Unix timestamp indicating when the fee estimate was generated.

### Additional Notes

- Fee estimates are based on current network conditions and may vary. It's advisable to check closer to the time of transaction submission.
- If `target_blocks` is set too low, the estimated fee might be higher to ensure timely confirmation.

---

For details about swap operations, proceed to [Swap APIs](./swap-apis.md).