# Telegram AI Travel & Business Advisor (Text-only)
This repository contains a ready-to-deploy Telegram bot that uses **Gemini** (for deep travel & business advice)
and **Groq** (for fast factual responses). It is a **text-only** assistant for now.

## Files
- `bot.py` - Main bot script (text-only).
- `requirements.txt` - Python dependencies.
- `README.md` - This file.

## Setup (Railway / Replit / Render / Local)
1. Create a Telegram bot with BotFather and get `TELEGRAM_TOKEN`.
2. Create a Gemini API key (Google AI Studio) -> `GEMINI_KEY` (optional if you prefer only Groq).
3. Create a Groq API key -> `GROQ_KEY` (optional if you prefer only Gemini).
4. (Optional) If you only want one model, set only that model's key.

## Environment variables
Set the following environment variables in your host (Railway / Replit Secrets / Render):

- `TELEGRAM_TOKEN` (required)
- `GEMINI_KEY` (recommended)
- `GROQ_KEY` (recommended)

## Deploy on Railway (quick)
- Create a new project on https://railway.app
- Connect to this GitHub repo or paste the `bot.py` file into a Railway project
- Add Environment variables in the Railway project settings
- Set the start command to: `python3 bot.py`
- Deploy. Check logs — you should see `Bot starting...`.

## Deploy on Replit (quick)
- Create a new Repl (Python)
- Upload `bot.py` and `requirements.txt`
- Add secrets in the Replit Secrets tab (`TELEGRAM_TOKEN`, `GEMINI_KEY`, `GROQ_KEY`)
- Click Run

## Usage
- Open your Telegram bot and send `/start`
- Ask travel or business questions in plain English.

## Next steps / Upgrades
- Add travel API integrations (Skyscanner / Amadeus) for live price comparison.
- Add persistence (Airtable / Postgres) for memory & client data.
- Add voice (STT/TTS) later if you want voice replies.

## Notes & Security
- Do not commit your API keys to public repos. Use environment variables / secrets.
- This repo is provided as-is for testing and quick deployment.
