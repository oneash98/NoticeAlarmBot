import requests
from bs4 import BeautifulSoup


# soup 생성
def create_soup(url, user_agent, verify = True, parser = "html.parser"):
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, parser)
    return soup

# 문자열 포맷팅 (오류 방지)
def format_string(text):
    text = text.replace("[", "{").replace("]", "}") # 텔레그램 봇 하이퍼링크 [] 인식 방해 방지
    text = text.replace("'", "")
    text = text.strip()
    return text