from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd

# 검색어 결과 제목 및 링크 크로링하기
def craw_title_href(num, news):
    global craw_df
    global href_data
    global search

    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome('./util/chromedriver', options=options)

    url = 'https://www.google.com/search?q='
    url += search
        
    # 뉴스 페이지에서 검색
    if news == 1:        
        url += '&source=lmns&tbm=nws' 

        url += '&start='
        url += str(num) + str(0)
        
        driver.get(url)
        
        html = driver.page_source
        soup = BeautifulSoup(html)
        
        title = soup.select('.xuvV6b.BGxR7d')             
        
        for i in title:      
            craw_df = craw_df.append({'title' : i.select_one('.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d').text}, ignore_index=True)
            href_data.append(i.a.attrs['href'])

        driver.close()
    
    # 전체 페이지에서 검색
    else:        
        url += '&start='
        url += str(num) + str(0)
        
        driver.get(url)
        
        html = driver.page_source
        soup = BeautifulSoup(html)
        
        title = soup.select('.kvH3mc.BToiNc.UK95Uc')  
                
        
        for i in title:      
            craw_df = craw_df.append({'title' : i.select_one('.LC20lb.MBeuO.DKV0Md').text}, ignore_index=True)
            href_data.append(i.a.attrs['href'])

        driver.close()


# 수집한 링크의 본문 글까지 크롤링하기
def additional_craw(href_data):
    global craw_df

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")    
    
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome('./util/chromedriver', options=options)

    for i in range(len(href_data)):
        url = href_data[i]
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html)

        text = soup.select('p')
        temp = ''

        for j in text:
            temp += j.text
        craw_df.loc[i, 'text'] = temp    

# 데이터프레임 선언
craw_df = pd.DataFrame({"title" : [],
                   "text" : []}
                   )

# title 링크 저장
href_data = []

# 검색어 입력받기
search = input('검색어를 입력하시요 : ')
news = int(input("\n전체 페이지 검색 : 0 \n뉴스 페이지에서 검색 : 1\n입력 : "))

# 페이지 10개 크로링
for i in range(1):
    craw_title_href(i, news)

# title의 링크에 들어가 본문 크롤링
additional_craw(href_data)

# csv 파일로 저장
file_name = search
craw_df.to_csv(f'./craw_data/{file_name}.csv', encoding='utf-8')