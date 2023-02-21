from MyBot import MyBot
from KEY import KEY

bot = MyBot(KEY.TELEGRAM_TOKEN.value)

bot_command_error = '/home/oneash082498/NoticeAlarmBot/src/bot_command_error.log'
notice_error = '/home/oneash082498/NoticeAlarmBot/src/notice_error.log'

bot.send_error_info(bot_command_error) # bot-command 파일 오류 발생 정보
bot.send_error_info(notice_error) # notice 경로 하 파일들 오류 발생 정보