import telegram
from MyDB import MyDB
from KEY import KEY

class MyBot:
    def __init__(self, bot_token):
        self.bot = telegram.Bot(bot_token)

    # 각 구독자들에게 메시지 보내기 (+ 메시지 기록 db에 저장)
    def send_message_to_subscribers(self, site_name, text):
        db = MyDB()
        db.connect_db_SUBSCRIPTION()
        subscribers = db.get_subscribers(site_name)
        
        for one in subscribers:
            chat_id = one[3]
            self.bot.send_message(chat_id = chat_id, text = text, parse_mode = "Markdown", disable_web_page_preview = True)

            # 기록 db에 저장
            subscription_id = one[0]
            db.save_NOTICE_LOG(subscription_id, text)
        
        db.SUBSCRIPTION.close()

    # 오류 메시지 (+ 기록 db에 저장)
    def send_error_message(self, site_name, error_message):
        self.bot.send_message(chat_id = KEY.TELEGRAM_ERROR_CHATID.value, text = f"{site_name} 오류 발생\n{error_message}")

        # 기록 db에 저장
        db = MyDB()
        db.connect_db_SUBSCRIPTION()
        db.save_ERROR_LOG(site_name, error_message)
        db.SUBSCRIPTION.close()