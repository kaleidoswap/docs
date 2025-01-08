---
id: order-new-channel
title: Order New Channel
sidebar_position: 4
---

# Order New Channel from LSP

This guide explains how to purchase a new Lightning Network channel with outbound liquidity from a KaleidoSwap LSP (Lightning Service Provider).

## Overview

Opening a channel through an LSP involves four steps:
1. Connect to LSP
2. Configure Channel Order
3. Make Payment
4. Channel Opening

## Step 1: Connect to LSP

First, you'll need to connect to an LSP:
1. Enter the LSP URL or use the default KaleidoSwap LSP
2. The LSP connection string will be displayed
3. Confirm the connection to proceed

## Step 2: Configure Channel Order

### Channel Capacity
- Set the total channel capacity (in satoshis)
- This is the total size of the channel
- Minimum: 20,000 sats
- Maximum: 16,777,215 sats

### Outbound Liquidity
- Choose how much outbound liquidity you want to purchase
- This is the amount the LSP commits to your channel
- The remaining capacity becomes your inbound liquidity
- Example: For a 1M sat channel with 700k outbound, you'll have 300k inbound

### Channel Duration
Select how long the LSP guarantees to keep the channel open:
- 1 week (1,008 blocks)
- 1 month (4,320 blocks)
- 6 months (25,920 blocks)

### Optional: RGB Assets
You can request RGB assets in your channel:
- Enable "Add Asset" option
- Select an RGB20 asset type
- Specify the amount you want the LSP to commit
- Note: Currently, RGB assets are provided from the LSP side only

### Fee Structure
When using KaleidoSwap LSP:
- Base fee: 1% of total channel balance
- Time-lock fee: 10 sats per block of guaranteed channel lifetime
- Example calculation:
  ```
  For a 1M sat channel locked for 1 month (4,320 blocks):
  - Base fee: 10,000 sats (1% of 1M)
  - Time-lock fee: 43,200 sats (10 sats × 4,320 blocks)
  - Total fee: 53,200 sats
  ```

## Step 3: Make Payment

Choose how to pay for your channel:

### Lightning Payment
- Scan the QR code or copy the Lightning invoice
- Pay using any Lightning wallet
- Amount includes:
  - Channel capacity
  - LSP fees (base + time-lock)
  - Network fees

### On-chain Payment
- Send Bitcoin to the provided address
- Include the exact amount shown
- Wait for blockchain confirmations

### Wallet Balance
If you have sufficient funds in your KaleidoSwap wallet:
- Select "Pay from Wallet"
- Confirm the payment details
- Funds will be deducted automatically

## Step 4: Channel Opening

After payment confirmation:
1. The LSP initiates channel opening
2. Wait for blockchain confirmations (3 blocks)
3. Your channel becomes active with the specified:
   - Total capacity
   - Outbound liquidity
   - RGB assets (if requested)
   - Lock period

## Order States

Your channel order can be in these states:
- `PENDING`: Waiting for payment
- `PAID`: Payment received, channel opening in progress
- `COMPLETED`: Channel successfully opened
- `FAILED`: Error occurred during process

## Refund Policy

If the channel opening fails after payment:
1. Note your `order_id` (shown in the interface)
2. Contact support with your order ID
3. Provide payment proof if requested
4. Refund will be processed after verification

## Best Practices

1. **Capacity Planning**
   - Calculate your required outbound/inbound ratio
   - Consider future RGB asset needs
   - Account for fees in your budget

2. **During Order**
   - Keep the application open during payment
   - Save your order ID
   - Wait for all confirmations

3. **After Opening**
   - Verify channel parameters
   - Test with small transactions
   - Monitor channel status

## Support

For assistance:
1. Check the [FAQ](./faq.md)
2. Join our [Telegram Group](https://t.me/kaleidoswap)
3. Open an issue on [GitHub](https://github.com/kaleidoswap/desktop-app)
4. For refunds, email support@kaleidoswap.com with your order ID 


---

*Next: [Channel Backups](channel-backups.md)*
