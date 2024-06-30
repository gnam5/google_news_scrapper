#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import pandas as pd


# In[ ]:


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start with maximized window

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
driver.get('https://www.otipy.com')  # Replace with the actual URL

# Wait for the popup to appear (Adjust the time as necessary)
time.sleep(10)

try:
    # Find the close button using its class name
    close_button = driver.find_element(By.CLASS_NAME, 'style_icon__nNhfo')
    
    # Click the close button
    close_button.click()
    
    print("Popup closed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
    
time.sleep(10)    
try:
    # Find the input field using its class name
    input_field = driver.find_element(By.CLASS_NAME, 'style_input1__BCMay')

    # Click on the input field to focus
    input_field.click()

    # Clear the input field if there's any pre-filled text
    input_field.clear()

    # Enter the location "Delhi" and press Enter
    input_field.send_keys("Delhi")
    input_field.send_keys(Keys.ENTER)

    print("Location entered successfully.")
except Exception as e:
    print(f"An error occurred: {e}")


# In[ ]:


time.sleep(10)
driver.get('https://www.otipy.com/category/fruits-2')
time.sleep(5)

# Scrolling function to scroll the page to the bottom
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)  # Wait to load the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to the bottom of the page
scroll_to_bottom(driver)

# Now, parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
#print(soup)


# In[ ]:


final_data_stock=[]
items = soup.find_all('div', attrs={'class': 'style_card__v4i84 }'})
for k in items:
    des_bb={}
    
    if k.find('h3', attrs={'class': 'style_prod_name__QllSp'}) != None:
        product_name=k.find('h3', attrs={'class': 'style_prod_name__QllSp'}).text
    else:
        product_name= "No Information Provided"
       
    if k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}) != None:
        quantity=k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}).text
    else:
        quantity= "No Information Provided"
     
    if k.find('p', attrs={'class': 'style_final_price__FERLK'}) != None:
        price=k.find('p', attrs={'class': 'style_final_price__FERLK'}).text.replace(quantity,'').strip()
    else:
        price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_striked_price__4ghn5'}) != None:
        striked_price=k.find('span', attrs={'class': 'style_striked_price__4ghn5'}).text.replace(quantity,'').strip()
    else:
        striked_price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_selling_price__GaIsF'}) != None:
        selling_price=k.find('span', attrs={'class': 'style_selling_price__GaIsF'}).text.replace(quantity,'').strip()
    else:
        selling_price= "No Information Provided"
        
    
    des_bb['Product Name (Otipy)']=product_name
    des_bb['Quantity (Otipy)']=quantity
    des_bb['MRP (per kg/pc/pack)']=striked_price
    des_bb['Discounted Price']=price
    des_bb['Different Variants']=selling_price
    des_bb['Availability']= 'In stock'
    des_bb['Data Fetched DateTime']=datetime.now().strftime('%d-%b-%y,%I:%M %p')
    des_bb['Category']="Fruits"
    
    final_data_stock.append(des_bb)


# In[ ]:


final_data_out_stock=[]
time.sleep(10)
items = soup.find_all('div', attrs={'class': 'style_card__v4i84 style_out_of_stock__l9lo4 }'})
for k in items:
    des_bb={}
    
    if k.find('h3', attrs={'class': 'style_prod_name__QllSp'}) != None:
        product_name=k.find('h3', attrs={'class': 'style_prod_name__QllSp'}).text
    else:
        product_name= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}) != None:
        quantity=k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}).text
    else:
        quantity= "No Information Provided"
     
    if k.find('p', attrs={'class': 'style_final_price__FERLK'}) != None:
        price=k.find('p', attrs={'class': 'style_final_price__FERLK'}).text.replace(quantity,'').strip()
    else:
        price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_striked_price__4ghn5'}) != None:
        striked_price=k.find('span', attrs={'class': 'style_striked_price__4ghn5'}).text.replace(quantity,'').strip()
    else:
        striked_price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_selling_price__GaIsF'}) != None:
        selling_price=k.find('span', attrs={'class': 'style_selling_price__GaIsF'}).text.replace(quantity,'').strip()
    else:
        selling_price= "No Information Provided"
        
    
    des_bb['Product Name (Otipy)']=product_name
    des_bb['Quantity (Otipy)']=quantity
    des_bb['MRP (per kg/pc/pack)']=striked_price
    des_bb['Discounted Price']=price
    des_bb['Different Variants']=selling_price
    des_bb['Availability']= 'Out of stock'
    des_bb['Data Fetched DateTime']=datetime.now().strftime('%d-%b-%y,%I:%M %p')
    des_bb['Category']="Fruits"
    
    final_data_out_stock.append(des_bb)


