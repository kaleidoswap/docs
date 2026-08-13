# Translation Guide — Simplified Chinese (`cn`)

Canonical rules and glossary for the Chinese localization of the KaleidoSwap docs.
Read this before translating or updating any file under `mintlify-docs/cn/`.

## Layout

- English (default language) stays at the repo root: `mintlify-docs/<section>/<page>.mdx`.
- Simplified Chinese mirrors that tree one-to-one under `mintlify-docs/cn/`:
  `mintlify-docs/whats-kaleidoswap/introduction.mdx` → `mintlify-docs/cn/whats-kaleidoswap/introduction.mdx`
- `docs.json` declares both under `navigation.languages` (`en` first, then `cn`).
  Adding or removing a page means updating **both** language trees.
- `mintlify-docs/snippets/` is shared. Chinese pages import the same snippet with the
  same absolute path (`/snippets/versions.mdx`) — do not duplicate it.
- `mintlify-docs/openapi.json` is shared and not translated.

## Tooling

Run both after any change to the `cn/` tree:

```bash
python scripts/check-cn-parity.py     # structure, links, anchors, coverage
python scripts/pin-cn-anchors.py      # add --apply to write
```

`check-cn-parity.py` compares every translated page against its English source
(heading count, code fences, components, table rows, images, links), confirms each
page in the `cn` navigation exists, and verifies every internal link is `/cn`-prefixed
and resolves. It exits with `PROBLEMS FOUND` if anything is off.

## What to translate

Translate:

- Prose, headings, list items, table cells.
- Frontmatter **values** for `title`, `sidebarTitle`, `description`.
  For `description`, target **60–80 CJK characters**, not the 150–160 used for
  English. CJK glyphs are roughly double-width, so 60–80 of them occupy the same
  space in a search result as a 150–160 character English description. Do not pad
  a description to hit a count.
- User-facing component props: `title=`, `label=`, `header=`, `<Tooltip>` text,
  `<Accordion title=>`, `<Card title=>`, `<Step title=>`, `<Tab title=>`.
- Image `alt` text (the square-bracket part of `![alt](path)`).
- Comments inside code blocks (`// ...`, `# ...`).

Leave in English / untouched:

- Product and brand names: KaleidoSwap, KaleidoMind, KaleidoAgent, Thunderstack.
- Protocol and standard names: Bitcoin, Lightning, RGB, Taproot Assets, LSPS1, NWC,
  HTLC, PSBT, UTXO, MCP, QVAC.
- All code: identifiers, string literals, JSON keys, API field names, CLI commands
  and flags, env vars, file paths, package names, URLs, version numbers.
