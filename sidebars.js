module.exports = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'introduction',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'SDK',
      collapsed: true,
      items: [
        {
          type: 'category',
          label: 'Python SDK',
          collapsed: true,
          items: [
            'sdk/python/index',
            'sdk/python/getting-started',
            'sdk/python/api-reference',
            'sdk/python/types',
            'sdk/python/examples',
            'sdk/python/error-handling',
            'sdk/python/websocket',
            'sdk/python/utilities',
          ],
        },
        {
          type: 'category',
          label: 'TypeScript SDK',
          collapsed: true,
          items: [
            'sdk/typescript/index',
            'sdk/typescript/getting-started',
            'sdk/typescript/api-reference',
            'sdk/typescript/types',
            'sdk/typescript/utilities',
            'sdk/typescript/error-handling',
            'sdk/typescript/examples',
            'sdk/typescript/websocket',
            'sdk/typescript/best-practices',
            'sdk/typescript/troubleshooting',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Desktop App Guide',
      items: [
        'desktop-app/introduction',
        'desktop-app/installation',
        'desktop-app/verify-binaries',
        'desktop-app/node-hosting',
        'desktop-app/creating-wallet',
        'desktop-app/deposits',
        'desktop-app/opening-channel',
        'desktop-app/order-new-channel',
        'desktop-app/asset-swaps',
        'desktop-app/channel-backups',
        'desktop-app/channel-requests',
        'desktop-app/withdrawals',
        'desktop-app/faq',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/introduction',
        'api/getting-started',
        'api/rgb-lsps1-apis',
        'api/market-apis',
        'api/swap-apis',
        'api/error-handling',
      ],
    }
  ],
}; 