# In[ ]:


driver.get('https://www.otipy.com/category/vegetables-1')
time.sleep(5)

# Scrolling function to scroll the page to the bottom
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)  # Wait to load the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to the bottom of the page
scroll_to_bottom(driver)

# Now, parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
#print(soup)


# In[ ]:


final_data_stock_1=[]
time.sleep(10)
items = soup.find_all('div', attrs={'class': 'style_card__v4i84 }'})
for k in items:
    des_bb={}
    
    if k.find('h3', attrs={'class': 'style_prod_name__QllSp'}) != None:
        product_name=k.find('h3', attrs={'class': 'style_prod_name__QllSp'}).text
    else:
        product_name= "No Information Provided"
       
    if k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}) != None:
        quantity=k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}).text
    else:
        quantity= "No Information Provided"
     
    if k.find('p', attrs={'class': 'style_final_price__FERLK'}) != None:
        price=k.find('p', attrs={'class': 'style_final_price__FERLK'}).text.replace(quantity,'').strip()
    else:
        price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_striked_price__4ghn5'}) != None:
        striked_price=k.find('span', attrs={'class': 'style_striked_price__4ghn5'}).text.replace(quantity,'').strip()
    else:
        striked_price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_selling_price__GaIsF'}) != None:
        selling_price=k.find('span', attrs={'class': 'style_selling_price__GaIsF'}).text.replace(quantity,'').strip()
    else:
        selling_price= "No Information Provided"
        
    
    des_bb['Product Name (Otipy)']=product_name
    des_bb['Quantity (Otipy)']=quantity
    des_bb['MRP (per kg/pc/pack)']=striked_price
    des_bb['Discounted Price']=price
    des_bb['Different Variants']=selling_price
    des_bb['Availability']= 'In stock'
    des_bb['Data Fetched DateTime']=datetime.now().strftime('%d-%b-%y,%I:%M %p')
    des_bb['Category']="Vegetables"
    
    final_data_stock_1.append(des_bb)


# In[ ]:


final_data_out_stock_1=[]
items = soup.find_all('div', attrs={'class': 'style_card__v4i84 style_out_of_stock__l9lo4 }'})
for k in items:
    des_bb={}
    
    if k.find('h3', attrs={'class': 'style_prod_name__QllSp'}) != None:
        product_name=k.find('h3', attrs={'class': 'style_prod_name__QllSp'}).text
    else:
        product_name= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}) != None:
        quantity=k.find('span', attrs={'class': 'style_prod_qt__cXcqe'}).text
    else:
        quantity= "No Information Provided"
     
    if k.find('p', attrs={'class': 'style_final_price__FERLK'}) != None:
        price=k.find('p', attrs={'class': 'style_final_price__FERLK'}).text.replace(quantity,'').strip()
    else:
        price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_striked_price__4ghn5'}) != None:
        striked_price=k.find('span', attrs={'class': 'style_striked_price__4ghn5'}).text.replace(quantity,'').strip()
    else:
        striked_price= "No Information Provided"
        
    if k.find('span', attrs={'class': 'style_selling_price__GaIsF'}) != None:
        selling_price=k.find('span', attrs={'class': 'style_selling_price__GaIsF'}).text.replace(quantity,'').strip()
    else:
        selling_price= "No Information Provided"
        
    
    des_bb['Product Name (Otipy)']=product_name
    des_bb['Quantity (Otipy)']=quantity
    des_bb['MRP (per kg/pc/pack)']=striked_price
    des_bb['Discounted Price']=price
    des_bb['Different Variants']=selling_price
    des_bb['Availability']= 'Out of stock'
    des_bb['Data Fetched DateTime']=datetime.now().strftime('%d-%b-%y,%I:%M %p')
    des_bb['Category']="Vegetables"
    
    final_data_out_stock_1.append(des_bb)


# In[ ]:


stock = pd.DataFrame(final_data_stock)
out_stock = pd.DataFrame(final_data_out_stock)
df1 = pd.concat([stock, out_stock], ignore_index=True)
df1['PLP Ranking'] = range(1, len(df1)+1)

