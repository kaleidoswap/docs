const { themes } = require('prism-react-renderer');
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const config = {
  title: 'KaleidoSwap Documentation',
  tagline: 'Documentation for the KaleidoSwap platform',
  url: 'https://docs.kaleidoswap.com',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'kaleidoswap',
  projectName: 'kaleidoswap-docs',
  staticDirectories: ['static', 'src/assets'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: path.resolve(__dirname, './sidebars.js'),
          routeBasePath: '/',
          path: 'docs',
          editUrl: 'https://github.com/kaleidoswap/kaleidoswap/tree/main/docs/',
        },
        blog: false,
        theme: {
          customCss: path.resolve(__dirname, './src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'KaleidoSwap',
      logo: {
        alt: 'KaleidoSwap Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/kaleidoswap/kaleidoswap',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/introduction',
            },
            {
              label: 'API Reference',
              to: '/api/introduction',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Telegram',
              href: 'https://t.me/kaleidoswap',
            },
            {
              label: 'X',
              href: 'https://x.com/kaleidoswap',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} KaleidoSwap. Built with Docusaurus.`,
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
    },
  },
  stylesheets: [
    {
      href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap',
      type: 'text/css',
    },
  ],
};

module.exports = config; 