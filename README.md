### Version

python: 3.10.5

beautifulsoup4: 4.10.0

selenium: 4.7.2

requests: 2.27.1

python-telegram-bot: 13.10

PyMySQL: 1.0.2

<br/>

### 초기 데이터베이스

DB_init.sql: 초기 데이터베이스 및 테이블 생성 쿼리 정리

DB_Export: 초기 데이터베이스 추출 파일

<br/>

### KEY.py

src 경로 밑에 KEY.py 파일 생성 후 아래 내용 추가
- USER_AGENT = ""
- TELEGRAM_TOKEN = ""
- MYSQL_USER = ""
- MYSQL_PASSWD = ""

<br/>

### start_command.py

텔레그램 봇 첫 시작(/start) 시 사용자 정보 db 저장 및 환영 메시지 전송

<br/>

### MyDB.py

### MyBot.py

### notice 디렉토리

YONSEI_MSE: 연세대 신소재공학과