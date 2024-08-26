![Kaleidoswap Logo](https://kaleidoswap.com/_astro/logo.23ce5f59.svg)

# Kaleidoswap API Documentation


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

The Kaleidoswap API allows interaction with an RGB Lightning Node (RLN) that provides liquidity on request and enables swap functionalities. The swap protocol operates on a taker-maker model, where clients can subscribe to trading pairs, receive real-time price updates, and initiate swaps. The API also supports the RGB LSPS1 (Lightning Service Provider Specification) for managing channels and liquidity services.

### Key Features
- **LSPS1 (Lightning Service Provider Specification) Support**: Liquidity services and swap functionalities following the modified LSPS1 protocol.
- **Real-time Market Data**: WebSocket-based subscription for price updates.
- **Swap Protocol**: Taker-maker model for initiating and executing swaps.
- **Asset and Trading Pair Management**: Comprehensive API for fetching supported assets and pairs.

## 2. Getting Started

### Base URL

#### Testnet
- **Base URL:** `https://api.testnet.kaleidoswap.com/api/v1`


#### Mainnet (Coming Soon)
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
      "max_initial_lsp_amount": 1000000,
      "min_channel_amount": 0,
      "max_channel_amount": 1000000
    }
  ]
}
```

#### 3.1.2 Create Order

##### `POST /api/v1/lsps1/create_order`

**Description:** Create a new order for a channel with the RGB Lightning Service Provider.

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

##### WebSocket: `wss://testnet.kaleidoswap.com/ws/{client_id}`

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
  "action": "priceUpdate",
  "data": {
    "buyPrice": 3000000,
    "sellPrice": 3001000,
    "markPrice": 3000500,
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "pair": "BTC/USDT",
    "size": 100000000,
    "timestamp": "2023-08-28T12:00:00Z"
  }
}
```

**Note:** 
- The server validates the requested pair against the list of available pairs. If an invalid pair is requested, the subscription will be ignored.
- Clients can subscribe to multiple pairs by sending multiple subscription messages.
- The WebSocket connection will remain open until the client disconnects or a network error occurs.

#### 3.3.3 Initiate Swap

##### `POST /api/v1/swaps/init`

**Description:** Initiate a swap based on the price update received via WebSocket.

**Request Body:**
- `request_for_quotation_id`: The ID of the price update received via WebSocket.
- `from_asset`: The asset to swap from.
- `from_amount`: The amount of the asset to swap from.
- `to_asset`: The asset to swap to.
- `to_amount`: The amount of the asset to swap to.

**Example Request:**
```json
{
  "request_for_quotation_id": "550e8400-e29b-41d4-a716-446655440000",
  "from_asset": "BTC",
  "from_amount": 100000000,
  "to_asset": "USDT",
  "to_amount": 3000000000
}
```

**Response:**
- `swapstring`: A string representing the swap to be executed.
- `payment_hash`: The payment hash associated with the swap.

**Example Response:**
```json
{
  "swapstring": "30/rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd/10/rgb:2eVw8uw-8G88LQ2tQ-kexM12SoD-nCX8DmQrw-yLMu6JDfK-xx1SCfc/1715896416/9d342c6ba006e24abee84a2e034a22d5e30c1f2599fb9c3574d46d3cde3d65a2",
  "payment_hash": "3febfae1e68b190c15461f4c2a3290f9af1dae63fd7d620d2bd61601869026cd"
}
```

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
  "swapstring": "30/rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd/10/rgb:2eVw8uw-8G88LQ2tQ-kexM12SoD-nCX8DmQrw-yLMu6JDfK-xx1SCfc/1715896416/9d342c6ba006e24abee84a2e034a22d5e30c1f2599fb9c3574d46d3cde3d65a2",
  "taker_pubkey": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
  "payment_hash": "3febfae1e68b190c15461f4c2a3290f9af1dae63fd7d620d2bd61601869026cd"
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