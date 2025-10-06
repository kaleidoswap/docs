# Examples

This guide provides complete, working examples for common use cases with the KaleidoSwap SDK.

## Basic Quote Example

Get a simple price quote for swapping assets.

```typescript
import { KaleidoClient, QuoteError, NetworkError } from 'kaleidoswap-sdk';

async function getBasicQuote() {
  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
  });

  try {
    // Get available pairs first
    const pairs = await client.pairList();
    console.log(`Found ${pairs.pairs.length} trading pairs`);

    // Find a BTC/USDT pair
    const btcUsdtPair = pairs.pairs.find(pair => 
      pair.base_asset === 'BTC' && pair.quote_asset === 'USDT'
    );

    if (!btcUsdtPair) {
      console.log('BTC/USDT pair not available');
      return;
    }

    // Request quote for 0.001 BTC (100,000 satoshis)
    const quote = await client.quoteRequest(
      btcUsdtPair.base_asset_id,
      btcUsdtPair.quote_asset_id,
      100000
    );

    console.log('Quote received:');
    console.log(`- From: ${quote.from_amount} satoshis`);
    console.log(`- To: ${quote.to_amount} USDT units`);
    console.log(`- Price: ${quote.price}`);
    console.log(`- RFQ ID: ${quote.rfq_id}`);
    console.log(`- Expires: ${quote.expires_at}`);

  } catch (error) {
    if (error instanceof QuoteError) {
      console.error('Quote failed:', error.message);
    } else if (error instanceof NetworkError) {
      console.error('Network error:', error.message);
    } else {
      console.error('Unexpected error:', error);
    }
  }
}

getBasicQuote();
```

## Complete Swap Example

A comprehensive example showing the full swap workflow with proper error handling and precision management.

```typescript
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
  SwapError,
  TimeoutError,
  ValidationError
} from 'kaleidoswap-sdk';

async function performCompleteSwap() {
  console.log('Starting BTC to USDT swap...\n');

  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
  });

  try {
    // Step 1: Initialize utilities
    console.log('1. Fetching trading pairs...');
    const pairs = await client.pairList();
    const assetMapper = createAssetPairMapper(pairs);
    const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

    // Step 2: Find and validate assets
    console.log('2. Finding assets...');
    const btc = assetMapper.findByTicker('BTC');
    const usdt = assetMapper.findByTicker('USDT');

    if (!btc || !usdt) {
      throw new ValidationError('BTC or USDT not found');
    }

    console.log(`Found: ${btc.ticker} (${btc.asset_id})`);
    console.log(`Found: ${usdt.ticker} (${usdt.asset_id})`);

    // Step 3: Check trading pair availability
    if (!assetMapper.canTrade(btc.asset_id, usdt.asset_id)) {
      throw new ValidationError('No trading pair between BTC and USDT');
    }

    // Step 4: Validate amount
    const decimalAmount = 0.001; // 0.001 BTC
    console.log(`\n3. Validating amount: ${decimalAmount} ${btc.ticker}`);

    const validation = precisionHandler.validateOrderSize(decimalAmount, btc);
    if (!validation.valid) {
      throw new ValidationError(validation.error);
    }

    console.log(`✓ Amount validation passed`);
    console.log(`  Decimal: ${decimalAmount} ${btc.ticker}`);
    console.log(`  Atomic: ${validation.atomicAmount} units`);

    // Step 5: Get quote
    console.log('\n4. Getting quote...');
    const quote = await client.quoteRequest(
      btc.asset_id,
      usdt.asset_id,
      validation.atomicAmount
    );

    // Convert amounts for display
    const fromDecimal = precisionHandler.toDecimalAmount(quote.from_amount, btc.asset_id);
    const toDecimal = precisionHandler.toDecimalAmount(quote.to_amount, usdt.asset_id);

    console.log('✓ Quote received:');
    console.log(`  From: ${fromDecimal} ${btc.ticker}`);
    console.log(`  To: ${toDecimal} ${usdt.ticker}`);
    console.log(`  Price: ${quote.price}`);
    console.log(`  RFQ ID: ${quote.rfq_id}`);

    // Step 6: Create order
    console.log('\n5. Creating swap order...');
    const orderRequest = {
      rfq_id: quote.rfq_id,
      from_type: 'ONCHAIN' as const,
      to_type: 'ONCHAIN' as const,
      min_onchain_conf: 1,
      dest_onchain_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
      refund_address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
      client_pubkey: '02' + '0'.repeat(64),
      lsp_balance_sat: 0,
      client_balance_sat: 0,
      required_channel_confirmations: 1,
      funding_confirms_within_blocks: 144,
      channel_expiry_blocks: 1008,
      announce_channel: true
    };

    const order = await client.createOrder(orderRequest);
    console.log('✓ Order created:');
    console.log(`  Order ID: ${order.order_id || order.rfq_id}`);
    console.log(`  Status: ${order.order_state || order.status}`);

    // Step 7: Monitor order (simplified for example)
    console.log('\n6. Monitoring order status...');
    const orderId = order.order_id || order.rfq_id;
    
    // In a real application, you'd want to monitor continuously
    setTimeout(async () => {
      try {
        const status = await client.swapOrderStatus(orderId);
        console.log(`Order status: ${status.order_state || 'Unknown'}`);
      } catch (error) {
        console.log('Status check failed:', error);
      }
    }, 5000);

    console.log('\n✅ Swap initiated successfully!');
    console.log(`Monitor your order with ID: ${orderId}`);

  } catch (error) {
    console.error('\n❌ Swap failed:');
    
    if (error instanceof ValidationError) {
      console.error('Validation error:', error.message);
    } else if (error instanceof SwapError) {
      console.error('Swap error:', error.message);
    } else if (error instanceof TimeoutError) {
      console.error('Timeout error:', error.message);
    } else {
      console.error('Unexpected error:', error);
    }
  }
}

performCompleteSwap();
```

