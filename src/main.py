import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pymysql
from pymysql.err import IntegrityError
 

# token = 
# id = 
# user = 
# passwd = 

bot = telegram.Bot(token)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start_command(update, context):
    con = pymysql.connect(host='localhost', port=3306, user=user, passwd=passwd, db='SUBSCRIPTION', charset='utf8')
    cur = con.cursor()

    chat_id = update.message.chat_id
    firstname = update.message.from_user.first_name
    lastname = update.message.from_user.last_name

    try:
        sql = f"INSERT INTO USER (chatid, lastname, firstname, date_enrolled) VALUES({chat_id}, '{lastname}', '{firstname}', NOW())"
        cur.execute(sql)
        con.commit()
    except IntegrityError as e:
        pass
    
    con.close()

    update.message.reply_text("안녕하세요!")
 

start_handler = CommandHandler("start", start_command)
dispatcher.add_handler(start_handler)

updater.start_polling()