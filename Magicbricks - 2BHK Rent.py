#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import timedelta
from selenium import webdriver
import numpy as np


# In[ ]:


driver = webdriver.Chrome()


# In[ ]:


#url of the page that we want to Scarpe
#+str() is used to convert int datatype of the page no. and concatenate that to a URL for pagination purposes.
driver = webdriver.Chrome()
URL = 'https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Dwarka-Expressway&cityName=Gurgaon'

driver.get(URL)
source = driver.page_source
soup = BeautifulSoup(source, "html.parser")
news_titles = {}
news_titles_count = 0

links = soup.find_all("div",attrs={'class':"mb-srp__card"})
print(links)


# In[ ]:


tag_dup = []
page_break = -10

while len(tag_dup)<=3000 and len(tag_dup)>=page_break:
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    news_titles = {}
    news_titles_count = 0
    links = soup.find_all("div",attrs={'class':"mb-srp__card"})
    
    try:
        new_tags = set(links).difference(tag_dup)
    except:
        new_tags = links

    tag_dup = []

    for tag_du in links:
        tag_dup.append(tag_du)

    page_break+=1
    
    #print(len(new_tags))
    #print(len(tag_dup))
    
    for row in new_tags:
        label=[]
        details=[]

        title=row.find("h2",attrs={'class':"mb-srp__card--title"}).text
        #print(title)
        
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    next_page = driver.find_elements_by_class_name('autoload_continue')
    driver.execute_script("$(arguments[0]).click();", next_page)
    time.sleep(2)


# In[ ]:


len(tag_dup)


# In[ ]:


for row in tag_dup:
    label1=[]
    label2=[]
    details=[]

    title=row.find("h2",attrs={'class':"mb-srp__card--title"}).text
    #print("Title :",title)
    
#To extract heading
    if row.find("div",attrs={"class":"mb-srp__card__society"}) != None:
        society=row.find("div",attrs={"class":"mb-srp__card__society"}).text
        #print("Society Name :",society)
    else:
        society="Not mentioned"
        #print("Society Name :",society)

#To extract builder name
    if row.find("div",attrs={"class":"mb-srp__card__ads--name"}) != None:
        builder=row.find("div",attrs={"class":"mb-srp__card__ads--name"}).text
        #print("Builder/Agent : ",builder)
    elif row.find("div",attrs={"class":"mb-srp__card__ads__info--name"}) != None :
        builder=row.find("div",attrs={"mb-srp__card__ads__info--name"}).text
        #print("Builder/Agent : ",builder)
    else:
        builder="Not mentioned"
        #print("Builder/Agent : ",builder)
        
#To extract establishment year
    if row.find("div",attrs={"class":"mb-srp__card__ads--since"}) != None:
        Since=row.find("div",attrs={"class":"mb-srp__card__ads--since"}).text
        #print(Since)
    else:
        Since="Not mentioned"
        #print("Operating Since : ",Since)
        
#To extract number of buyers served
    if row.find("div",attrs={"class":"mb-srp__card__ads--served"}) != None:
        Served=row.find("div",attrs={"class":"mb-srp__card__ads--served"}).text
       # print("Buyers Served : ",Served)
    elif row.find("div",attrs={"class":"mb-srp__card__ads__info--served"}) != None :
        Served=row.find("div",attrs={"mb-srp__card__ads__info--served"}).text
       # print("Buyers Served : ",Served)
    else:
        Served="Not mentioned"
        #print("Buyers Served : ",Served)
        
