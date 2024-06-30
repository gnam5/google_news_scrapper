#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests, json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from time import sleep
from datetime import datetime

BASE_URL = "https://www.bigbasket.com"

endpoint = "listing-svc/v2/products"


def build_url(endpoint):
    return f"{BASE_URL}/{endpoint}"


def build_headers():
    return {
        "user-agent": " ",
        "x-csurftoken": " ",
        "cookie": ' ' }


def build_request_data(params, page):
    return {
        "bucket_id": params['bucket_id'],
        "ec_id": params["ec_id"],
        "session_data": params["session_data"],
        "page": page+1,
        "type": params["type"],
        "slug": params["slug"],
        'tab_type': params["tab_type"],
    }

def make_api_call(endpoint, params):
    response = {}
    time_stamp = ''
    for page in range(30):
        retries = 3
        success = False
        for attempt in range(retries):
            try:
                url = build_url(endpoint)
                headers = build_headers()
                data = build_request_data(params, page)
                r = requests.get(url, headers=headers, params=data, verify=False)
                time_stamp = r.headers['Date']
                if r.status_code == 200:
                    try:
                        response[f'page_{page+1}'] = r.json()
                        success = True
                        break  # Exit retry loop on success
                    except Exception as e:
                        response[f'page_{page+1}'] = {"error": str(e)}
                else:
                    response[f'page_{page+1}'] = {"error": f"Failed to fetch data. Status code: {r.status_code}"}
            except Exception as e:
                response[f'page_{page+1}'] = {"error": str(e)}
            sleep(2)  # Add delay between retries
        if not success:
            break  # Exit the loop if all retries fail
        sleep(5)  # Add delay between pages
    return response, time_stamp
        
        
def extract_products(response, category):
    pages = max([int(k.split('_')[1]) for k in response.keys() if k.startswith('page_')], default=0)

    products = []

    for j in range(pages):
        try:
            page_key = f'page_{j + 1}'
            if page_key in response:
                tabs = response[page_key].get('tabs', [])
                if not tabs:
                    continue  # Skip if tabs are empty
                product_info = tabs[0].get('product_info', {})
                if not product_info.get('products', []):
                    continue  # Skip if products are empty
                
                for i in product_info.get('products', []):
                    status = 'In stock' if i.get('availability', {}).get('avail_status') == '001' else 'Out of stock'

                    product_details = {
                        'User Profiling': 'New',
                        'Vendor Name': i.get('brand', {}).get('name', 'N/A'),
                        'Device': 'Mobile',
                        'City/Region': 'Delhi',
                        'Zip Code': 110020,
                        'Product Name': i.get('desc', 'N/A'),
                        'Quantity': i.get('w', 'N/A'),
                        'MRP': i.get('pricing', {}).get('discount', {}).get('mrp', 'N/A'),
                        'Discounted Price': i.get('pricing', {}).get('discount', {}).get('prim_price', {}).get('sp', 'N/A'),
                        'Availability': status,
                        'Offer': i.get('pricing', {}).get('discount', {}).get('d_text', 'N/A'),
                        'Membership Price': i.get('pricing', {}).get('discount', {}).get('subscription_price', 'N/A'),
                        'Category': category
                    }
                    products.append(product_details)

                    if i.get('children'):
                        for k in i['children']:
                            status = 'In stock' if k.get('availability', {}).get('avail_status') == '001' else 'Out of stock'

                            child_product_details = {
                                'User Profiling': 'New',
                                'Vendor Name': k.get('brand', {}).get('name', 'N/A'),
                                'Device': 'Mobile',
                                'City/Region': 'Delhi',
                                'Zip Code': 110020,
                                'Product Name': k.get('desc', 'N/A'),
                                'Quantity': k.get('w', 'N/A'),
                                'MRP': k.get('pricing', {}).get('discount', {}).get('mrp', 'N/A'),
                                'Discounted Price': k.get('pricing', {}).get('discount', {}).get('prim_price', {}).get('sp', 'N/A'),
                                'Availability': status,
                                'Offer': k.get('pricing', {}).get('discount', {}).get('d_text', 'N/A'),
                                'Membership Price': k.get('pricing', {}).get('discount', {}).get('subscription_price', 'N/A'),
                                'Category': category
                            }
                            products.append(child_product_details)

        except Exception as e:
            print(f"Exception: {e} in page {j + 1}")
    return products


