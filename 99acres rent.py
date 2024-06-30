#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


driver = webdriver.Chrome("C:\\Users\\Lenovo\\chromedriver_win32\\chromedriver.exe")

ll=[]
for i in range(1,1481):
    link='https://www.99acres.com/search/property/rent/gurgaon?city=8&preference=R&area_unit=1&budget_min=0&res_com=R&page='+str(i)
    ll.append(link)


# In[ ]:


df = pd.DataFrame()
for link in ll:  
    URL = link
    driver.get(URL)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    news_titles = {}
    news_titles_count = 0
    links = soup.find_all("div",attrs={'class':"srpTuple__cardWrap"})
    tag_dup = []
    page_break = -10

    while len(tag_dup)<=50 and len(tag_dup)>=page_break:
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        news_titles = {}
        news_titles_count = 0
        links = soup.find_all("div",attrs={'class':"srpTuple__cardWrap"})

        try:
            new_tags = set(links).difference(tag_dup)
        except:
            new_tags = links

        tag_dup = []

        for tag_du in links:
            tag_dup.append(tag_du)

        page_break+=1

        for row in new_tags:
            label=[]
            details=[]

            title=row.find("h2").text
        

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        next_page = driver.find_elements(By.CLASS_NAME,'autoload_continue')
        time.sleep(2)
        for elem in next_page:
            elem.click()  

        for row in tag_dup:
            
            #title
            title=row.find("h2").text
    


            #To extract url
            url=row.find("td",attrs={'class':"srpTuple__tdClassPremium"})
            url=url.find('a').get('href')
            url= 'https://www.99acres.com'+url
            #print(url)
         
    
            URL1=url
            driver.get(URL1)
            source1 = driver.page_source
            soup1 = BeautifulSoup(source1, "html.parser")
            
            
            #price
            if soup1.find('span',attrs={'class':"component__pdPropValue"}) != None:
                price =  soup1.find('span',attrs={'class':"component__pdPropValue"}).text
            elif soup1.find('div',attrs={'class':"factTableComponent__npPrice"}) != None:
                price = soup1.find('div',attrs={'class':"factTableComponent__npPrice"}).text 
            else:
                price="NA"
        
            price=price.replace('\n', '').replace('\t', '')
            price=price.strip()
          
    
            #per sq ft price
            if soup1.find('div',attrs={'class':"component__pdPropArea pd__pdPropArea"}) != None:
                price1 =  soup1.find('div',attrs={'class':"component__pdPropArea pd__pdPropArea"}).text
            elif soup1.find('div',attrs={'class':"factTableComponent__npBasePrice pd__pdPropEmi"}) != None:
                price1 = soup1.find('div',attrs={'class':"factTableComponent__npBasePrice pd__pdPropEmi"}).text
            else:
                price1="NA"
        
            price1=price1.replace('\n', '').replace('\t', '').replace('@','')
            price1=price1.strip() 

    
            #emi
            if soup1.find('a',attrs={'class':"component__pdPropEmi pd__pdPropEmi"}) != None:
                emi =  soup1.find('a',attrs={'class':"component__pdPropEmi pd__pdPropEmi"}).text
            else:
                emi = "NA"  
        
            emi=emi.replace('\n', '').replace('\t', '')
            emi = emi.strip()

   

            #extract information from within link
            links1 = soup1.find_all("table",attrs={'class':"component__factTable generic__listNone"})

            label11=[]
            label22=[]
            for row in links1:
    
                for item1 in row.find_all('div', {'class':'component__tableHead'}):
                    label11.append(item1.text)

            
                converted_list11 = []
                for z in label11:
                    converted_list11.append(z.strip())

                for item2 in row.find_all('div', {'class':'component__details'}):
                    label22.append(item2.text.replace('\n', '').replace('\t', ''))
            
                converted_list22 = []
                for x in label22:
                    converted_list22.append(x.strip())

                converted_list111=['Price','Possession','Facing','Floors Allowed For Construction',
                          'Overlooking','Configuration','Floor Number','Property Age','Possession in','Address']
                          
                bbb=[]
                for i in converted_list111:
                    if i in converted_list11:
                        rank=converted_list11.index(i)
                        i11=converted_list22[rank]
                

                    else:
                        i11="NA"
                
                
                    bbb.append(i11)
        
                c1=bbb[0]
                d1=bbb[1]
                e1=bbb[2]
                f1=bbb[3]
                g1=bbb[4]
                h1=bbb[5]
                i1=bbb[6]
                j1=bbb[7]
                k1=bbb[8]
                l1=bbb[9]
 
                
            
            
            #carpet_area
            if soup1.find('span',attrs={'id':"carpetArea_span"}) != None:
                carpet_area1 =  soup1.find('span',attrs={'id':"carpetArea_span"}).text
                dim1 = soup1.find('a',attrs={'class':"component__unitDropdown component__unit [object Object]"}).text
                if soup1.find('span',attrs={'id':"builtupAreaLabel"})!= None:
                    dim11 = soup1.find('span',attrs={'id':"builtupAreaLabel"}).text
                else:
                    dim11=''
                carpet_area=carpet_area1+dim11+dim1
            else:
                carpet_area="NA"
        
            carpet_area=carpet_area.replace('\n', '').replace('\t', '')
            carpet_area=carpet_area.strip()

            
            
            #plot_area
            if soup1.find('span',attrs={'id':"superArea_span"}) != None:
                plot_area1 =  soup1.find('span',attrs={'id':"superArea_span"}).text
                dim2 = soup1.find('a',attrs={'class':"component__unitDropdown component__unit [object Object]"}).text
                if soup1.find('span',attrs={'id':"builtupAreaLabel"})!= None:
                    dim22 = soup1.find('span',attrs={'id':"builtupAreaLabel"}).text
                else:
                    dim22=''
                plot_area=plot_area1+dim22+dim2
                
            else:
                plot_area="NA"
        
            plot_area=plot_area.replace('\n', '').replace('\t', '')
            plot_area=plot_area.strip()


            
            #super_area
            if soup1.find('span',attrs={'id':"superbuiltupArea_span"}) != None:
                super_area1 =  soup1.find('span',attrs={'id':"superbuiltupArea_span"}).text
                dim3 = soup1.find('a',attrs={'class':"component__unitDropdown component__unit [object Object]"}).text
                if soup1.find('span',attrs={'id':"builtupAreaLabel"})!= None:
                    dim33 = soup1.find('span',attrs={'id':"builtupAreaLabel"}).text
                else:
                    dim33=''
                super_area=super_area1+dim33+dim3
            else:
                super_area="NA"
        
            super_area=super_area.replace('\n', '').replace('\t', '')
            super_area=super_area.strip()

            
            
            #built_area
            if soup1.find('span',attrs={'id':"builtupArea_span"}) != None:
                built_area1 =  soup1.find('span',attrs={'id':"builtupArea_span"}).text
                dim4 = soup1.find('a',attrs={'class':"component__unitDropdown component__unit [object Object]"}).text
                if soup1.find('span',attrs={'id':"builtupAreaLabel"})!= None:
                    dim44 = soup1.find('span',attrs={'id':"builtupAreaLabel"}).text
                else:
                    dim44=''
                built_area=built_area1+dim44+dim4
            else:
                built_area="NA"
        
            built_area=built_area.replace('\n', '').replace('\t', '')
            built_area=built_area.strip()

            
            
            #completed_in
            if soup1.find('div',attrs={'class':"factTableComponent__npPossessionDate pd__pdPropEmi"}) != None:
                completed_in =  soup1.find('div',attrs={'class':"factTableComponent__npPossessionDate pd__pdPropEmi"}).text
            else:
                completed_in="NA"
        
            completed_in=completed_in.replace('\n', '').replace('\t', '')
            completed_in=completed_in.strip()  
            
            #brokerage
            if soup1.find('span',attrs={'class':"component__noBrokerage"}) != None:
                brokerage =  soup1.find('span',attrs={'class':"component__noBrokerage"}).text
            else:
                brokerage="NA"
        
            brokerage=brokerage.replace('\n', '').replace('\t', '')
            brokerage=brokerage.strip()              
            
    
            #RERA_status
            if soup1.find('span',attrs={'class':"component__status"}) != None:
                RERA_status =  soup1.find('span',attrs={'class':"component__status"}).text
            else:
                RERA_status = "NA"  
        
            RERA_status = RERA_status.replace('\n', '').replace('\t', '')
            RERA_status = RERA_status.strip() 

            
            #registration_no
            if soup1.find('div',attrs={'class':"component__reraWrap"}) != None:
                registration_no = soup1.find('div',attrs={'class':"component__reraWrap"}).text
            else:
                registration_no = "NA"  
        
            registration_no = registration_no.replace('\n', '').replace('\t', '')
            registration_no = registration_no.strip() 
 

            #posted_on
            if soup1.find('i',attrs={'id':"pdPropDate"}) != None:
                posted_on =  soup1.find('i',attrs={'id':"pdPropDate"}).text
            elif soup1.find('div',attrs={'class':"component__postedBy component__postedBy2"}) != None:
                posted_on =  soup1.find('div',attrs={'class':"component__postedBy component__postedBy2"}).text
            elif soup1.find('span',attrs={'class':"factTableComponent__pdPropDate"}) != None:
                posted_on = soup1.find('span',attrs={'class':"factTableComponent__pdPropDate"}).text
            else:
                posted_on = "NA"  
        
            posted_on = posted_on.replace('\n', '').replace('\t', '')
            posted_on = posted_on.strip()

    
    
    
            #Availability
            if soup1.find('span',attrs={'id':"Availability_Lbl"}) != None:
                Availability =  soup1.find('span',attrs={'id':"Availability_Lbl"}).text
            elif soup1.find('div',attrs={'class':"factTableComponent__npPossession"}) != None:
                Availability =  soup1.find('div',attrs={'class':"factTableComponent__npPossession"}).text
            else:
                Availability = "NA"  

            Availability = Availability.replace('\n', '').replace('\t', '')
            Availability = Availability.strip()
   
    
           #Transaction_Type
            if soup1.find('span',attrs={'id':"Transact_Type_Label"}) != None:
                Transaction_Type =  soup1.find('span',attrs={'id':"Transact_Type_Label"}).text
            else:
                 Transaction_Type = "NA"  

            Transaction_Type = Transaction_Type.replace('\n', '').replace('\t', '')
            Transaction_Type = Transaction_Type.strip()


            #Property_Ownership
            if soup1.find('span',attrs={'id':"Owntype_Label"}) != None:
                 Property_Ownership =  soup1.find('span',attrs={'id':"Owntype_Label"}).text
            else:
                Property_Ownership = "NA"  

            Property_Ownership = Property_Ownership.replace('\n', '').replace('\t', '')
            Property_Ownership = Property_Ownership.strip()


            #Width_Of_Facing_Road
            if soup1.find('span',attrs={'id':"Width_Of_Facing_Road"}) != None:
                Width_Of_Facing_Road =  soup1.find('span',attrs={'id':"Width_Of_Facing_Road"}).text
            else:
                Width_Of_Facing_Road = "NA"  

            Width_Of_Facing_Road = Width_Of_Facing_Road.replace('\n', '').replace('\t', '')
            Width_Of_Facing_Road = Width_Of_Facing_Road.strip()
     
            
            #Gated_community
            if soup1.find('span',attrs={'id':"Gated_community"}) != None:
                Gated_community =  soup1.find('span',attrs={'id':"Gated_community"}).text
            else:
                Gated_community = "NA"  

            Gated_community = Gated_community.replace('\n', '').replace('\t', '')
            Gated_community = Gated_community.strip()
 
    
           #Boundary_Wall
            if soup1.find('span',attrs={'id':"Is_Boundary_Wall_Made_Label"}) != None:
                Boundary_Wall =  soup1.find('span',attrs={'id':"Is_Boundary_Wall_Made_Label"}).text
            else:
                Boundary_Wall = "NA"  

            Boundary_Wall = Boundary_Wall.replace('\n', '').replace('\t', '')
            Boundary_Wall = Boundary_Wall.strip()
    
 
            #Prop_Id
            if soup1.find('span',attrs={'id':"Prop_Id"}) != None:
                Prop_Id =  soup1.find('span',attrs={'id':"Prop_Id"}).text
            else:
                Prop_Id = "NA"  

            Prop_Id = Prop_Id.replace('\n', '').replace('\t', '')
            Prop_Id = Prop_Id.strip()
  
    
    
            #Parking
            if soup1.find('span',attrs={'id':"Reserved_Parking_Label"}) != None:
                Parking =  soup1.find('span',attrs={'id':"Reserved_Parking_Label"}).text
            else:
                 Parking = "NA"  

            Parking = Parking.replace('\n', '').replace('\t', '')
            Parking = Parking.strip()

    
    
    
            #Power_Backup
            if soup1.find('span',attrs={'id':"Powerbackup_Label"}) != None:
                Power_Backup =  soup1.find('span',attrs={'id':"Powerbackup_Label"}).text
            else:
                Power_Backup = "NA"  

            Power_Backup = Power_Backup.replace('\n', '').replace('\t', '')
            Power_Backup = Power_Backup.strip() 
    
    
    
            #Flooring
            if soup1.find('span',attrs={'id':"Flooring_Label"}) != None:
                Flooring =  soup1.find('span',attrs={'id':"Flooring_Label"}).text
            else:
                Flooring = "NA"  

            Flooring = Flooring.replace('\n', '').replace('\t', '')
            Flooring = Flooring.strip()
    
    
    
            #Furnishing
            if soup1.find('span',attrs={'id':"Furnish_Label"}) != None:
                Furnishing =  soup1.find('span',attrs={'id':"Furnish_Label"}).text
            else:
                Furnishing = "NA"  

            Furnishing = Furnishing.replace('\n', '').replace('\t', '')
            Furnishing = Furnishing.strip()

   
    
            #Corner_Property
            if soup1.find('span',attrs={'id':"Corner_Property"}) != None:
                Corner_Property =  soup1.find('span',attrs={'id':"Corner_Property"}).text
            else:
                Corner_Property = "NA"  

            Corner_Property = Corner_Property.replace('\n', '').replace('\t', '')
            Corner_Property = Corner_Property.strip()
 
   
    
            #WheelChairFriendly
            if soup1.find('span',attrs={'id':"WheelChairFriendly"}) != None:
                WheelChairFriendly =  soup1.find('span',attrs={'id':"WheelChairFriendly"}).text
            else:
                WheelChairFriendly = "NA"  

            WheelChairFriendly = WheelChairFriendly.replace('\n', '').replace('\t', '')
            WheelChairFriendly = WheelChairFriendly.strip()

    
    
            #PetFriendly
            if soup1.find('span',attrs={'id':"PetFriendly"}) != None:
                PetFriendly =  soup1.find('span',attrs={'id':"PetFriendly"}).text
            else:
                    PetFriendly = "NA"  

            PetFriendly = PetFriendly.replace('\n', '').replace('\t', '')
            PetFriendly = PetFriendly.strip()

    
    
            #Watersource
            if soup1.find('span',attrs={'id':"Watersource_Label"}) != None:
                Watersource =  soup1.find('span',attrs={'id':"Watersource_Label"}).text
            else:
                Watersource = "NA"  

            Watersource = Watersource.replace('\n', '').replace('\t', '')
            Watersource = Watersource.strip()

    
    
            #Address
            if soup1.find('i',attrs={'id':"address"}) != None:
                Address =  soup1.find('i',attrs={'id':"address"}).text
            elif soup1.find('div',attrs={'class':"aboutProperty__pdDescAdd"}) != None:
                Address =  soup1.find('div',attrs={'class':"aboutProperty__pdDescAdd"}).text
            else:
                Address = "NA"  

            Address = Address.replace('\n', '').replace('\t', '')
            Address = Address.strip()

    
    
            #features
            links2 = soup1.find_all("div",attrs={'class':'component__features pd__pdBlock'})
            for row1 in links2:
                features_list=[]
                if links2 != []:
                    features=row1.find_all("li")
                    for i in features:
                        features_list.append(i.text.replace('\n', '').replace('\t', '').strip())

                else:
                    features_list.append("NA")

                    
                    
            #furnishing_details
            links3 = soup1.find_all("div",attrs={'id':"FurnishDetails"})

            for row2 in links3:
                furnishing_details_list=[]
                if links3 != []:
                    furnishing_details=row2.find_all("li")
                    for i in furnishing_details:
                        furnishing_details_list.append(i.text.replace('\n', '').replace('\t', '').strip())

                else:
                    furnishing_details_list.append("NA")

   

            #company
            if soup1.find('div',attrs={'class':"badges_regular_secondary Ng400 spacer4 fdDetail__capitalize"}) != None:
                company =  soup1.find('div',attrs={'class':"badges_regular_secondary Ng400 spacer4 fdDetail__capitalize"}).text
            elif soup1.find('div',attrs={'class':"component__company"}) != None:
                company =  soup1.find('div',attrs={'class':"component__company"}).text
            else:
                company = "NA"  

            company = company.replace('\n', '').replace('\t', '')
            company = company.strip()   
    

    
    
            #dealer name
            if soup1.find('div',attrs={'class':"list_header_semiBold Ng800"}) != None:
                    name =  soup1.find('div',attrs={'class':"list_header_semiBold Ng800"}).text
            elif soup1.find('div',attrs={'class':"component__primaryInfo"}) != None:
                name= soup1.find('div',attrs={'class':"component__primaryInfo"}).text
            else:
                name = "NA"  

            name = name.replace('\n', '').replace('\t', '')
            name = name.strip()

            if soup1.find('div',attrs={'id':"BuilderDetails"}) != None:
                dealer_info1 =  soup1.find('div',attrs={'id':"BuilderDetails"})
            else:
                dealer_info1 = "NA"  
         

    
            #dealer info
            if soup1.find('div',attrs={'class':"FeatureDealerCard__addInfo"}) != None:
                dealer_info =  soup1.find('div',attrs={'class':"FeatureDealerCard__addInfo"}).text
            else:
                dealer_info = "NA"  

            dealer_info = dealer_info.replace('\n', '').replace('\t', '')
            dealer_info = dealer_info.strip()

     

 

             #dealer address
            if soup1.find('div',attrs={'class':"component__dealerCard"}) != None:
                dealer_address  =  soup1.find('div',attrs={'class':"component__dealerCard"}).text
            else:
                dealer_address  = "NA"  

            dealer_address  = dealer_address.replace('\n', '').replace('\t', '')
            dealer_address  = dealer_address.strip()

    
    

            #member_since
            if soup1.find('div',attrs={'class':"caption_subdued_medium"}) != None:
                member_since =  soup1.find('div',attrs={'class':"caption_subdued_medium"}).text
            else:
                member_since = "NA"  

            member_since = member_since.replace('\n', '').replace('\t', '')
            member_since = member_since.strip()

    
    
    
            #properties_listed
            if soup1.find('div',attrs={'class':"component__listed"}) != None:
                properties_listed =  soup1.find('div',attrs={'class':"component__listed"}).text
            else:
                properties_listed = "NA"  

            properties_listed = properties_listed.replace('\n', '').replace('\t', '')
            properties_listed = properties_listed.strip()

    
    
            #verified_properties
            if soup1.find('div',attrs={'class':"component__verifed"}) != None:
                verified_properties =  soup1.find('div',attrs={'class':"component__verifed"}).text
            else:
                verified_properties = "NA"  

            verified_properties = verified_properties.replace('\n', '').replace('\t', '')
            verified_properties = verified_properties.strip()
 
    
    
            #dealer_rera
            if soup1.find('div',attrs={'class':"component__rera"}) != None:
                dealer_rera =  soup1.find('div',attrs={'class':"component__rera"}).text
            else:
                dealer_rera = "NA"  

            dealer_rera = dealer_rera.replace('\n', '').replace('\t', '')
            dealer_rera = dealer_rera.strip()


            
            #rooms
            if soup1.find('div',attrs={'class':"floorplan__floorContentContainer floorplan__inclusions floorplan__floorPlanInclusionContent"}) != None:
                rooms =  soup1.find('div',attrs={'class':"floorplan__floorContentContainer floorplan__inclusions floorplan__floorPlanInclusionContent"}).text
            else:
                rooms = "NA"  

            rooms = rooms.replace('\n', '').replace('\t', '')
            rooms = rooms.strip()


            #society_name
            if soup1.find('div',attrs={'id':"societyWrp"}) != None:
                society_name =  soup1.find('div',attrs={'id':"societyWrp"}).text
            else:
                society_name = "NA"  

            society_name = society_name.replace('\n', '').replace('\t', '')
            society_name = society_name.strip() 
            
            
            #project_area
            if soup1.find('div',attrs={'class':"component__npPrjArea"}) != None:
                project_area =  soup1.find('div',attrs={'class':"component__npPrjArea"}).text
            else:
                project_area = "NA"  

            project_area = project_area.replace('\n', '').replace('\t', '')
            project_area = project_area.strip()
            
            
            #project_floors
            if soup1.find('span',attrs={'id':"floorCountSociety"}) != None:
                project_floors =  soup1.find('span',attrs={'id':"floorCountSociety"}).text
            else:
                project_floors = "NA"  

            project_floors = project_floors.replace('\n', '').replace('\t', '')
            project_floors = project_floors.strip() 
            
            
            #project_towers
            if soup1.find('span',attrs={'id':"floorToweCountSociety"}) != None:
                project_towers =  soup1.find('span',attrs={'id':"floorToweCountSociety"}).text
            else:
                project_towers = "NA"  

            project_towers = project_towers.replace('\n', '').replace('\t', '')
            project_towers = project_towers.strip()
    
    
            #properties_sale
            if soup1.find('div',attrs={'class':"component__socUnit4Sale"}) != None:
                properties_sale =  soup1.find('div',attrs={'class':"component__socUnit4Sale"}).text
            else:
                properties_sale = "NA"  

            properties_sale = properties_sale.replace('\n', '').replace('\t', '')
            properties_sale = properties_sale.strip()

            
            
            #properties_rent
            if soup1.find('div',attrs={'class':"component__socUnit4Rent"}) != None:
                properties_rent =  soup1.find('div',attrs={'class':"component__socUnit4Rent"}).text
            else:
                properties_rent = "NA"  

            properties_rent = properties_rent.replace('\n', '').replace('\t', '')
            properties_rent = properties_rent.strip()

           
        
            #project_details
            if soup1.find('div',attrs={'class':"pd__pdBlock component__societyWidget undefined"}) != None:
                project_details =  soup1.find('div',attrs={'class':"pd__pdBlock component__societyWidget undefined"}).text
            else:
                project_details = "NA"  

            project_details = project_details.replace('\n', '').replace('\t', '')
            project_details = project_details.strip()  
            
            
            
            #amenities
            if soup1.find('div',attrs={'id':"amenitiesWrp"}) != None:
                amenities1 =  soup1.find('div',attrs={'id':"amenitiesWrp"})  
                for row4 in amenities1:
                    amenities=[]
                    amenities11 =  row4.find_all('div',attrs={'class':"undefined"})
                    for i in amenities11:
                        amenities.append(i.text.replace('\n', '').replace('\t', '').strip())

            else:
                amenities = "NA"     
            
        
            #features
            if soup1.find('div',attrs={'id':"lifeStyleWrp"}) != None:
                features1 =  soup1.find('div',attrs={'id':"lifeStyleWrp"})
                for row5 in features1:
                    features11=[] 
                    features111 = row5.find_all('li',attrs={'class':"undefined"})
                    for i in features111:
                        features11.append(i.text.replace('\n', '').replace('\t', '').strip())
            else:
                features11 = "NA" 

                
            #area
            if soup1.find('div',attrs={'class':"factTableComponent__npAreaBlock2"}) != None:
                area1 = soup1.find('div',attrs={'class':"factTableComponent__npAreaBlock2"}).text
                
                area1 = area1.replace('\n', '').replace('\t', '')
                area1 = area1.strip()  
                        
            else:
                area1 = "NA"
            
                
  
            
            news_titles_count+=1
            news_titles[news_titles_count]=[title,url,price,price1,emi,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,carpet_area,
                    plot_area,super_area,built_area,
                    completed_in,brokerage,RERA_status,registration_no,posted_on,Availability,Transaction_Type,Property_Ownership,
                    Width_Of_Facing_Road,Gated_community,Boundary_Wall,Prop_Id,Parking,Power_Backup,Flooring,
                    Furnishing,Corner_Property,WheelChairFriendly,PetFriendly,Watersource,Address,features_list,
                    furnishing_details_list,company,name,dealer_info,
                    dealer_address,member_since,properties_listed,verified_properties,
    dealer_rera,rooms,society_name,project_area,project_floors,project_towers,properties_sale,properties_rent,
            project_details,amenities,features11,area1]



            features_list=[]
            furnishing_details_list=[]
            name_list=[]
            dealer_address=[]
            c1=[]
            d1=[]
            e1=[]
            f1=[]
            g1=[]
            h1=[]
            i1=[]
            j1=[]
            k1=[]
            l1=[]
            m1=[]
            amenities=[]
            features11=[]

    
            
            
            
            title_df = pd.DataFrame.from_dict(news_titles,orient='index',columns=['Title','URL','Price',
                'per sq price','Estimated EMI','Price1','Possession','Facing',
        'Floors Allowed For Construction','Overlooking','Configuration','Floor Number','Property Age','Possession in','Address',
    'Carpet Area','Plot Area','Super Built up area','Built Up area',
    'Completed in','Brokerage Status','RERA Status','Registration No.','Posted Date','Availability','Transaction Type',
    'Property Ownership','Width of facing road','Gated Community','Boundary Wall','Property Code','Parking',
    'Power Backup','Flooring','Furnishing','Corner Property','Wheel Chair Friendly','Pet Friendly',
    'Water Source','Address','Features','Furnishing Details','Builder/Dealer Company','Builder/Dealer Name',
    'Dealer Info','Dealer Address1','Member Since','Properties Listed',
'Verified Properties',"Dealer RERA no.",'Rooms','Society Name',
    'Project Area','Number of Project Floors','Project Towers','Society Properties Resale','Society Properties Rent',
    'Project Details','Amenities',"Features1",'Area1'])



               
            df=pd.concat([df,title_df])


