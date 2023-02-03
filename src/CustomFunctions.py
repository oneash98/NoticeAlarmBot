import requests
from bs4 import BeautifulSoup


# soup 생성
def create_soup(url, user_agent, verify = True, parser = "html.parser"):
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, parser)
    return soup