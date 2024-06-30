import time
from bs4 import BeautifulSoup
import time
import pandas as pd
import time
import warnings
import re
import base64
import requests
from msal import ConfidentialClientApplication

# from Onedrive import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# "/Users/nitingarg/dev/chromedriver"
driver = webdriver.Chrome()  # path of your chromedriver

login_url = " "
driver.get(login_url)
wait = WebDriverWait(driver, 10)

username_input = driver.find_element(By.NAME, "sUserName")
password_input = driver.find_element(By.NAME, "sPassword")
org_key_input = driver.find_element(By.NAME, "sParentUID")

username_input.send_keys("test1")
password_input.send_keys("bot234!")
org_key_input.send_keys("v7408")


login_button = driver.find_element(By.XPATH, '//button[text()="Login"]')
login_button.click()
wait = WebDriverWait(driver, 10)

dashboard_url = " "
driver.get(dashboard_url)
wait = WebDriverWait(driver, 25)

# Replace these values with your registered app's credentials
CLIENT_ID = " "
CLIENT_SECRET = " "
TENANT_ID = " "

# SCOPES = ['https://graph.microsoft.com/Files.ReadWrite']
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/.default"]


def get_access_token():
    # Create a ConfidentialClientApplication object for client credential flow
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )

    # Acquire a token using client credential flow
    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError("Could not retrieve access token.")


def list_folder(access_token, user_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"{GRAPH_API_BASE_URL}/users/{user_id}/drive/items/root/children"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        res = response.json()
        print(res.get("value"))
    else:
        print(
            f"Failed to create folder. Status Code: {response.status_code}, Error Message: {response.json()}"
        )


def createNewOrGetDetails(access_token, user_id, folder_name, parent_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f'{GRAPH_API_BASE_URL}/users/{user_id}/drive/items/{ parent_id if parent_id else "root"}/children'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        res = response.json()
        # print(res.get("value"))

        folderList = res.get("value")
        for i in range(len(folderList)):
            folder = folderList[i]
            if folder["name"] == folder_name:
                return {"folder_url": folder["webUrl"], "folder_id": folder["id"]}

        # if code continues, then there is no such folder, create new folder now
    else:
        print(
            f"Parent does not exist. Status Code: {response.status_code}, Error Message: {response.json()}"
        )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename",
    }

    url = f'{GRAPH_API_BASE_URL}/users/{user_id}/drive/items/{ parent_id if parent_id else "root"}/children'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        folder_metadata = response.json()
        folder_url = folder_metadata.get("webUrl")
        folder_id = folder_metadata.get("id")
        return {"folder_url": folder_url, "folder_id": folder_id}
    else:
        print(
            f"Failed to create folder. Status Code: {response.status_code}, Error Message: {response.json()}"
        )
        return


def create_folder(access_token, user_id, path):
    print(path)
    directories = path.split("/")
    parent_id = ""
    folder_url = ""

    try:
        for i in range(len(directories)):
            folderMeta = createNewOrGetDetails(
                access_token, user_id, directories[i], parent_id
            )
            parent_id = folderMeta.get("folder_id")
            folder_url = folderMeta.get("folder_url")
        print(f"Folder '{path}' created successfully.")
    except Exception as e:
        print(e)
    
    return {"folder_url": folder_url, "folder_id": parent_id}



def upload_file(access_token, user_id, parent_id, file_name, data):
    try:
        url = f'{GRAPH_API_BASE_URL}/users/{user_id}/drive/items/{ parent_id if parent_id else "root"}:/{file_name}:/content'
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/octet-stream",
        }
        response = requests.put(url, headers=headers, data=data)

        if response.status_code == 200:
            print("File upload successful.")
            return True
        elif response.status_code == 201:
            print("File created and uploaded successfully.")
            return True
        else:
            print(
                f"Failed to upload file. Status Code: {response.status_code}, Error Message: {response.json()}"
            )
            return False

    except Exception as e:
        print(e)
        return False
        
        

access_token = get_access_token()
user_id = " "  # Replace with the actual user ID    