# In[ ]:


len(df)


# In[ ]:


df.drop_duplicates(subset ="URL", keep = "first", inplace = True)
df= df.replace(np.nan,"NA")


# In[ ]:


df.to_csv("raw_data.csv",encoding='utf-8-sig')


# In[ ]:





# In[ ]:


import pandas as pd
import numpy as np
df=pd.read_csv("raw_data.csv")


# In[ ]:


df["Estimated EMI"]=df["Estimated EMI"].astype(str)
def replace1(i):
    i=i.replace("Estimated EMI ","")
    return i

df["Estimated EMI"]=df["Estimated EMI"].apply(replace1)


# In[ ]:


df["per sq price"]=df["per sq price"].astype(str)
def replace2(i):
    i=i.replace("Base Price:","")
    return i

df["per sq price"]=df["per sq price"].apply(replace2)


# In[ ]:


new1=df["Price1"].str.split('Maintenance', n=1, expand=True)
df["junk6"]=new1[0]
df["junk1"]=new1[1]

new2=df["junk1"].str.split('Expected Rental', n=1, expand=True)
df["junk2"]=new2[0]
df["junk4"]=new2[1]

new3=df["junk2"].str.split('Booking Amount', n=1, expand=True)
df["Maintenance"]=new3[0]
df["junk3"]=new3[1]

