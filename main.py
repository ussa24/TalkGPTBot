from telegram.ext import *
import openai
from keys import OPENAI_KEY, TELEGRAM_KEY

openai.api_key = OPENAI_KEY

print("Starting up bot...")


def start_command(update, context):
    update.message.reply_text("Hello, I'm TalkGPT, your Telegram AI assistant :)")


def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": text}],
    )
    print(response)
    reply_content = response.choices[0].message.content
    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    update.message.reply_text(reply_content)


def error(update, context):
    print(f'error: {context.error}')


if __name__ == '__main__':
    updater = Updater(TELEGRAM_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(1.0)
    updater.idle()