def scrape_page_data(driver):
    time.sleep(10)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    links = soup.find_all("tr", attrs={"role": "row"})

    title_and_form_data = []

    for row in links:
        time.sleep(10)
        title_element = row.find(
            "span", attrs={"class": "x-grid3-cell-inner x-grid3-col-ReqTitle"}
        )
        if title_element:
            title = title_element.text
            print("\n")
            print(title)
            form = title_element.find("a").get("href")
            form = "https://vms.vectorvms.com/" + form

        id_element = row.find(
            "span", attrs={"class": "x-grid3-cell-inner x-grid3-col-ReqIDDisp"}
        )
        if id_element:
            ID = id_element.text
            print(ID)

        status_element = row.find(
            "span", attrs={"class": "x-grid3-cell-inner x-grid3-col-ReqStatus"}
        )
        if status_element:
            status = status_element.text
            print(status)

        client_element = row.find(
            "span", attrs={"class": "x-grid3-cell-inner x-grid3-col-Org"}
        )
        if client_element:
            client = client_element.text
            client = client.strip()
            print(client)
            client = client.replace("State of ", "") if client.startswith("State of ") else client
            company = title.replace('-', ' ')
            company = company.split(' ')
            company = list(filter(lambda c: len(c) > 0, company))
            companyName = company[0] if len(company[0]) > 2 else company[1]
            jobTitle = company[1:] if len(company[0]) > 2 else company[2:]
            jobTitle = " ".join(jobTitle)
            jobFolder = re.sub(r'[^\w\s-]', '', jobTitle)
            folderPath = f"CCI Operations 2023/Philippines Support 2023/USA/MSP-VMS/{client}/{companyName}/{jobFolder}"
            folderLink = create_folder(access_token, user_id, folderPath)
            folderId = folderLink.get("folder_id")
            folderLink = folderLink.get("folder_url")
            create_folder(access_token, user_id, f"{folderPath}/Candidates")
            create_folder(access_token, user_id, f"{folderPath}/Finals")
            create_folder(access_token, user_id, f"{folderPath}/Matrix")
            title_and_form_data.append(
                {
                    "Req Title": title,
                    "Form Link": form,
                    "Req ID": f'=HYPERLINK("{folderLink}","{ID}")',
                    "Req Status": status,
                    "Client": client,
                    "Company": companyName,
                    "Job Title": jobTitle,
                    "Folder Id": folderId
                }
            )

    return title_and_form_data

def get_data_from_iframe(name_list):
    value = "NA"
    try:
        for name in name_list:
            element_inside_iframe = wait.until(
                EC.presence_of_element_located(
                    (By.NAME, name)
                )
            )
            _value = element_inside_iframe.get_attribute("value")
            if _value:
                value = _value
                break
    except Exception as err:
        print(err)

    print(value)
    print("\n")

    return value

def get_data_from_iframe_by_tagname(tagname, text):
    value = "NA"
    element_inside_iframe = wait.until(
        EC.presence_of_all_elements_located(
            (By.TAG_NAME, tagname)
        )
    )
    try:
        for element in element_inside_iframe:
            if text.upper() in element.get_attribute("innerText").upper():
                value = get_data_from_iframe([element.get_attribute("for")])
                print(text)
                break
    except Exception as err:
        print(err)

    print(value)
    print("\n")

    return value


all_title_and_form_data = []
pages_fetched = 0

while pages_fetched < 1:
    current_page_data = scrape_page_data(driver)
    print(current_page_data)
    all_title_and_form_data.extend(current_page_data)

    pages_fetched += 1
    next_page = driver.find_elements(By.ID, "ext-comp-2507_btn")
    if len(next_page) == 0 or not next_page[0].is_enabled():
        break

    next_page[0].click()
    time.sleep(25)

counter = 0

for data in all_title_and_form_data:
    
    if counter > 15:
        break

    form_link = data["Form Link"]
    driver.get(form_link)
    #time.sleep(10)

    wait = WebDriverWait(driver, 20)
    
    str_1 = driver.print_page()
    # print(str)
    # _pdf = open(f"./{data['Req Title']}.pdf", 'wb')
    upload_file(access_token, user_id, data["Folder Id"], f"{data['Req Title']}.pdf", base64.b64decode(str_1))
    # _pdf.write(base64.b64decode(str))
    
    data.pop("Folder Id")
    
    
    iframe_element = wait.until(
        EC.presence_of_element_located((By.ID, "ContentPH_pnlDetail_IFrame"))
    )
    driver.switch_to.frame(iframe_element)
    
    # close date
    closing_date_arr = ["ContentPH_closed_date"]
    print("Closing Date")
    data["Closing Date"] = get_data_from_iframe(closing_date_arr)

    # start date
    start_date_arr = ["ContentPH_start_date"]
    print("Start Date")
    data["Start Date"] = get_data_from_iframe(start_date_arr)

    # end date
    end_date_arr = ["ContentPH_end_date"]
    print("End Date")
    data["End Date"] = get_data_from_iframe(end_date_arr)
    
    # work arrangement    
    data["Work Arrangement"] = get_data_from_iframe_by_tagname("label" ,"Work Arrangement:")
    print("Work Arrangement")
    
    # bill rate low amount
    bill_rate_low_arr = ["ContentPH_csBillFromRate_amount"]
    print("Bill Rate Low")
    data["Bill Rate Low"] = get_data_from_iframe(bill_rate_low_arr)
    
    # bill rate high amount
    bill_rate_high_arr = ["ContentPH_csBillToRate_amount"]
    print("Bill Rate High")
    data["Bill Rate High"] = get_data_from_iframe(bill_rate_high_arr)

    # Max pay rate
    bill_rate_high_arr = ["ContentPH_csMaxPayRate_amount"]
    print("Max Pay Rate")
    data["Max Pay Rate"] = get_data_from_iframe(bill_rate_high_arr)
    
    driver.switch_to.default_content()
    counter += 1


df = pd.DataFrame(all_title_and_form_data)

df.to_csv('VMS Data.csv', index=False, encoding='utf-8-sig')

