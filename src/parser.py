# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import pymysql

def queryToSQL(listedChart):
    # DB Connect
    sql = pymysql.connect( host='localhost', port=3306, user="root",
                           passwd="mocha00", charset="utf8", autocommit=True )

    cursor = sql.cursor()

    try:
        cursor.execute("create database MelonChart;")
    except pymysql.err.ProgrammingError:   # 예외 처리
        print("\nDB is Already Exist")
        print("Keep Going Next Part!\n")
        cursor.execute("use melonchart;")
        cursor.execute("drop table chartmelon;")

        pass

    cursor.execute("use melonchart;")
    
    ## TODO: 각 쿼리문 설명 달기
    cursor.execute(
        "CREATE TABLE chartmelon(_id INT AUTO_INCREMENT PRIMARY KEY,"  
        " img VARCHAR(1000),"      
        " name VARCHAR(1000) NOT NULL,"
        " artist VARCHAR(1000) DEFAULT 'Unknown',"
        " album VARCHAR(1000)) ENGINE=INNODB;"
    )

    for i in range(0, 400, 4):
        cursor.execute(
            "INSERT INTO chartmelon"
            " ( img, name, artist, album ) "
            "VALUES ( '%s', '%s', '%s', '%s' );" %(listedChart[i], listedChart[i + 1], listedChart[i + 2], listedChart[i + 3])
        )

    sql.close()

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
    print("Parsing Success!\nPlease Check MariaDB DataBase!")
init()