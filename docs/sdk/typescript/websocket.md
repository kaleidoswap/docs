# WebSocket Guide

The KaleidoSwap SDK provides real-time data streaming through WebSocket connections for live quotes, market updates, and order status changes.

## Overview

WebSocket connections offer several advantages over HTTP requests:
- **Real-time Updates**: Receive live price quotes and market data
- **Lower Latency**: Faster response times for time-sensitive operations
- **Reduced Overhead**: Persistent connection reduces connection setup time
- **Push Notifications**: Server can push updates without client polling

## WebSocket Client

### Basic Setup

```typescript
import { WebSocketClient, WebSocketConfig } from 'kaleidoswap-sdk';

const wsConfig: WebSocketConfig = {
  baseUrl: 'wss://api.kaleidoswap.com/ws',
  apiKey: 'your-api-key', // Optional
};

const wsClient = new WebSocketClient(wsConfig);
```

### Configuration Options

```typescript
interface WebSocketConfig {
  baseUrl: string;                    // WebSocket URL
  apiKey?: string;                    // Optional API key
  pingInterval?: number;              // Ping interval (default: 30000ms)
  pingTimeout?: number;               // Ping timeout (default: 10000ms)
  reconnectInterval?: number;         // Reconnect interval (default: 5000ms)
  maxReconnectAttempts?: number;      // Max reconnect attempts (default: 5)
}
```

### Advanced Configuration

```typescript
const wsConfig: WebSocketConfig = {
  baseUrl: 'wss://api.kaleidoswap.com/ws',
  apiKey: 'your-api-key',
  pingInterval: 30000,        // Send ping every 30 seconds
  pingTimeout: 10000,         // Wait 10 seconds for pong
  reconnectInterval: 5000,    // Wait 5 seconds before reconnecting
  maxReconnectAttempts: 10    // Try reconnecting up to 10 times
};

const wsClient = new WebSocketClient(wsConfig);
```

## Connection Management

### Connecting

```typescript
// Connect to WebSocket
await wsClient.connect();

// Check connection status
if (wsClient.isConnected()) {
  console.log('WebSocket connected successfully');
}
```

### Connection States

```typescript
// Get current connection state
const state = wsClient.getConnectionState();

// WebSocket states:
// WebSocket.CONNECTING (0) - Connection is being established
// WebSocket.OPEN (1)       - Connection is open and ready
// WebSocket.CLOSING (2)    - Connection is being closed
// WebSocket.CLOSED (3)     - Connection is closed

switch (state) {
  case WebSocket.OPEN:
    console.log('Connected and ready');
    break;
  case WebSocket.CONNECTING:
    console.log('Connecting...');
    break;
  case WebSocket.CLOSED:
    console.log('Disconnected');
    break;
}
```

### Disconnecting

```typescript
// Graceful disconnect
await wsClient.disconnect();

// Disconnect with custom code and reason
await wsClient.disconnect(1000, 'User initiated disconnect');
```

## Message Handling

### Event Listeners

```typescript
// Listen for quote responses
wsClient.on('quote_response', (data) => {
  console.log('Received quote:', data);
});

// Listen for connection errors
wsClient.on('error', (error) => {
  console.error('WebSocket error:', error);
});

// Listen for custom events
wsClient.on('market_update', (data) => {
  console.log('Market update:', data);
});
```

### Removing Event Listeners

```typescript
// Method 1: Using the unsubscribe function returned by on()
const unsubscribe = wsClient.on('quote_response', handleQuote);
unsubscribe(); // Remove this specific listener

// Method 2: Using off() method
function handleQuote(data: any) {
  console.log('Quote:', data);
}

wsClient.on('quote_response', handleQuote);
wsClient.off('quote_response', handleQuote); // Remove specific handler
```

### Sending Messages

```typescript
// Send a custom message
await wsClient.send({
  action: 'custom_action',
  data: { key: 'value' }
});

// Send quote request
await wsClient.send({
  action: 'quote_request',
  from_asset: 'btc_asset_id',
  to_asset: 'usdt_asset_id',
  from_amount: 100000,
  timestamp: Math.floor(Date.now() / 1000)
});
```

## Real-time Quotes

### Using KaleidoClient WebSocket Methods

The main client provides convenient WebSocket methods:

```typescript
import { KaleidoClient } from 'kaleidoswap-sdk';

const client = new KaleidoClient({
  baseUrl: 'https://api.kaleidoswap.com/api/v1',
  wsUrl: 'wss://api.kaleidoswap.com/ws'
});

// Get real-time quote via WebSocket
const quote = await client.quoteRequestWS(
  'btc_asset_id',
  'usdt_asset_id',
  100000 // 100,000 satoshis
);

console.log('Real-time quote:', quote);
```

### Manual WebSocket Quote Requests

