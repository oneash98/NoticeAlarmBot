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

### bot_command.py

텔레그램 봇 명령

<br/>

### MyDB.py

### MyBot.py

### notice 디렉토리

- Yonsei_MSE: 연세대 신소재공학과
- Yonsei_Engineering: 연세대 공과대학

<br/>

### 작업 플로우

1. 카톡으로 사용자 정보, 구독할 사이트 파악

2. (신규 사이트인 경우) test 파일에 크롤링 코드 작성 -> id, 제목, 링크 제대로 출력되나 확인

3. (신규 사이트인 경우) SITELOG 데이터베이스에 해당 사이트 테이블 생성
```sql
CREATE TABLE '사이트이름' (
	id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    url VARCHAR(500),
    datetime DATETIME NOT NULL,
    PRIMARY KEY (id)
);
```

4. (신규 사이트인 경우) WEBSITE 테이블에 웹사이트 정보 저장
```sql
INSERT INTO WEBSITE (site_name, url) VALUES ('사이트이름', '사이트url');
```

5. 크롤링 코드 완성

6. (신규 사이트인 경우) SITELOG 데이터베이스에 기록 저장 (크롤링 코드의 MyDB.host를 서버 ip로 변경해서 save_sitelog까지만 실행)

7. (신규 유저인 경우) SUBSCRIPTION 데이터베이스 USER 테이블에 유저 저장
```sql
INSERT INTO USER VALUES ('인증코드', 0, '이름', NOW());
-- chatid 는 0으로 지정
```

8. SUBSCRIPTION 테이블에 구독 정보 저장
```sql
INSERT INTO SUBSCRIPTION (website_id, date_start, user_id) VALUES ((SELECT id FROM WEBSITE WHERE site_name = '사이트이름'), NOW(), '인증코드');
```

9. (신규 사이트인 경우) 서버 notice 경로에 크롤링 파일 저장, crontab 추가 후 재시작 (sudo service cron restart)

10. (신규 유저인 경우) 유저에게 카톡으로 텔레그램 링크와 인증코드 제공 (유저가 인증코드 입력하면 자동으로 데이터베이스에 chatid 저장)

11. (기존 유저인 경우) 유저에게 등록 완료 안내

12. 끝

13. 혹시나 오류 발생하는지 확인하기 위해 log 때때로 확인