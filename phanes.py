from telethon import TelegramClient, events
import re
import asyncio
from flask import Flask

# Your API credentials (from https://my.telegram.org)
api_id = 29355939  # Replace with your API ID
api_hash = 'f2979dc0234f4803f57e9c57a5f4346b'  # Replace with your API Hash

# The group/chat to listen to
source_chat_id = -4544449317  # Replace with the group/chat ID to listen to
# The group/chat to send messages to
target_chat_id = -1002477832073  # Replace with the target group/chat ID
# Bot's user ID or username in the group
bot_username = 'diabolicalChef_bot'  # Replace with the bot's username

# Initialize the Telegram client
client = TelegramClient('user_session', api_id, api_hash)

# Initialize Flask app
app = Flask(__name__)

@client.on(events.NewMessage(chats=source_chat_id))
async def handler(event):
    try:
        # Check if the message is from the specified bot
        sender = await event.get_sender()
        if sender.username == bot_username:
            print(f"New message from {bot_username} in {source_chat_id}: {event.text}")

            # Extract the part after "Mint Address:"
            mint_address = None
            for line in event.text.splitlines():
                # Remove potential formatting (e.g., ** or spaces) and look for "Mint Address:"
                line = line.strip()
                match = re.match(r"\*\*?Mint Address:\*\*?\s*(.+)", line)
                if match:
                    mint_address = match.group(1).strip()
                    break
            
            if mint_address:
                # Format the message as `/pf mint`
                formatted_message = f'/pf {mint_address}'
                print(f"Formatted message: {formatted_message}")
                # Add a 10-second delay before sending the message
                await asyncio.sleep(10)
                # Send the formatted Mint Address to the target group
                await client.send_message(target_chat_id, formatted_message)
                print(f"Formatted message forwarded to target group: {formatted_message}")
            else:
                print("No Mint Address found in the message.")
        else:
            print(f"Ignored message from {sender.username} or another user.")
    except Exception as e:
        print(f"Error while forwarding message: {e}")

# Flask route for health checks
@app.route('/')
def health_check():
    return "The bot is running and listening for messages."

# Flask route to check the current status
@app.route('/status')
def status():
    return "Bot is active and monitoring the source group."

async def main():
    print("Starting the user session...")
    # Start the client
    await client.start()
    print("User session started. Listening for messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import threading

    # Run the Telethon bot in a separate thread
    bot_thread = threading.Thread(target=lambda: asyncio.run(main()))
    bot_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=8080)
