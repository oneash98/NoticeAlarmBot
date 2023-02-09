import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from CustomFunctions import create_soup
from KEY import KEY
from MyBot import MyBot
from MyDB import MyDB

# 사이트
site_name = '연세대신소재공학과'

# 텔레그램 봇
bot = MyBot(KEY.TELEGRAM_TOKEN.value)

# 데이터베이스
db = MyDB()
db.connect_db_SITELOG()
db.connect_db_SUBSCRIPTION()

# SOUP
url = db.get_url(site_name) # 공지 url
try:
    soup = create_soup(url, KEY.USER_AGENT.value)
    notice_list = soup.select("table.board-table tbody tr")


    for notice in notice_list:
        href = notice.a['href']
        id = href.split("&")[1].replace("articleNo=", "")

        check = db.check_SITELOG(site_name, id) # DB에 해당 id 있나 확인
        if check == 1: # 있을 경우
            break
        else: # 없을 경우
            title = notice.a.text.strip()
            link = url + href
            db.save_SITELOG(site_name, id, title, link) # db SITELOG에 게시물 기록 저장

            # 텔레그램으로 구독자들에게 공지
            title = title.replace("[", "{").replace("]", "}")
            text = f"[{title}]({link})" # 텔레그램으로 보낼 메시지
            bot.send_message_to_subscribers(site_name, text)

except:
    pass

db.SITELOG.close()
db.SUBSCRIPTION.close()