- Code-fence language tags and their tab titles (```` ```typescript TypeScript ````).
- Component and prop **names**, and icon/layout values (`icon="wallet"`, `cols={2}`,
  `horizontal`, `openapi=`).
- Image paths (`/assets/images/...`) — only the alt text changes.
- Network names: mainnet is 主网 and testnet is 测试网, but `signet` and `regtest`
  stay lowercase in English.

## Links

- Rewrite every internal absolute link to the `cn` tree:
  `[SDK](/sdk/introduction)` → `[SDK](/cn/sdk/introduction)`
- External links (`https://…`) are unchanged, including their `#fragments`.
- **Anchor fragments on internal links:** leave the English fragment verbatim
  (e.g. `/cn/sdk/websocket#events`), including same-page anchors (`](#some-heading)`).
  Do not translate fragments and do not guess another page's headings.

### How anchors survive translation

Mintlify derives a heading's anchor from its text, so translating a heading would
break every link pointing at it. Instead, any heading that is the target of a link
carries an explicit id with the **English** slug, using Mintlify's `{#custom-id}`
syntax:

```mdx
## 客户端配置 {#client-configuration}
```

The link stays `](/cn/ai-tools/mcp-servers#client-configuration)` and keeps working
no matter how the heading text is later reworded. Consequences:

- Never reorder or drop headings in a translated page — `scripts/pin-cn-anchors.py`
  maps English to Chinese headings by position.
- After adding or changing any cross-page anchor link, re-run that script; it pins
  the ids it needs and reports anything it cannot resolve.
- Headings with no inbound links need no id. Mintlify generates both the id and its
  own table-of-contents link, so those stay self-consistent.
- A fragment containing `&` is normalised (`installation-&-configuration` becomes
  `installation-and-configuration`) and the `cn` links are repointed to match.
  Mintlify keeps `&` when it generates a slug from heading text, but its handling of
  `&` inside an explicit `{#id}` is undocumented; since both sides live in the `cn`
  tree, the script picks an id that cannot be ambiguous. The English pages are
  untouched and keep their original `&` anchors.

## Style

Audience is Chinese-speaking Bitcoin developers and traders. Aim for the register of
good native technical documentation, not literal translation.

- Simplified Chinese (简体), mainland conventions.
- Full-width punctuation for Chinese sentences: `，。：；！？、（）「」`.
  Keep half-width punctuation inside code and inside English phrases.
- Put a half-width space between CJK and adjacent Latin text or numerals:
  `使用 KaleidoSwap 桌面应用`, `需要 2 个通道`.
- Prefer verb-first, concise imperative sentences in instructions (`点击「创建钱包」`).
- Do not pad. If the English is one sentence, the Chinese is one sentence.
- Keep Markdown structure identical: same heading levels, same list nesting,
  same number of table rows, same component tree. Only text changes.
- UI labels that appear in the app's English interface: translate, then keep the
  English in parentheses on first use in a page — `点击「解锁钱包」(Unlock Wallet)`.

## Positioning

Do **not** frame KaleidoSwap as an RGB-first product. It is a multi-protocol Bitcoin
DEX; RGB is one of the supported Bitcoin layers. Use 多协议 / 比特币分层 framing.
This applies especially to `title` and `description` frontmatter.

## Glossary

| English | 简体中文 | Note |
|---|---|---|
| atomic swap | 原子交换 | |
| swap (noun/verb) | 交换 | consistent with 原子交换; never 兑换 |
| swap protocol | 交换协议 | |
| trading pair | 交易对 | |
| quote | 报价 | |
| request for quote (RFQ) | 询价 | |
| order | 订单 | |
| Lightning Network | 闪电网络 | |
| Lightning channel | 闪电通道 | `channel` alone → 通道 |
| open a channel | 开通通道 | |
| channel capacity | 通道容量 | |
| inbound / outbound liquidity | 入向流动性 / 出向流动性 | |
| liquidity | 流动性 | |
| LSP (Lightning Service Provider) | 闪电服务提供商（LSP） | |
| market maker | 做市商 | |
| maker / taker | 做市方 / 接单方 | |
| node | 节点 | |
| peer | 对等节点 | |
| non-custodial | 非托管 | |
| custodial | 托管 | |
| trustless | 无需信任 | |
| self-custody / sovereign | 自主保管 / 自主掌控 | |
| wallet | 钱包 | |
| mnemonic / recovery phrase | 助记词 | |
| seed | 种子 | |
| unlock the wallet | 解锁钱包 | |
| on-chain / off-chain | 链上 / 链下 | |
| Bitcoin | 比特币 | |
| BTC | BTC | never translate the ticker |
| sats / satoshis | 聪 | |
| Bitcoin Layers | 比特币分层协议 | |
| Layer 2 | 二层 | |
| RGB assets | RGB 资产 | |
| asset ID | 资产 ID | |
| mainnet / testnet | 主网 / 测试网 | |
| deposit | 存入 | noun 存入操作 / 充值 in UI context |
| withdrawal | 提取 | |
| balance | 余额 | |
| payment | 支付 | |
| invoice | 发票 | Lightning invoice → 闪电发票 |
| fee | 费用 | routing fee → 路由费 |
| backup | 备份 | |
| restore | 恢复 | |
| desktop app | 桌面应用 | |
| browser extension | 浏览器扩展 | |
| DApp | DApp | |
| open source | 开源 | |
| whitelist | 白名单 | |
| rate limit | 速率限制 | |
| endpoint | 接口端点 | |
| webhook | Webhook | |
| SDK / CLI / API / REST | keep in English | |
