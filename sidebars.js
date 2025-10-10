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
          label: 'On-Chain Lightning Orders',
          items: [
            'sdk/typescript/index',
            'sdk/typescript/getting-started',
            'sdk/typescript/api-reference',
            'sdk/typescript/types',
            'sdk/typescript/utilities',
            'sdk/typescript/error-handling',
            'sdk/typescript/examples',
          ],
        },
        {
          type: 'category',
          label: 'Atomic Lightning Swaps',
          items: [
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