#To extract front card values
    for item1 in row.find_all('div', {'class':'mb-srp__card__summary--label'}):
        label1.append(item1.text)
    
    #to remove /n and /t     
    converted_list1 = []
    for element1 in label1:
        converted_list1.append(element1.strip())
        converted_list1
        
    for item2 in row.find_all('div', {'class':'mb-srp__card__summary--value'}):
        label2.append(item2.text)
        
    converted_list2 = []
    for element2 in label2:
        converted_list2.append(element2.strip())
        converted_list2
        
    converted_list=['Carpet Area', 'Super Area','Tenant Preferred','Availability', 'Floor', 
                     'facing', 'Owner Resides','Car Parking']
    aaa=[]
    for i in converted_list:
        if i in converted_list1:
            rank=converted_list1.index(i)
            i1=converted_list2[rank]
            #print(i," : ",i1)

        else:
            i1="No respond"
            #print(i," : ",i1)
        aaa.append(i1)
   
    q1111=aaa[0]
    w1111=aaa[1]
    e1111=aaa[2]
    r1111=aaa[3]
    t1111=aaa[4]
    y1111=aaa[5]
    u1111=aaa[6]
    i1111=aaa[7]
    #print(aaa)
            
    #To extract url and description from metadeta
    meta=row.find_all('meta')
    for m in meta:
        if m['itemprop']=='url':
            url=m['content']
            #print("URL :",url)
        
        if m['itemprop']=='description':
            description=m['content']
            #print("Description :",description)            
            
 
    #drill down to next link  
    URL1=url
    driver.get(URL1)
    source1 = driver.page_source
    soup1 = BeautifulSoup(source1, "html.parser")

    links1 = soup1.find_all("div",attrs={'class':"descriptionCont"})
    #print(links1)

    label11=[]
    label22=[]
    for row in links1:

        for item1 in row.find_all('div', {'class':'p_title'}):
            label11.append(item1.text)

        #to remove /n and /t     
        converted_list11 = []
        for z in label11:
            converted_list11.append(z.strip())

        for item2 in row.find_all('div', {'class':'p_value'}):
            label22.append(item2.text.replace('\n', '').replace('\t', ''))
            
        converted_list22 = []
        for x in label22:
            converted_list22.append(x.strip())

        converted_list111=['Rental Value', 'Booking Amount', 'Facilities', 'Address', 'Landmarks','Status', 
                           'Flooring', 'Brokerage Response', 'Authority Approval', 'Lift', 'Overlooking',
                           'Furnishing Details','Furnishing', 'Other Tenants Preferred','Units Available',
                           'Age of Construction','Type of Ownership','RERA ID','Store Room','Status of Electricity',
                           'Lift','Study Room','Servant Room']
        bbb=[]
        for i in converted_list111:
            if i in converted_list11:
                rank=converted_list11.index(i)
                i11=converted_list22[rank]
                #print(i," : ",i11)

            else:
                i11="No respond"
                #print(i," : ",i11) 
                
            bbb.append(i11)
        
        f1111=bbb[0]
        g1111=bbb[1]
        h1111=bbb[2]
        j1111=bbb[3]
        k1111=bbb[4] 
        l1111=bbb[5]
        z1111=bbb[6]
        x1111=bbb[7]
        c1111=bbb[8]
        v1111=bbb[9]
        b1111=bbb[10]
        n1111=bbb[11]
        m1111=bbb[12]
        qq=bbb[13]
        wwww=bbb[14]
        eeee=bbb[15]
        ffff=bbb[16]
        gggg=bbb[17]
        hhhh=bbb[18]
        iiii=bbb[19]
        jjjj=bbb[20]
        kkkk=bbb[21]
        llll=bbb[22]
        
    
            

      
    label111=[]
    label222=[]
    
    
    links2 = soup1.find_all("div",attrs={'class':"propInfoBlockInn"})
    #print(links2)
    for row in links2:
        for item1 in row.find_all('div', {'class':'p_title'}):
            label111.append(item1.text.replace('\n', '').replace('\t', ''))
            
        #to remove /n and /t     
        converted_list111 = []
        for z in label111:
            converted_list111.append(z.strip())
            
        for item1 in row.find_all('div', {'class':'p_value'}):
            label222.append(item1.text.replace('\n', '').replace('\t', '').strip())
            
        converted_list222 = []
        for x in label222:
            converted_list222.append(x.strip())
            
        converted_list1111=['Bedrooms', 'Bathroom','Bathrooms','Project','Water Availability','Balconies',
                            'Status of Electricity','Units on Floor','Facing','Study Room','Store Room',
                           'Puja Room','Available From','Plot area','Balcony','Servant Room']
        bbbb=[]
        for i in converted_list1111:
            if i in converted_list111:
                rank=converted_list111.index(i)
                i111=converted_list222[rank]
                #print(i," : ",i111)

            else:
                i111="No respond"
                #print(i," : ",i111) 
                
            bbbb.append(i111)
        ff=bbbb[0]
        gg=bbbb[1]
        hhh=bbbb[2]
        jjj=bbbb[3]
        kkk=bbbb[4]
        lll=bbbb[5]
        mmm=bbbb[6]
        nnn=bbbb[7]
        ooo=bbbb[8]
        ppp=bbbb[9]
        qqq=bbbb[10]
        rrr=bbbb[11]
        sss=bbbb[12]
        ttt=bbbb[13]
        uuu=bbbb[14]
        vvv=bbbb[15]
        
    
    links3 = soup1.find_all("div",attrs={'class':"amenities"})
    #print(links3)
    for row in links3:
        Amenities_list=[]
        if links3 != []:
            Amenities=row.find_all("li")
            for i in Amenities:
                Amenities_list.append(i.text)
                #print(Amenities_list)
                
        else:
            Amenities_list.append("Not Responded")
    #print(Amenities_list)
    
    links4 = soup1.find_all("div",attrs={'class':"bg_greyMid"})  
    for row in links4: 
        rate_list1=[]
        rate1=row.find_all("div",attrs={'class':"td"})
        for i in rate1:
            rate_list1.append(i.text.replace('\n', '').replace('\t', '').strip())
            
            
    links5 = soup1.find_all("div",attrs={'class':"applicableCharges"})  
    for row in links5: 
        rate_list2=[]
        if links5 != []:
            rate2=row.find_all("div",attrs={'class':"td"})
            for i in rate2:
                rate_list2.append(i.text.replace('\n', '').replace('\t', '').strip())
                
        else:
            rate_list2.append("Not Responded")        

            
            
    links6 = soup1.find_all("div",attrs={'class':"bdrTop_Btm bg_greyLgt firstMontPay"})  
    for row in links6: 
        rate_list3=[]
        if links6 != []:
            rate3=row.find_all("div",attrs={'class':"td"})
            for i in rate3:
                rate_list3.append(i.text.replace('\n', '').replace('\t', '').strip())
                
        else:
            rate_list3.append("Not Responded")                      
    
   
    news_titles_count+=1
    news_titles[news_titles_count] = [title,society,builder,Since,Served,q1111,w1111,e1111,r1111,t1111,y1111,u1111,i1111,
                                      url,f1111,g1111,h1111,j1111,k1111,l1111,z1111,x1111,c1111,v1111,b1111,n1111,
                                      m1111,qq,wwww,eeee,ffff,gggg,hhhh,iiii,jjjj,kkkk,llll,ff,gg,hhh,jjj,kkk,lll,
                                      mmm,nnn,ooo,ppp,qqq,rrr,sss,ttt,uuu,vvv,Amenities_list,
                                      rate_list1,rate_list2,rate_list3]
                                      
    Amenities_list=[]
    rate_list1=[]
    rate_list2=[]
    rate_list3=[]