new4=df["junk3"].str.split('Brokerage', n=1, expand=True)
df["Booking Amount"]=new4[0]
df["Brokerage"]=new4[1]

new5=df["junk4"].str.split('Booking Amount', n=1, expand=True)
df["Expected Rental"]=new5[0]
df["junk5"]=new5[1]

new6=df["junk5"].str.split('Brokerage', n=1, expand=True)
df["Booking Amount1"]=new6[0]
df["Brokerage1"]=new6[1]

new7=df["junk6"].str.split('Brokerage', n=1, expand=True)
df["Brokerage2"]=new7[1]


df=df.drop(["Price1",'junk1','junk2','junk3','junk4','junk5','junk6'],axis=1)
df= df.replace(np.nan,"NA")


# In[ ]:


df["Booking Amount"]=np.where(df['Booking Amount']=='NA',df["Booking Amount1"],np.where(df['Booking Amount1']=='NA',df["Booking Amount"],df["Booking Amount"]))
df["Brokerage"]=np.where(df['Brokerage']=='NA',df["Brokerage1"],np.where(df['Brokerage1']=='NA',df["Brokerage"],df["Brokerage"]))
df["Brokerage"]=np.where(df['Brokerage']=='NA',df["Brokerage2"],np.where(df['Brokerage2']=='NA',df["Brokerage"],df["Brokerage"]))
df["Brokerage"]=np.where(df['Brokerage']=='NA',df["Brokerage Status"],np.where(df['Brokerage Status']=='NA',df["Brokerage"],df["Brokerage"]))


