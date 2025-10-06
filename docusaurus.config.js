const { themes } = require('prism-react-renderer');
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const config = {
  title: 'KaleidoSwap Docs',
  tagline: 'Documentation for the KaleidoSwap App and Protocol',
  url: 'https://docs.kaleidoswap.com',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  favicon: 'img/favicon/favicon.svg',
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
          href: 'https://github.com/kaleidoswap',
          label: 'GitHub',
          position: 'right',
        },
      ],
      hideOnScroll: false,
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
            {
              label: 'GitHub',
              href: 'https://github.com/kaleidoswap',
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
      copyright: `Copyright © ${new Date().getFullYear()} KaleidoSwap`,
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
    sidebar: {
      hideable: true,
      autoCollapseCategories: true,
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
  },
  stylesheets: [
    {
      href: 'https://fonts.googleapis.com/css2?family=Mulish:wght@400;500;600;700&family=Mulish+Mono&display=swap',
      type: 'text/css',
    },
  ],
};

module.exports = config; 