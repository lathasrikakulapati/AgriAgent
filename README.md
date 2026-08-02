<p align="center">
  <img src="https://img.shields.io/badge/Claude-Opus%204.6-blueviolet?style=for-the-badge&logo=anthropic" />
  <img src="https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

# 🌾 AgriAgent — AI-Powered Agricultural Intelligence

> **Multi-agent platform that democratizes agricultural expertise for farmers worldwide — in French, English, and Wolof.**

Built for the **"Built with Claude: Claude Code Hackathon"** (February 10–16, 2026).

---

## 🎯 The Problem

Over **500 million smallholder farmers** worldwide lack access to timely, expert agricultural advice. Language barriers, costly consultants, and limited internet connectivity leave them making decisions based on incomplete information — leading to crop losses, pest damage, and missed market opportunities.

## 💡 The Solution

**AgriAgent** is an autonomous multi-agent AI system powered by **Claude Opus 4.6** that delivers personalized, real-time advice on **weather**, **crop management**, **disease diagnosis**, and **market pricing** — accessible via web, mobile, or SMS in the farmer's own language.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent Chat** | Orchestrator routes queries to specialized Weather, Agro, and Market agents running in parallel |
| 📸 **Crop Photo Diagnosis** | Upload a photo → Claude Vision identifies diseases and recommends treatments |
| 🎤 **Voice Input/Output** | Speech-to-text input + text-to-speech for responses (accessibility) |
| 🌍 **Interactive World Map** | Leaflet map with 20+ countries, agricultural data, and city-level weather |
| 🗓️ **Agricultural Calendar** | Zone-specific planting calendars in grid and timeline views |
| 🌱 **Field Management** | Full CRUD for parcelles (fields), crops, season history, rotation advice |
| 📊 **Market Intelligence** | Crop prices by region with inter-city comparison |
| 📱 **SMS Interface** | Text METEO, NJEG, TOOL, or JEGGE via Twilio — response in Wolof or French |
| 🌗 **Dark/Light Theme** | Full theme support with CSS variables |
| 🌐 **Trilingual** | French, English, and Wolof across every page and notification |
| 🏆 **Gamification** | Farmer levels, badges, and achievement stats |
| 🔔 **Smart Alerts** | AI-generated personalized alerts (weather, pests, market, calendar) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    USERS                            │
│            Web · SMS · Voice                        │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│              NEXT.JS 16 FRONTEND                    │
│     React 19 · Tailwind 4 · Framer Motion           │
│     Auth · i18n (FR/EN/WO) · Dark/Light             │
└────────────────────┬────────────────────────────────┘
                     │ REST + SSE Streaming
┌────────────────────┴────────────────────────────────┐
│              FASTAPI BACKEND                        │
│        Supabase JWT · Public + Protected Routes     │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│            ORCHESTRATOR AGENT                       │
│         Claude Sonnet 4 · Keyword Routing           │
│      Auto Language Detection · Multi-Agent Sync     │
└──────┬─────────────┬──────────────┬─────────────────┘
       │             │              │
┌──────┴──────┐ ┌────┴─────┐ ┌─────┴──────┐
│ WEATHER     │ │  AGRO    │ │  MARKET    │
│ Claude 3    │ │ Claude 3 │ │  Claude 3  │
│ Haiku       │ │ Haiku    │ │  Haiku     │
│ +Open-Meteo │ │ +Crops   │ │  +Prices   │
│  Tool Use   │ │ +Disease │ │  +Compare  │
│  50+ cities │ │ +Zones   │ │  Tool Use  │
└─────────────┘ └──────────┘ └────────────┘
```

Each agent uses **Claude tool-use** to call specialized functions (weather API, crop database, market data), then the orchestrator synthesizes a unified response.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Claude Sonnet 4 (orchestrator) + Claude 3 Haiku (sub-agents) |
| **Backend** | Python 3.12 · FastAPI · Uvicorn |
| **Frontend** | Next.js 16 · React 19 · TypeScript 5 |
| **Styling** | Tailwind CSS 4 · Framer Motion 12 |
| **Maps** | Leaflet · React-Leaflet |
| **Auth** | Supabase (PostgreSQL · JWT · RLS) |
| **SMS** | Twilio |
| **Weather** | Open-Meteo API (free, no key required) |
| **AI Vision** | Claude Vision (crop photo diagnosis) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase project (free tier works)
- Anthropic API key

### 1. Clone & Setup

```bash
git clone https://github.com/MedouneSGB/AgriAgent-SN.git
cd AgriAgent-SN
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_JWT_SECRET=your-jwt-secret
# Optional:
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
```

Run the SQL migration in your Supabase dashboard:
```bash
# Copy backend/migration.sql into Supabase SQL Editor and execute
```

Start the server:
```bash
uvicorn main:app --reload --port 8095
```

### 3. Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
NEXT_PUBLIC_API_URL=http://localhost:8095/api
```