# In[ ]:


df=df.drop(['Booking Amount1','Brokerage1','Brokerage2','Brokerage Status'],axis=1)


# In[ ]:


new8=df["Registration No."].str.split('Registration No: ', n=1, expand=True)
df["junk7"]=new8[1]

new9=df["junk7"].str.split('Website', n=1, expand=True)
df["Registration No."]=new9[0]

df=df.drop(['junk7'],axis=1)
df= df.replace(np.nan,"NA")


# In[ ]:


df["Address"]=df["Address"].astype(str)
def replace44(i):
    i=i.replace('[]', 'NA')
    return i

df["Address"]=df["Address"].astype(str)
df["Address"]=np.where(df['Address']=='NA',df["Address1"],np.where(df['Address1']=='NA',df["Address"],df["Address"]))
df=df.drop(['Address1'],axis=1)


# In[ ]:


df["Property Age"]=df["Property Age"].astype(str)
def replace11(i):
    i=i.replace("    View Construction Status","")
    return i

df["Property Age"]=df["Property Age"].apply(replace11)


# In[ ]:


df["Area1"]=df["Area1"].astype(str)


# In[ ]:


def carpet(i):
    word = 'carpet'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["Carpet Area11"]=df["Area1"].apply(carpet)


# In[ ]:


def plot(i):
    word = 'plot'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["Plot Area11"]=df["Area1"].apply(plot)


