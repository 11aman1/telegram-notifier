import os
import requests
from flask import Flask
from threading import Thread
from telethon.sync import TelegramClient, events

######################
# 1) KEEP-ALIVE SETUP (For Replit & UptimeRobot)
######################
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

########################
# 2) TELEGRAM SETUP (Environment Variables)
########################
API_ID = os.getenv("27801749")  
API_HASH = os.getenv("fd15670a0247a978f008987ea0581e13")
PHONE_NUMBER = os.getenv("+917049042428")  

if not API_ID or not API_HASH or not PHONE_NUMBER:
    raise ValueError("Missing API_ID, API_HASH, or PHONE_NUMBER. Set them as environment variables.")

# Keywords to monitor
keywords = ['1BHK', '1 bhk', '1 BHK', '1bhk', '1BHK', '1 BHK', '1 BHK' '1BHK', '1 BHK', '1BHK', '1 BHK', '1 BHK', '1-BHK', '1-bhk']

# Create a Telethon client session
client = TelegramClient("session_name", API_ID, API_HASH)

###############################
# 3) EVENT HANDLER FOR MESSAGES
###############################
@client.on(events.NewMessage)
async def new_message_listener(event):
    message_text = event.message.message or ""
    message_text_lower = message_text.lower()

    # Check for matching keywords
    if any(keyword.lower() in message_text_lower for keyword in keywords):
        chat_id = event.chat_id
        message_id = event.message.id

        # Construct a link to view the post
        if str(chat_id).startswith("-100"):
            message_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{message_id}"
        else:
            if event.chat and hasattr(event.chat, 'username') and event.chat.username:
                message_link = f"https://t.me/{event.chat.username}/{message_id}"
            else:
                message_link = "🔗 Link Not Available"

        # Send a notification to "Saved Messages"
        await client.send_message(
            "me",
            f"🚨 *New Matching Post* 🚨\n\n{message_text}\n\n🔗 [View Post]({message_link})",
            parse_mode="Markdown"
        )

########################
# 4) MAIN FUNCTION
########################
def run_telegram_client():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        client.sign_in(PHONE_NUMBER, input('Enter the code: '))

    print("✅ Telegram client is running...")
    client.run_until_disconnected()

def main():
    keep_alive()  # Start Flask for UptimeRobot

    telegram_thread = Thread(target=run_telegram_client)
    telegram_thread.daemon = True
    telegram_thread.start()

    try:
        while True:
            import time
            time.sleep(60)
    except KeyboardInterrupt:
        print("❌ Shutting down...")

if __name__ == "__main__":
    main()

