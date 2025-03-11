module.exports = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'introduction',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Desktop App Guide',
      items: [
        'desktop-app/introduction',
        'desktop-app/node-hosting',
        'desktop-app/installation',
        'desktop-app/creating-wallet',
        'desktop-app/funding-wallet',
        'desktop-app/opening-channel',
        'desktop-app/order-new-channel',
        'desktop-app/channel-backups',
        'desktop-app/channel-requests',
        'desktop-app/asset-swaps',
        'desktop-app/deposits',
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