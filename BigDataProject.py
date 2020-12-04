
# 네이버 뉴스 IT/과학 부분 최근 30일간 가장 많이나온 단어 상위 30개

import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import requests
from collections import Counter
import matplotlib
from matplotlib import font_manager
from datetime import date, timedelta
from konlpy.tag import Okt
import time
import sys

font_location = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.figsize'] = (12, 6)

okt = Okt()
stopwords = []

with open('stopword.txt', 'r', encoding="UTF8") as file:
    stopwords = file.readlines()
    for index, word in enumerate(stopwords):
        stopwords[index] = word.replace('\n', '')
    print("stopword 읽기끝")


def multireplaceEmpty(strData, replacewords):
    for word in list(replacewords):
        strData = strData.replace(word, '')
    return strData


def multiwordreplaceEmpty(strData):
    for word in stopwords:
        if(word == strData):
            strData = strData.replace(word, '')
    return strData


def StringSplit(strData):
    words = okt.nouns(strData)
    # words = strData.split(' ')
    result = []
    for word in words:
        temp = multireplaceEmpty(
            word, '\',\".·/<>}{][;:?!\r\n\t“‘’”…#-`()\u2028®')
        temp = multiwordreplaceEmpty(
            temp)
        if(temp != ''):
            result.append(temp)

    return result


def paging(sid, date, number):
    url = f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2={sid}&sid1=105&date={date}&page={number}'
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = bs(res, "html.parser")
    pages = soup.select('.paging > a')
    pagelist = []
    for page in pages:
        if(page.get_text() == '다음'):
            return paging(sid, date, number+10)
        pagelist.append(page.get_text())

    if(pagelist == []):
        return 1
    if(pagelist[-1] == '이전'):
        return number
    return pagelist[-1]


days = 0

if len(sys.argv) != 2:
    days = 1
else:
    if(sys.argv[1].isdecimal()):
        days = int(sys.argv[1])
    else:
        days = 1


sids = [731, 226, 227, 230, 732, 283, 229, 228]
group = {731: '모바일', 226: '인터넷SNS', 227: '통신뉴미디어', 230: 'IT일반',
         732: '보안해킹', 283: '컴퓨터', 229: '게임리뷰', 228: '과학일반'}
today = date.today()
startTime = time.time()

dic = {}

for sid in sids:
    sei = []
    for i in range(days):
        DateData = (today - timedelta(days=i)).isoformat().replace('-', '')
        print(f'sid = {sid}, Date = {DateData} Point')

        for page in range(1, int(paging(sid, DateData, 1))+1):
            url = f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2={sid}&sid1=105&date={DateData}&page={page}'
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
            soup = bs(res, "html.parser")
            list_title = soup.select('#main_content li a')
            print(f'{page}번 페이지 검색 Point')
            for title in list_title:
                sei.extend(StringSplit(title.get_text()))
    dic[sid] = sei
print(
    f"-------------------------{round(time.time() - startTime,2)}초-------------------------")


DFdatas = {}
for key, value in dic.items():
    DFdatas[key] = pd.DataFrame(pd.Series(Counter(value)), columns=['count'])

excel_writer = pd.ExcelWriter(u'네이버뉴스_IT_과학_제목_단어수.xlsx', engine='xlsxwriter')
i = 0
for key, value in DFdatas.items():
    DFdata = value.sort_values(['count'], ascending=False)
    DFdata.to_excel(excel_writer, index=True, sheet_name=f'분류 {group[key]}')
    topDFdata = DFdata.head(30)
    topDFdata.to_excel(excel_writer, index=True,
                       sheet_name=f'분류 {group[key]} 상위30개 단어들')
    topDFdata.sort_values(['count']).plot(kind='barh')
    plt.title(f'{group[key]}뉴스 최근 {days}일간 가장 많이 나온 단어 상위 30개')
    i = i+1


excel_writer.save()
plt.show()
