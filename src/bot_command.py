from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pymysql
from KEY import KEY


updater = Updater(token=KEY.TELEGRAM_TOKEN.value, use_context=True)
dispatcher = updater.dispatcher

VERIFICATION = range(1)

# /start 누를 때 실행할 함수
def start_command(update, context):
    
    # 구독 시작 버튼
    buttons = [[InlineKeyboardButton('구독 시작', callback_data= "start")]]
    reply_markup = InlineKeyboardMarkup(buttons)
 
    # 환영 메시지
    update.message.reply_text(text = "안녕하세요! 사이트 알람입니다.\n구독 시작 버튼을 누른 후 인증번호를 입력해야 구독이 시작됩니다!", reply_markup = reply_markup)

# 인증번호 입력 (구독 시작 버튼 눌렀을 때)
def enter_code(update, context):
    query = update.callback_query
    if query.data == "start":
        context.bot.edit_message_text(chat_id = query.message.chat_id, message_id = query.message.message_id, text = "인증코드를 입력해주세요")
        return VERIFICATION

# 인증번호 확인
def verification(update, context):
    chat_id = update.message.chat_id
    verification_code = update.message.text # 인증번호
    verification_code = verification_code.replace("\\", '') # 역슬래시 오류 방지
    
    # 인증 종료
    if verification_code == '종료':
        update.message.reply_text('인증 종료')
        return ConversationHandler.END

    con = pymysql.connect(host='localhost', port=3306, user=KEY.MYSQL_USER.value, passwd=KEY.MYSQL_PASSWD.value, db='SUBSCRIPTION', charset='utf8')
    cur = con.cursor()
    # 인증번호가 db에 있나 확인
    sql = f"SELECT EXISTS (SELECT * FROM USER WHERE id = '{verification_code}');"
    cur.execute(sql)  
    check = cur.fetchone()[0] # 있으면 1, 없으면 0

    if check == 0: # 잘못된 인증번호
        update.message.reply_text("잘못된 인증번호입니다. 다시 입력하거나 '종료'를 입력해주세요.")
        con.close()
        return VERIFICATION
    
    else: # 해당 인증번호가 db에 존재
        sql = f"SELECT chatid FROM USER WHERE id = '{verification_code}';"
        cur.execute(sql)
        chatid = cur.fetchone()[0]
        
        # 해당 인증번호에 chatid 등록
        if chatid == 0:
            sql = f"UPDATE USER SET chatid = {chat_id} WHERE id = '{verification_code}';" # 유저 chatid 등록
            cur.execute(sql)
            con.commit()
            con.close()
            update.message.reply_text("사용자 등록이 완료되었습니다.")
            return ConversationHandler.END
            
        # 이미 할당된 chatid가 있는 경우
        else:
            update.message.reply_text("이미 등록된 유저입니다. 관리자에게 문의하세요.")
            con.close()
            return ConversationHandler.END
        
    
# 내 구독 리스트 확인
def mysubs_command(update, context):
    chat_id = update.message.chat_id

    con = pymysql.connect(host='localhost', port=3306, user=KEY.MYSQL_USER.value, passwd=KEY.MYSQL_PASSWD.value, db='SUBSCRIPTION', charset='utf8')
    cur = con.cursor()
    sql = f"""
        SELECT site_name FROM WEBSITE W 
            INNER JOIN SUBSCRIPTION S ON W.id = S.website_id 
            WHERE S.user_id = (SELECT id FROM USER WHERE chatid = {chat_id});
        """
    cur.execute(sql)
    websites = cur.fetchall()
    text = ""
    for w in websites:
        text += w[0] + "\n"
    text = text.strip()
    con.close()

    if text == "": # 구독 정보 없는 경우
        text = "구독한 사이트가 없습니다."
        
    update.message.reply_text(text)


start_command_handler = CommandHandler("start", start_command)
enter_code_hander = CallbackQueryHandler(enter_code)
mysubs_command_handler = CommandHandler("mysubs", mysubs_command)


# 사용자 인증 절차
verify_handler = ConversationHandler(
    entry_points = [enter_code_hander], # 구독 시작 버튼 누르면 인증 절차 시작
    states = {VERIFICATION: [MessageHandler(Filters.text, verification)]},
    fallbacks = [enter_code_hander]
)

# handler 추가
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(verify_handler)
dispatcher.add_handler(mysubs_command_handler)

# 실행
updater.start_polling()