def get_formatted_time():
    return datetime.now().strftime('%d-%b-%y,%I:%M %p')


#fresh Vegetables 
print("in veg")   
    
params = {
     "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":36513,\"2\":\"20240518170810399121796869\",\"3\":8,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":2,\"7\":\"Fresh Vegetables\",\"8\":2,\"9\":0,\"10\":0,\"11\":[\"sis&slug=240223-mango\",\"pc&slug=fresh-vegetables\",\"pc&slug=fresh-fruits\",\"pc&slug=herbs-seasonings\",\"pc&slug=cuts-sprouts\",\"pc&slug=exotic-fruits-veggies\",\"pc&slug=flower-bouquets-bunches\",\"pc&slug=organic-fruits-vegetables\"]}","asset_tracker":"{\"asset_id\":\"36513\"}"}',
    "type": "pc",
    "slug": "fresh-vegetables",
    'tab_type':'["all"]'
}

endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_veg, time_stamp = make_api_call(endpoint, params)
    category = 'Fresh Vegetables'
    products = extract_products(response_veg, category)
    vegetables_df = pd.DataFrame(products)
    vegetables_df['Data Fetched DateTime'] = vegetables_df.apply(lambda row: get_formatted_time(), axis=1)
    
    if not vegetables_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


print('\n')
print("in dairy products")   

params = {
    "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":38863,\"2\":\"20240518171254199121796869\",\"3\":6,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":1,\"7\":\"Dairy\",\"8\":1,\"9\":0,\"10\":0,\"11\":[\"pc&slug=dairy\",\"pc&slug=bakery-snacks\",\"pc&slug=breads-buns\",\"pc&slug=cookies-rusk-khari\",\"pc&slug=gourmet-breads\",\"pc&slug=cakes-pastries\"]}","asset_tracker":"{\"asset_id\":\"38863\"}"}',
    "type": "pc",
    "slug": "dairy",
    'tab_type': '["all"]',

}

endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_dairy, time_stamp = make_api_call(endpoint, params)
    category = 'Dairy'
    products = extract_products(response_dairy, category)
    dairy_df = pd.DataFrame(products)
    dairy_df['Data Fetched DateTime'] = dairy_df.apply(lambda row: get_formatted_time(), axis=1)

    if not dairy_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


    
print('\n')
## Cereals
print("in cereals")   

params = {
     "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":43276,\"2\":\"20240518171432299121796869\",\"3\":4,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":1,\"7\":\"Breakfast Cereals\",\"8\":1,\"9\":0,\"10\":0,\"11\":[\"pc&slug=breakfast-cereals\",\"pc&slug=spreads-sauces-ketchup\",\"pc&slug=pickles-chutney\",\"sis&slug=honey-sis\"]}","asset_tracker":"{\"asset_id\":\"43276\"}"}',
    "type": "pc",
    "slug": "breakfast-cereals",
    'tab_type':'["all"]'
}

endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_cereals, time_stamp = make_api_call(endpoint, params)
    category = 'Breakfast Cereals'
    products = extract_products(response_cereals, category)
    cereals_df = pd.DataFrame(products)
    cereals_df['Data Fetched DateTime'] = cereals_df.apply(lambda row: get_formatted_time(), axis=1)
    
    if not cereals_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


    
    
print('\n')
#Hydroponics
print("in hydroponics")   

def build_request_data(params, page):
    return {
         "bucket_id": params['bucket_id'],
        "ec_id": params["ec_id"],
        "session_data": params["session_data"],
        "page": page+1,
        "type": params["type"],
        "slug": params["slug"],
    }
 
