![Kaleidoswap Logo](https://kaleidoswap.com/_astro/logo.23ce5f59.svg)

# RGB Lightning DEX API Documentation


## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Endpoints](#3-endpoints)
   - [3.1 RGB LSPS1 APIs](#31-rgb-lsps1-apis)
   - [3.2 Market APIs](#32-market-apis)
   - [3.3 Swap APIs](#33-swap-apis)
4. [Error Handling](#4-error-handling)
5. [License](#5-license)

## 1. Introduction

The RGB Lightning DEX API allows interaction with an RGB Lightning Node (RLN) that provides liquidity on request and enables swap functionalities. The swap protocol operates on a taker-maker model, where clients can subscribe to trading pairs, receive real-time price updates, and initiate swaps. The API also supports the RGB LSPS1 (Lightning Service Provider Specification) for managing channels and liquidity services.

### Key Features
- **RGB LSPS1**: Liquidity services following the modified LSPS1 protocol.
- **Real-time Market Data**: WebSocket-based subscription for price updates.
- **Swap Protocol**: Taker-maker model for initiating and executing swaps.
- **Asset and Trading Pair Management**: Comprehensive API for fetching supported assets and pairs.

## 2. Getting Started

### Base URL

#### Bitcoin Testnet4
- **Base URL:** `https://api.testnet.kaleidoswap.com/api/v1`


#### Bitcoin Mainnet (Coming Soon)
- **Base URL:** `https://api.kaleidoswap.com/api/v1`


All API requests in the test environment should be sent to the base URL provided above.

### Authentication

Currently, the API does not require authentication for its endpoints. Future versions may introduce authentication mechanisms.

### API Versioning

The current API version is v1, reflected in the base URL.

## 3. Endpoints

### 3.1 RGB LSPS1 APIs

#### 3.1.1 Get LSP Information

##### `GET /api/v1/lsps1/get_info`

**Description:** Retrieve information about the RGB Lightning Service Provider, including available assets, liquidity options, and order options.

**Response:**
- `options`: Configuration settings for orders and channels.
- `assets`: List of assets managed by the LSP.

**Example Response:**
```json
{
  "options": {
    "min_required_channel_confirmations": 0,
    "min_funding_confirms_within_blocks": 0,
    "min_onchain_payment_confirmations": 0,
    "supports_zero_channel_reserve": true,
    "min_onchain_payment_size_sat": 0,
    "max_channel_expiry_blocks": 30160,
    "min_initial_client_balance_sat": 0,
    "max_initial_client_balance_sat": 100000000,
    "min_initial_lsp_balance_sat": 0,
    "max_initial_lsp_balance_sat": 100000000,
    "min_channel_balance_sat": 50000,
    "max_channel_balance_sat": 100000000
  },
  "assets": [
    {
      "name": "Tether USD",
      "asset_id": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB",
      "ticker": "USDT",
      "precision": 6,
      "issued_supply": 100000000000,
      "min_initial_client_amount": 0,
      "max_initial_client_amount": 0,
      "min_initial_lsp_amount": 0,
      "max_initial_lsp_amount": 1000000000,
      "min_channel_amount": 0,
      "max_channel_amount": 1000000000
    }
  ]
}
```

#### 3.1.2 Create Order

##### `POST /api/v1/lsps1/create_order`

**Description:** Create a new order request for a channel with the RGB Lightning Service Provider.

**Request Body:**
- `client_pubkey`: The public key of the client (not spec compliant, but required in this implementation).
- `lsp_balance_sat`: The balance in satoshis for the LSP side of the channel.
- `client_balance_sat`: The balance in satoshis for the client side of the channel.
- `required_channel_confirmations`: The number of confirmations required for the channel.
- `funding_confirms_within_blocks`: The number of blocks within which funding should be confirmed.
- `channel_expiry_blocks`: The number of blocks after which the channel expires.
- `token`: (Optional) A token for the order.
- `refund_onchain_address`: (Optional) An on-chain address for refunds.
- `announce_channel`: Whether to announce the channel publicly.
- `asset_id`: (Optional) The ID of the RGB asset for the channel.
- `lsp_asset_amount`: (Optional) The amount of RGB asset for the LSP side.
- `client_asset_amount`: (Optional) The amount of RGB asset for the client side.

**Example Request:**
```json
{
  "client_pubkey": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
  "lsp_balance_sat": 100000,
  "client_balance_sat": 50000,
  "required_channel_confirmations": 3,
  "funding_confirms_within_blocks": 144,
  "channel_expiry_blocks": 4032,
  "announce_channel": true,
  "asset_id": "rgb:$i4cFKwt-2C5LZ3X-l$kOTGN-O6l1AOP-aP9COyn-7IeBkEM",
  "lsp_asset_amount": 5000,
  "client_asset_amount": 2500
}
```

**Response:**
- `order_id`: Unique identifier for the created order.
- `client_pubkey`: The public key of the client.
- `lsp_balance_sat`: The balance in satoshis for the LSP side of the channel.
- `client_balance_sat`: The balance in satoshis for the client side of the channel.
- `required_channel_confirmations`: The number of confirmations required for the channel.
- `funding_confirms_within_blocks`: The number of blocks within which funding should be confirmed.
- `channel_expiry_blocks`: The number of blocks after which the channel expires.
- `token`: The token associated with the order (if provided).
- `created_at`: Timestamp of order creation.
- `expires_at`: Timestamp when the order expires.
- `announce_channel`: Whether the channel will be announced publicly.
- `order_state`: Current state of the order (e.g., "CREATED").
- `payment`: Payment details including fees, invoice, and on-chain address.
- `channel`: (Optional) Channel details if the channel has been created.
- `asset_id`: (Optional) The ID of the RGB asset for the channel.
- `lsp_asset_amount`: (Optional) The amount of RGB asset for the LSP side.
- `client_asset_amount`: (Optional) The amount of RGB asset for the client side.

**Example Response:**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "client_pubkey": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
  "lsp_balance_sat": 100000,
  "client_balance_sat": 50000,
  "required_channel_confirmations": 3,
  "funding_confirms_within_blocks": 144,
  "channel_expiry_blocks": 4032,
  "token": "",
  "created_at": "2023-08-28T12:00:00Z",
  "expires_at": "2023-08-28T13:00:00Z",
  "announce_channel": true,
  "order_state": "CREATED",
  "payment": {
    "state": "EXPECT_PAYMENT",
    "fee_total_sat": 1500,
    "order_total_sat": 151500,
    "bolt11_invoice": "lnbc1515000n1...",
    "onchain_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "min_onchain_payment_confirmations": 0,
    "min_fee_for_0conf": 253
  },
  "asset_id": "rgb:$i4cFKwt-2C5LZ3X-l$kOTGN-O6l1AOP-aP9COyn-7IeBkEM",
  "lsp_asset_amount": 5000,
  "client_asset_amount": 2500
}
```

#### 3.1.3 Get Order

##### `POST /api/v1/lsps1/get_order`

**Description:** Retrieve information about an existing order.

**Request Body:**
- `order_id`: The unique identifier of the order to retrieve.

**Example Request:**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:** The response structure is identical to the response of the `create_order` endpoint.

### 3.2 Market APIs

#### 3.2.1 List Assets

##### `GET /api/v1/market/assets`

**Description:** Fetch the list of assets available for trading on the RGB Lightning Node.

**Response:**
- `assets`: Array of supported assets, including their IDs, tickers, names, and other details.
- `network`: Indicates whether the response pertains to the mainnet or testnet.
- `timestamp`: The server-side timestamp of the response.

**Example Response:**
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

#### 3.2.2 List Trading Pairs

##### `GET /api/v1/market/pairs`

**Description:** Retrieve the list of supported trading pairs for swap operations.

**Response:**
- `pairs`: Array of supported trading pairs, including details about base and quote assets, order size limits, and precision.

**Example Response:**
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
#### 3.2.3 Request Quote for a Pair

##### `POST /api/v1/market/quote`

**Description:** Request a quote for a specific trading pair and amount. The response includes detailed information about the quote, including prices, fees, and expiration time.

**Request Body:**
- `pair_id`: The unique identifier of the trading pair (obtained from the `/api/v1/market/pairs` endpoint).
- `from_asset`: The asset ID of the asset to swap from.
- `from_amount`: The amount of the base asset to swap from.
- `to_asset`: The asset ID of the asset to swap to.


**Example Request:**
```json
{
  "pair_id": "BTC_USDT",
  "from_asset": "BTC",
  "from_amount": 100000000,
  "to_asset": "rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB"
}
```

**Response:**
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

**Example Response:**
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

**Additional Notes:**
- The `pair_id` in the request should match an ID returned from the `/api/v1/market/pairs` endpoint.
- The `from_amount` should adhere to the `min_order_size` and `max_order_size` defined in the trading pair details.
- The `expires_at` field indicates when this quote will no longer be valid for initiating a swap.
- The `fee` is already included in the `to_amount`.
- Precision fields help clients format and display values correctly.
- The `rfq_id` can be used in subsequent swap initiation requests if the client decides to proceed with the trade.
- 
#### **3.2.4 Estimate Bitcoin Fee**

##### `GET /api/v1/market/bitcoin_fee_estimate`

**Description:** Estimate the Bitcoin fee required to include a transaction in a specified number of target blocks.

**Query Parameters:**
- `target_blocks` (integer, required): The number of blocks within which you aim to have the transaction confirmed.

**Example Request:**
```
GET /api/v1/market/bitcoin_fee_estimate?target_blocks=3
```

**Response:**
- `estimated_fee_sat`: The estimated fee in satoshis required for the transaction to be confirmed within the target number of blocks.
- `target_blocks`: The number of blocks within which the fee estimate is applicable.
- `timestamp`: The server-side timestamp when the estimate was generated.

**Example Response:**
```json
{
  "estimated_fee_sat": 253,
  "target_blocks": 3,
  "timestamp": 1691160765
}
```

**Field Descriptions:**
- **`estimated_fee_sat`**: The estimated fee in satoshis needed for the transaction to be included in the next `target_blocks` blocks.
- **`target_blocks`**: The user-specified number of blocks within which the transaction should be confirmed.
- **`timestamp`**: The Unix timestamp indicating when the fee estimate was generated.

**Additional Notes:**
- Fee estimates are based on current network conditions and may vary. It's advisable to check closer to the time of transaction submission.
- If `target_blocks` is set too low, the estimated fee might be higher to ensure timely confirmation.


---

### 3.3 Swap APIs

#### 3.3.1 Get Node Information

##### `GET /api/v1/swaps/nodeinfo`

**Description:** Retrieve information about the RGB Lightning Node.

**Response:**
- Various node information details.

**Example Response:**
```json
{
  "node_id": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
  "alias": "RGB-LSP-Node",
  "color": "#000000",
  "num_peers": 5,
  "num_channels": 10,
  "block_height": 700000,
  "synced_to_chain": true
}
```

#### 3.3.2 Real-time Price Updates

##### Testnet WebSocket (not-active): `wss://testnet.api.kaleidoswap.com/ws/{client_id}`
##### Mainnet WebSocket (not-active): `wss://api.kaleidoswap.com/ws/{client_id}`

**Description:** Establish a WebSocket connection to subscribe to real-time price updates for specific trading pairs.

**Connection:**
- Replace `{client_id}` with a unique identifier for your client.

**Subscription:**
To subscribe to a trading pair, send a JSON message with the following format:

```json
{
  "action": "subscribe",
  "pair": "BTC/USDT"
}
```

To unsubscribe from a trading pair:

```json
{
  "action": "unsubscribe",
  "pair": "BTC/USDT"
}
```

**Response:** 
The server will stream JSON objects with price updates for subscribed pairs:

```json
{
  "action": "price_update",
  "data": {
    "rfq_id": "13d4777c-ae96-4858-9c7c-3ca730c5039a",
    "price_buy": 59507000000,
    "price_sell": 59508000000,
    "fee_base": 100,
    "fee_rate": 0.1,
    "price_precision": 6,
    "base_precision": 8,
    "pair": "BTC/USDT",
    "timestamp": 1630296243,
    "expires_at": 1630296248
  }
}
```

**Field Descriptions:**

- **`rfq_id`**: The `request_for_quotation_id`, a unique identifier generated by the maker. This ID is crucial for initiating swaps and must be passed in the `init` endpoint.
  
- **`price_buy`**: The buy price for the trading pair. 
- 
- **`price_sell`**: The sell price for the trading pair.

- **`price_precision`**: The number of decimal places to which the price is quoted, relevant to the quote asset. For example, if `pricePrecision` is `6` for the BTC/USDT pair, it indicates that the USDT is quoted to six decimal places.

- **`base_precision`**:  The number of decimal places to which the base asset is quoted. For example, if `basePrecision` is `8` for the BTC/USDT pair, it indicates that BTC is quoted to eight decimal places.

- **`pair`**: The trading pair, such as BTC/USDT.

- **`timestamp`**: The timestamp when the price update was generated in unix time.

- **`expires_at`**: The timestamp when the `rfqId` will expire in unix time.



**Price Precision Note:**
- Prices provided in the response do not reflect the precision of the base asset. For instance, in a BTC/USDT pair, the base asset (BTC) is always denominated in satoshis, and the quote asset (USDT) price precision is found in the update. For example, a `buyPrice` of `59507000000` unit for a size of `100000000` sats (1 BTC) corresponds to `59507` USDT, considering the `pricePrecision` of `8`.

**Additional Notes:**
- The server validates the requested pair against the list of available pairs. If an invalid pair is requested, the subscription will be ignored.
- When BTC is in a pair, it is always denominated in satoshis (sats) with a precision of `0`.
- Clients can subscribe to multiple pairs by sending multiple subscription messages.
- The WebSocket connection will remain open until the client disconnects or a network error occurs.

---

#### 3.3.3 Initiate Swap

##### `POST /api/v1/swaps/init`

**Description:** Initiate a swap based on the price update received via WebSocket.

**Request Body:**
- `rfq_id`: The ID of the price update received via WebSocket.
- `from_asset`: The RGB asset ID to swap from.
- `from_amount`: The amount of the asset to swap from. If the asset is BTC, the amount should be specified in **millisatoshis (msat)**. For other assets, the amount should be provided in the asset’s native unit without considering precision.
- `to_asset`: The RGB asset ID to swap to.
- `to_amount`: The amount of the asset to swap to. If the asset is BTC, the amount should be specified in **millisatoshis (msat)**. For other assets, the amount should be provided in the asset’s native unit without considering precision.

**Example Request:**
```json
{
  "rfq_id": "8e6635fb-ab37-4aed-89f4-bc9c98fb8b49",
  "from_asset": "btc", 
  "from_amount": 1000000, 
  "to_asset": "rgb:2V2f58W-Tabtk3J4j-qGVQQwPWt-ksbujLNxx-x1BMTNBEf-KVsg2j3",
  "to_amount": 587770
}
```

**Response:**
- `swapstring`: A string representing the swap to be executed.
- `payment_hash`: The payment hash associated with the swap.

**Example Response:**
```json
{
  "swapstring": "1000000/btc/587770/rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB/be35403fcd85722cb0373db0527a452ce9c2eb23d3ec489af8e33ffb57d5271e",
  "payment_hash": "be35403fcd85722cb0373db0527a452ce9c2eb23d3ec489af8e33ffb57d5271e"
}
```

**Note:** 
- The precision for an RGB asset can be obtained using the  [`/assets`](#321-list-assets) API on the maker's node. If the client has the same asset, the precision can also be retrieved via the node API.
- The swapstring returned by this endpoint needs to be whitelisted using the `/taker` API of the RGB Lightning Node (RLN) of the client before executing the swap.
- In this example, the user is selling 1,000 sats for 0.5877 USDT (using the RGB asset rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB).


#### 3.3.4 Execute Swap

##### `POST /api/v1/swaps/execute`

**Description:** Execute the swap after the initial setup.

**Request Body:**
- `swapstring`: The swap string generated by the `init` endpoint.
- `taker_pubkey`: The public key of the taker.
- `payment_hash`: The payment hash associated with the swap.

**Example Request:**
```json
{
  "swapstring": "1000000/btc/587770/rgb:2NZGjyz-pJePUgegh-RLHbpx1Hy-iZMagWiZZ-qY4AxGymW-yCEYwwB/be35403fcd85722cb0373db0527a452ce9c2eb23d3ec489af8e33ffb57d5271e",
  "taker_pubkey": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
  "payment_hash": "be35403fcd85722cb0373db0527a452ce9c2eb23d3ec489af8e33ffb57d5271e"
}
```

**Response:**
- `status`: Status code of the swap execution.
- `message`: Additional details about the execution.

**Example Response:**
```json
{
  "status": 200,
  "message": "Swap executed successfully"
}
```

#### **3.3.5 Get Swap Status**

##### `GET /api/v1/swaps/status`

**Description:** Retrieve the current status of a swap using the associated `payment_hash`.

**Query Parameters:**
- `payment_hash` (string, required): The payment hash of the swap whose status is to be retrieved.

**Example Request:**
```
GET /api/v1/swaps/status?payment_hash=7c2c95b9c2aa0a7d140495b664de7973b76561de833f0dd84def3efa08941664
```

**Response:**
- `swap`: An object containing detailed information about the swap.

**Example Response:**
```json
{
  "swap": {
    "qty_from": 1000000,
    "qty_to": 587770,
    "from_asset": "btc",
    "to_asset": "rgb:2V2f58W-Tabtk3J4j-qGVQQwPWt-ksbujLNxx-x1BMTNBEf-KVsg2j3",
    "payment_hash": "7c2c95b9c2aa0a7d140495b664de7973b76561de833f0dd84def3efa08941664",
    "status": "Pending",
    "requested_at": 1691160765,
    "initiated_at": 1691168512,
    "expires_at": 1691172703,
    "completed_at": 1691171075
  }
}
```

**Swap Object Schema:**
- **`qty_from`** (`integer`): The quantity of the asset being swapped from. Example: `30`
- **`qty_to`** (`integer`): The quantity of the asset being swapped to. Example: `10`
- **`from_asset`** (`string`): The RGB asset ID being swapped from. Example: `rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd`
- **`to_asset`** (`string`): The RGB asset ID being swapped to. Example: `rgb:2eVw8uw-8G88LQ2tQ-kexM12SoD-nCX8DmQrw-yLMu6JDfK-xx1SCfc`
- **`payment_hash`** (`string`): The unique payment hash associated with the swap. Example: `7c2c95b9c2aa0a7d140495b664de7973b76561de833f0dd84def3efa08941664`
- **`status`** (`SwapStatus`): The current status of the swap. Possible values:
  - `Waiting`
  - `Pending`
  - `Succeeded`
  - `Expired`
  - `Failed`
- **`requested_at`** (`integer`): Unix timestamp when the swap was requested. Example: `1691160765`
- **`initiated_at`** (`integer`): Unix timestamp when the swap was initiated. Example: `1691168512`
- **`expires_at`** (`integer`): Unix timestamp when the swap expires. Example: `1691172703`
- **`completed_at`** (`integer`): Unix timestamp when the swap was completed. Example: `1691171075`

**Additional Notes:**
- The `status` field provides real-time updates on the swap's progress.
- Ensure that the `payment_hash` provided is accurate to retrieve the correct swap status.
- Time-related fields are in Unix timestamp format.
- The `SwapStatus` field in the `Swap` object can have one of the following values:
  - **`Waiting`**: The swap is awaiting initiation.
  - **`Pending`**: The swap has been initiated and is currently in progress.
  - **`Succeeded`**: The swap has been successfully completed.
  - **`Expired`**: The swap was not completed within the required timeframe.
  - **`Failed`**: The swap encountered an error and did not complete successfully.

---

## 4. Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request. Errors are returned in the following format:

```json
{
  "detail": "Error message here"
}
```

### Common Errors

- `400 Bad Request`: The request parameters are invalid or missing.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An unexpected error occurred on the server.

For WebSocket connections, errors will be sent as JSON messages through the WebSocket, and in case of critical errors, the connection may be closed by the server.

## 5. License

This API is licensed under the MIT License. For more information, please refer to the LICENSE file in the repository.

---

Feel free to open an issue or submit a pull request for any suggestions or improvements to this documentation.
