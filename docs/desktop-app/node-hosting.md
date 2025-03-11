---
title: RGB Lightning Node Hosting
description: Learn how to self-host a RGB Lightning Node for use with KaleidoSwap
sidebar_position: 3
---

# RGB Lightning Node Hosting

This guide explains how to host your own RGB Lightning Node for use with KaleidoSwap. Self-hosting gives you full control over your node and can be a great option for users familiar with running servers.

## Overview

The RGB Lightning Node (RLN) is a specialized Lightning Network node that supports RGB assets on the Lightning Network. It allows you to:

- Create payment channels containing RGB assets
- Route RGB asset-denominated payments across multiple channels
- Transfer RGB assets with the same user experience and security as regular Bitcoin Lightning payments

## Hosting Methods Comparison

There are several ways to host an RGB Lightning Node, each with their own advantages and requirements:

| Hosting Method | Advantages | Considerations | Technical Expertise |
|----------------|------------|----------------|---------------------|
| **Docker** | Easy setup, isolated environment, simple updates | Requires Docker knowledge | Medium |
| **Direct Installation** | Full control, no containerization overhead | Manual setup of dependencies, firewall, etc. | High |
| **Hosted Provider** | No technical setup, professional support | Less control, subscription cost | Low |

Choose the method that best aligns with your technical skills and requirements:

- **Docker-based installation**: Best for most users - provides an easy setup with the option to run full infrastructure or just the node.
- **Direct installation on a VPS**: Best for advanced users who need complete control over the system configuration.
- **Hosted solution (ThunderStack)**: Best for users who want a professionally managed solution with minimal technical overhead.

## Network Options

Regardless of your hosting method, you can run your node on different Bitcoin networks:

| Network | Description | Use Case |
|---------|-------------|----------|
| **Signet (Mutinynet)** | Custom signet with 30-second blocks | Ideal for testing and development |
| **Testnet** | Bitcoin's global testnet | Testing in a broader network |
| **Regtest** | Local testing network | Development and isolated testing |
| **Mainnet** | Bitcoin production network | Production use (coming soon) |

With our Docker solution, you can easily run your own Bitcoin Core and Electrs instances for any of these networks, giving you complete control over your stack.

## Trust Considerations

The infrastructure components you choose to run yourself vs. connect to externally impacts the level of trust required:

- **Zero-Trust Setup**: Run your own Bitcoin Core, Electrs, RGB Proxy, and RGB Lightning Node
- **Minimal Trust Setup**: Run only the RGB Lightning Node and connect to hosted instances for other services

## Option 1: Docker-Based Installation

Our Docker solution provides the easiest way to run an RGB Lightning Node. You can run the complete stack or just the node component.

### Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM and 50GB storage
- Basic knowledge of terminal commands

### Quick Start with Makefile

The easiest way to get started is using the included Makefile:

1. Clone the repository:

```bash
git clone https://github.com/kaleidoswap/docker-images.git
cd docker-images
```

2. Choose how you want to run the stack:

```bash
# To see all available commands
make help

# To run only the RGB Lightning Node (connect then to external services)
make node-only

# To run the full stack (all components on signet)
make full

# To view logs from all services
make logs
```

