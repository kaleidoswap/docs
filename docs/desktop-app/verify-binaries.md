---
sidebar_position: 2.5
---

# Verifying Binary Downloads

[← Back to Installation](./installation.md)

Security is crucial when installing applications that handle your assets. This guide explains how to verify the authenticity of the Kaleidoswap Desktop App binaries you download.

## Why Verify Downloads?

Verifying downloaded binaries is an essential security practice to ensure:
- The file hasn't been tampered with or corrupted during download
- You're installing software created by the actual Kaleidoswap developers
- No malicious code has been injected into the application

## Prerequisites

Before you begin verification, you'll need:
- **GPG** (GNU Privacy Guard) installed on your system
- **curl** or a web browser to download files
- The Kaleidoswap binary you want to verify

## Verification Process

### 1. Import the Developer's Public Key

First, you need to import the Kaleidoswap developer's public GPG key:

```sh
# Option 1: Import directly from GitHub
curl -s https://github.com/bitwalt.gpg | gpg --import

```

### 2. Download the Manifest and Signature

From the [Releases](https://github.com/kaleidoswap/desktop-app/releases) page, download:
- Your desired application binary
- `manifest.txt` - A file containing checksums of all release files
- `manifest.txt.sig` - The GPG signature for the manifest file

### 3. Verify the Manifest Signature

Verify that the manifest was created by the Kaleidoswap developers:

```sh
gpg --verify manifest.txt.sig manifest.txt
```

You should see output similar to:
```
gpg: Signature made Wed 13 Mar 2024 03:11:45 PM CET
gpg: using RSA key 8F8FDBB8B397E731381A42B8F8D2XXXXXXXXXXXXX
gpg: Good signature from "Walter (Kaleidoswap Developer) <walter@kaleidoswap.com>" [ultimate]
```

Make sure it says "Good signature" and check that the key ID matches the expected key.

### 4. Verify Your Binary's Checksum

Verify that your downloaded binary's checksum matches the one in the manifest:

```sh
# On macOS/Linux
shasum -a 256 Kaleido-Swap_[version]_[platform].dmg

# On Windows (PowerShell)
Get-FileHash -Algorithm SHA256 Kaleido-Swap_[version]_[platform].exe
```

Compare the output hash with the corresponding hash in the `manifest.txt` file. They should match exactly.

## Troubleshooting

If verification fails, there are several potential issues:

1. **"No public key" error**: You haven't imported the correct public key.
2. **"BAD signature" error**: The manifest file has been tampered with or corrupted.
3. **Checksum mismatch**: The binary file is corrupted or has been modified.

In any of these cases, **DO NOT INSTALL THE APPLICATION**. Instead:
- Try downloading the files again from the official source
- Contact the Kaleidoswap team via [GitHub Issues](https://github.com/kaleidoswap/desktop-app/issues) or [Discord](https://discord.gg/kaleidoswap)

## Example Manifest File

A `manifest.txt` file typically looks like this:

```
# Kaleidoswap Desktop App v0.0.1 Release
# Generated: 2024-03-13

8a7d3e2f1b5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d  Kaleido-Swap_0.0.1_x64.dmg
2f1b5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d0e4f2c  Kaleido-Swap_0.0.1_x64-setup.exe
5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d0e4f2c7b8a9d3e2f1b5c9a6d0e4f2c7b8a  kaleido-swap_0.0.1_amd64.AppImage
```

---

*Next: [Creating a New Wallet](./creating-wallet.md) or [RGB Lightning Node Hosting](./node-hosting.md)* 