## WebSocket Real-time Quotes

Example showing how to get real-time quotes using WebSocket connections.

```typescript
import { 
  KaleidoClient,
  WebSocketClient,
  WebSocketError,
  TimeoutError
} from 'kaleidoswap-sdk';

class RealtimeQuoteService {
  private client: KaleidoClient;
  private wsClient: WebSocketClient;
  private isConnected = false;

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
      wsUrl: 'wss://api.staging.kaleidoswap.com/ws'
    });

    this.wsClient = new WebSocketClient({
      baseUrl: 'wss://api.staging.kaleidoswap.com/ws',
      reconnectInterval: 5000,
      maxReconnectAttempts: 5
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers() {
    this.wsClient.on('quote_response', (data) => {
      console.log('📈 Real-time quote received:', {
        from: data.from_asset,
        to: data.to_asset,
        price: data.price,
        timestamp: new Date().toISOString()
      });
    });

    this.wsClient.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.wsClient.on('reconnected', () => {
      console.log('🔄 WebSocket reconnected');
      this.isConnected = true;
    });
  }

  async connect() {
    try {
      await this.wsClient.connect();
      this.isConnected = true;
      console.log('✅ WebSocket connected');
    } catch (error) {
      console.error('❌ WebSocket connection failed:', error);
      throw error;
    }
  }

  async getRealtimeQuote(fromAsset: string, toAsset: string, amount: number) {
    try {
      // Try WebSocket first
      const quote = await this.client.quoteRequestWS(fromAsset, toAsset, amount);
      console.log('📡 WebSocket quote received');
      return quote;
    } catch (error) {
      if (error instanceof WebSocketError || error instanceof TimeoutError) {
        console.log('⚠️ WebSocket failed, falling back to HTTP');
        return await this.client.quoteRequest(fromAsset, toAsset, amount);
      }
      throw error;
    }
  }

  async subscribeToUpdates(pairId: string) {
    if (!this.isConnected) {
      await this.connect();
    }

    await this.wsClient.subscribe(pairId);
    console.log(`📺 Subscribed to ${pairId} updates`);
  }

  async disconnect() {
    await this.wsClient.disconnect();
    this.isConnected = false;
    console.log('👋 WebSocket disconnected');
  }
}

// Usage example
async function realtimeQuoteExample() {
  const quoteService = new RealtimeQuoteService();

  try {
    await quoteService.connect();

    // Get a one-time real-time quote
    const quote = await quoteService.getRealtimeQuote(
      'btc_asset_id',
      'usdt_asset_id',
      100000
    );
    console.log('Quote:', quote);

    // Subscribe to live updates
    await quoteService.subscribeToUpdates('BTC_USDT');

    // Keep connection alive for 30 seconds
    setTimeout(async () => {
      await quoteService.disconnect();
    }, 30000);

  } catch (error) {
    console.error('Real-time quote example failed:', error);
  }
}

realtimeQuoteExample();
```

