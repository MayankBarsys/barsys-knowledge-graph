# Barsys AI — Knowledge Graph

Interactive knowledge graph of the Barsys AI iOS app and Defteros backend. 89 nodes across iOS, Backend API, Data, Infrastructure, and BLE/Hardware layers.

## Features

- Force-directed graph with 89 nodes and 168+ connections
- Directory view — browse all nodes by category
- **AI Search** — ask natural language questions, get answers with clickable node references

## Deploy to Railway (recommended — one URL to share)

1. Fork or clone this repo to your GitHub account
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Select this repo
4. After deploy: go to **Variables** tab → add:
   ```
   ANTHROPIC_API_KEY = sk-ant-api03-...
   ```
5. Railway redeploys automatically → share the generated URL

Anyone who opens the URL gets full AI search with no setup.

## Run locally

```bash
python3 server.py
# Opens http://localhost:8765 in your browser
```

Without `ANTHROPIC_API_KEY` set, you'll see a **NO KEY** badge in the search bar. Click it to enter your own Anthropic API key.

## How to search

- Press `/` or click **SEARCH** to open
- **AI SEARCH** — any natural language question:
  - *how are mixlists populated?*
  - *show me how station connects to recipe endpoint*
  - *what happens after BLE sends pour complete?*
  - *how does auth work end to end?*
- **NODE SEARCH** — short keyword queries like `auth-flow` or `delta-sync`

## Stack

- Pure HTML/CSS/JS — no build step, no npm
- Python standard library server — no pip installs
- Claude Haiku via Anthropic API for AI search