```typescript
async function getRealtimeQuote() {
  // Connect if not already connected
  if (!wsClient.isConnected()) {
    await wsClient.connect();
  }

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      wsClient.off('quote_response', handleResponse);
      reject(new Error('Quote request timeout'));
    }, 30000);

    const handleResponse = (data: any) => {
      clearTimeout(timeout);
      wsClient.off('quote_response', handleResponse);
      
      if (data.error) {
        reject(new Error(data.error.message));
      } else {
        resolve(data);
      }
    };

    wsClient.on('quote_response', handleResponse);

    wsClient.send({
      action: 'quote_request',
      from_asset: 'btc_asset_id',
      to_asset: 'usdt_asset_id',
      from_amount: 100000,
      timestamp: Math.floor(Date.now() / 1000)
    });
  });
}
```

## Subscriptions

### Subscribe to Trading Pairs

```typescript
// Subscribe to BTC/USDT pair updates
await wsClient.subscribe('BTC_USDT');

// Listen for pair updates
wsClient.on('pair_update', (data) => {
  console.log('Pair update:', data);
});
```

### Unsubscribe from Trading Pairs

```typescript
// Unsubscribe from pair updates
await wsClient.unsubscribe('BTC_USDT');
```

### Multiple Subscriptions

```typescript
// Subscribe to multiple pairs
const pairs = ['BTC_USDT', 'ETH_USDT', 'LTC_BTC'];

for (const pair of pairs) {
  await wsClient.subscribe(pair);
}

// Handle updates for all subscribed pairs
wsClient.on('pair_update', (data) => {
  console.log(`Update for ${data.pair}:`, data);
});
```

## Error Handling

### Connection Errors

```typescript
wsClient.on('error', (error) => {
  console.error('WebSocket error:', error);
  
  if (error.action === 'connection_failed') {
    console.log('Failed to connect, retrying...');
    // Implement custom retry logic if needed
  } else if (error.action === 'max_reconnect_attempts') {
    console.log('Max reconnection attempts reached');
    // Handle permanent connection failure
  }
});
```

### Message Errors

```typescript
wsClient.on('error', (error) => {
  if (error.action === 'message_parse_error') {
    console.error('Failed to parse message:', error.error);
  }
});
```

### Timeout Handling

```typescript
import { TimeoutError } from 'kaleidoswap-sdk';

try {
  const quote = await client.quoteRequestWS('btc_id', 'usdt_id', 100000);
} catch (error) {
  if (error instanceof TimeoutError) {
    console.error('Quote request timed out');
    // Fall back to HTTP request
    const httpQuote = await client.quoteRequest('btc_id', 'usdt_id', 100000);
  }
}
```

## Automatic Reconnection

The WebSocket client automatically handles reconnections:

```typescript
// Reconnection is automatic, but you can listen for events
wsClient.on('reconnecting', (attempt) => {
  console.log(`Reconnection attempt ${attempt}`);
});

wsClient.on('reconnected', () => {
  console.log('Successfully reconnected');
  // Re-subscribe to any pairs if needed
});

wsClient.on('max_reconnect_attempts', () => {
  console.log('Failed to reconnect after maximum attempts');
  // Handle permanent disconnection
});
```

## Debug Mode

Enable debug logging for troubleshooting:

```typescript
// Enable WebSocket debugging
process.env.DEBUG_WS = 'true';

// Or set it programmatically before creating the client
process.env.DEBUG_WS = 'true';
const wsClient = new WebSocketClient(config);
```

Debug output includes:
- Connection attempts and status
- Message sending and receiving
- Reconnection attempts
- Error details

