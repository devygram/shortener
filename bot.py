import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Get environment variables for tokens
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BITLY_TOKEN = os.getenv('BITLY_TOKEN')
BITLY_API_URL = 'https://api-ssl.bitly.com/v4/shorten'

# Function to shorten URLs using Bitly
def shorten_url(url):
    headers = {
        'Authorization': f'Bearer {BITLY_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        'long_url': url,
    }
    response = requests.post(BITLY_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('link')
    else:
        return None

# Command handler to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a link, and I will shorten it for you!')

# Command handler to shorten URLs
def shorten(update: Update, context: CallbackContext) -> None:
    long_url = ' '.join(context.args)
    if not long_url:
        update.message.reply_text('Please provide a URL to shorten.')
        return
    short_url = shorten_url(long_url)
    if short_url:
        update.message.reply_text(f'Shortened URL: {short_url}')
    else:
        update.message.reply_text('Failed to shorten URL. Please try again.')

# Main function to start the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('shorten', shorten))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
