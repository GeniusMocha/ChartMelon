# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import pymysql

def queryToSQL(listedChart):
    # DB 접속
    sql = pymysql.connect(host='localhost', port=3306, user="root",
                         passwd="mocha00", charset="utf8", autocommit=True)
 
    # 잘 모르겠지만 커넥트 후 SQL 명령어 쿼리를 내릴 커서를 준비하는듯.
    # 일단 SQL은 처음 다루니 조심스럽게..(?)
    cursor = sql.cursor()
 
    # (대충 실행을 execute() 함수로 한다는 설명)
    try:
        cursor.execute("create database MelonChart;")
    except pymysql.err.ProgrammingError:   # 대충 예외처리.. 배우면서 합시다!
        print("\nDB is Already Exist")     # log 보면서 예외처리 하니까 잘 되네..
        print("Keep Going Next Part!\n")
        cursor.execute("use melonchart;")
        cursor.execute("drop table chartmelon;")  # 함수가 여러번 실행된다면 행이 무한으로 늘어남
                                                  # 또한 멜론차트 갱신의 문제도 있기에 이렇게 함.
        pass

    cursor.execute("use melonchart;")
    
    ## TODO: 각 쿼리문 설명 달기!
    cursor.execute(
        "CREATE TABLE chartmelon(_id INT AUTO_INCREMENT PRIMARY KEY,"
        " name VARCHAR(1000) NOT NULL,"
        " artist VARCHAR(1000) DEFAULT 'Unknown',"
        " album VARCHAR(1000)) ENGINE=INNODB;"
    )

    for i in range(0, 300, 3):
        ## if (corsor.exe)
        cursor.execute("INSERT INTO chartmelon"
        " ( name, artist, album ) "
        "VALUES ( '%s', '%s', '%s' );" %(listedChart[i], listedChart[i + 1], listedChart[i + 2])
        )

    # connect() 후 close()로 연결 종료.
    sql.close()

def parse():
    URL = "https://www.melon.com/chart/index.htm"

    # Header의 경우 인터넷을 참고했다. 멜론의 내부 구조 변경으로 인해
    # 일반적인 방법으로 Requests를 사용 불가하기 때문.
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    res = requests.get(URL, headers = header) # 멜론 사이트 가져옴.

    soup = BeautifulSoup(res.text, 'lxml')

    # 받아온 HTML의 태그들 중 class에 ellipsis가 포함된 div 찾아 저장.
    coreList = soup.find_all("div", {"class" : "ellipsis"})

    # 리스트 생성
    tmp = []
    cleanedList = []

    # 후처리, 필요 없는 인자 제거.
    for src in coreList:
        tmp.append(src.find("a"))

    for src1 in tmp:
        cleanedList.append(src1.get_text())

    del cleanedList[:6]

    # SQL로 넘긴다!
    queryToSQL(cleanedList)

def init():
    parse()
    print("Parsing Success!\nPlease Check MariaDB DataBase!")
init()
## TODO: JS측으로 넘겨서 Object로 후처리.