stock_1 = pd.DataFrame(final_data_stock_1)
out_stock_1 = pd.DataFrame(final_data_out_stock_1)
df2 = pd.concat([stock_1, out_stock_1], ignore_index=True)
df2['PLP Ranking'] = range(1, len(df2)+1)

final_data = pd.concat([df1,df2])

final_data.insert(0, 'User Profiling', ['New'] * len(final_data))
final_data.insert(1, 'Device', ['Desktop'] * len(final_data))
final_data.insert(2, 'City/ Region', ['Delhi'] * len(final_data))
final_data['Combos Flag'] = final_data.apply(lambda row: 'Yes' if 'combo' in row['Product Name (Otipy)'].lower() else 'No', axis=1)


#final_data.to_excel("otipy.xlsx", index=False, engine='openpyxl')


# In[ ]:


import numpy as np
import re
import pandas as pd

def replace_L_with_ltr(value):
    if 'Ltr' in value:
        return value.replace('Ltr', 'Ltr')
    elif 'L' in value:
        return value.replace('L', 'Ltr')
    return value

def replace_l_with_ltr(value_1):
    if 'ml' in value_1:
        return value_1.replace('ml', 'ml')
    elif 'l' in value_1:
        return value_1.replace('l', 'Ltr')
    return value_1

final_data['Quantity (Otipy)'] = final_data['Quantity (Otipy)'].apply(replace_L_with_ltr)
final_data['Quantity (Otipy)'] = final_data['Quantity (Otipy)'].apply(replace_l_with_ltr)


# Function to convert weight to grams
def convert_to_grams(weight):
    if isinstance(weight, str):
        weight = weight.lower()  # Make the weight string lowercase for uniformity
        weight = re.sub(r'\bapprox\.\b', '', weight)
        weight = re.sub(r'\bapprox\b', '', weight)
        
        # Handle ranges with 'to' or '-'
        if 'to' in weight or '-' in weight:
            numbers = re.findall(r'\d*\.?\d+', weight)
            if len(numbers) == 3:
                # If there are three numbers, exclude the first and take the average of the other two
                if 'kg' in weight or 'ltr' in weight:
                    weights = [float(numbers[1]), float(numbers[2])]
                else:
                    weights = [float(numbers[1])/1000, float(numbers[2])/1000]
                avg_weight = np.mean(weights)
                return f"{avg_weight:.2f} kg"
            else:
                if 'kg' in weight or 'ltr' in weight:
                    weights = [float(num) for num in numbers]
                else:
                    weights = [float(numbers[0])/1000, float(numbers[1])/1000]
                
            avg_weight = np.mean(weights)
            return f"{avg_weight:.2f} kg"

        
        # Handle weights in kg
        if 'kg' in weight or 'ltr' in weight:
            numeric_part = re.search(r'\d*\.?\d+', weight)
            if numeric_part:
                return f"{float(numeric_part.group()):.2f} kg"
        
        # Handle weights in grams
        if 'g' in weight or 'gm' in weight or 'ml' in weight:
            numeric_part = re.search(r'\d*\.?\d+', weight)
            if numeric_part:
                return f"{float(numeric_part.group()) / 1000:.2f} kg"


    return weight  # Return NaN for non-kg/gm values

final_data['Normalize quantity (in kg/pc/pack)'] = final_data['Quantity (Otipy)'].apply(convert_to_grams)


# In[ ]:


# Function to extract numeric value from the price
def extract_price(price):
    return float(price.replace("₹", "").strip())

# Function to extract numeric value from the quantity
def extract_quantity(quantity):
    return float(quantity.replace("kg", "").replace("pcs", "").replace("pc", "").replace("pack", "").strip())

# Apply the extraction functions to create new columns
final_data['Price'] = final_data['Discounted Price'].apply(extract_price)
final_data['Quantity'] = final_data['Normalize quantity (in kg/pc/pack)'].apply(extract_quantity)

# Calculate the price per unit
final_data['Discounted Price (per kg/pc/pack)'] = final_data['Price'] / final_data['Quantity']
final_data['Discounted Price (per kg/pc/pack)'] = final_data['Discounted Price (per kg/pc/pack)'].round(2)

# Drop the intermediate columns used for calculations
final_data = final_data.drop(columns=['Price', 'Quantity'])


# In[ ]:


final_data.to_excel("otipy.xlsx", index=False, engine='openpyxl')

