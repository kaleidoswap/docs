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
> Remember that BTC is not an asset on rgb and is the native coin on Bitcoin network, that's why the asset_id for BTC remians as `BTC`.

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
```
<details>
  <summary>
    Available Pairs:
  </summary>
  ```json
  {
    "pairs": [
      {
        "id": "30302cec-6a8e-4951-ba0a-2f5bf451979e",
        "base_asset": "BTC",
        "base_asset_id": "BTC",
        "base_precision": 11,
        "quote_asset": "USDT",
        "quote_asset_id": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
        "quote_precision": 6,
        "is_active": true,
        "min_base_order_size": 1000000,
        "max_base_order_size": 1000000000,
        "min_quote_order_size": 2000000,
        "max_quote_order_size": 1000000000
      },
      {
        "id": "47b20cf2-1268-4866-bf54-4556e6f49b37",
        "base_asset": "BTC",
        "base_asset_id": "BTC",
        "base_precision": 11,
        "quote_asset": "XAUT",
        "quote_asset_id": "rgb:7r5InPtB-PpkGVrA-h3vW_tB-bN3NVki-Nrj4trt-rlG42ng",
        "quote_precision": 9,
        "is_active": true,
        "min_base_order_size": 1000000,
        "max_base_order_size": 1000000000,
        "min_quote_order_size": 1000000,
        "max_quote_order_size": 1000000000
      },
      {
        "id": "7bbbc40a-e791-4103-bc59-4bf54aaa78e1",
        "base_asset": "XAUT",
        "base_asset_id": "rgb:7r5InPtB-PpkGVrA-h3vW_tB-bN3NVki-Nrj4trt-rlG42ng",
        "base_precision": 9,
        "quote_asset": "USDT",
        "quote_asset_id": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
        "quote_precision": 6,
        "is_active": true,
        "min_base_order_size": 1000000,
        "max_base_order_size": 1000000000,
        "min_quote_order_size": 1000000,
        "max_quote_order_size": 1000000000
      }
    ]
  }
  ```
</details>

```ts
// Get available assets
const assets = await client.assetList();
```

<details>
  <summary>
    Available assets:
  </summary>
  ```json
  {
    "assets": [
      {
        "asset_id": "rgb:q1O5Mn5y-7EoxdTy-xu3ChkP-HmhgGvJ-vQ3ryQ9-CcMxkfg",
        "ticker": "USDT",
        "name": "Tether USD",
        "details": null,
        "precision": 6,
        "issued_supply": 1000000000000000,
        "timestamp": 1759944618,
        "added_at": 1759944618,
        "balance": {
          "settled": 999999979729794,
          "future": 999999979729794,
          "spendable": 999999979729794,
          "offchain_outbound": 0,
          "offchain_inbound": 0
        },
        "media": null,
        "asset_iface": null,
        "is_active": true
      },
      {
        "asset_id": "rgb:7r5InPtB-PpkGVrA-h3vW_tB-bN3NVki-Nrj4trt-rlG42ng",
        "ticker": "XAUT",
        "name": "Tether Gold",
        "details": null,
        "precision": 9,
        "issued_supply": 1000000000000000,
        "timestamp": 1759944619,
        "added_at": 1759944619,
        "balance": {
          "settled": 999999750000000,
          "future": 999999750000000,
          "spendable": 999999750000000,
          "offchain_outbound": 249411646,
          "offchain_inbound": 588354
        },
        "media": null,
        "asset_iface": null,
        "is_active": true
      },
      {
        "asset_id": "rgb:hdGiSx0Q-YaV7uw1-cMbY9ED-kTu4KLP-tbWc5g0-D9Gn6MY",
        "ticker": "XAG",
        "name": "Tether Silver",
        "details": null,
        "precision": 9,
        "issued_supply": 1000000000000000,
        "timestamp": 1759944619,
        "added_at": 1759944619,
        "balance": {
          "settled": 1000000000000000,
          "future": 1000000000000000,
          "spendable": 1000000000000000,
          "offchain_outbound": 0,
          "offchain_inbound": 0
        },
        "media": null,
        "asset_iface": null,
        "is_active": true
      }
    ],
    "network": "regtest",
    "timestamp": 1760053210
  }
  ```
</details>

## Configuration Options

The `KaleidoClient` class accepts a configuration object with the following options:

```typescript
import { KaleidoClient, KaleidoConfig } from '@kaleidoswap/kaleidoswap-sdk';

const config: KaleidoConfig = {
  // *Required*  API base URL (if skipped, it defaults to using our staging node below)
  baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
  
  // Your RGB Lightning Node (required for some node operations)
  nodeUrl: '',
  
  // API key for authenticated requests (has not been implemented yet)
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

> If you set this, the SDK will automatically use `KALEIDO_API_URL` if no `baseUrl` is provided in the configuration.

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
