import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
 

# token = 
# id = 

bot = telegram.Bot(token)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start_command(update, context):
    update.reply_text("test")
    print(update.message.chat_id)
 
start_handler = CommandHandler("start", start_command)
dispatcher.add_handler(start_handler)


updater.start_polling()