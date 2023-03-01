import datetime
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from CustomFunctions import create_soup, format_string
from KEY import KEY
from MyBot import MyBot
from MyDB import MyDB

# 사이트
site_name = '경북대국제교류처'

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
    notice_list = soup.select("tbody tr")
    top_notice_list = [n for n in notice_list if n.td.text == '공지'] # 상단 고정 공지
    bottom_notice_list = [n for n in notice_list if n.td.text != '공지'] # 하단 공지

    if top_notice_list == [] or bottom_notice_list == []: # 무슨 이유에서든, 제대로 크롤링이 안됐을 때
        raise Exception('notice_list가 비었습니다')

    # 상단 고정 공지
    for notice in top_notice_list:
        href = notice.a['href']
        id = href.split('&')[1].replace("mv_data=", "")

        check = db.check_SITELOG(site_name, id) # DB에 해당 id 있나 확인
        if check == 1: # 있을 경우
            break
        else: # 없을 경우
            title = notice.a.text
            title = format_string(title)
            link = "https://home.knu.ac.kr" + href
            db.save_SITELOG(site_name, id, title, link) # db SITELOG에 게시물 기록 저장

            # 텔레그램으로 구독자들에게 공지
            text = f"{site_name}\n[{title}]({link})" # 텔레그램으로 보낼 메시지
            bot.send_message_to_subscribers(site_name, text)

    # 하단 공지
    for notice in bottom_notice_list:
        href = notice.a['href']
        id = href.split('&')[1].replace("mv_data=", "")

        check = db.check_SITELOG(site_name, id) # DB에 해당 id 있나 확인
        if check == 1: # 있을 경우
            break
        else: # 없을 경우
            title = notice.a.text
            title = format_string(title)
            link = "https://home.knu.ac.kr" + href
            db.save_SITELOG(site_name, id, title, link) # db SITELOG에 게시물 기록 저장

            # 텔레그램으로 구독자들에게 공지
            text = f"{site_name}\n[{title}]({link})" # 텔레그램으로 보낼 메시지
            bot.send_message_to_subscribers(site_name, text)

except Exception:
    print(datetime.datetime.now())
    print(traceback.format_exc())

db.SITELOG.close()
db.SUBSCRIPTION.close()