## Asset Discovery and Analysis

Example showing how to discover and analyze available assets and trading pairs.

```typescript
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler
} from 'kaleidoswap-sdk';

async function analyzeMarket() {
  const client = new KaleidoClient({
    baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
  });

  try {
    console.log('🔍 Analyzing KaleidoSwap market...\n');

    // Get market data
    const pairs = await client.pairList();
    const assetMapper = createAssetPairMapper(pairs);
    const precisionHandler = createPrecisionHandler(assetMapper.getAllAssets());

    // Analyze assets
    const allAssets = assetMapper.getAllAssets();
    const activeAssets = allAssets.filter(asset => asset.is_active);

    console.log(`📊 Market Overview:`);
    console.log(`  Total assets: ${allAssets.length}`);
    console.log(`  Active assets: ${activeAssets.length}`);
    console.log(`  Trading pairs: ${pairs.pairs.length}`);
    console.log();

    // Show asset details
    console.log('💰 Available Assets:');
    activeAssets.forEach(asset => {
      const limits = precisionHandler.getOrderSizeLimits(asset);
      const partners = assetMapper.getTradingPartners(asset.asset_id);
      
      console.log(`\n  ${asset.ticker} (${asset.name})`);
      console.log(`    Asset ID: ${asset.asset_id}`);
      console.log(`    Precision: ${asset.precision} decimal places`);
      console.log(`    Order range: ${limits.minDecimal} - ${limits.maxDecimal} ${asset.ticker}`);
      console.log(`    Trading partners: ${partners.length}`);
      
      if (partners.length > 0) {
        const partnerTickers = partners.map(p => p.ticker).join(', ');
        console.log(`    Can trade with: ${partnerTickers}`);
      }
    });

    // Find most connected assets
    console.log('\n🔗 Most Connected Assets:');
    const assetConnections = activeAssets
      .map(asset => ({
        ticker: asset.ticker,
        connections: assetMapper.getTradingPartners(asset.asset_id).length
      }))
      .sort((a, b) => b.connections - a.connections)
      .slice(0, 5);

    assetConnections.forEach((asset, index) => {
      console.log(`  ${index + 1}. ${asset.ticker}: ${asset.connections} trading pairs`);
    });

    // Show active trading pairs
    console.log('\n📈 Active Trading Pairs:');
    const activePairs = assetMapper.getActivePairs();
    activePairs.slice(0, 10).forEach(pair => {
      console.log(`  ${pair.base_asset}/${pair.quote_asset}`);
    });

    if (activePairs.length > 10) {
      console.log(`  ... and ${activePairs.length - 10} more pairs`);
    }

    // Test a specific trading path
    console.log('\n🛤️  Testing BTC Trading Paths:');
    const btc = assetMapper.findByTicker('BTC');
    if (btc) {
      const btcPartners = assetMapper.getTradingPartners(btc.asset_id);
      console.log(`  BTC can trade directly with ${btcPartners.length} assets:`);
      btcPartners.forEach(partner => {
        console.log(`    BTC → ${partner.ticker}`);
      });
    } else {
      console.log('  BTC not found in available assets');
    }

  } catch (error) {
    console.error('❌ Market analysis failed:', error);
  }
}

analyzeMarket();
```

## Order Monitoring

Example showing how to monitor swap orders and handle different states.

