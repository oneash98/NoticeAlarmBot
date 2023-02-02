from telegram.ext import Updater, CommandHandler
import pymysql
from pymysql.err import IntegrityError
from KEY import KEY


updater = Updater(token=KEY.TELEGRAM_TOKEN.value, use_context=True)
dispatcher = updater.dispatcher

# /start 누를 때 실행할 함수
def start_command(update, context):
    # SUBSCRIPTION DB 접속
    con = pymysql.connect(host='localhost', port=3306, user=KEY.MYSQL_USER.value, passwd=KEY.MYSQL_PASSWD.value, db='SUBSCRIPTION', charset='utf8')
    cur = con.cursor()

    chat_id = update.message.chat_id # 사용자 텔레그램 chat_id
    firstname = update.message.from_user.first_name # 사용자 이름
    lastname = update.message.from_user.last_name # 사용자 성

    # USER 테이블에 사용자 정보 저장(id, 이름, 등록 날짜)
    try:
        sql = f"INSERT INTO USER (chatid, lastname, firstname, date_enrolled) VALUES({chat_id}, '{lastname}', '{firstname}', NOW())"
        cur.execute(sql)
        con.commit()
    except IntegrityError as e: # chatid가 동일한 경우, 즉 /start를 동일 인물이 두 번 이상 눌렀을 경우
        pass
    
    con.close()

    # 환영 메시지
    update.message.reply_text("안녕하세요!")
 

# /start 명령 추가 
start_handler = CommandHandler("start", start_command)
dispatcher.add_handler(start_handler)

# 실행
updater.start_polling()