Start the dev server:
```bash
npm run dev
```

Open **http://localhost:3000** 🎉

---

## 📡 API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | AI chat (JSON response) |
| `POST` | `/api/chat/stream` | AI chat (SSE streaming) |
| `GET` | `/api/weather/{city}` | 7-day forecast for 50+ cities |
| `POST` | `/api/diagnose` | Crop photo diagnosis (Vision) |
| `POST` | `/api/sms/incoming` | Twilio SMS webhook |
| `GET` | `/api/crops` | Crop database |
| `GET` | `/api/markets` | Market prices |
| `GET` | `/api/zones` | Agro-ecological zones |
| `GET` | `/api/cities` | City coordinates |

### Protected (JWT required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/PUT` | `/api/me` | User profile |
| `GET/POST` | `/api/parcelles` | Field management |
| `GET/POST` | `/api/cultures` | Crop tracking |
| `GET/POST` | `/api/history` | Season history |
| `GET` | `/api/alerts` | Personalized alerts |
| `POST` | `/api/alerts/generate` | AI-generate alerts |
| `GET` | `/api/calendar/{zone}` | Agricultural calendar |
| `GET` | `/api/rotation/{id}` | Crop rotation advice |

---

## 🌍 Coverage

- **50+ cities** with weather data across 5 continents
- **20+ countries** with agricultural data (crops, zones, markets)
- **16+ agro-ecological zones** with specific crop calendars
- **50+ crops** with full growing guides
- **3 languages** — French, English, Wolof

---

## 📁 Project Structure

```
agriagent/
├── backend/
│   ├── main.py               # FastAPI app entry
│   ├── api.py                # Public endpoints
│   ├── api_protected.py      # JWT-protected endpoints
│   ├── auth.py               # Supabase JWT verification
│   ├── config.py             # Settings, cities, zones
│   ├── data_loader.py        # JSON data loader
│   ├── migration.sql         # Supabase DB schema + RLS
│   ├── agents/
│   │   ├── orchestrator.py   # Multi-agent router
│   │   ├── weather_agent.py  # Weather + Open-Meteo
│   │   ├── agro_agent.py     # Crops + diseases + zones
│   │   ├── market_agent.py   # Prices + comparison
│   │   └── alerts_agent.py   # AI alert generation
│   ├── services/
│   │   ├── weather_service.py    # Open-Meteo client
│   │   ├── supabase_service.py   # Supabase client
│   │   └── sms_service.py        # Twilio SMS parsing
│   └── data/
│       ├── crops.json        # Crop knowledge base
│       ├── diseases.json     # Disease/pest database
│       ├── markets.json      # Market price data
│       └── zones.json        # Agro-ecological zones
│
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages (7 routes)
│       ├── components/       # React components (12)
│       ├── components/ui/    # Design system (14)
│       ├── context/          # Auth, Language, Theme
│       ├── lib/              # API client, Supabase
│       └── data/             # World agriculture data
│
└── .claude/docs/             # Project documentation
```

---

## 🤝 How Claude is Used

AgriAgent is built entirely on the **Claude Opus 4.6 ecosystem**, leveraging its capabilities across the entire stack:

1. **Claude Opus 4.6** — Powers the orchestrator agent for intelligent routing, language detection, and multi-agent synthesis
2. **Claude 3 Haiku** — Fast sub-agents (weather, agro, market) with tool-use for real-time data access
3. **Claude Vision** — Crop disease diagnosis from uploaded photos
4. **Tool Use** — Each agent defines tools (functions) that Claude calls to fetch weather data, search crops, compare prices
5. **Multilingual** — Claude generates responses in French, English, or Wolof based on detected language
6. **Streaming** — SSE streaming for word-by-word chat responses
7. **Claude Code** — The entire project was built using Claude Code as the development agent

---

## 📜 License

MIT — See [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ for the <strong>Claude Code Hackathon 2026</strong>
  <br/>
  <em>Empowering farmers worldwide with AI-driven agricultural intelligence</em>
</p>
Here are the commands to run your project locally. You will need to open **two separate terminal windows**.

**1. Run the Backend (FastAPI)**
In your first terminal, navigate to the `backend` folder and start the Uvicorn server:
```powershell
cd C:\Users\latha\OneDrive\Pictures\Desktop\AgriAgent-main\backend
python -m uvicorn main:app --reload --port 8095
```

**2. Run the Frontend (Next.js)**
In your second terminal, navigate to the `frontend` folder and start the development server:
```powershell
cd C:\Users\latha\OneDrive\Pictures\Desktop\AgriAgent-main\frontend
npm run dev
```

Once both are running, your application will be available in your browser at `http://localhost:3000`.