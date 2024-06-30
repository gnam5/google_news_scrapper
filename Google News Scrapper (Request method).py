#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import Request, urlopen
import re
from newspaper import Article
from newspaper import Config
import dateparser
from langdetect import detect
from datetime import datetime,timedelta, date
import pandas as pd

# This function takes a URL as input and returns a news link from Google News. 
# It uses the requests and BeautifulSoup modules to extract the link.
def find_news_link(URL11):
    try:
        page=requests.get(URL11,timeout=60)
        soup11 = BeautifulSoup(page.content, 'html.parser')
        result11 = soup11.find('div', {'class':'Pg70bf Uv67qb'})
        links = result11.find_all('a', {'class':'eZt8xd'})
        link_list = links[0]['href']
        return "https://www.google.com/"+link_list
        time.sleep(10)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None


# This function takes a news URL as input and returns a list of dictionaries that contain news data such as source, link, title, and date. 
# It uses the requests and BeautifulSoup modules to extract the data. It also uses a loop to fetch data from multiple pages of Google News.
def find_news_data(url):
    URL = find_news_link(url)
    page=requests.get(URL,timeout=60)
    

    final_list=[]
    page_num = 0
    while page_num < 1:
        page_num += 1
        print(f"{page_num} page:")
        soup11 = BeautifulSoup(page.content, 'html.parser')

        
        result = soup11.find_all('div', {'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})#Gx5Zad xpd EtOod pkphOe #Gx5Zad fP1Qef xpd EtOod pkphOe

        for i in result:
            des={}
            source = i.find('div', {'class':'BNeawe UPmit AP7Wnd lRVwie'}).text
            link = i.find('a')['href'].replace('/url?q=','')
            title = i.find('h3').text
            date=i.find('span', {'class':'r0bn4c rQMQod'}).text

            final_link=link.split('&')[0]

            des['source']=source
            des['link']=final_link
            des['title']=title
            des['date']=date
            final_list.append(des)
        
        try:
            next_link = soup11.find('a', {'aria-label':'Next page'})['href']


            URL1='https://www.google.com/'+next_link
            page=requests.get(URL1,timeout=60)
            print(URL1)
        except:
            break        
    return final_list,soup11
    time.sleep(10)


# This function takes a news link as input and returns the headline of the news. 
# It uses the newspaper module to extract the headline.
def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        page.download()
        page.parse()
        return page.title
    except:
        return 'Untitled Page'


# This function takes a URL as input and returns the title of the webpage. (used if the number of words in headline>10) 
# It uses the requests and BeautifulSoup modules to extract the title.
# def get_page_title(url):
#     try:
#         r = requests.get(url,timeout=60)
#         soup = BeautifulSoup(r.content, "html.parser")
#         if soup.title and soup.title.text:
#             return soup.title.text
#         else:
#             return "Error"
#     except requests.exceptions.Timeout:
#         return "Error"
#     except requests.exceptions.RequestException:
#         return None

def get_page_title(url):
    try:
        r = requests.get(url,timeout=60)
        soup = BeautifulSoup(r.content, "html.parser")
        if soup.find("h1"):
            return soup.find("h1").text
        else:
            return "Error"
    except requests.exceptions.Timeout:
        return "Error"
    except requests.exceptions.RequestException:
        return None


# The handle method first obtains the current date and then calculates the date of yesterday. 
# It uses the datetime module to achieve this.
#now = date.today()

now = datetime.now()
now = now.date()
yesterday = now - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')

y = []
# It constructs a Google search URL by concatenating the keyword and industry category, 
# and then it passes this URL to the find_news_data function to scrape the news data from the Google search results page.
URL = 'https://www.google.com/search?q='+'real estate gurgaon news'
print(URL)


data,soup11 = find_news_data(URL)
user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
print("*"*50)                  
#print(data)


# The code then processes the scraped news data by extracting the date of each article and filtering out any articles that 
# are not from the previous day. 
DATE = []
for i in data:
    if i['date']:
        date = dateparser.parse(i['date'])
    if date:
        date = date.strftime("%Y-%m-%d")
        DATE.append(date)

filtered_data = []
for data1, modified_date in zip(data, DATE):
    if modified_date:
        data1['Modified Dates'] = modified_date
        filtered_data.append(data1)



    filtered_data_final = []
    for data2 in filtered_data:
        if data2['Modified Dates']:
            modified_date = dateparser.parse(data2['Modified Dates'], date_formats=['%Y-%m-%d'])
            modified_date = modified_date.strftime('%Y-%m-%d')
            if modified_date == yesterday:
                filtered_data_final.append(data2)



# It filters out any articles that are not in English.
list1 = []
for item in filtered_data_final:
    title = item['title']
    if detect(title) == 'en':  
        list1.append(item)     
        

# This fetches the headline if number of words>10.
for item in list1:
    if len(item['title'].split()) > 10:
        item['title'] = get_page_title(item['link'])
    else:
        item['title'] = headlines(item['link']) 
    

# Removes news of the given sources
list1 = [x for x in list1 if isinstance(x, dict) and x.get('source') is not None and ('Analytics Insight' not in x['source']) and ('Informist' not in x['source']) and
         ('Home' not in x['source']) and ('Medium' not in x['source']) and ('Macro Hive' not in x['source']) and
         ('SourceSecurity.com' not in x['source']) and ('Airbus' not in x['source']) and 
         ('Aviation International News' not in x['source']) and ('Fitch Ratings' not in x['source']) and 
         ('www' not in x['source']) and ('Stock Market | FinancialContent Business Page' not in x['source']) 
         and ('502' not in x['source']) and ('POPSUGAR Australia' not in x['source']) and 
         ('Arab News' not in x['source']) and ('The Financial Express' not in x['source']) and 
         ('Seeking Alpha' not in x['source']) and ('Dalal Street Investment Journal' not in x['source']) and 
         ('Detroit News' not in x['source']) and ('Beaver County Times' not in x['source']) and 
         ('The New York Times' not in x['source']) and ('52 week high stocks: Stock market update: Stocks that hit 52-week ...' not in x['source']) 
         and ('European Commission' not in x['source']) and ('Financial Times' not in x['source'])
         and ('chescotimes.com |' not in x['source']) and ('Times Higher Education' not in x['source'])
         and ('UBC In The News' not in x['source']) and ('The Fayetteville Observer' not in x['source'])
         and ('Top Gear' not in x['source']) and ('Construction World' not in x['source'])
         and ('Illinois.gov' not in x['source']) and ('Dalhousie University' not in x['source'])
         and ('Redfin' not in x['source']) and ('Yahoo Finance' not in x['source'])]       




# Removes news of the given title
list1 = [x for x in list1 if isinstance(x, dict) and x.get('title') is not None and ('Error' not in x['title']) and ('Captcha' not in x['title']) and
         ('Are you a robot?' not in x['title']) and ('Untitled Page' not in x['title']) and 
         ('Subscribe' not in x['title']) and ('You are being redirected...' not in x['title']) and 
         ('Not Acceptable!' not in x['title']) and ('403 Forbidden' not in x['title']) and 
         ('ERROR: The request could not be satisfied' not in x['title']) and ('Just a moment...' not in x['title']) and 
         ('403 - Forbidden: Access is denied.' not in x['title']) and ('Not Found' not in x['title']) and 
         ('Page Not Found' not in x['title']) and ('StackPath' not in x['title']) and ('Access denied' not in x['title'])
         and ('Yahoo' not in x['title']) and ('Stock Market Insights' not in x['title']) and 
         ('Attention Required!' not in x['title']) and ('Access Denied' not in x['title'])
         and ('403 forbidden' not in x['title']) and ('Too Many Requests' not in x['title'])
         and ('403 - Forbidden' not in x['title']) and ('NCSC' not in x['title'])
         and ('BC Gov News' not in x['title']) and ('The Verge' not in x['title']) and ('Trackinsight' not in x['title'])
         and ('Morning Headlines' not in x['title']) and ('Forbidden' not in x['title'])
         and ('forbidden' not in x['title']) and ('Detroit Free Press' not in x['title'])
         and ('reuters.com' not in x['title']) and ('403 unauthorized' not in x['title'])
         and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
         and ('Your access to this site has been limited by the site owner' not in x['title'])
         and ('404 - File or directory not found.' not in x['title'])]


# Changing the this relevant source name
for item in list1:
    if 'Fortune India: Business News, Strategy, Finance and Corporate ...' in item['source']:
        item['source'] = 'Fortune India'
#print("-"*50)
#print(list1)  
# Add the keyword to each item in the list


# Extend the all_data list with the current list1
y.extend(list1)
df = pd.DataFrame(y)
df

