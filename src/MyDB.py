import pymysql
from KEY import KEY

class MyDB:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = KEY.MYSQL_USER.value
        self.passwd = KEY.MYSQL_PASSWD.value
        
        self.SITELOG = None
        self.SUBSCRIPTION = None

    # SITELOG 데이터베이스 연결
    def connect_db_SITELOG(self):
        self.SITELOG = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db='SITELOG', charset='utf8')

    # SUBSCRIPTION 데이터베이스 연결
    def connect_db_SUBSCRIPTION(self):
        self.SUBSCRIPTION = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db='SUBSCRIPTION', charset='utf8')
    

    # 사이트 url 가져오기 (self.SUBSCRIPTION 설정 필요)
    def get_url(self, site_name):
        cur = self.SUBSCRIPTION.cursor()
        sql = f"""
            SELECT url FROM WEBSITE WHERE site_name = '{site_name}';
            """
        cur.execute(sql)
        url = cur.fetchone()[0]
        return(url)

    # 구독자 정보 가져오기 (self.SUBSCRIPTION 설정 필요)
    def get_subscribers(self, site_name):
        cur = self.SUBSCRIPTION.cursor()
        sql =  f"""
            SELECT S.id, U.id, U.chatid, U.name FROM SUBSCRIPTION S
                INNER JOIN USER U ON S.user_id = U.id
                WHERE website_id = (SELECT id FROM WEBSITE WHERE site_name = '{site_name}');
            """
        cur.execute(sql)
        subscribers = cur.fetchall() # (SUBSCRIPTION id, USER id, USER chatid, USER name)
        return(subscribers)
    
    # SITELOG에 특정 게시물 기록 있나 확인 (self.SITELOG 설정 필요)
    def check_SITELOG(self, site_name, id):
        cur = self.SITELOG.cursor()
        sql = f"""
            SELECT EXISTS (
                SELECT * FROM {site_name} WHERE id = {id}
                );
            """
        cur.execute(sql)
        return cur.fetchone()[0] # 있으면 1, 없으면 0
    
    # SITELOG에 게시물 기록 저장 (self.SITELOG 설정 필요)
    def save_SITELOG(self, site_name, id, title, link):
        cur = self.SITELOG.cursor()
        sql = f"""
            INSERT INTO {site_name} VALUES ({id}, '{title}', '{link}', NOW());
            """
        cur.execute(sql)
        self.SITELOG.commit()

    # SUBSCRIPTION의 NOTICE_LOG테이블에 메시지 기록 저장 (self.SUBSCRIPTION 설정 필요)
    def save_NOTICE_LOG(self, subscription_id, text):
        cur = self.SUBSCRIPTION.cursor()
        sql = f"""
            INSERT INTO NOTICE_LOG (subscription, message_info, datetime)
                VALUES ({subscription_id}, '{text}', NOW());
            """
        cur.execute(sql)
        self.SUBSCRIPTION.commit()