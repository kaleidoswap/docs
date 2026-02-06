// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
    title: 'KaleidoSwap',
    tagline: 'Trade Bitcoin and RGB assets on Lightning',
    favicon: 'img/favicon.ico',

    // Set the production url of your site here
    url: 'https://docs.kaleidoswap.com',
    // Set the /<baseUrl>/ pathname under which your site is served
    baseUrl: '/',

    // GitHub pages deployment config.
    organizationName: 'kaleidoswap',
    projectName: 'docs',

    onBrokenLinks: 'warn',
    onBrokenMarkdownLinks: 'warn',

    i18n: {
        defaultLocale: 'en',
        locales: ['en'],
    },

    presets: [
        [
            'classic',
            /** @type {import('@docusaurus/preset-classic').Options} */
            ({
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                    routeBasePath: '/',
                    editUrl: 'https://github.com/kaleidoswap/docs/tree/main/',
                },
                blog: false,
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            }),
        ],
    ],

    themeConfig:
        /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
        ({
            // Replace with your project's social card
            image: 'img/social-card.jpg',
            navbar: {
                title: 'KaleidoSwap',
                logo: {
                    alt: 'KaleidoSwap Logo',
                    src: 'img/logo.svg',
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
            },
            footer: {
                style: 'dark',
                links: [
                    {
                        title: 'Docs',
                        items: [
                            {
                                label: 'Introduction',
                                to: '/introduction',
                            },
                            {
                                label: 'SDK',
                                to: '/sdk/overview',
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
                                label: 'Twitter',
                                href: 'https://x.com/kaleidoswap',
                            },
                        ],
                    },
                    {
                        title: 'More',
                        items: [
                            {
                                label: 'GitHub',
                                href: 'https://github.com/kaleidoswap',
                            },
                            {
                                label: 'Website',
                                href: 'https://kaleidoswap.com',
                            },
                        ],
                    },
                ],
                copyright: `Copyright © ${new Date().getFullYear()} KaleidoSwap. Built with Docusaurus.`,
            },
            prism: {
                theme: lightCodeTheme,
                darkTheme: darkCodeTheme,
                additionalLanguages: ['python', 'bash', 'typescript', 'rust'],
            },
        }),
};

module.exports = config;
