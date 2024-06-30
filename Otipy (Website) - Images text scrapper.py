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


import cv2
import numpy as np
from PIL import Image
import pytesseract
import requests
from io import BytesIO


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Assuming you have already initialized the driver and navigated to the page
soup = BeautifulSoup(driver.page_source, 'html.parser')
final_data_stock = []

items = soup.find_all('div', attrs={'class': 'style_deal__XEg0S'})
for k in items:
    des_bb = {}

    # Extract the image URL from the srcset attribute
    img_tag = k.find('img', attrs={'class': 'style_img__L5K5o'})
    if img_tag and 'srcset' in img_tag.attrs:
        srcset = img_tag['srcset']
        # Split the srcset string to get the first URL
        image_url = srcset.split(' ')[0]
        # Prepend the base URL
        full_url = f"https://www.otipy.com{image_url}"
    else:
        full_url = "No Information Provided"

    # Extract text from image
    if full_url != "No Information Provided":
        try:
        
        # Fetch the image
            response = requests.get(full_url)
            img = Image.open(BytesIO(response.content))

            # Convert the image to grayscale using OpenCV
            open_cv_image = np.array(img.convert('RGB'))
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to increase contrast
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Apply morphological operations to enhance text regions
            kernel = np.ones((1, 1), np.uint8)
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

            # Convert back to PIL image
            processed_img = Image.fromarray(morph)

            # Extract text from the preprocessed image using pytesseract
            text = pytesseract.image_to_string(processed_img)
    
        except Exception as e:
            text = f"Error extracting text: {str(e)}"
            
    else:
        text = "No Image URL Provided"
        
        
    if k.find('span', attrs={'class': 'style_deal_qt__eOzdS'}) != None:
        quantity = k.find('span', attrs={'class': 'style_deal_qt__eOzdS'}).text
    else:
        quantity = "No Information Provided"
     
    if k.find('span', attrs={'class': 'style_deal_price__BrE2z'}) != None:
        price = k.find('span', attrs={'class': 'style_deal_price__BrE2z'}).text.replace(quantity, '').strip()
    else:
        price = "No Information Provided"
        
    des_bb['image_url'] = full_url
    des_bb['Quantity (Flash Sale)'] = quantity
    des_bb['MRP (Flash Sale)'] = price
    des_bb['Image Text'] = text
                             
    final_data_stock.append(des_bb)

# Output the final data
final_data_stock


# In[ ]:


df = pd.DataFrame(final_data_stock)

def extract_qty(qty):
    return qty.replace("/", "").strip()

df['Quantity (Flash Sale)'] = df['Quantity (Flash Sale)'].apply(extract_qty)


# In[ ]:


df.to_excel("test.xlsx", index=False, engine='openpyxl')

