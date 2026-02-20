# 🛡️ Scam Shield Sentinel

> **Autonomous Threat Intelligence for the AI Agent Economy.**
> *Powered by OpenClaw & x402 Protocol on Base L2.*

[![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-00ff41)](https://scamshield.duckdns.org)
[![Network](https://img.shields.io/badge/NETWORK-BASE%20L2-blue)](https://base.org)
[![License](https://img.shields.io/badge/LICENSE-MIT-gray)]()

## 👁️ Overview
[![Scam Shield Status](https://scamshield.duckdns.org/badge/marcodzano-lgtm/scam-shield-sentinel)](https://scamshield.duckdns.org)
The **Scam Shield Sentinel** is an autonomous Python agent designed to protect the OpenClaw ecosystem. It perpetually scans GitHub, Farcaster, and other sources for malicious autonomous skills, wallet drainers, and backdoors.

When a threat is detected, it is logged into a decentralized threat intelligence database, protecting users before they execute dangerous code.

🔴 **Live Dashboard:** [https://scamshield.duckdns.org](https://scamshield.duckdns.org)

## ⚡ Features

- **24/7 Surveillance:** Runs as a systemd service, scanning repositories hourly.
- **Pattern Recognition:** Detects `private_key` leaks, infinite approvals (`type(uint256).max`), and obfuscated code (`eval`, `exec`).
- **x402 Monetization:** Threat data is accessible via a crypto-gated API (Pay-per-Request).
- **Auto-Reporting:** Alerts admins via Telegram and posts warnings to Farcaster.

## 🛠️ Architecture

```mermaid
graph TD;
    GitHub[GitHub API] -->|Scan| Sentinel[🛡️ Sentinel Python Core];
    Farcaster[Neynar API] -->|Scan| Sentinel;
    Sentinel -->|Write| DB[(Threat DB JSON)];
    DB -->|Read| Dashboard[Live Web Dashboard];
    DB -->|Read| x402[💰 x402 Payment Server];
    x402 -->|0.001 USDC| Client[External Agent / User];
