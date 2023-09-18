from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
import os
import time
import json
class Vita:

    # Specify the path to your ChromeDriver executable
    CHROMEDRIVER_PATH = "chromedriver-windows-x64.exe"

    def __init__(self, username:str, password:str, brand_name:str=None) -> None:
        """
        Argument: username and password
        """
        self.brand_name = brand_name
        self.username = username
        self.password = password
        # Configure ChromeOptions
        options = webdriver.ChromeOptions()
        # Create a Chrome WebDriver instance
        options.add_argument(fr'--user-data-dir={os.getcwd()}\user_data')
        service = ChromeService(executable_path=self.CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.vital.ly/signin/")

    

    def authenticate(self):
        if os.path.exists('cookies.pkl'):
            # Load the saved cookies from the pickle file
            with open('cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)

            # Loop through the list of cookies and add each one to the WebDriver
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.get_brand()
        else:
            username = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="login_user"]'))
            )
            password = self.driver.find_element(By.CSS_SELECTOR,'input[name="login_pass"]')
            username.send_keys(self.username)
            password.send_keys(self.password)

            #submit button login
            self.driver.find_element(By.XPATH,"//button[@type='submit' and contains(text(), 'Sign-in')]").click()

            cookies = self.driver.get_cookies()

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'span.header-name'))
            )
            self.get_cookies(cookies)


    def get_cookies(self,cookies):
        """Saving cookies"""
        cookies = self.driver.get_cookies()
        # Save the cookies to a pickle file for later use
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)

    def get_brand(self):
        # Initialize a dictionary to store text content and src attributes
        self.driver.get("https://www.vital.ly/brands/")
        data_dict = []
        if self.brand_name == "PB":
            row_data = self.driver.find_element(By.XPATH, '//div[@class="row right-border"]')
            for row in row_data.find_elements(By.XPATH, './div//a'):

            
            # Iterate through the <a> elements and extract the information
                text_content = row.text
                url = row.get_attribute("href")
                # Create a dictionary for the current <a> element
                a_data = {
                    "text_content": text_content,
                    "url": url
                }
                data_dict.append(a_data)
                # Save the data to a JSON file for each iteration
            with open('data.json', 'w', encoding='utf-8') as json_file:
                json.dump(data_dict, json_file, ensure_ascii=False)
        elif self.brand_name == "RB":
            row_data = self.driver.find_element(By.XPATH, '//div[@class="row hidden-xs right-border "]')
            for row in row_data.find_elements(By.XPATH,'./div//a'):
                # Iterate through the <a> elements and extract the information
                text_content = row.text
                url = row.get_attribute("href")
                # Create a dictionary for the current <a> element
                a_data = {
                    "brands": text_content,
                    "url": url
                }
                data_dict.append(a_data)
                # Save the data to a JSON file for each iteration
            # Save the entire list as a JSON file
            with open('retail_brand.json', 'w', encoding='utf-8') as json_file:
                json.dump(data_dict, json_file, ensure_ascii=False)

 
