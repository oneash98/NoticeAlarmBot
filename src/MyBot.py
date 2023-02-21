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
        subscribers = db.get_subscribers(site_name) # (SUBSCRIPTION id, USER id, USER chatid, USER name)
        
        for one in subscribers:
            chat_id = one[2]
            if chat_id == 0: # 아직 인증코드 입력 전인 유저
                pass
            else: # 인증 후 chatid 등록 완료된 유저
                self.bot.send_message(chat_id = chat_id, text = text, parse_mode = "Markdown", disable_web_page_preview = True)

                # 기록 db에 저장
                subscription_id = one[0]
                db.save_NOTICE_LOG(subscription_id, text)
        
        db.SUBSCRIPTION.close()

    # 오류 발생 시 알림
    def send_error_info(self, log_file):
        with open (log_file, 'r') as f:
            if f.read(): # 파일에 내용 있을 경우
                self.bot.send_message(chat_id = KEY.TELEGRAM_ONEASH.value, text = f'오류 발생\n{log_file} 확인 필요')
            else: # 파일에 내용 없을 경우
                pass 