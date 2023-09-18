from app import Vita
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
import os
import time
import json

class Product(Vita):
    
    def __init__(self, username: str, password: str, brand_name: str) -> None:
        super().__init__(username, password, brand_name)



    def get_product(self, file_path:str):
        self.authenticate()
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        brand_products = {}
        for dict_value in data:
            self.driver.get(dict_value['url'])
            while True:
                try:
                    load_more = WebDriverWait(self.driver,5).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@id="loadall"]')))
                    load_more.click()
                except:
                    # Simulate pressing the down arrow key in a loop
                    body_element = self.driver.find_element(By.TAG_NAME,"body")
                    body_element.send_keys(Keys.ARROW_DOWN)
                    time.sleep(1)  # Optional: Add a delay between key presses
                    break
            products = WebDriverWait(self.driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH,'//div[@class="name pb5 hidden-xs hidden-sm"]//a'))
            )  
            for product in products:
                # Open a new tab using JavaScript
                self.driver.execute_script(f"window.open('{product.get_attribute('href')}', '_blank');")
                # Switch to the new tab (the last tab in the list)
                window_handles = self.driver.window_handles
                new_tab_handle = window_handles[-1]
                self.driver.switch_to.window(new_tab_handle)
                product_title = WebDriverWait(self.driver,500).until(
                    EC.presence_of_element_located((By.XPATH,'//div[@class="name hidden-xs hidden-sm pb5"]//a'))
                )

                try:
                    title_product = product_title.text
                    try:
                        product_description = self.driver.find_element(By.XPATH,'//div[@class="product-callout"]//p').text
                    except:
                        pass
                    try:
                        product_price = self.driver.find_element(By.CSS_SELECTOR,'span.big').text
                    except:
                        pass
                    try:
                        product_price_strike = self.driver.find_element(By.CSS_SELECTOR,'font.rrp-strikethrough').text
                    except:
                        pass

                    try:
                        delivery_info_url = self.driver.find_element(By.XPATH,'//div[@class="product-delivery hidden-xs"]//a').get_attribute('href')
                    except:
                        pass
                    try:
                        product_delivery_prices = [element.text for element in self.driver.find_elements(By.XPATH,'//div[@class="product-delivery hidden-xs"]//ul//li')]
                    except:
                        pass
                    try:
                        product_summary = """
                            const productSummary = document.querySelector('div.product-summary');
                            const childElements = productSummary.children;
                            let concatenatedText = "";
                            let remainingText = ""; // Initialize a variable to store the remaining text

                            for (let i = 0; i < childElements.length; i++) {
                            if (i !== 0) { // Skip the first iteration
                                concatenatedText += childElements[i].textContent + " ";
                                
                                // Check if the text contains "Ingredients:"
                                if (childElements[i].textContent.includes("Ingredients:")) {
                                // Get the index of "Ingredients:"
                                const index = childElements[i].textContent.indexOf("Ingredients:");
                                
                                // Extract the text before "Ingredients:" and assign it to remainingText
                                remainingText = childElements[i].textContent.substring(0, index);
                                
                                // Stop the loop, as we have found "Ingredients:"
                                break;
                                }
                            }
                            }

                            if (remainingText === "") {
                            return concatenatedText
                            } else {
                            return remainingText; // Print the remaining text after removing "Ingredients:" if "Ingredients:" was found
                            }

                        """
                        product_summary = self.driver.execute_script(product_summary)
                        print(product_summary)
                    except:
                        pass
                    try:
                        product_ingredients = """const productSummary = document.querySelector('div.product-summary');
                        const childElements = productSummary.children;
                        let concatenatedText = "";
                        let remainingText = ""; // Initialize a variable to store the remaining text

                        for (let i = 0; i < childElements.length; i++) {
                        if (i !== 0) { // Skip the first iteration
                            concatenatedText += childElements[i].textContent + " ";
                            
                            // Check if the text contains "Ingredients:"
                            if (childElements[i].textContent.includes("Ingredients:")) {
                            // Get the index of "Ingredients:"
                            const index = childElements[i].textContent.indexOf("Ingredients:");
                            
                            // Extract the text after "Ingredients:" and assign it to remainingText
                            remainingText = childElements[i].textContent.substring(index + "Ingredients:".length);
                            
                            // Stop the loop, as we have found "Ingredients:"
                            break;
                            }
                        }
                        }


                        return remainingText; // Print the remaining text after "Ingredients:" if "Ingredients:" was found

                        """
                        ingredients = self.driver.execute_script(product_ingredients)
                        print(ingredients)
                    except:
                        pass
                    try:
                        formula = """// Select all table elements on the page
                        const tables = document.querySelectorAll('table');

                        // Initialize an empty string to store the combined table content
                        let combinedTableContent = '';

                        // Loop through each table
                        tables.forEach(table => {
                        // Loop through the rows in the current table
                        const tbody = table.querySelector('tbody');
                        if (tbody) {
                            const rows = tbody.querySelectorAll('tr');
                            rows.forEach(row => {
                            const cells = row.querySelectorAll('td');
                            const rowContent = Array.from(cells).map(cell => cell.textContent.trim()).join(', ');
                            combinedTableContent += rowContent + '\n'; // Append the row content with a newline character
                            });
                        }
                        });

                        console.log(combinedTableContent);
                        """
                    except:
                        pass
                except:
                    pass



                
   


if __name__== "__main__":
    product.get_product('retail_brand.json')



                