# In[ ]:


title_df = pd.DataFrame.from_dict(news_titles,orient='index',columns=['Title','Society','Builder/Agent','Operating Since',
        "Buyers Served",'Carpet Area', 'Super Area','Tenant Preferred','Availability', 'Floor', 
        'facing', 'Owner Resides','Car Parking',"URL",'Rental Value', 'Booking Amount',
        'Facilities', 'Address', 'Landmarks','Status','Flooring', 'Brokerage Response', 'Authority Approval', 'Lift', 
        'Overlooking','Furnishing Details','Furnishing','Other Tenants Preferred','Units Available',
        'Age of Construction','Type of Ownership','RERA ID','Store Room','Status of Electricity',
        'Lift1','Study Room','Servant Room',
        'Bedrooms', 'Bathroom','Bathrooms','Project','Water Availability','Balconies',
        'Status of Electricity1','Units on Floor','Facing','Study Room1','Store Room1',
        'Puja Room','Available From','Plot area','Balcony',"Servant Room1",
        'Amenities',"Rates1","Rates2","Rates3"])



print(len(title_df))
title_df.to_csv("mb_test.csv")


# In[ ]:


import pandas as pd
title_df=pd.read_csv("mb_test.csv")


# In[ ]:


title_df.drop_duplicates(subset ="URL", keep = "first", inplace = True)
#title_df.drop_duplicates()
print(len(title_df))
print('\n')


# In[ ]:


def replace1(i):
    i=i.replace("Builder: ","")
    i=i.replace("Agent: ","")
    return i

title_df["Builder/Agent"]=title_df["Builder/Agent"].apply(replace1)


# In[ ]:


def replace2(i):
    i=i.replace("Operating Since: ","")
    return i

title_df["Operating Since"]=title_df["Operating Since"].apply(replace2)


# In[ ]:


def replace3(i):
    i=i.replace('\n', '').replace('\t', '').replace('  ','').replace('See Other Charges','')
    i=i.replace("₹","   ₹").replace('FREE Rent Agreement', '')
    i=i.replace(",", '').strip()
    return i

title_df["Rental Value"]=title_df["Rental Value"].apply(replace3)