```typescript
import { 
  KaleidoClient,
  SwapError,
  TimeoutError
} from 'kaleidoswap-sdk';

class OrderMonitor {
  private client: KaleidoClient;
  private monitoringOrders = new Map<string, NodeJS.Timeout>();

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
    });
  }

  async monitorOrder(
    orderId: string,
    onStatusChange?: (status: string) => void,
    timeoutMinutes = 30
  ): Promise<any> {
    console.log(`📊 Starting to monitor order: ${orderId}`);

    return new Promise((resolve, reject) => {
      const startTime = Date.now();
      const timeoutMs = timeoutMinutes * 60 * 1000;
      let attempts = 0;

      const checkStatus = async () => {
        try {
          attempts++;
          const status = await this.client.swapOrderStatus(orderId);
          const currentStatus = status.order_state || status.status || 'Unknown';
          
          console.log(`[${attempts}] Order ${orderId}: ${currentStatus}`);
          
          if (onStatusChange) {
            onStatusChange(currentStatus);
          }

          // Check for terminal states
          if (currentStatus === 'COMPLETED' || currentStatus === 'Succeeded') {
            console.log('✅ Order completed successfully');
            this.stopMonitoring(orderId);
            resolve(status);
            return;
          }

          if (currentStatus === 'FAILED' || currentStatus === 'Failed') {
            console.log('❌ Order failed');
            this.stopMonitoring(orderId);
            reject(new SwapError(`Order failed: ${currentStatus}`));
            return;
          }

          if (currentStatus === 'EXPIRED' || currentStatus === 'Expired') {
            console.log('⏰ Order expired');
            this.stopMonitoring(orderId);
            reject(new SwapError(`Order expired: ${currentStatus}`));
            return;
          }

          // Check timeout
          if (Date.now() - startTime >= timeoutMs) {
            console.log('⏱️ Monitoring timeout reached');
            this.stopMonitoring(orderId);
            reject(new TimeoutError(`Order monitoring timed out after ${timeoutMinutes} minutes`));
            return;
          }

          // Schedule next check
          const timer = setTimeout(checkStatus, 10000); // Check every 10 seconds
          this.monitoringOrders.set(orderId, timer);

        } catch (error) {
          console.error(`❌ Error checking order status:`, error);
          
          // Continue monitoring unless it's a critical error
          if (error instanceof SwapError) {
            this.stopMonitoring(orderId);
            reject(error);
          } else {
            // Network error, retry
            const timer = setTimeout(checkStatus, 15000); // Wait longer on error
            this.monitoringOrders.set(orderId, timer);
          }
        }
      };

      // Start monitoring
      checkStatus();
    });
  }

  stopMonitoring(orderId: string) {
    const timer = this.monitoringOrders.get(orderId);
    if (timer) {
      clearTimeout(timer);
      this.monitoringOrders.delete(orderId);
      console.log(`🛑 Stopped monitoring order: ${orderId}`);
    }
  }

  stopAllMonitoring() {
    for (const [orderId, timer] of this.monitoringOrders) {
      clearTimeout(timer);
      console.log(`🛑 Stopped monitoring order: ${orderId}`);
    }
    this.monitoringOrders.clear();
  }

  getMonitoredOrders(): string[] {
    return Array.from(this.monitoringOrders.keys());
  }
}

// Usage example
async function orderMonitoringExample() {
  const monitor = new OrderMonitor();

  try {
    // Simulate creating an order (you'd get this from createOrder)
    const orderId = 'example_order_id_123';

    console.log('🚀 Starting order monitoring example...');

    // Monitor with status callback
    const finalStatus = await monitor.monitorOrder(
      orderId,
      (status) => {
        console.log(`📱 Status update: ${status}`);
        
        // You could update UI, send notifications, etc.
        if (status === 'PROCESSING') {
          console.log('💫 Order is being processed...');
        } else if (status === 'CONFIRMING') {
          console.log('⏳ Waiting for confirmations...');
        }
      },
      10 // 10 minute timeout
    );

    console.log('🎉 Final order status:', finalStatus);

  } catch (error) {
    if (error instanceof TimeoutError) {
      console.error('⏰ Order monitoring timed out');
    } else if (error instanceof SwapError) {
      console.error('💥 Order failed:', error.message);
    } else {
      console.error('❌ Unexpected error:', error);
    }
  } finally {
    // Clean up
    monitor.stopAllMonitoring();
  }
}

// Run the example
orderMonitoringExample();
```

