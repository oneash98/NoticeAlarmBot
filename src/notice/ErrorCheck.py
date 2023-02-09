import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from CustomFunctions import create_soup
from KEY import KEY
from MyBot import MyBot
from MyDB import MyDB

# 텔레그램 봇
bot = MyBot(KEY.TELEGRAM_TOKEN.value)

# 데이터베이스
db = MyDB()
db.connect_db_SUBSCRIPTION()


######################## 연세대신소재공학과 ################################
site_name = '연세대신소재공학과'

try:
    url = db.get_url(site_name) # 공지 url
    soup = create_soup(url, KEY.USER_AGENT.value)
    notice_list = soup.select("table.board-table tbody tr333")
    if notice_list == []:
        raise Exception('notice_list가 비었습니다')
    for notice in notice_list:
        href = notice.a['href']
        id = href.split("&")[1].replace("articleNo=", "")
        title = notice.a.text.strip()
except Exception as e:
    bot.send_error_message(site_name, e)


#######################################################################
db.SUBSCRIPTION.close()