# In[ ]:


def super2(i):
    i=i.replace('Super Built Up AreaView Floor Plans', 'superarea')
    return i

df["Area1"]=df["Area1"].apply(super2)
df["Area1"]=df["Area1"].astype(str)


# In[ ]:


def super1(i):
    word = 'superarea'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["Super Area11"]=df["Area1"].apply(super1)


# In[ ]:


def built(i):
    word = 'builtup'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["Built Area11"]=df["Area1"].apply(built)


# In[ ]:


new20=df["Carpet Area11"].str.split('(', n=1, expand=True)
df['Carpet Area1']=new20[0]

new21=df["Plot Area11"].str.split('(', n=1, expand=True)
df['Plot Area1']=new21[0]

new22=df["Super Area11"].str.split('(', n=1, expand=True)
df['Super Built up area1']=new22[0]

new23=df["Built Area11"].str.split('(', n=1, expand=True)
df['Built Up area1']=new23[0]


# In[ ]:


df= df.replace(np.nan,"NA")

df["Carpet Area"]=np.where(df['Carpet Area']=='NA',df["Carpet Area1"],np.where(df['Carpet Area1']=='NA',df["Carpet Area"],df["Carpet Area"]))
df["Plot Area"]=np.where(df['Plot Area']=='NA',df["Plot Area1"],np.where(df['Plot Area1']=='NA',df["Plot Area"],df["Plot Area"]))
df["Super Built up area"]=np.where(df['Super Built up area']=='NA',df["Super Built up area1"],np.where(df['Super Built up area1']=='NA',df["Super Built up area"],df["Super Built up area"]))
df["Built Up area"]=np.where(df['Built Up area']=='NA',df["Built Up area1"],np.where(df['Built Up area1']=='NA',df["Built Up area"],df["Built Up area"]))


