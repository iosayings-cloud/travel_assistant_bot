    # bot.py - Telegram AI Travel & Business Advisor (text-only)
    # Usage: set required env vars (see README) and run `python3 bot.py`
import os
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")    # Google Gemini API key
GROQ_KEY = os.environ.get("GROQ_KEY")        # Groq API key
if not TELEGRAM_TOKEN:
    raise SystemExit("Please set TELEGRAM_TOKEN env var")
if not (GEMINI_KEY or GROQ_KEY):
    raise SystemExit("Please set at least one of GEMINI_KEY or GROQ_KEY env vars")
def ask_groq(prompt):
    if not GROQ_KEY:
        return None
    try:
        url = "https://api.groq.com/v1/models/groq-1.1/outputs"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
            payload = {"input": prompt}
            r = requests.post(url, json=payload, headers=headers, timeout=20)
            r.raise_for_status()
            out = r.json()
            # Groq response structures vary; attempt to extract text
            if isinstance(out, dict):
                if 'output' in out:
                    return out['output']
                # fallback: stringify
                return str(out)
            return str(out)
        except Exception as e:
            print("Groq error:", e)
            return None

    def ask_gemini(prompt):
        if not GEMINI_KEY:
            return None
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            params = {"key": GEMINI_KEY}
            headers = {"Content-Type": "application/json"}
            body = {
                "temperature": 0.2,
                "candidateCount": 1,
                "maxOutputTokens": 800,
                "prompt": {
                    "text": prompt
                }
            }
            r = requests.post(url, params=params, json=body, headers=headers, timeout=30)
            r.raise_for_status()
            dd = r.json()
            candidates = dd.get("candidates") or []
            if candidates:
                # Gemini returns content with parts -- defensive extraction
                content = candidates[0].get("content") or {}
                parts = content.get("parts") or []
                if parts and isinstance(parts, list) and len(parts) > 0:
                    return parts[0].get("text") or str(parts[0])
            # fallback stringify
            return str(dd)
        except Exception as e:
            print("Gemini error:", e)
            return None
    def choose_model_for_prompt(prompt):
        quick_keywords = ["time", "duration", "visa", "weather", "price", "cost", "fare", "exchange", "when", "where", "how far", "flight", "hotel"]
        lowered = prompt.lower()
        if any(k in lowered for k in quick_keywords) and len(prompt.split()) < 20:
            return "groq"
        return "gemini"
    def start_cmd(update: Update, context: CallbackContext):
        update.message.reply_text("Hi — I'm your Travel & Business Advisor (text-only). Ask travel or business questions.")
    def help_cmd(update: Update, context: CallbackContext):
        update.message.reply_text("Commands: /start /help
Ask: 'Plan 3 days in Udaipur for 2 adults' or 'Draft a corporate pitch'.")
    def handle_text(update: Update, context: CallbackContext):
        user_text = update.message.text
        model = choose_model_for_prompt(user_text)
        # Try Groq for quick factual answers first when applicable
        if model == "groq" and GROQ_KEY:
            resp = ask_groq(user_text)
            if resp:
                update.message.reply_text(resp)
                return
        # Else fallback to Gemini if available
        if GEMINI_KEY:
            resp = ask_gemini(user_text)
            if resp:
                update.message.reply_text(resp)
                return
        # If nothing returned
        update.message.reply_text("Sorry — I'm having trouble right now. Try again or check the bot logs.")
    def main():
        updater = Updater(TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start_cmd))
        dp.add_handler(CommandHandler("help", help_cmd))
        dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_text))
        print("Bot starting...")
        updater.start_polling()
        updater.idle()
    if __name__ == "__main__":
        main()