Have a look at the [README.md file](https://github.com/kaleidoswap/docker-images/blob/main/README.md) for more information on the different commands and options.

## Option 2: Direct Installation on a VPS

For advanced users who prefer complete control over their server environment, you can install the RGB Lightning Node directly on a VPS or bare-metal server.

### Prerequisites

- A VPS or server running Linux (Ubuntu/Debian recommended)
- Rust development environment
- Properly configured firewall (opening ports 3001 for API and 9735 for Lightning)
- Sufficient storage for blockchain data

### Installation

1. Clone the repository:

```bash
git clone https://github.com/RGB-Tools/rgb-lightning-node --recurse-submodules --shallow-submodules
cd rgb-lightning-node
```

2. Install the binary:

```bash
cargo install --locked --debug --path .
```

3. Start the node:

```bash
rgb-lightning-node <data-dir>/ --daemon-listening-port 3001 \
    --ldk-peer-listening-port 9735 --network <network>
```

Replace:
- `<data-dir>` with your chosen data directory 
- `<network>` with `regtest`, `testnet`, or `signet` (for Mutinynet)

4. When unlocking the node, you'll need to provide:

- Bitcoin RPC connection details
- Indexer URL
- RGB proxy endpoint

### VPS Firewall Configuration
When running on a VPS, you'll need to configure the firewall to allow necessary connections

```bash
# Allow SSH
ufw allow ssh

# Allow RGB Lightning Node API
ufw allow 3001/tcp

# Allow Lightning Network P2P connections
ufw allow 9735/tcp

# Enable the firewall
ufw enable
```

### Running as a System Service

For a production setup, create a systemd service:

```bash
sudo nano /etc/systemd/system/rgb-lightning-node.service
```

Add the following content:

```
[Unit]
Description=RGB Lightning Node
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME
ExecStart=/home/YOUR_USERNAME/.cargo/bin/rgb-lightning-node /home/YOUR_USERNAME/rgbln-data/ --daemon-listening-port 3001 --ldk-peer-listening-port 9735 --network signet
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable rgb-lightning-node
sudo systemctl start rgb-lightning-node
```

## Option 3: Hosted Provider (ThunderStack)

If you prefer a professionally managed solution without the technical overhead of self-hosting, [ThunderStack](https://thunderstack.org/product) offers cloud-based RGB Lightning Node hosting.

### What is ThunderStack?

ThunderStack is a cloud-based solution designed to provide seamless node management for RGB and Lightning applications. It ensures high availability, enhanced security, and ease of management without the technical overhead of self-hosting.

### Key Features

- **24/7 Availability**: Always-on infrastructure ensures uninterrupted operations
- **No Maintenance**: Leave the operational complexities of node management to ThunderStack
- **Scalability**: Add or remove nodes on demand as your needs evolve
- **Security**: Advanced security protocols like mTLS and Cognito for access control
- **Integration Ready**: Supports APIs, webhooks, and SDKs for easy integration

### ThunderStack vs. Self-Hosting

| Aspect | ThunderStack | Self-Hosting |
|--------|-------------|--------------|
| Technical Expertise | Minimal | Moderate to High |
| Setup Time | Minutes | Hours to Days |
| Maintenance | Handled by ThunderStack | User Responsibility |
| Control | Limited to API | Full Control |
| Cost | Subscription-based | Infrastructure Costs |
| Uptime | Professional SLAs | Depends on Your Setup |

Choose ThunderStack if you prioritize convenience, reliability, and professional support. Choose self-hosting if you prioritize complete control, customization, and minimal third-party trust.

## Network Environments

### Connection Details for Different Networks

#### Regtest Environment

For regtest testing, you can use these connection details:

```json
{
  "password": "<YOUR_NODE_PASSWORD>",
  "bitcoind_rpc_username": "user",
  "bitcoind_rpc_password": "password",
  "bitcoind_rpc_host": "regtest-bitcoind.rgbtools.org",
  "bitcoind_rpc_port": 80,
  "indexer_url": "electrum.rgbtools.org:50041",
  "proxy_endpoint": "rpcs://proxy.iriswallet.com/0.2/json-rpc"
}
```

#### Testnet Environment

For testnet3 testing, you can use:

```json
{
  "password": "<YOUR_NODE_PASSWORD>",
  "bitcoind_rpc_username": "user",
  "bitcoind_rpc_password": "password",
  "bitcoind_rpc_host": "electrum.iriswallet.com",
  "bitcoind_rpc_port": 18332,
  "indexer_url": "ssl://electrum.iriswallet.com:50013",
  "proxy_endpoint": "rpcs://proxy.iriswallet.com/0.2/json-rpc"
}
```

#### Signet (Mutinynet) Environment

For signet testing, you can use:

```json
{
  "password": "<YOUR_NODE_PASSWORD>",
  "bitcoind_rpc_username": "user",
  "bitcoind_rpc_password": "default_password",
  "bitcoind_rpc_host": "bitcoind.signet.kaleidoswap.com",
  "bitcoind_rpc_port": 38332,
  "indexer_url": "ssl://electrum.signet.kaleidoswap.com:60601",
  "proxy_endpoint": "rpcs://proxy.signet.kaleidoswap.com/json-rpc"
}
```

## Mutinynet: A Custom Bitcoin Signet for Testing

[Mutinynet](https://github.com/MutinyWallet/mutiny-net) is a custom Bitcoin Signet network designed specifically for testing Lightning Network applications. It offers:

- Extremely fast block times (30 seconds per block vs. 10 minutes on mainnet)
- Stable testnet environment without competition for block space
- Pre-configured for compatibility with RGB Lightning Nodes
- Ideal for testing RGB assets on Lightning

**Mutinynet Resources:**

- [Mutinynet Explorer & Mempool](https://mutinynet.com/) - View blocks, transactions, and mempool
- [Mutinynet Faucet](https://faucet.mutinynet.com/) - Get free test coins for development
- [Mutinynet GitHub Repository](https://github.com/MutinyWallet/mutiny-net) - Technical documentation and source code

## Node Operation

Once your node is running, it can be operated via REST APIs.

### API Overview

The node exposes a comprehensive API for managing your node:

- Channel management: open/close channels, connect/disconnect peers
- Asset operations: issue, send, and manage RGB assets
- Payment handling: create/pay invoices, keysend, etc.
- Node information and control

For detailed API documentation, see the [OpenAPI specification](https://rgb-tools.github.io/rgb-lightning-node).

### Basic Operations

Here are some common operations:

#### Get a Bitcoin Address
```bash
curl -X POST http://localhost:3001/address
```

#### Get Node Information
```bash
curl http://localhost:3001/nodeinfo
```

#### Check Bitcoin Balance
```bash
curl -X POST -H "Content-type: application/json" \
    -d '{}' http://localhost:3001/btcbalance
```

## Hardware Requirements

For optimal performance:

| Environment | CPU | RAM | Storage | Network |
|-------------|-----|-----|---------|---------|
| Testing (Mutinynet) | 2 cores | 4GB | 25GB | 10Mbps |
| Testnet | 2 cores | 4GB | 50GB | 10Mbps |
| Production | 4+ cores | 8GB+ | 500GB+ SSD | 100Mbps+ |

## Security Considerations

When hosting your own node:

1. **Firewall Configuration**: Only expose necessary ports (3001 for API, 9735 for LN peers)
2. **Authentication**: Use strong passwords and consider adding API authentication
3. **Backups**: Regularly backup your node's data directory
4. **Updates**: Keep all components updated to patch security vulnerabilities

## Troubleshooting

### Common Issues

**Node won't start**
- Check if Bitcoin Core is running and accessible
- Verify the indexer connection is working
- Ensure the RGB proxy server is running

**Cannot connect from KaleidoSwap**
- Check firewall settings
- Verify the node URL is correct
- Ensure the node is running and unencrypted

**Synchronization problems**
- Bitcoin Core might still be syncing
- The indexer might be behind the blockchain
- For Mutinynet, make sure you're using the correct signet seed nodes

**Mutinynet-specific issues**
- Ensure you're using the custom Bitcoin build with Mutinynet support
- Check that your electrs instance is configured for Signet
- Verify the `NETWORK=signet` environment variable is set
- For connection issues, verify Mutinynet seeds are correctly configured
- If transactions aren't confirming, check the [Mutinynet Explorer](https://mutinynet.com/) for network status

## Getting Help

If you encounter issues:

1. Check the [GitHub repository](https://github.com/RGB-Tools/rgb-lightning-node) for known issues
2. Visit the [KaleidoSwap Telegram](https://t.me/kaleidoswap) for community support
3. Open an issue on the GitHub repository with detailed information about your problem

## Additional Resources

- [RGB Protocol Documentation](https://docs.rgb.info)
- [RGB Lightning Node Repository](https://github.com/RGB-Tools/rgb-lightning-node)
- [Mutinynet Explorer](https://mutinynet.com/)
- [Mutinynet Faucet](https://faucet.mutinynet.com/)
- [Mutinynet Documentation](https://github.com/MutinyWallet/mutiny-net)
- [KaleidoSwap Documentation](https://docs.kaleidoswap.org)