## Complete Example

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
  private subscribers: Map<string, Set<(quote: any) => void>> = new Map();

  constructor() {
    this.client = new KaleidoClient({
      baseUrl: 'https://api.kaleidoswap.com/api/v1',
      wsUrl: 'wss://api.kaleidoswap.com/ws'
    });

    this.wsClient = new WebSocketClient({
      baseUrl: 'wss://api.kaleidoswap.com/ws',
      reconnectInterval: 5000,
      maxReconnectAttempts: 10
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers() {
    // Handle quote responses
    this.wsClient.on('quote_response', (data) => {
      const pairKey = `${data.from_asset}_${data.to_asset}`;
      const callbacks = this.subscribers.get(pairKey);
      
      if (callbacks) {
        callbacks.forEach(callback => callback(data));
      }
    });

    // Handle connection errors
    this.wsClient.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    // Handle reconnection
    this.wsClient.on('reconnected', () => {
      console.log('WebSocket reconnected');
      // Re-subscribe to all pairs
      this.resubscribeAll();
    });
  }

  async connect() {
    try {
      await this.wsClient.connect();
      console.log('WebSocket connected');
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      throw error;
    }
  }

  async subscribeToQuotes(
    fromAsset: string, 
    toAsset: string, 
    callback: (quote: any) => void
  ) {
    const pairKey = `${fromAsset}_${toAsset}`;
    
    if (!this.subscribers.has(pairKey)) {
      this.subscribers.set(pairKey, new Set());
    }
    
    this.subscribers.get(pairKey)!.add(callback);

    // Subscribe to pair updates
    await this.wsClient.subscribe(pairKey);
  }

  async unsubscribeFromQuotes(
    fromAsset: string, 
    toAsset: string, 
    callback: (quote: any) => void
  ) {
    const pairKey = `${fromAsset}_${toAsset}`;
    const callbacks = this.subscribers.get(pairKey);
    
    if (callbacks) {
      callbacks.delete(callback);
      
      if (callbacks.size === 0) {
        this.subscribers.delete(pairKey);
        await this.wsClient.unsubscribe(pairKey);
      }
    }
  }

  async getRealtimeQuote(fromAsset: string, toAsset: string, amount: number) {
    try {
      return await this.client.quoteRequestWS(fromAsset, toAsset, amount);
    } catch (error) {
      if (error instanceof WebSocketError || error instanceof TimeoutError) {
        // Fall back to HTTP
        console.log('WebSocket failed, falling back to HTTP');
        return await this.client.quoteRequest(fromAsset, toAsset, amount);
      }
      throw error;
    }
  }

  private async resubscribeAll() {
    for (const pairKey of this.subscribers.keys()) {
      try {
        await this.wsClient.subscribe(pairKey);
      } catch (error) {
        console.error(`Failed to resubscribe to ${pairKey}:`, error);
      }
    }
  }

  async disconnect() {
    await this.wsClient.disconnect();
    this.subscribers.clear();
  }
}

// Usage
const quoteService = new RealtimeQuoteService();

async function example() {
  await quoteService.connect();

  // Subscribe to BTC/USDT quotes
  quoteService.subscribeToQuotes('btc_id', 'usdt_id', (quote) => {
    console.log('New BTC/USDT quote:', quote);
  });

  // Get a one-time quote
  const quote = await quoteService.getRealtimeQuote('btc_id', 'usdt_id', 100000);
  console.log('One-time quote:', quote);

  // Clean up
  setTimeout(async () => {
    await quoteService.disconnect();
  }, 60000);
}
```

## Best Practices

### 1. Connection Management

```typescript
// ✅ Check connection before sending messages
if (wsClient.isConnected()) {
  await wsClient.send(message);
} else {
  await wsClient.connect();
  await wsClient.send(message);
}

// ✅ Handle reconnection gracefully
wsClient.on('reconnected', () => {
  // Re-establish subscriptions
  resubscribeToImportantPairs();
});
```

### 2. Error Handling

```typescript
// ✅ Always have fallback to HTTP
async function getQuoteWithFallback(fromAsset: string, toAsset: string, amount: number) {
  try {
    return await client.quoteRequestWS(fromAsset, toAsset, amount);
  } catch (error) {
    if (error instanceof WebSocketError) {
      console.log('WebSocket failed, using HTTP fallback');
      return await client.quoteRequest(fromAsset, toAsset, amount);
    }
    throw error;
  }
}
```

### 3. Resource Management

```typescript
// ✅ Clean up event listeners
class QuoteManager {
  private unsubscribeFunctions: (() => void)[] = [];

  addQuoteListener(callback: (data: any) => void) {
    const unsubscribe = wsClient.on('quote_response', callback);
    this.unsubscribeFunctions.push(unsubscribe);
  }

  cleanup() {
    this.unsubscribeFunctions.forEach(unsubscribe => unsubscribe());
    this.unsubscribeFunctions = [];
  }
}
```

### 4. Rate Limiting

```typescript
// ✅ Throttle quote requests
class ThrottledQuoteService {
  private lastRequestTime = 0;
  private minInterval = 1000; // 1 second between requests

  async getQuote(fromAsset: string, toAsset: string, amount: number) {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    
    if (timeSinceLastRequest < this.minInterval) {
      await new Promise(resolve => 
        setTimeout(resolve, this.minInterval - timeSinceLastRequest)
      );
    }
    
    this.lastRequestTime = Date.now();
    return await client.quoteRequestWS(fromAsset, toAsset, amount);
  }
}
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   ```typescript
   // Increase timeout values
   const wsClient = new WebSocketClient({
     baseUrl: 'wss://api.kaleidoswap.com/ws',
     pingTimeout: 15000, // Increase from default 10s
     reconnectInterval: 10000 // Increase from default 5s
   });
   ```

2. **Message Not Received**
   ```typescript
   // Enable debug logging
   process.env.DEBUG_WS = 'true';
   
   // Check connection state
   console.log('Connection state:', wsClient.getConnectionState());
   ```

3. **Frequent Reconnections**
   ```typescript
   // Check network stability
   wsClient.on('reconnecting', (attempt) => {
     console.log(`Reconnection attempt ${attempt} - check network`);
   });
   ```

### Debug Information

```typescript
// Log all WebSocket events for debugging
const events = ['open', 'close', 'error', 'message', 'reconnecting', 'reconnected'];

events.forEach(event => {
  wsClient.on(event, (data) => {
    console.log(`WebSocket ${event}:`, data);
  });
});
```