## Batch Operations

Example showing how to perform multiple operations efficiently.

```typescript
import { 
  KaleidoClient,
  createAssetPairMapper,
  createPrecisionHandler,
  retry
} from 'kaleidoswap-sdk';

class BatchQuoteService {
  private client: KaleidoClient;
  private assetMapper: any;
  private precisionHandler: any;

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.staging.kaleidoswap.com/api/v1'
    });
  }

  async initialize() {
    const pairs = await this.client.pairList();
    this.assetMapper = createAssetPairMapper(pairs);
    this.precisionHandler = createPrecisionHandler(this.assetMapper.getAllAssets());
  }

  async getBatchQuotes(requests: Array<{
    fromTicker: string;
    toTicker: string;
    amount: number;
  }>) {
    console.log(`📊 Getting ${requests.length} quotes...`);

    const results = await Promise.allSettled(
      requests.map(async (request, index) => {
        try {
          // Add delay to avoid rate limiting
          await new Promise(resolve => setTimeout(resolve, index * 200));

          const fromAsset = this.assetMapper.findByTicker(request.fromTicker);
          const toAsset = this.assetMapper.findByTicker(request.toTicker);

          if (!fromAsset || !toAsset) {
            throw new Error(`Assets not found: ${request.fromTicker} or ${request.toTicker}`);
          }

          const validation = this.precisionHandler.validateOrderSize(request.amount, fromAsset);
          if (!validation.valid) {
            throw new Error(validation.error);
          }

          const quote = await retry(() => 
            this.client.quoteRequest(
              fromAsset.asset_id,
              toAsset.asset_id,
              validation.atomicAmount
            )
          );

          return {
            request,
            quote: {
              ...quote,
              fromAmountDecimal: this.precisionHandler.toDecimalAmount(
                quote.from_amount,
                fromAsset.asset_id
              ),
              toAmountDecimal: this.precisionHandler.toDecimalAmount(
                quote.to_amount,
                toAsset.asset_id
              )
            },
            success: true
          };

        } catch (error) {
          return {
            request,
            error: error instanceof Error ? error.message : String(error),
            success: false
          };
        }
      })
    );

    // Process results
    const successful = results
      .filter((result): result is PromiseFulfilledResult<any> => 
        result.status === 'fulfilled' && result.value.success
      )
      .map(result => result.value);

    const failed = results
      .filter((result): result is PromiseFulfilledResult<any> => 
        result.status === 'fulfilled' && !result.value.success
      )
      .map(result => result.value);

    console.log(`✅ ${successful.length} quotes successful`);
    console.log(`❌ ${failed.length} quotes failed`);

    return { successful, failed };
  }

  async compareRates(baseTicker: string, targetTickers: string[], amount: number) {
    console.log(`💱 Comparing rates: ${baseTicker} → [${targetTickers.join(', ')}]`);

    const requests = targetTickers.map(ticker => ({
      fromTicker: baseTicker,
      toTicker: ticker,
      amount
    }));

    const { successful, failed } = await this.getBatchQuotes(requests);

    // Sort by best rate (highest output amount)
    const sortedRates = successful
      .sort((a, b) => b.quote.toAmountDecimal - a.quote.toAmountDecimal)
      .map((result, index) => ({
        rank: index + 1,
        pair: `${result.request.fromTicker}/${result.request.toTicker}`,
        rate: parseFloat(result.quote.price),
        output: result.quote.toAmountDecimal,
        rfqId: result.quote.rfq_id
      }));

    console.log('\n🏆 Rate Comparison Results:');
    sortedRates.forEach(rate => {
      console.log(`  ${rate.rank}. ${rate.pair}: ${rate.output} (rate: ${rate.rate})`);
    });

    if (failed.length > 0) {
      console.log('\n❌ Failed quotes:');
      failed.forEach(failure => {
        console.log(`  ${failure.request.fromTicker}/${failure.request.toTicker}: ${failure.error}`);
      });
    }

    return { rates: sortedRates, failures: failed };
  }
}

// Usage example
async function batchOperationsExample() {
  const batchService = new BatchQuoteService();
  await batchService.initialize();

  try {
    // Example 1: Multiple quote requests
    const quoteRequests = [
      { fromTicker: 'BTC', toTicker: 'USDT', amount: 0.001 },
      { fromTicker: 'BTC', toTicker: 'ETH', amount: 0.001 },
      { fromTicker: 'ETH', toTicker: 'USDT', amount: 0.1 },
      { fromTicker: 'USDT', toTicker: 'BTC', amount: 1000 }
    ];

    console.log('📈 Batch Quote Example:');
    const batchResults = await batchService.getBatchQuotes(quoteRequests);
    
    console.log('\nSuccessful quotes:');
    batchResults.successful.forEach(result => {
      console.log(`  ${result.request.fromTicker} → ${result.request.toTicker}: ${result.quote.price}`);
    });

    // Example 2: Rate comparison
    console.log('\n💰 Rate Comparison Example:');
    await batchService.compareRates('BTC', ['USDT', 'ETH', 'LTC'], 0.001);

  } catch (error) {
    console.error('❌ Batch operations failed:', error);
  }
}

batchOperationsExample();
```

