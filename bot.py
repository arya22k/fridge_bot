from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from database import add_subscriber, get_subscribers
from flask import Flask
import threading

TOKEN = "8464694895:AAHX0BJeHCr7jXV0RC-f4jeIyVhPAz39nfM"

# Create Flask app
app = Flask(__name__)

def send_message(chat_id, text):
    """Send a message to a specific chat"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()

def broadcast_to_fridge(fridge_id, message):
    """Send a message to all subscribers of a fridge"""
    subscribers = get_subscribers(fridge_id)
    print(f"Broadcasting to {len(subscribers)} subscribers...")
    for chat_id in subscribers:
        send_message(chat_id, message)
        print(f"Sent to {chat_id}")

# Flask route for triggering reminders
@app.route('/trigger', methods=['GET'])
def trigger_reminders():
    """Send expiry reminders to all subscribers"""
    fridge_id = "arya"
    message = "⚠️ Food expiring soon! Check your fridge."
    
    broadcast_to_fridge(fridge_id, message)
    
    return f"<h1>Reminders Sent!</h1><p>Sent to all subscribers of fridge: {fridge_id}</p>"

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧊 Welcome to Freedge Bot!\n\n"
        "Commands:\n"
        "/join [fridge_name] - Subscribe to notifications\n"
        "/add [food_item] - Add food and notify others"
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User subscribes to a fridge"""
    chat_id = update.effective_chat.id
    fridge_id = context.args[0] if context.args else "default"
    add_subscriber(fridge_id, chat_id)
    await update.message.reply_text(
        f"✅ Subscribed to fridge: {fridge_id}\n"
        f"Your chat ID: {chat_id}"
    )

async def add_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User adds food and broadcasts to all subscribers"""
    fridge_id = "arya"
    food_item = " ".join(context.args) if context.args else "Unknown item"
    message = f"🍎 New food added: {food_item}"
    broadcast_to_fridge(fridge_id, message)
    await update.message.reply_text(
        f"✅ Added: {food_item}\n"
        f"📢 Notifications sent!"
    )

def run_bot():
    """Run the Telegram bot"""
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("join", join))
    bot_app.add_handler(CommandHandler("add", add_food))
    print("🤖 Bot is running with broadcast functionality...")
    bot_app.run_polling()

def run_flask():
    """Run the Flask web server"""
    print("🌐 Flask server starting on http://localhost:5000")
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run bot in main thread
    run_bot()