# In[ ]:


df=df.drop(['Carpet Area1','Plot Area1','Super Built up area1','Built Up area1',"Carpet Area11","Plot Area11","Super Area11","Built Area11",'Area1'],axis=1)


# In[ ]:


df["Rooms"]=df["Rooms"].astype(str)

def replace3(i):
    i=i.replace("1",',1').replace("2",',2').replace("3",',3').replace("4",',4').replace("5",',5')
    i=i.replace('6', ',6').replace('7', ',7').replace("8",',8').replace("9",',9').replace("10",',10')
    return i

df["Rooms"]=df["Rooms"].apply(replace3)


# In[ ]:


new10=df["Rooms"].str.split(',', n=1, expand=True)
df["Rooms"]=new10[1]


# In[ ]:


df= df.replace(np.nan,"NA")
df["Configuration"]=np.where(df['Configuration']=='NA',df["Rooms"],np.where(df['Rooms']=='NA',df["Configuration"],df["Configuration"]))
df=df.drop(["Rooms"],axis=1)


# In[ ]:


new11=df["Completed in"].str.split('Completed in: ', n=1, expand=True)
df["Completed in"]=new11[1]
df['junk8']=new11[0]

new12=df["junk8"].str.split('Possession:', n=1, expand=True)
df["Possession1"]=new12[1]

df= df.replace(np.nan,"NA")
df["Possession"]=np.where(df['Possession']=='NA',df["Possession in"],np.where(df['Possession in']=='NA',df["Possession"],df["Possession"]))
df["Possession"]=np.where(df['Possession']=='NA',df["Possession1"],np.where(df['Possession1']=='NA',df["Possession"],df["Possession"]))
df=df.drop(["junk8",'Possession in','Possession1'],axis=1)


# In[ ]:


df["Features"]=df["Features"].astype(str)
df["Furnishing Details"]=df["Furnishing Details"].astype(str)
def replace4(i):
    i=i.replace('[]', 'NA')
    return i

df["Features"]=df["Features"].apply(replace4)
df["Furnishing Details"]=df["Furnishing Details"].apply(replace4)


# In[ ]:


df["Features"]=np.where(df['Features']=='NA',df["Features1"],np.where(df['Features1']=='NA',df["Features"],df["Features"]))
df["Furnishing Details"]=np.where(df['Furnishing Details']=='NA',df["Amenities"],np.where(df['Amenities']=='NA',df["Furnishing Details"],df["Furnishing Details"]))
df=df.drop(["Features1","Amenities"],axis=1)


