from CustomFunctions import create_soup_selenium, format_string
from KEY import KEY
from selenium.webdriver.common.by import By
import traceback

# SOUP
url = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do"
try:
    soup = create_soup_selenium(url, KEY.USER_AGENT.value)
    notice_list = soup.select("li.notice")

    for notice in notice_list:
        href = notice.a['href']
        id = href.replace("javascript:go_view(", "").replace(");", "")

        title = notice.a.p.text
        title = format_string(title)
        link = (f"https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn={id}&page=1&schStr=regist&pbancEndYn=N")

        print(title, link)

except Exception:
    print(traceback.format_exc())