params = {
    "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":36513,\"2\":\"202405181625439099121796869\",\"3\":8,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":2,\"7\":\"Fresh Vegetables\",\"8\":2,\"9\":1,\"10\":0,\"11\":[\"sis&slug=240223-mango\",\"pc&slug=fresh-vegetables\",\"pc&slug=fresh-fruits\",\"pc&slug=herbs-seasonings\",\"pc&slug=cuts-sprouts\",\"pc&slug=exotic-fruits-veggies\",\"pc&slug=flower-bouquets-bunches\",\"pc&slug=organic-fruits-vegetables\"]}","asset_tracker":"{\"asset_id\":\"36513\"}"}',
    "type": "pc",
    "slug": "leafy-vegetables",
}


endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_hydro, time_stamp = make_api_call(endpoint, params)
    category = 'Hydroponics'
    products = extract_products(response_hydro, category)
    hydroponics_df = pd.DataFrame(products)
    hydroponics_df['Data Fetched DateTime'] = hydroponics_df.apply(lambda row: get_formatted_time(), axis=1)

    if not hydroponics_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")



print('\n')
#Fresh Fruits
print("in fresh fruits")   

params = {
    "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":36513,\"2\":\"20240518162546199121796869\",\"3\":8,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":2,\"7\":\"Fresh Fruits\",\"8\":3,\"9\":0,\"10\":0,\"11\":[\"sis&slug=240223-mango\",\"pc&slug=fresh-vegetables\",\"pc&slug=fresh-fruits\",\"pc&slug=herbs-seasonings\",\"pc&slug=cuts-sprouts\",\"pc&slug=exotic-fruits-veggies\",\"pc&slug=flower-bouquets-bunches\",\"pc&slug=organic-fruits-vegetables\"]}","asset_tracker":"{\"asset_id\":\"36513\"}"}',
    "type": "pc",
    "slug": "fresh-fruits"
}


endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_fruits, time_stamp = make_api_call(endpoint, params)
    category = 'Fresh Fruits'
    products = extract_products(response_fruits, category)
    fruits_df = pd.DataFrame(products)
    fruits_df['Data Fetched DateTime'] = fruits_df.apply(lambda row: get_formatted_time(), axis=1)

    if not fruits_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


    
print('\n')

##Dal Pulses
print("in dal and pulses")   

params = {
     "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":44326,\"2\":\"20240518163002599121796869\",\"3\":5,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":1,\"7\":\"Dals & Pulses\",\"8\":2,\"9\":0,\"10\":0,\"11\":[\"pc&slug=atta-whole-wheat\",\"pc&slug=dals-pulses\",\"pc&slug=rice-rice-products\",\"pc&slug=salt-sugar-jaggery\",\"sis&slug=2404382s-attaricedals\"]}","asset_tracker":"{\"asset_id\":\"44326\"}"}',
    "type": "pc",
    "slug": "dals-pulses"
}


endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_dal, time_stamp = make_api_call(endpoint, params)
    category = 'Dals & Pulses'
    products = extract_products(response_dal, category)
    dals_df = pd.DataFrame(products)
    dals_df['Data Fetched DateTime'] = dals_df.apply(lambda row: get_formatted_time(), axis=1)

    if not dals_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


    
##Edible OIl

print('\n')
print("in edible oil")   

# Example usage
params = {
    "bucket_id": 31,
    "ec_id": 100,
    "session_data": '{"client_asset_tracker":"{\"1\":44075,\"2\":\"20240518163133299121796869\",\"3\":5,\"4\":\"npc_javelin-310-310\",\"5\":1,\"6\":1,\"7\":\"Edible Oils\",\"8\":1,\"9\":0,\"10\":0,\"11\":[\"pc&slug=edible-oils-ghee\",\"pc&slug=masalas-spices\",\"pc&slug=dry-fruits\",\"pc&slug=ghee-vanaspati\",\"sis&slug=180424-organic-mod\"]}","asset_tracker":"{\"asset_id\":\"44075\"}"}',
    "type": "pc",
    "slug": "edible-oils-ghee"
}

endpoint = "listing-svc/v2/products"
max_retries = 3
retry_interval = 5  # in seconds

