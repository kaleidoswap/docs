# Utilities

The KaleidoSwap SDK includes several utility classes and functions to simplify common operations like asset management, precision handling, and retry logic.

## AssetPairMapper

KaleidoSwap's SDK offers a set of utility functions for the ease of development. `createAssetPairMapper(<pairs>)` is one of them.

With our asset mapper, you can map existing supported pairs to a list of available assets that you can use in your project, and it helps you better manage trading pairs and asset relationships.

One of the experimentory methods of this function is `findByTicker(<ticker>)`, that lets you search for the `asset_id` of an asset from their `ticker`.

> Remember that this method only works in cases where there is only one ticker with a given `asset_id`. (This works as long as you're connecting to our maker node.)

### Creating an AssetPairMapper

```typescript
import { createAssetPairMapper } from 'kaleidoswap-sdk';

const pairs = await client.pairList();

const assetMapper = createAssetPairMapper(pairs);
```

### Finding Assets by Ticker

```typescript
const btc = assetMapper.findByTicker('BTC');
const usdt = assetMapper.findByTicker('USDT');

if (btc && usdt) {
  console.log(`Found BTC: ${btc.asset_id}`);
  console.log(`Found USDT: ${usdt.asset_id}`);
}

const asset = assetMapper.findById('specific_asset_id');
```

### Asset Information

```typescript
const allAssets = assetMapper.getAllAssets();

allAssets.forEach(asset => {
  console.log(`${asset.ticker} (${asset.asset_id})`);
  console.log(`  Precision: ${asset.precision}`);
  console.log(`  Min order: ${asset.min_order_size}`);
  console.log(`  Max order: ${asset.max_order_size}`);
  console.log(`  Active: ${asset.is_active}`);
});
```

### Trading Relationships

```typescript
// Check if two assets can be traded directly
const canTrade = assetMapper.canTrade('btc_asset_id', 'usdt_asset_id');
console.log(`Can trade BTC -> USDT: ${canTrade}`);

// Get all trading partners for an asset
const btcPartners = assetMapper.getTradingPartners('btc_asset_id');
console.log('BTC can be traded with:');
btcPartners.forEach(partner => {
  console.log(`  - ${partner.ticker} (${partner.asset_id})`);
});
```

### Active Trading Pairs

```typescript
// Get all active trading pairs
const activePairs = assetMapper.getActivePairs();
console.log(`${activePairs.length} active trading pairs`);

activePairs.forEach(pair => {
  console.log(`${pair.base_asset}/${pair.quote_asset}`);
});
```

### MappedAsset Interface

```typescript
interface MappedAsset {
  asset_id: string;           // Unique asset identifier
  ticker: string;             // Asset symbol (e.g., 'BTC', 'USDT')
  name: string;               // Asset name
  precision: number;          // Decimal precision
  is_active: boolean;         // Whether asset is active for trading
  min_order_size: number;     // Minimum order size (atomic units)
  max_order_size: number;     // Maximum order size (atomic units)
  trading_pairs: string[];    // Asset IDs this asset can trade with
}
```

## PrecisionHandler

The `PrecisionHandler` manages conversion between decimal amounts (user-friendly) and atomic units (API format).

### Creating a PrecisionHandler

```typescript
import { createPrecisionHandler } from 'kaleidoswap-sdk';

// Get assets from AssetPairMapper
const assets = assetMapper.getAllAssets();

// Create precision handler
const precisionHandler = createPrecisionHandler(assets);
```

### Amount Conversions

```typescript
// Convert decimal amount to atomic units
const btc = assetMapper.findByTicker('BTC');
const decimalAmount = 0.001; // 0.001 BTC

const atomicAmount = precisionHandler.toAtomicAmount(decimalAmount, btc.asset_id);
console.log(`${decimalAmount} BTC = ${atomicAmount} satoshis`);

// Convert atomic units back to decimal
const backToDecimal = precisionHandler.toDecimalAmount(atomicAmount, btc.asset_id);
console.log(`${atomicAmount} satoshis = ${backToDecimal} BTC`);
```

### Order Size Validation

```typescript
// Validate if an order size is within limits
const validation = precisionHandler.validateOrderSize(0.001, btc);

if (validation.valid) {
  console.log('Order size is valid');
  console.log(`Atomic amount: ${validation.atomicAmount}`);
} else {
  console.error('Invalid order size:', validation.error);
}

// Get the validation result structure
interface ValidationResult {
  valid: boolean;
  error?: string;
  atomicAmount: number;
  minOrderSize: number;
  maxOrderSize: number;
}
```

### Order Size Limits

```typescript
// Get human-readable order limits for an asset
const limits = precisionHandler.getOrderSizeLimits(btc);

console.log(`${btc.ticker} order limits:`);
console.log(`  Min: ${limits.minDecimal} ${btc.ticker}`);
console.log(`  Max: ${limits.maxDecimal} ${btc.ticker}`);
console.log(`  Precision: ${limits.precision} decimal places`);

// Limits interface
interface OrderSizeLimits {
  minDecimal: number;    // Minimum in decimal format
  maxDecimal: number;    // Maximum in decimal format
  minAtomic: number;     // Minimum in atomic units
  maxAtomic: number;     // Maximum in atomic units
  precision: number;     // Asset precision
}
```

### Amount Formatting

```typescript
// Format amount for display with proper decimal places
const formattedAmount = precisionHandler.formatAmount(0.00123456, btc.asset_id);
console.log(`Formatted: ${formattedAmount} BTC`); // "0.00123456 BTC"

// Get precision for an asset
const precision = precisionHandler.getPrecision(btc.asset_id);
console.log(`BTC precision: ${precision} decimal places`);
```

### Individual Validations

```typescript
// Check minimum order size only
const meetsMin = precisionHandler.validateMinOrderSize(0.001, btc);
console.log(`Meets minimum: ${meetsMin}`);

// Check maximum order size only
const meetsMax = precisionHandler.validateMaxOrderSize(0.001, btc);
console.log(`Meets maximum: ${meetsMax}`);
```

## Retry Utilities

The SDK includes retry utilities for handling transient failures.

### Basic Retry Function

```typescript
import { retry, RetryConfig } from 'kaleidoswap-sdk';

// Retry a function with default configuration
const result = await retry(async () => {
  return await client.quoteRequest('btc_id', 'usdt_id', 100000);
});
```

### Custom Retry Configuration

```typescript
const customRetryConfig: Partial<RetryConfig> = {
  maxRetries: 5,              // Maximum retry attempts
  initialDelay: 2000,         // Initial delay in milliseconds
  maxDelay: 30000,            // Maximum delay in milliseconds
  exponentialBase: 2,         // Exponential backoff multiplier
  jitter: true,               // Add random jitter to delays
  retryOnExceptions: [        // Exception types to retry on
    NetworkError,
    RateLimitError
  ]
};

const result = await retry(async () => {
  return await client.quoteRequest('btc_id', 'usdt_id', 100000);
}, customRetryConfig);
```

### Retry Wrapper Function

```typescript
import { withRetry } from 'kaleidoswap-sdk';

// Create a wrapped function with retry logic
const retryableQuoteRequest = withRetry(
  client.quoteRequest.bind(client),
  { maxRetries: 3, initialDelay: 1000 }
);

// Use the wrapped function
const quote = await retryableQuoteRequest('btc_id', 'usdt_id', 100000);
```

### RetryConfig Interface

```typescript
interface RetryConfig {
  maxRetries: number;                              // Maximum retry attempts
  initialDelay: number;                            // Initial delay in ms
  maxDelay: number;                                // Maximum delay in ms
  exponentialBase: number;                         // Exponential backoff base
  jitter: boolean;                                 // Add random jitter
  retryOnExceptions: Array<new (...args: any[]) => Error>; // Exception types to retry
}

// Default configuration
const defaultRetryConfig: RetryConfig = {
  maxRetries: 3,
  initialDelay: 1000,
  maxDelay: 10000,
  exponentialBase: 2,
  jitter: true,
  retryOnExceptions: [NetworkError, RateLimitError]
};
```

## Complete Utility Example

Here's a comprehensive example showing how to use all utilities together:

```typescript
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
  retry,
  NetworkError,
  ValidationError
} from 'kaleidoswap-sdk';

class TradingService {
  private client: KaleidoClient;
  private assetMapper: any;
  private precisionHandler: any;

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.kaleidoswap.com/api/v1'
    });
  }

  async initialize() {
    // Get pairs and create utilities
    const pairs = await retry(() => this.client.pairList());
    this.assetMapper = createAssetPairMapper(pairs);
    this.precisionHandler = createPrecisionHandler(this.assetMapper.getAllAssets());
  }

  async getValidatedQuote(
    fromTicker: string,
    toTicker: string,
    decimalAmount: number
  ) {
    // Find assets
    const fromAsset = this.assetMapper.findByTicker(fromTicker);
    const toAsset = this.assetMapper.findByTicker(toTicker);

    if (!fromAsset || !toAsset) {
      throw new ValidationError(`Asset not found: ${fromTicker} or ${toTicker}`);
    }

    // Check if trading is possible
    if (!this.assetMapper.canTrade(fromAsset.asset_id, toAsset.asset_id)) {
      throw new ValidationError(`Cannot trade ${fromTicker} -> ${toTicker}`);
    }

    // Validate amount
    const validation = this.precisionHandler.validateOrderSize(decimalAmount, fromAsset);
    if (!validation.valid) {
      throw new ValidationError(validation.error);
    }

    // Get quote with retry logic
    const quote = await retry(
      () => this.client.quoteRequest(
        fromAsset.asset_id,
        toAsset.asset_id,
        validation.atomicAmount
      ),
      { maxRetries: 3, initialDelay: 1000 }
    );

    // Convert amounts back to decimal for display
    return {
      ...quote,
      fromAmountDecimal: this.precisionHandler.toDecimalAmount(
        quote.from_amount,
        fromAsset.asset_id
      ),
      toAmountDecimal: this.precisionHandler.toDecimalAmount(
        quote.to_amount,
        toAsset.asset_id
      ),
      fromAsset,
      toAsset
    };
  }

  async getAssetInfo(ticker: string) {
    const asset = this.assetMapper.findByTicker(ticker);
    if (!asset) {
      throw new ValidationError(`Asset not found: ${ticker}`);
    }

    const limits = this.precisionHandler.getOrderSizeLimits(asset);
    const partners = this.assetMapper.getTradingPartners(asset.asset_id);

    return {
      asset,
      limits,
      tradingPartners: partners.map(p => p.ticker)
    };
  }

  async getAllAssetInfo() {
    const assets = this.assetMapper.getAllAssets();
    
    return assets.map(asset => {
      const limits = this.precisionHandler.getOrderSizeLimits(asset);
      const partners = this.assetMapper.getTradingPartners(asset.asset_id);
      
      return {
        ticker: asset.ticker,
        assetId: asset.asset_id,
        precision: asset.precision,
        isActive: asset.is_active,
        minOrder: limits.minDecimal,
        maxOrder: limits.maxDecimal,
        tradingPartners: partners.length
      };
    });
  }

  formatAmount(amount: number, assetId: string): string {
    return this.precisionHandler.formatAmount(amount, assetId);
  }

  validateAmount(amount: number, ticker: string): boolean {
    const asset = this.assetMapper.findByTicker(ticker);
    if (!asset) return false;

    const validation = this.precisionHandler.validateOrderSize(amount, asset);
    return validation.valid;
  }
}

// Usage example
async function example() {
  const tradingService = new TradingService();
  await tradingService.initialize();

  try {
    // Get asset information
    const btcInfo = await tradingService.getAssetInfo('BTC');
    console.log('BTC Info:', btcInfo);

    // Get a validated quote
    const quote = await tradingService.getValidatedQuote('BTC', 'USDT', 0.001);
    console.log('Quote:', {
      from: `${quote.fromAmountDecimal} ${quote.fromAsset.ticker}`,
      to: `${quote.toAmountDecimal} ${quote.toAsset.ticker}`,
      price: quote.price,
      rfqId: quote.rfq_id
    });

    // Get all asset information
    const allAssets = await tradingService.getAllAssetInfo();
    console.log('All assets:', allAssets);

  } catch (error) {
    if (error instanceof ValidationError) {
      console.error('Validation error:', error.message);
    } else if (error instanceof NetworkError) {
      console.error('Network error:', error.message);
    } else {
      console.error('Unexpected error:', error);
    }
  }
}
```

## Utility Best Practices

### 1. Initialize Utilities Once

```typescript
// ✅ Initialize utilities once and reuse
class AppService {
  private assetMapper: any;
  private precisionHandler: any;

  async initialize() {
    const pairs = await client.pairList();
    this.assetMapper = createAssetPairMapper(pairs);
    this.precisionHandler = createPrecisionHandler(this.assetMapper.getAllAssets());
  }
}

// ❌ Don't recreate utilities for each operation
async function badExample() {
  const pairs = await client.pairList();
  const assetMapper = createAssetPairMapper(pairs); // Recreated every time
  const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());
}
```

### 2. Always Validate Amounts

```typescript
// ✅ Always validate before API calls
const validation = precisionHandler.validateOrderSize(amount, asset);
if (validation.valid) {
  const quote = await client.quoteRequest(fromId, toId, validation.atomicAmount);
} else {
  throw new Error(validation.error);
}

// ❌ Don't skip validation
const atomicAmount = precisionHandler.toAtomicAmount(amount, assetId); // Might be invalid
const quote = await client.quoteRequest(fromId, toId, atomicAmount);
```

### 3. Handle Asset Not Found

```typescript
// ✅ Always check if assets exist
const btc = assetMapper.findByTicker('BTC');
if (!btc) {
  throw new Error('BTC asset not available');
}

// ❌ Don't assume assets exist
const btc = assetMapper.findByTicker('BTC');
const quote = await client.quoteRequest(btc.asset_id, toId, amount); // btc might be undefined
```

### 4. Use Appropriate Retry Configuration

```typescript
// ✅ Configure retries based on operation type
const quickRetry = { maxRetries: 2, initialDelay: 500 };
const robustRetry = { maxRetries: 5, initialDelay: 2000, maxDelay: 30000 };

// For quick operations
const assets = await retry(() => client.assetList(), quickRetry);

// For important operations
const quote = await retry(() => client.quoteRequest(from, to, amount), robustRetry);
```

### 5. Cache Utility Data

```typescript
// ✅ Cache asset data to reduce API calls
class CachedAssetService {
  private assetCache: Map<string, any> = new Map();
  private cacheExpiry = 5 * 60 * 1000; // 5 minutes

  async getAsset(ticker: string) {
    const cacheKey = `asset_${ticker}`;
    const cached = this.assetCache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }

    // Refresh cache
    const pairs = await client.pairList();
    const assetMapper = createAssetPairMapper(pairs);
    const asset = assetMapper.findByTicker(ticker);
    
    this.assetCache.set(cacheKey, {
      data: asset,
      timestamp: Date.now()
    });
    
    return asset;
  }
}
```