# In[ ]:


new14=df["Dealer Info"].str.split('Address: ', n=1, expand=True)
df["Dealer Address"]=new14[1]

df= df.replace(np.nan,"NA")
df["Dealer Address"]=np.where(df['Dealer Address']=='NA',df["Dealer Address1"],np.where(df['Dealer Address1']=='NA',df["Dealer Address"],df["Dealer Address"]))
df=df.drop(['Dealer Address1','Dealer Info'],axis=1)


# In[ ]:


new15=df["Properties Listed"].str.split('Properties Listed:', n=1, expand=True)
df["Dealer Properties Listed"]=new15[1]

new16=df["Verified Properties"].str.split('Verified Properties:', n=1, expand=True)
df["Dealer Verified Properties"]=new16[1]


# In[ ]:


def project_area(i):
    word = 'total occupied area'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["Project Area1"]=df['Project Details'].apply(project_area)


# In[ ]:


new17=df["Project Area1"].str.split(')', n=1, expand=True)
df['junk9']=new17[0]

new18=df["junk9"].str.split('area', n=1, expand=True)
df["Project Area1"]=new18[1]

df= df.replace(np.nan,"NA")
df["Project Area"]=np.where(df['Project Area']=='NA',df["Project Area1"],np.where(df['Project Area1']=='NA',df["Project Area"],df["Project Area"]))
df=df.drop(['junk9','Project Area1'],axis=1)


# In[ ]:


df["Project Area"]=df["Project Area"].astype(str)
def replace22(i):
    i=i.replace(" View Master Plan","")
    return i

df["Project Area"]=df["Project Area"].apply(replace22)


# In[ ]:


df["Project Details"]=df["Project Details"].astype(str)

def details(i):
    word = 'units' or 'towers' or 'floors'
    
    if word in i.lower():
        return i
    else:
        
        return 'NA' 

df["junk10"]=df['Project Details'].apply(details)


# In[ ]:


def units11(i):
    word = 'towers'
    
    if word not in i.lower():
        return i
    else:
        
        return 'NA' 

df["Units11"]=df['junk10'].apply(units11)


# In[ ]:


def units1(i):
    word = 'floors'
    
    if word not in i.lower():
        return i
    else:
        
        return 'NA' 

df["Units1"]=df['Units11'].apply(units1)


# In[ ]:


new19=df["Units1"].str.split(' Units', n=1, expand=True)
df['junk11']=new19[0]

new20=df["junk11"].str.split('Project Details', n=1, expand=True)
df['Units1']=new20[1]


# In[ ]:


def units22(i):
    word = 'towers'
    
    if word not in i.lower():
        return i
    else:
        
        return "NA"

df["Units22"]=df['junk10'].apply(units22)


# In[ ]:


def units2(i):
    word = 'floors'
    
    if word not in i.lower():
        return "NA"
    else:
        
        return i

df["Units2"]=df['Units22'].apply(units2)


# In[ ]:


new21=df["Units2"].str.split(' Units', n=1, expand=True)
df['junk12']=new21[0]
df['junk13']=new21[1]

new22=df["junk12"].str.split('Project Details', n=1, expand=True)
df['Units2']=new22[1]

new23=df["junk13"].str.split(' Floors', n=1, expand=True)
df['Floors1']=new23[0]


# In[ ]:


def units33(i):
    word = 'floors'
    
    if word not in i.lower():
        return i
    else:
        
        return "NA"

df["Units33"]=df['junk10'].apply(units33)


# In[ ]:


def units3(i):
    word = 'towers'
    
    if word not in i.lower():
        return "NA"
    else:
        
        return i

df["Units3"]=df['Units33'].apply(units3)


# In[ ]:


new24=df["Units3"].str.split(' Units', n=1, expand=True)
df['junk14']=new24[0]

new25=df["junk14"].str.split(' Towers, ', n=1, expand=True)
df['Units3']=new25[1]
df['junk15']=new25[0]

new26=df["junk15"].str.split('Project Details', n=1, expand=True)
df['Towers1']=new26[1]


# In[ ]:


def details1(i):
    word = 'floors'
    
    if word not in i.lower():
        return "NA"
    else:
        
        return i

df["details1"]=df['junk10'].apply(details1)


# In[ ]:


def details2(i):
    word = 'towers'
    
    if word not in i.lower():
        return "NA"
    else:
        
        return i

df["details2"]=df['details1'].apply(details2)


# In[ ]:


new30=df["details2"].str.split('Units', n=1, expand=True)
df['junk18']=new30[0]
df['junk19']=new30[1]

new31=df["junk19"].str.split('Floors', n=1, expand=True)
df['Floors3']=new31[0]

new32=df["junk18"].str.split(' Towers, ', n=1, expand=True)
df['junk20']=new32[0]
df['Units4']=new32[1]

new33=df["junk20"].str.split('Project Details', n=1, expand=True)
df['Towers3']=new33[1]


# In[ ]:


df= df.replace(np.nan,"NA")


df["Units1"]=np.where(df['Units1']=='NA',df["Units2"],np.where(df['Units2']=='NA',df["Units1"],df["Units1"]))
df["Units1"]=np.where(df['Units1']=='NA',df["Units3"],np.where(df['Units3']=='NA',df["Units1"],df["Units1"]))
df["Units1"]=np.where(df['Units1']=='NA',df["Units4"],np.where(df['Units4']=='NA',df["Units1"],df["Units1"]))
df.rename(columns = {'Units1':'Number of Project Units'}, inplace = True)


df["Number of Project Floors"]=np.where(df['Number of Project Floors']=='NA',df["Floors1"],np.where(df['Floors1']=='NA',df["Number of Project Floors"],df["Number of Project Floors"]))
#df["Number of Project Floors"]=np.where(df['Number of Project Floors']=='NA',df["Floors2"],np.where(df['Floors2']=='NA',df["Number of Project Floors"],df["Number of Project Floors"]))
df["Number of Project Floors"]=np.where(df['Number of Project Floors']=='NA',df["Floors3"],np.where(df['Floors3']=='NA',df["Number of Project Floors"],df["Number of Project Floors"]))


