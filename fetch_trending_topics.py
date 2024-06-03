from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

def getTrendingTopics(inputs):
    driver = None  # Initialize driver to None
    try:
        options = Options()  
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.binary_location = "/usr/bin/google-chrome-stable" 
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)

        driver.get("https://twitter.com/login")

        # Your logic to log in and fetch trending topics goes here

        # Mocking data for the example
        trending_topics = ["Trend1", "Trend2", "Trend3", "Trend4", "Trend5"]

        return {
            "trending_topics": trending_topics
        }

    except Exception as e:
        # Handle exception and ensure driver is quit
        print(f"Error occurred: {e}")
        raise
    finally:
        if driver:
            driver.quit()