new1=title_df["Rental Value"].str.split(' ', n=1, expand=True)
title_df=title_df.drop(["Rental Value"],axis=1)
title_df["Rental Amount"]=new1[0]
title_df["Rental Amount"]=title_df["Rental Amount"].fillna(0)
title_df["Rental Amount"] = title_df["Rental Amount"].replace(['No'],0)
title_df["Rental Amount"]=title_df["Rental Amount"].astype(str)


# In[ ]:


title_df[['Address','junk']] = title_df['Address'].str.split('Get Lowest price quotes from best Packers and MoversGet Lowest Price Quote',expand=True)
title_df=title_df.drop(["junk"],axis=1)


# In[ ]:


title_df[['Bedrooms','Dimensions']] = title_df['Bedrooms'].str.split('See Dimensions',expand=True)
def replace5(i):
    i=i.strip()
    return i

title_df["Bedrooms"]=title_df["Bedrooms"].apply(replace5)


def replace6(i):
    if i!=None:
        i=i.replace('ft', 'ft ').strip()
        return i
    else:
        i="Not mentioned"
        return i
    
title_df["Dimensions"]=title_df["Dimensions"].apply(replace6)


# In[ ]:


title_df[['Rates1_1','Rates1_2']] = title_df['Rates1'].str.split("₹ ",expand=True)
title_df[['Monthly Rent','Rates1_3']] = title_df['Rates1_2'].str.split("']",expand=True)
title_df['Monthly Rent']="₹"+title_df['Monthly Rent']
title_df=title_df.drop(["Rates1_1"],axis=1)
title_df=title_df.drop(["Rates1_3"],axis=1)
title_df=title_df.drop(["Rates1_2"],axis=1)
title_df=title_df.drop(["Rates1"],axis=1)
title_df["Monthly Rent"]=title_df["Monthly Rent"].astype(str)


# In[ ]:


def replace3(i):
    i=i.replace(",", '').strip()
    return i

title_df["Monthly Rent"]=title_df["Monthly Rent"].apply(replace3)
title_df["Monthly Rent"]=title_df["Monthly Rent"].fillna("₹0")
title_df["Monthly Rent"] = title_df["Monthly Rent"].replace(['nan'],"₹0")
title_df["Monthly Rent"]=title_df["Monthly Rent"].astype(str)


# In[ ]:


def replace10(i):
    i=i.replace("₹", '').strip()
    return i

title_df["ra"]=title_df["Rental Amount"].apply(replace10)
title_df["mr"]=title_df["Monthly Rent"].apply(replace10)


# In[ ]:


title_df["ra"]=title_df["ra"].astype(int)
title_df["mr"]=title_df["mr"].astype(int)


# In[ ]:


import numpy as np
conditions = [(title_df['ra'] == title_df['mr']),(title_df['ra'] < title_df['mr'])]
values = [0,(title_df["mr"]-title_df['ra'])]
title_df["Monthly Maintenance"] = np.select(conditions, values).astype(str)
title_df['Monthly Maintenance']="₹"+title_df['Monthly Maintenance']


# In[ ]:


title_df=title_df.drop(["ra"],axis=1)
title_df=title_df.drop(["mr"],axis=1)


# In[ ]:


def replace7(i):
    i=i.replace('\n', '').replace('\t', '').replace("Security Deposit",'').replace("Brokerage",'').replace(",",'')
    i=i.replace("₹ ","₹").replace("'",'').replace("[",'').replace("]",'').replace("   ",' ')
    #i=i.replace(",", '').strip()
    return i

title_df["Rates2"]=title_df["Rates2"].apply(replace7)

new2=title_df["Rates2"].str.split('  ', n=1, expand=True)
title_df=title_df.drop(["Rates2"],axis=1)
title_df["Security Deposit"]=new2[0]
title_df["Brokerage"]=new2[1] 


# In[ ]:


title_df[['Rates3_1','Rates3_2']] = title_df['Rates3'].str.split("₹ ",expand=True)
title_df[['First Month Payment','Rates3_3']] = title_df['Rates3_2'].str.split("']",expand=True)
title_df['First Month Payment']="₹"+title_df['First Month Payment']
title_df=title_df.drop(["Rates3_1"],axis=1)
title_df=title_df.drop(["Rates3_3"],axis=1)
title_df=title_df.drop(["Rates3_2"],axis=1)
title_df=title_df.drop(["Rates3"],axis=1)


# In[ ]:


new3=title_df["Plot area"].str.split(' ', n=1, expand=True)
title_df["Plot Area"]=new3[0]
title_df=title_df.drop(["Plot area"],axis=1)


