import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from CustomFunctions import create_soup
from KEY import KEY
import pymysql
import telegram


# 텔레그램 봇
bot = telegram.Bot(KEY.TELEGRAM_TOKEN.value)

# DB 기록
db_SITELOG = pymysql.connect(host='localhost', port=3306, user=KEY.MYSQL_USER.value, passwd=KEY.MYSQL_PASSWD.value, db='SITELOG', charset='utf8')
cur_SITELOG = db_SITELOG.cursor()

db_SUBSCRIPTION = pymysql.connect(host='localhost', port=3306, user=KEY.MYSQL_USER.value, passwd=KEY.MYSQL_PASSWD.value, db='SUBSCRIPTION', charset='utf8')
cur_SUBSCRIPTION = db_SUBSCRIPTION.cursor()

# 구독자들
cur_SUBSCRIPTION.execute("""
    SELECT id, chatid FROM SUBSCRIPTION 
        WHERE website IN (
            SELECT id FROM WEBSITE WHERE site_name = '연세대신소재공학과'
            );
    """)
subscribers = cur_SUBSCRIPTION.fetchall() # (id, chatid)

# SOUP
url = "https://mse.yonsei.ac.kr/mse/board/news.do" # 연세대 신소재공학과 공지 url
soup = create_soup(url, KEY.USER_AGENT.value)
notice_list = soup.select("table.board-table tbody tr")


for notice in notice_list:
    href = notice.a['href']
    id = href.split("&")[1].replace("articleNo=", "")
    cur_SITELOG.execute(f"SELECT EXISTS (SELECT * FROM 연세대신소재공학과 WHERE id = {id})") # DB에 해당 id 있나 확인
    if cur_SITELOG.fetchone()[0] == 1: # 있을 경우
        break
    else: # 없을 경우
        title = notice.a.text.strip()
        link = url + href
        cur_SITELOG.execute(f"INSERT INTO 연세대신소재공학과 VALUES ({id}, '{title}', '{link}', NOW())") # DB에 저장

        # 텔레그램으로 구독자들에게 공지
        for one in subscribers:
            chat_id = one[1] # (id, chatid)
            title = title.replace("[", "{").replace("]", "}")
            text = f"[{title}]({link})" # 텔레그램으로 보낼 메시지
            bot.send_message(chat_id = chat_id, text = text, parse_mode = "Markdown", disable_web_page_preview = True)

            # DB에 로그 저장
            subscription_id = one[0] # (id, chatid)
            cur_SUBSCRIPTION.execute(f"INSERT INTO NOTICE_LOG (subscription, message_info) VALUES ({subscription_id}, '{text}')")


db_SUBSCRIPTION.commit()
db_SITELOG.commit()
db_SUBSCRIPTION.close() 
db_SITELOG.close()