df["Project Towers"]=np.where(df['Project Towers']=='NA',df["Towers1"],np.where(df['Towers1']=='NA',df["Project Towers"],df["Project Towers"]))
#df["Project Towers"]=np.where(df['Project Towers']=='NA',df["Towers2"],np.where(df['Towers2']=='NA',df["Project Towers"],df["Project Towers"]))
df["Project Towers"]=np.where(df['Project Towers']=='NA',df["Towers3"],np.where(df['Towers3']=='NA',df["Project Towers"],df["Project Towers"]))


# In[ ]:


df=df.drop(['junk10','junk11','junk12','junk13','junk14','junk15','junk18','junk19','junk20','Units11','Units2','Units22','Units3','Units33','Units4','Floors1','Floors3','Towers1','Towers3','details1','details2','Project Details'],axis=1)


# In[ ]:


df["Builder/Dealer Name"]=df["Builder/Dealer Name"].astype(str)
df["Builder/Dealer Company"]=df["Builder/Dealer Company"].astype(str)

def replace33(i):
    list1=list(df["Builder/Dealer Name"])
    list2=list(df["Builder/Dealer Company"])
    rank1=list1.index(i)
    i=i.replace(list2[rank1],"")
    return i

df["Builder/Dealer Name"]=df["Builder/Dealer Name"].apply(replace33)
df["Builder/Dealer Name"]=df["Builder/Dealer Name"].astype(str)
df["Builder/Dealer Name"].mask(df["Builder/Dealer Name"] == '', 'NA', inplace=True)


# In[ ]:


new34=df["Society Properties Resale"].str.split(': ', n=1, expand=True)
df['Society Name1']=new34[0]
df["Society Properties Resale"]=new34[1]

new35=df["Society Properties Rent"].str.split(': ', n=1, expand=True)
df['Society Name2']=new35[0]
df["Society Properties Rent"]=new35[1]

df= df.replace(np.nan,"NA")
df["Society Name"]=np.where(df['Society Name']=='NA',df["Society Name1"],np.where(df['Society Name1']=='NA',df["Society Name"],df["Society Name"]))
df["Society Name"]=np.where(df['Society Name']=='NA',df["Society Name2"],np.where(df['Society Name2']=='NA',df["Society Name"],df["Society Name"]))

df=df.drop(['Society Name1'],axis=1)


# In[ ]:


def date1(i):
    word = 'this property is posted by'
    
    if word in i.lower():
        return i
    else:
        
        return "NA"

df["date1"]=df['Posted Date'].apply(date1)


# In[ ]:


def date2(i):
    word = 'this property is posted by'
    
    if word not in i.lower():
        return i
    else:
        
        return "NA"

df["date2"]=df['Posted Date'].apply(date2)


# In[ ]:


df=df.drop(["Posted Date"],axis=1)
new36=df["date1"].str.split('This property is posted by a ', n=1, expand=True)
df['junk21']=new36[1]


new37=df["junk21"].str.split(' on ', n=1, expand=True)
df['date1']=new37[1]
df["Name1"]=new37[0]

df= df.replace(np.nan,"NA")


# In[ ]:


new38=df["date2"].str.split(' by ', n=1, expand=True)
df['date2']=new38[0]
df['Name2']=new38[1]

df= df.replace(np.nan,"NA")


# In[ ]:


df["Name1"]=np.where(df['Name1']=='NA',df["Name2"],np.where(df['Name2']=='NA',df["Name1"],df["Name1"]))
df["Builder/Dealer Name"]=np.where(df['Builder/Dealer Name']=='NA',df["Name1"],np.where(df['Name1']=='NA',df["Builder/Dealer Name"],df["Builder/Dealer Name"]))

df["date1"]=np.where(df['date1']=='NA',df["date2"],np.where(df['date2']=='NA',df["date1"],df["date1"]))

df=df.drop(["Name2",'date2',"Name1",'junk21'],axis=1)


# In[ ]:


df.rename(columns = {'date1':'Posted Date'}, inplace = True)

df["Posted Date"]=df["Posted Date"].astype(str)
def replace55(i):
    i=i.replace(".","")
    return i

df["Posted Date"]=df["Posted Date"].apply(replace55)


# In[ ]:


df["Locality"]="Gurgaon"
df["Locality Link"]="https://www.99acres.com/property-in-gurgaon-ffid"
df["Category"]="Sale"
df= df.replace(np.nan,"NA")


# In[ ]:


df=df.reindex(columns=['Locality','Locality Link','Category','Title','URL','Price','per sq price','Maintenance',
                       'Expected Rental','Booking Amount','Brokerage','Estimated EMI','Posted Date','Availability',
                       'Completed in','Address','RERA Status','Registration No.','Carpet Area','Plot Area',
                       'Super Built up area','Built Up area','Configuration','Floor Number','Property Age',
                       'Facing','Floors Allowed For Construction','Overlooking','Possession','Transaction Type',
                       'Property Ownership','Flooring','Furnishing','Width of facing road','Gated Community','Boundary Wall',
                       'Corner Property','Parking','Wheel Chair Friendly','Pet Friendly','Water Source','Power Backup',
                       'Property Code','Furnishing Details','Features','Project Area','Number of Project Floors','Project Towers',
                       'Number of Project Units','Society Name','Society Properties Resale','Society Properties Rent',
                       "Builder/Dealer Company","Builder/Dealer Name",'Member Since','Dealer RERA no.',
                       'Dealer Address','Dealer Properties Listed','Dealer Verified Properties'])





# In[ ]:


df.to_csv("99acres sales data.csv",encoding='utf-8-sig')