## Error Recovery and Resilience

Example showing robust error handling and recovery strategies.

```typescript
import { 
  KaleidoClient,
  NetworkError,
  RateLimitError,
  QuoteError,
  SwapError,
  TimeoutError,
  retry
} from 'kaleidoswap-sdk';

class ResilientTradingService {
  private client: KaleidoClient;
  private circuitBreaker = new Map<string, { failures: number; lastFailure: number }>();
  private readonly maxFailures = 3;
  private readonly resetTimeout = 60000; // 1 minute

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.staging.kaleidoswap.com/api/v1',
      retryConfig: {
        maxRetries: 5,
        initialDelay: 1000,
        maxDelay: 30000,
        exponentialBase: 2,
        jitter: true
      }
    });
  }

  private isCircuitOpen(operation: string): boolean {
    const circuit = this.circuitBreaker.get(operation);
    if (!circuit) return false;

    const now = Date.now();
    if (now - circuit.lastFailure > this.resetTimeout) {
      // Reset circuit after timeout
      this.circuitBreaker.delete(operation);
      return false;
    }

    return circuit.failures >= this.maxFailures;
  }

  private recordFailure(operation: string) {
    const circuit = this.circuitBreaker.get(operation) || { failures: 0, lastFailure: 0 };
    circuit.failures++;
    circuit.lastFailure = Date.now();
    this.circuitBreaker.set(operation, circuit);
  }

  private recordSuccess(operation: string) {
    this.circuitBreaker.delete(operation);
  }

  async getResilientQuote(fromAsset: string, toAsset: string, amount: number) {
    const operation = 'quote';
    
    if (this.isCircuitOpen(operation)) {
      throw new Error('Quote service temporarily unavailable (circuit breaker open)');
    }

    try {
      const quote = await this.executeWithFallback(
        // Primary: HTTP quote
        () => this.client.quoteRequest(fromAsset, toAsset, amount),
        // Fallback: WebSocket quote
        () => this.client.quoteRequestWS(fromAsset, toAsset, amount)
      );

      this.recordSuccess(operation);
      return quote;

    } catch (error) {
      this.recordFailure(operation);
      throw error;
    }
  }

  private async executeWithFallback<T>(
    primary: () => Promise<T>,
    fallback: () => Promise<T>
  ): Promise<T> {
    try {
      return await primary();
    } catch (primaryError) {
      console.log('Primary method failed, trying fallback...');
      
      try {
        return await fallback();
      } catch (fallbackError) {
        console.error('Both primary and fallback methods failed');
        throw primaryError; // Throw original error
      }
    }
  }

  async createResilientOrder(orderRequest: any) {
    const operation = 'createOrder';
    
    if (this.isCircuitOpen(operation)) {
      throw new Error('Order service temporarily unavailable (circuit breaker open)');
    }

    const maxAttempts = 3;
    let attempt = 0;

    while (attempt < maxAttempts) {
      attempt++;
      
      try {
        console.log(`Creating order (attempt ${attempt}/${maxAttempts})...`);
        
        const order = await retry(
          () => this.client.createOrder(orderRequest),
          {
            maxRetries: 2,
            initialDelay: 1000,
            retryOnExceptions: [NetworkError, RateLimitError]
          }
        );

        this.recordSuccess(operation);
        return order;

      } catch (error) {
        console.error(`Order creation attempt ${attempt} failed:`, error);

        if (error instanceof QuoteError && error.message.includes('expired')) {
          console.log('Quote expired, getting new quote...');
          // In a real app, you'd refresh the quote here
          throw new Error('Quote expired - please get a new quote');
        }

        if (error instanceof SwapError) {
          // Don't retry swap errors
          this.recordFailure(operation);
          throw error;
        }

        if (attempt === maxAttempts) {
          this.recordFailure(operation);
          throw error;
        }

        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
      }
    }

    throw new Error('Max attempts reached');
  }

  async monitorOrderWithRecovery(orderId: string, timeoutMinutes = 30) {
    const operation = 'monitorOrder';
    let consecutiveFailures = 0;
    const maxConsecutiveFailures = 5;

    return new Promise((resolve, reject) => {
      const startTime = Date.now();
      const timeoutMs = timeoutMinutes * 60 * 1000;

      const checkStatus = async () => {
        try {
          const status = await this.client.swapOrderStatus(orderId);
          consecutiveFailures = 0; // Reset on success
          
          const currentStatus = status.order_state || status.status;
          console.log(`Order ${orderId}: ${currentStatus}`);

          // Check terminal states
          if (['COMPLETED', 'Succeeded'].includes(currentStatus)) {
            resolve(status);
            return;
          }

          if (['FAILED', 'Failed', 'EXPIRED', 'Expired'].includes(currentStatus)) {
            reject(new SwapError(`Order ${currentStatus.toLowerCase()}`));
            return;
          }

          // Check timeout
          if (Date.now() - startTime >= timeoutMs) {
            reject(new TimeoutError('Order monitoring timeout'));
            return;
          }

          // Schedule next check
          setTimeout(checkStatus, 10000);

        } catch (error) {
          consecutiveFailures++;
          console.error(`Status check failed (${consecutiveFailures}/${maxConsecutiveFailures}):`, error);

          if (consecutiveFailures >= maxConsecutiveFailures) {
            reject(new Error('Too many consecutive monitoring failures'));
            return;
          }

          // Exponential backoff for retries
          const delay = Math.min(5000 * Math.pow(2, consecutiveFailures - 1), 60000);
          setTimeout(checkStatus, delay);
        }
      };

      checkStatus();
    });
  }

  getCircuitBreakerStatus() {
    const status: Record<string, any> = {};
    
    for (const [operation, circuit] of this.circuitBreaker) {
      status[operation] = {
        failures: circuit.failures,
        isOpen: this.isCircuitOpen(operation),
        lastFailure: new Date(circuit.lastFailure).toISOString()
      };
    }

    return status;
  }
}

// Usage example
async function resilienceExample() {
  const tradingService = new ResilientTradingService();

  try {
    console.log('🛡️ Testing resilient trading service...\n');

    // Test resilient quote
    console.log('1. Getting resilient quote...');
    const quote = await tradingService.getResilientQuote(
      'btc_asset_id',
      'usdt_asset_id',
      100000
    );
    console.log('✅ Quote received:', quote.price);

    // Test resilient order creation
    console.log('\n2. Creating resilient order...');
    const orderRequest = {
      rfq_id: quote.rfq_id,
      from_type: 'ONCHAIN' as const,
      to_type: 'ONCHAIN' as const,
      // ... other required fields
    };

    // Simulate this in a real scenario
    // const order = await tradingService.createResilientOrder(orderRequest);
    // console.log('✅ Order created:', order.order_id);

    // Check circuit breaker status
    console.log('\n3. Circuit breaker status:');
    const circuitStatus = tradingService.getCircuitBreakerStatus();
    console.log(circuitStatus);

  } catch (error) {
    console.error('❌ Resilience test failed:', error);
  }
}

resilienceExample();
```

These examples demonstrate real-world usage patterns and best practices for the KaleidoSwap SDK. Each example includes proper error handling, logging, and follows the recommended patterns for production applications.
