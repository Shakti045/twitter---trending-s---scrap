import os
import uuid
from datetime import datetime
import requests
import time
import uuid


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import pymongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB setup
mongodb_url = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(mongodb_url)
db = client["twitter_trends"]
collection = db["trends"]

def getTrendingTopics(inputs):
    try:
        options = Options()  
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.binary_location = "/usr/bin/google-chrome-stable"
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)
    
        USERNAME = inputs.get("username") if 'username' in inputs else os.getenv("TWITTER_USERNAME") 
        PASSWORD = inputs.get("password") if 'password' in inputs else os.getenv("TWITTER_PASSWORD")
        if not USERNAME or not PASSWORD:
            raise Exception("Twitter username or password not found.")
        # Twitter login URL
        url = "https://x.com/i/flow/login"
        driver.get(url)
        
        # Log in to Twitter
        username = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username.send_keys(USERNAME)
        username.send_keys(Keys.ENTER)
        
        password = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        
        # Wait for the home page to load
        time.sleep(10)
        
        # Fetch trending topics
        trends = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="css-175oi2r r-16y2uox r-bnwqim"]')))
        if not trends:
            raise TimeoutException
        top_trends = [trend.text for trend in trends[:5]]
        
        # Get current IP
        ip_response = requests.get("http://ip-api.com/json")
        ip_address = ip_response.json()["query"]
        
        # Store the data in MongoDB
        unique_id = str(uuid.uuid4())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "_id": unique_id,
            "trend1": top_trends[0].replace("\n", " - "),
            "trend2": top_trends[1].replace("\n", " - "),
            "trend3": top_trends[2].replace("\n", " - "),
            "trend4": top_trends[3].replace("\n", " - "),
            "trend5": top_trends[4].replace("\n", " - "),
            "end_time": end_time,
            "ip_address": ip_address
        }
        collection.insert_one(data)
        driver.quit()
        return data
    
    except TimeoutException:
        return {"error": "Timeout: Element not found. Check locator strategy or page load delays."}
        
    
    except NoSuchWindowException:
        return {"error": "NoSuchWindowException: Browser window closed unexpectedly."}
         
    
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    except:
        return {"error": "An unknown error occurred."}
            
