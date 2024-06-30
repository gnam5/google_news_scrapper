#!/usr/bin/env python
# coding: utf-8

# # Invest India (static)

# In[ ]:


import requests
from bs4 import BeautifulSoup
import re

base_url = "https://www.investindia.gov.in"
result_dict = []

page_number = 0
while True:
    URL = f'https://www.investindia.gov.in/schemes-msmes-india?title=&page={page_number}'
    page = requests.get(URL, timeout=60)
    soup = BeautifulSoup(page.content, 'html.parser')

    ul_element = soup.find("ul", attrs={'class': 'msme-list'})
    if not ul_element:
        break

    result = ul_element.find_all("li")

    final_list = []

    for i in result:
        link = i.find('p').find('a')['href']
        link = f'{base_url}{link}'
        final_list.append(link)

    for j in final_list:
        response = requests.get(j)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1').text
        print(title)
    
            
        try:
            link_1 = soup.find("div", attrs={'class': 'msme-apply-section section-background block views-blockmsme-schemes-block-2 block-views'})
            apply_link_element = link_1.find('a')
            apply_link = apply_link_element['href'] if apply_link_element else ''

        except AttributeError:
            apply_link = ''
            
            
        try:
            link_2 = soup.find("div", attrs={'class': 'readmore-section'})
            apply_text_1 = link_2.find('p').text if link_2 and link_2.find('p') else ''
            
            if apply_text_1 == 'Click "Apply Now"':
                apply_text = ''
            else:
                apply_text = apply_text_1

        except AttributeError:
            apply_text = ''

            
            
        try:
            link_2 = soup.find("div", attrs={'class': 'msme-files section-background block views-blockmsme-schemes-block-5 block-views'})
            pdf_link_element = link_2.find('a')
            pdf_link = pdf_link_element['href'] if pdf_link_element else ''
        
        except AttributeError:
            pdf_link = ''
        
        
        all_lines = ""
        ul_elements = soup.find("ul", attrs={'class': "msme-main-table"}).find_all('ul')
        for ul_element in ul_elements:
            li_elements = ul_element.find_all('li')
            for li_element in li_elements:
                all_lines += li_element.get_text(strip=True) + ' '
                
         #new code       
        if soup.find('span', string='SCHEME APPLICABLE FOR') == None:
            scheme_applicable_li = soup.find('span', string='SCHEME APPLICABLE FOR ')
            
        else:
            scheme_applicable_li = soup.find('span', string='SCHEME APPLICABLE FOR')
            
        text_after_scheme = scheme_applicable_li.find_next_sibling().text.strip()

        result_dict.append({'link': j, 'title': title, 'content': all_lines, 'applicable_for': text_after_scheme, 'Apply now link': apply_link, 'Apply now text': apply_text, 'PDF Link': pdf_link, 'state': 'All'})

    page_number += 1


# In[ ]:


type(result_dict)


# # Invest India (live)

# In[ ]:


#chron job will run at 12am

import requests
from bs4 import BeautifulSoup
import re


URL = "https://www.investindia.gov.in"
page = requests.get(URL, timeout=60)
soup = BeautifulSoup(page.content, 'html.parser')

script_tag = soup.find('script', text=re.compile(r'window\.__PRELOADED_STATE__'))
script_content = script_tag.contents[0]

start_index = script_content.find('"id":"policy_incentive_updates"')
end_index = script_content.find(']', start_index)
policy_incentive_updates = script_content[start_index:end_index+1]

pattern = re.compile(r'"url":"(.*?)","title":"(.*?)"')
matches = re.findall(pattern, policy_incentive_updates)

#states list from sql
states = ['Jharkhand','Ladakh','Odisha']

for match in matches:
    url, title = match
    title = re.sub(r'"nofollow":"\d"', '', title)
    url = url.replace(r'u002F', '')
    title = title.replace(r'u002F', '')
    
found_state = "All"
for state in states:
    if state.lower() in title.lower():
        found_state = state

    print(f"Title: {title}\nURL: {url}\nState: {found_state}\n")


    
#add code to match sector and industry from title


# # MSME govt (static) 

# In[ ]:


import requests
from bs4 import BeautifulSoup
import re

def concatenate_dicts(dicts, common_key):
    result_dict = {}

    for d in dicts:
        key_value = d.get(common_key)
        if key_value is not None:
            result_dict[key_value] = {**result_dict.get(key_value, {}), **d}

    return result_dict


URL = "https://msme.gov.in/"
page = requests.get(URL, timeout=60)
soup = BeautifulSoup(page.content, 'html.parser')

schemes_span = soup.find('span', {'title': 'Schemes'})
links = schemes_span.find_next('ul').find_all('a')