# In[ ]:


title_df["facing"]=np.where(title_df['facing']=='No respond',title_df["Facing"],np.where(title_df['Facing']=='No respond',title_df["facing"],title_df["facing"]))
title_df["Status of Electricity"]=np.where(title_df['Status of Electricity']=='No respond',title_df["Status of Electricity1"],np.where(title_df['Status of Electricity1']=='No respond',title_df["Status of Electricity"],title_df["Status of Electricity"]))
title_df["Store Room"]=np.where(title_df['Store Room']=='No respond',title_df["Store Room1"],np.where(title_df['Store Room1']=='No respond',title_df["Store Room"],title_df["Store Room"]))
title_df["Lift"]=np.where(title_df['Lift']=='No respond',title_df["Lift1"],np.where(title_df['Lift1']=='No respond',title_df["Lift"],title_df["Lift"]))
title_df["Study Room"]=np.where(title_df['Study Room']=='No respond',title_df["Study Room1"],np.where(title_df['Study Room1']=='No respond',title_df["Study Room"],title_df["Study Room"]))
title_df["Servant Room"]=np.where(title_df['Servant Room']=='No respond',title_df["Servant Room1"],np.where(title_df['Servant Room1']=='No respond',title_df["Servant Room"],title_df["Servant Room"]))
title_df["Balconies"]=np.where(title_df['Balconies']=='No respond',title_df["Balcony"],np.where(title_df['Balcony']=='No respond',title_df["Balconies"],title_df["Balconies"]))
title_df["Bathrooms"]=np.where(title_df['Bathrooms']=='No respond',title_df["Bathroom"],np.where(title_df['Bathroom']=='No respond',title_df["Bathrooms"],title_df["Bathrooms"]))


# In[ ]:


title_df=title_df.drop(["Facing","Status of Electricity1","Store Room1",'Lift1',"Study Room1","Servant Room1","Balcony","Bathroom"],axis=1)


# In[ ]:


def replace8(i):
    i=i.replace('\n', '').replace('\t', '').replace("1",',1').replace("2",',2').replace("3",',3').replace("4",',4').replace("5",',5')
    i=i.replace("View all Furnishing Details","")
    i=i.replace(" ", '')
    i=i.replace("GasConnection", ',Gas Connection').replace("DiningTable",",Dining Table").replace("Fridge",",Fridge")
    i=i.replace("Sofa",",Sofa").replace("WashingMachine",",Washing Machine").replace("Microwave",",Microwave")
    i=i.replace("1",'1 ').replace("2",'2 ').replace("3",'3 ').replace("4",'4 ').replace("5",'5 ')
    return i

title_df["Furnishing Details"]=title_df["Furnishing Details"].apply(replace8)

new4=title_df["Furnishing Details"].str.split(',', n=1, expand=True)
title_df["Furnishing details"]=new4[1]
title_df=title_df.drop(["Furnishing Details"],axis=1)


# In[ ]:


title_df["Locality"]="Dwarka Expressway, Gurgaon"
title_df["Locality Link"]="https://www.magicbricks.com/Dwarka-Expressway-in-Gurgaon-Overview"
title_df["Category"]="Rent"


# In[ ]:


title_df["Security Deposit"]=title_df["Security Deposit"].replace(np.nan,"₹0")


# In[ ]:


title_df= title_df.replace(np.nan,"No response")


# In[ ]:


title_df=title_df.reindex(columns=['Locality','Locality Link','Category','Title','Society','Builder/Agent',
                                   'Operating Since','Buyers Served','Furnishing','Tenant Preferred','Other Tenants Preferred',
                                   'Car Parking','Availability','Carpet Area','Super Area','Floor','URL','Bedrooms',
                                   'Dimensions','Bathrooms','Balconies','Study Room','Servant Room','Store Room',
                                   'Puja Room','Project','Plot Area','Available From','Water Availability','Units on Floor',
                                   'facing','Rental Amount',"Monthly Rent",'Monthly Maintenance','Security Deposit',
                                   'Brokerage','First Month Payment','Booking Amount','Facilities','Address','Status',
                                   'RERA ID','Overlooking','Flooring','Status of Electricity','Lift','Age of Construction',
                                   'Units Available','Brokerage Response','Furnishing details','Authority Approval',
                                   'Type of Ownership','Owner Resides','Amenities'])


# In[ ]:


title_df.to_csv("magicbricks.rent.csv",encoding='utf-8-sig')

