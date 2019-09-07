# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import psycopg2 as pg2

def queryToSQL(listedChart):
    # 이 부분 받아올 수 있게 짜 놓은거 가져오기.
    conn = pg2.connect( host='localhost', port=5432, user="postgres",
                           password="mocha00", database="postgres" )

    conn.autocommit = True
    curs = conn.cursor()

    try:
        curs.execute("CREATE DATABASE melonchart")
    except Exception as e:
        print("\nDB is Already Exist\nKeep Going.\n")
        curs.execute("ALTER DATABASE melonchart")
        curs.execute("DROP TABLE chartmelon")

        pass

    curs.execute("ALTER DATABASE melonchart")
    
    ## TODO: 각 쿼리문 설명 달기
    curs.execute(
        "CREATE TABLE chartmelon(_id SERIAL PRIMARY KEY,"  
        " img VARCHAR(500),"      
        " name VARCHAR(150) NOT NULL,"
        " artist VARCHAR(150) DEFAULT 'Unknown',"
        " album VARCHAR(150))"
    )

    for i in range(0, 400, 4):
        curs.execute(
            "INSERT INTO chartmelon "
            "( img, name, artist, album )"
            "VALUES ( '%s', '%s', '%s', '%s' );" %(listedChart[i], listedChart[i + 1], listedChart[i + 2], listedChart[i + 3])
        )

    conn.close()

def parse():
    URL = "https://www.melon.com/chart/index.htm"

    # Header의 경우 인터넷을 참고했다. 멜론의 내부 구조 변경으로 인해
    # 일반적인 방법으로 Requests를 사용 불가하기 때문.
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    res = requests.get(URL, headers = header) # 멜론 사이트 가져옴.

    soup = BeautifulSoup(res.text, 'lxml')

    # Tag : div in ellipsis
    songList = soup.find_all("div", {"class" : "ellipsis"})
    imgList = soup.find_all("img", {"src" : True})

    cleanedList = []
    cleanedImgList = []

    del imgList[:26]
    for srcc in imgList:
        cleanedImgList.append(srcc['src'])
    del cleanedImgList[100:]

    # 필요 없는 인자 제거
    for src in songList:
        cleanedList.append(src.find("a").get_text())

    del cleanedList[:6]

    for i in range(0, 100):
        cleanedList.insert(i + (3 * i), cleanedImgList[i])

    queryToSQL(cleanedList)

def init():
    parse()
    print("Parsing Success!\nPlease Check PostgreSQL DataBase!")
init()