base_url = "https://msme.gov.in/"
hrefs = [base_url + link['href'] for link in links][1:]

link_list = []

result_dict_1 = []
result_dict_2 = []
result_dict_3 = []

for i in hrefs:
    page = requests.get(i, timeout=60)
    soup = BeautifulSoup(page.content, 'html.parser')

    div_element = soup.find("div", class_='field-content')
    
    if div_element:
        tr_elements = div_element.find_all('tr')
        
        if tr_elements:
            link_list.append(i)
            
        else:
            h3_tag = div_element.find('a')
            href = h3_tag.get('href')
            link_list.append(href)
            
            
for j in link_list:
    response = requests.get(j)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_element = soup.find("div", class_='field-content')

        
    if div_element:
        tr_elements = div_element.find_all('tr')
        
        for tr_element in tr_elements:
            td_elements = tr_element.find_all('td')

            
            first_td_text = td_elements[0].get_text(strip=True)
            
            if first_td_text == "Related Scheme":
                title = td_elements[1].get_text(strip=True)
                
                
            if first_td_text == "How to apply?":
                apply_link = td_elements[1].get_text(strip=False)

            
            if first_td_text == "Whom to contact" or first_td_text == "Contact":
                apply_text = td_elements[1].get_text(strip=False)
                result_dict_1.append({'link': j,'title': title, 'apply_link': apply_link, 'apply_text': apply_text})
        
        
        for tr_element in tr_elements:
            td_elements = tr_element.find_all('td')
            
            first_td_text = td_elements[0].get_text(strip=True)
            
            if first_td_text == "Related Scheme":
                title = td_elements[1].get_text(strip=True)
                
            if first_td_text == "Who can apply?" or first_td_text == "Eligibility/ Applicability:":
                applicable_for = td_elements[1].get_text(strip=True)
                applicable_for = ' '.join(applicable_for.split())
                
                result_dict_2.append({'title': title, 'applicable_for': applicable_for})
            
            
        for tr_element in tr_elements:
            td_elements = tr_element.find_all('td')
            
            first_td_text = td_elements[0].get_text(strip=True)
            
            if first_td_text == "Related Scheme":
                title = td_elements[1].get_text(strip=True)
                
            if first_td_text == "Description":
                content = td_elements[1].get_text(strip=True)
                
                result_dict_3.append({'title': title, 'content': content})
 

        for item in result_dict_3:
            item['content'] = item['content'].replace('\t', '')

            
merged_dict = {}
for index, item in enumerate(result_dict_1):
    merged_dict[item['title']] = {**item, **result_dict_2[index], **(result_dict_3[index] if index < len(result_dict_3) else {})}


result_list = list(merged_dict.values())

print(result_list)


# # Startup India (static)

# In[ ]:


import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
import numpy as np
import re


driver = webdriver.Chrome()
result_dict = []
link= 'https://www.startupindia.gov.in/content/sih/en/government-schemes.html'
URL = link
driver.get(URL)
driver.implicitly_wait(10)
source = driver.page_source
soup = BeautifulSoup(source, "html.parser")

div_element = soup.find_all("div", attrs={'class': 'card-box'})
#print(div_element)
time.sleep(5)

for i in div_element:
    
    title = i.find('h3').get_text(strip=True)

    
    nodal_ministry_element = i.find('h4', text=' Nodal Ministry/Department: ')
    
    if nodal_ministry_element:
        nodal_ministry = nodal_ministry_element.find_next('p').text.strip()

    
    brief_content_element = i.find('h4', text='Brief:')
    
    if brief_content_element:
        brief_content = brief_content_element.find_next('p', class_='readmore').text.strip()

    eligibility_criteria_div = i.find('div', class_='readmore')
    
    ul_element_1 = eligibility_criteria_div.find('ul')
    
    if ul_element_1:
        applicable_for = ' '.join([li.text for li in ul_element_1.find_all('li')])

    
    benefits_div = eligibility_criteria_div.find_next('div', class_='readmore')

    ul_element_2 = benefits_div.find('ul')
    
    if ul_element_2:
        benefits_content = ' '.join([li.text for li in ul_element_2.find_all('li')])


    link_element = i.find("div", attrs={'class': 'link-set'})
    
    if link_element:
        link = link_element.find('p').find('a')['href']
    

    content = nodal_ministry +". "+ brief_content + benefits_content
    
    states = ['Jharkhand','Ladakh','Odisha']

    found_state = "All"
    for state in states:
        if state.lower() in title.lower():
            found_state = state

    result_dict.append({'link': URL, 'title': title, 'content': content, 'applicable_for': applicable_for, 'Apply now link': link,'state': found_state})


    
    


# In[ ]:


print(result_dict)