for attempt in range(max_retries):
    response_oil, time_stamp = make_api_call(endpoint, params)
    category = 'Edible Oil'
    products = extract_products(response_oil, category)
    oil_df = pd.DataFrame(products)
    oil_df['Data Fetched DateTime'] = oil_df.apply(lambda row: get_formatted_time(), axis=1)

    if not oil_df.empty:
        print(f"Number of products collected: {len(products)}")
        break  # Exit the loop if we have data
    else:
        print(f"Attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
        sleep(retry_interval)
else:
    print("Failed to collect data after multiple attempts.")


    
print('\n')
print("now in final df")   

vegetables_df['PLP Ranking'] = range(1, len(vegetables_df)+1)
fruits_df['PLP Ranking'] = range(1, len(fruits_df)+1)
hydroponics_df['PLP Ranking'] = range(1, len(hydroponics_df)+1)
oil_df['PLP Ranking'] = range(1, len(oil_df)+1)
cereals_df['PLP Ranking'] = range(1, len(cereals_df)+1)
dairy_df['PLP Ranking'] = range(1, len(dairy_df)+1)
dals_df['PLP Ranking'] = range(1, len(dals_df)+1)

final_df = pd.concat([vegetables_df, fruits_df, hydroponics_df, cereals_df, dairy_df, oil_df, dals_df])
final_df['Combos Flag'] = final_df.apply(lambda row: 'Yes' if 'combo' in row['Quantity'].lower() or 'combo' in row['Product Name'].lower() else 'No', axis=1)


print("final df")
final_df


# # CD catalogue weights cleaning

# In[ ]:


import re
import pandas as pd
import numpy as np

data= "C:cd_product_catalogue.xlsx"

df = pd.read_excel(data)


# import boto3
# from dotenv import load_dotenv
# import os
# import s3fs

# load_dotenv()

# access_key=os.getenv('aws_access_key_id')
# access_secret_key=os.getenv('aws_secret_access_key')

# Define the S3 bucket and file key

# bucket_name = 'bpbasket'
# file_key = 'cd_product_catalogue.xlsx'

# Initialize the S3 client with your credentials

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=access_key,
#     aws_secret_access_key=access_secret_key
# )

# Construct the S3 URL

# s3_url = f's3://{bucket_name}/{file_key}'

# Read the Excel file from S3

# df = pd.read_excel(s3_url, engine='openpyxl' , storage_options={'key': access_key,
#     'secret': access_secret_key })

# Function to clean the Product Name column
def split_description(description):
    # Check if hyphen is followed by a number using regex
    match = re.search(r'-\s*\d', description)
    if match:
        return description[:match.start()].strip()
    return description

df['product Name'] = df['product_name'].apply(split_description)

# filtering out CD catalogue data with gm or kg
def filter_kg_gm(df): 
    filtered_df = df[df['weight'].notnull() & df['weight'].str.contains('kg|gm', na=False)]
    return filtered_df


filtered_df1 = df[df['weight'].notnull() & df['weight'].str.contains('kg|gm', na=False)]

# converting weights in CD catalogue to grams
def convert_to_grams_cd(weight):
    if isinstance(weight, str):
        weight = weight.lower().strip()  # Make the weight string lowercase for uniformity

        # Handle combined weights like "X gm + Y gm"
        if re.match(r'\d+\s*gm\s*\+\s*\d+\s*gm', weight):
            numbers = re.findall(r'\d+', weight)
            return sum(int(num) for num in numbers)  # Sum up the individual weights

        # Handle weights like "X gm" or "X kg"
        if re.match(r'\d+\.?\d*\s*(kg|gm)', weight):
            numeric_part = re.search(r'\d+\.?\d*', weight)
            if numeric_part:
                value = float(numeric_part.group())
                if 'kg' in weight:
                    return value * 1000
                elif 'gm' in weight:
                    return value

        # Handle "X x Y kg", "X x Y gm", "Xkg x Y", and "Xgm x Y"
        if 'x' in weight:
            # Split the weight string into parts using 'x'
            parts = re.split(r'\s*x\s*', weight)

            if len(parts) == 2:
                # Check for parentheses enclosing the multiplier part
                if parts[1][0] == '(' and parts[1][-1] == ')':
                    parts[1] = parts[1][1:-1]  # Remove the parentheses

                quantity_str = parts[0].strip()
                unit_value_str = parts[1].strip()

                # Determine if the unit is in the first or second part
                if 'kg' in quantity_str or 'gm' in quantity_str:
                    unit_value_str, quantity_str = quantity_str, unit_value_str

                # Extract numeric values
                quantity = float(re.search(r'\d+\.?\d*', quantity_str).group())
                unit_value = float(re.search(r'\d+\.?\d*', unit_value_str).group())

                # Determine if the unit is kilograms or grams
                if 'kg' in unit_value_str:
                    return quantity * unit_value * 1000
                elif 'gm' in unit_value_str:
                    return quantity * unit_value

        # Handle formats like "X pc + Y pc" and "X pcs + Y pcs"
        if re.match(r'\d+\s*gm\s*\+\s*\d+\s*pc', weight) or re.match(r'\d+\s*g\s*\+\s*\d+\s*pcs', weight):
            numbers = re.findall(r'\d+', weight)
            return sum(int(num) for num in numbers) 

        
        # Handle weights in kg
        if 'pc' in weight or 'pcs' in weight:
            numeric_part = re.search(r'\d*\.?\d+', weight)
            if numeric_part:
                return float(numeric_part.group())
        
    return None  # Return None for non-kg/gm values


# Apply the function to the 'weight' column
filtered_df1['weight_in_g'] = filtered_df1['weight'].apply(convert_to_grams_cd)

# Display the dataframe with the converted weights
#filtered_df1.head(10)


# # BB  data weights cleaning

# In[2]:


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

#final_df['Quantity'] = final_df['Quantity'].apply(replace_L_with_ltr)
#final_df['Quantity'] = final_df['Quantity'].apply(replace_l_with_ltr)


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
                    weights = [float(numbers[1]), float(numbers[2]) * 1000]
                else:
                    weights = [float(numbers[1]), float(numbers[2])]
                avg_weight = np.mean(weights)
                return avg_weight
            else:
                if 'kg' in weight or 'ltr' in weight:
                    weights = [float(numbers[0]), float(numbers[1]) * 1000]
                else:
                    weights = [float(num) for num in numbers]
                
            avg_weight = np.mean(weights)
            return avg_weight

        # Handle parentheses
        if '(' in weight:
            inside_parentheses = re.search(r'\((.*?)\)', weight)
            if inside_parentheses:
                inside_text = inside_parentheses.group(1)
                if 'x' in inside_text:
                    pass  # Skip this condition and move to the next if 'x' is inside parentheses
                else:
                    numbers = re.findall(r'\d*\.?\d+', inside_text)
                    if len(numbers) == 3:
                        # If there are three numbers, exclude the first and take the average of the other two
                        if 'kg' in inside_text or 'ltr' in inside_text:
                            weights = [float(numbers[1]), float(numbers[2]) * 1000]
                        else:
                            weights = [float(numbers[1]), float(numbers[2])]
                        avg_weight = np.mean(weights)
                        return avg_weight
                    
                    elif len(numbers) == 1:
                        if 'kg' in inside_text or 'ltr' in inside_text:
                            return float(numbers[0]) * 1000  
                        else:
                            return float(numbers[0])
                        
            else:
                if 'kg' in weight or 'ltr' in weight:
                    weights = [float(numbers[0]), float(numbers[1]) * 1000]
                else:
                    weights = [float(num) for num in numbers]
                
                avg_weight = np.mean(weights)
                return avg_weight

        
        # Handle "X x Y kg", "X x Y gm", "Xkg x Y", and "Xgm x Y"
        if 'x' in weight:
            # Split the weight string into parts using 'x'
            parts = re.split(r'\s*x\s*', weight)
        
            if len(parts) >= 2:
                # Check for parentheses enclosing the multiplier part
                if parts[1][0] == '(' and parts[1][-1] == ')':
                    parts[1] = parts[1][1:-1]  # Remove the parentheses

                quantity_str = parts[0].strip()
                unit_value_str = parts[1].strip()

                # Determine if the unit is in the first or second part
                if ('kg' in quantity_str or 'ltr' in quantity_str) or ('gm' in quantity_str or 'g' in quantity_str or 'ml' in quantity_str):
                    unit_value_str, quantity_str = quantity_str, unit_value_str

                # Extract numeric values
                quantity = float(re.search(r'\d+\.?\d*', quantity_str).group())
                unit_value = float(re.search(r'\d+\.?\d*', unit_value_str).group())


                # Determine if the unit is kilograms or grams
                if 'kg' in unit_value_str or 'ltr' in unit_value_str:
                    return quantity * unit_value * 1000
                elif 'gm' in unit_value_str or 'g' in unit_value_str or 'ml' in unit_value_str:
                    return quantity * unit_value

        # Handle formats like "X gm + Y gm" and "X g + Y g"
        if re.match(r'\d+\s*gm\s*\+\s*\d+\s*gm', weight) or re.match(r'\d+\s*g\s*\+\s*\d+\s*g', weight) or re.match(r'\d+\s*g\s*\+\s*\d+\s*ml', weight):
            numbers = re.findall(r'\d+', weight)
            return sum(int(num) for num in numbers) 

        
        # Handle weights in kg
        if 'kg' in weight or 'ltr' in weight:
            numeric_part = re.search(r'\d*\.?\d+', weight)
            if numeric_part:
                return float(numeric_part.group()) * 1000
        
        # Handle weights in grams
        if 'g' in weight or 'gm' in weight or 'ml' in weight:
            numeric_part = re.search(r'\d*\.?\d+', weight)
            if numeric_part:
                return float(numeric_part.group())


    return np.nan  # Return NaN for non-kg/gm values

#final_df['Weight_gms'] = final_df['Quantity'].apply(convert_to_grams)
#final_df


# In[11]:


test_input = "1 pc (approx. 1-3 Kg)"
print(convert_to_grams(test_input))


# In[ ]:



#dataframe inro list dictionary
final_dict=[]
for i in range(len(list(filtered_df1['product Name']))):
    des={}
    des['product Name']=list(filtered_df1['product Name'])[i]
    des['weight']=list(filtered_df1['weight'])[i]
    des['weight_in_g']=list(filtered_df1['weight_in_g'])[i]
    final_dict.append(des)
    
final_dict


# In[ ]:


special_cases = {
    'Coriander Leaves - Chopped': 'Coriander (Dhaniya)',
    'Tomato - Local': 'Tomato Desi',
    'Tomato - Local (Loose)': 'Tomato Desi',
    'Tomato - Local, Organically Grown (Loose)': 'Tomato Desi'
}


# In[ ]:


def get_matched_value(product_name):
    # Check for special cases before cleaning the product name
    if product_name in special_cases:
        special_product_name = special_cases[product_name]
        return [item for item in final_dict if item['product Name'] == special_product_name]
    
    # Clean the product name if it's not a special case
    cleaned_product_name = product_name.replace('pc', '').replace('(Loose)', '').replace(' - ', ' ').replace(', Organically Grown', "").strip()
    
    # General matching logic
    alphabet_list = cleaned_product_name.split()
    output = [item for item in final_dict if all(letter.lower() in item['product Name'].lower() for letter in alphabet_list)]
    return output

final_df['Related Topics']=final_df['Product Name'].apply(get_matched_value)
final_df


# In[ ]:


# Defining the function
def find_initials(weights_list, target_weight):
    try:
        closest_weight_dict = min(weights_list, key=lambda x: abs(x['weight_in_g'] - target_weight))
    except:
        closest_weight_dict={'product Name': '','weight': '','weight_in_g': ''}
    return closest_weight_dict

# Applying it to two columns
final_df["initials"] = final_df.apply(lambda x: find_initials(x["Related Topics"], x["Weight_gms"]), axis=1)
final_df


# In[ ]:


# Example DataFrame with a dictionary column
df=final_df

# Expand the dictionary column into separate columns
expanded_df = pd.concat([df.drop(['initials','Related Topics'], axis=1), df['initials'].apply(pd.Series)], axis=1)

expanded_df


# In[ ]:


expanded_df = expanded_df.rename({'Product Name':'Product Name (BB)','Quantity':'Quantity Variants BB ',
                                  'Weight_gms': 'Normalised BB Weight in Grams', 'product Name': 'Product Name (CD match)', 
                    'weight' :'Weight (CD match)', 
                    'weight_in_g' : 'Normalised CD Weight in Grams'}, axis=1)
expanded_df.head(5)

expanded_df['Normalised CD Weight in Grams'] = pd.to_numeric(expanded_df['Normalised CD Weight in Grams'], errors='coerce')
expanded_df['Normalization Factor'] = expanded_df['Normalised BB Weight in Grams'] / expanded_df['Normalised CD Weight in Grams']
expanded_df['Normalization Factor'] = expanded_df['Normalization Factor'].round(2)
expanded_df['Normalization Factor'].fillna('', inplace=True)
expanded_df['Normalised CD Weight in Grams'].fillna('', inplace=True)
expanded_df


# In[ ]:


# Function to determine match type
def determine_match(row):
    if pd.isna(row['Product Name (BB)']) or pd.isna(row['Product Name (CD match)']) or        row['Product Name (BB)'] == '' or row['Product Name (CD match)'] == '' or        pd.isna(row['Normalised CD Weight in Grams']) or pd.isna(row['Normalised BB Weight in Grams']) or        row['Normalised CD Weight in Grams'] == '' or row['Normalised BB Weight in Grams'] == '':
        return ''
    elif row['Product Name (BB)'] == row['Product Name (CD match)'] and          row['Normalised CD Weight in Grams'] == row['Normalised BB Weight in Grams']:
        return 'Exact Match'
    else:
        return 'Variant Match'

# Apply the function to each row
expanded_df['Match'] = expanded_df.apply(determine_match, axis=1)
expanded_df = expanded_df.drop_duplicates()
expanded_df


# In[ ]:


# saving csv to google drive
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime, timedelta
import io
import os
from tempfile import NamedTemporaryFile
from pydrive.auth import ServiceAccountCredentials



gauth = GoogleAuth()
url = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('country-delight-424707-6fdaa01b7168.json', url)
gauth.credentials = creds
    

drive = GoogleDrive(gauth)

# Convert DataFrame to CSV bytes
csv_bytes = io.BytesIO()
expanded_df.to_csv(csv_bytes, index=False)

# Get current timestamp and the timestamp of the previous hour
current_time = datetime.now()
previous_time = current_time - timedelta(minutes=1)

# Define file names
current_file_name = f"File Creation: {current_time.strftime('%d-%b-%y,%I:%M %p')}.csv"



folder_id = ' '  
with NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
    tmp_file.write(csv_bytes.getvalue())


file = drive.CreateFile({'title': current_file_name, 'parents': [{'id': folder_id}]})
file.SetContentFile(tmp_file.name)
file.Upload()
tmp_file.close()

    
# deletion of temporary csv file   
previous_time_timestamp = previous_time.timestamp()

tmp_dir = os.path.dirname(tmp_file.name)
for filename in os.listdir(tmp_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(tmp_dir, filename)
        if os.path.isfile(file_path):
            modification_time = os.path.getmtime(file_path)
            if modification_time < previous_time_timestamp:
                os.remove(file_path)


print(f'File {current_file_name} uploaded to Google Drive.')



# moving csv to history folder
deletion_time = current_time - timedelta(hours=12)
destination_folder_id = ' '
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

for file in file_list:
    file_id = file['id']
    file_title = file['title']
    created_time = datetime.strptime(file['createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    if created_time < deletion_time:
        file['parents'] = [{'id': destination_folder_id}]
        file.Upload()
        print(f'File {file_title} moved to the destination folder.')

