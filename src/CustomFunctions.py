import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# soup 생성
def create_soup(url, user_agent, verify = True, parser = "html.parser"):
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()
    # 인코딩 문제 해결
    if not 'charset' in res.headers['content-type']:
        res.encoding = res.apparent_encoding

    soup = BeautifulSoup(res.text, parser)
    return soup

# soup 생성 - selenium 사용
def create_soup_selenium(url, user_agent, wait_for = None):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f"user-agent = {user_agent}")
    options.add_argument("window-size=1920x1080")
    options.add_argument("--no-sandbox") # 서버 no GUI
    options.add_argument("--disable-dev-shm-usage") # /dev/shm 디렉토리 사용 X
    options.add_argument("--disable-gpu") 
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    prefs = {'profile.default_content_setting_values': {'cookies'                   : 2, 'images': 2,
                                                        'plugins'                   : 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications'             : 2, 'auto_select_certificate': 2,
                                                        'fullscreen'                : 2,
                                                        'mouselock'                 : 2, 'mixed_script': 2,
                                                        'media_stream'              : 2,
                                                        'media_stream_mic'          : 2, 'media_stream_camera': 2,
                                                        'protocol_handlers'         : 2,
                                                        'ppapi_broker'              : 2, 'automatic_downloads': 2,
                                                        'midi_sysex'                : 2,
                                                        'push_messaging'            : 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop'   : 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement'           : 2,
                                                        'durable_storage'           : 2}}

    options.add_experimental_option('prefs', prefs)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    
    browser = webdriver.Chrome("./../../chromedriver", options=options)
    # browser.set_page_load_timeout(10) # 10초 이상 타임아웃 발생 시 에러 발생

    try:
        browser.get(url)
        # if wait_for == None:
        #     pass
        # else: # 특정 요소 기다리기
        #     WebDriverWait(browser, 120).until(EC.presence_of_element_located(wait_for)) # 10초

        soup = BeautifulSoup(browser.page_source, "html.parser")

    except:
        print(traceback.format_exc())

    finally:
        browser.quit()

    return soup


# 문자열 포맷팅 (오류 방지)
def format_string(text):
    text = text.replace("[", "{").replace("]", "}") # 텔레그램 봇 하이퍼링크 [] 인식 방해 방지
    text = text.replace("'", "")
    text = text.strip()
    return text