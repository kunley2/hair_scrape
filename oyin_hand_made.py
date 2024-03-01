"""
importing necessary libraries
"""
import requests
# import pandas as pd
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
import time
from selenium.webdriver.common.action_chains import ActionChains 

def scrape():
    url = "https://oyinhandmade.com/hair/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)
    browser.get(url)
    time.sleep(10)

    try:
        browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
        browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
    except JavascriptException:
        pass

    product_list = []
    data_list = {}
    i = 0
    while i < 4:
        items = browser.find_elements(By.XPATH, '//h4[@class="card-title"]/a')
        last_item = items[-1]
        browser.execute_script("arguments[0].scrollIntoView();", last_item)
        wait = WebDriverWait(browser, 10)      
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h4[@class="card-title"]/a')))
        time.sleep(20)
        [product_list.append(item) for item in items if item not in product_list]        
        i+=1

    home = browser.current_window_handle
    action = ActionChains(browser)
    product_brand = "oyin_hand_made"
    # product = product_list[0]
    for product in product_list:
        prod_name = product.get_attribute('innerHTML')
        print(f"Getting data for {product.get_attribute('innerHTML')}")
        time.sleep(5)
        try:
            browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
        except JavascriptException:
            pass
        time.sleep(2)
        try:
            browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
        except JavascriptException:
            pass
        time.sleep(5)
        product.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(10)
        browser.switch_to.window(browser.window_handles[1])
        product_page = browser.current_window_handle
        product_name = browser.find_element(By.XPATH,'//h1[@class="productView-title"]').text.strip()
        product_ingredients = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfKeyIngredients"]').text.strip()
        product_function = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfWhatItDoes"]').text.strip()
        time.sleep(5)
        next_page = browser.find_element(By.XPATH, '//li[@class="pagination-item pagination-item--next"]//a[@class="pagination-link"]') 
        time.sleep(5)
        # reviews = browser.find_elements(By.XPATH,'//li[@class="productReview"]/article')
        final_data = []
        while next_page:
            print(browser.current_url)
            browser.refresh()
            time.sleep(10)
            try:
                    browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
            except JavascriptException:
                    pass
            time.sleep(2)
            try:
                    browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
            except JavascriptException:
                    pass
            time.sleep(5)        
            try:
                reviews = browser.find_elements(By.XPATH,'//li[@class="productReview"]/article')
                if len(reviews) > 0:
                        for review in reviews:
                            reviewer_name = review.find_element(By.TAG_NAME, 'header').find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
                            review_topic = review.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'h5').get_attribute('innerHTML')
                            review_comment = review.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'p').get_attribute('innerHTML')
                            review_date = review.find_element(By.CLASS_NAME, "productReview-author").get_attribute('innerHTML').split("-")[1].strip()
                            review_rating = review.find_element(By.TAG_NAME, 'header').find_element(By.XPATH, './/span[@class="productReview-rating rating--small"]//span[@class="productReview-ratingNumber"]').get_attribute("innerHTML")
                            
                            data = {
                                'product_brand': product_brand,
                                'product_name': product_name,
                                'product_ingredients': product_ingredients,
                                'product_function': product_function,
                                'review_topic': review_topic,
                                'reviewer_name': reviewer_name,
                                'review_comment': review_comment,
                                'review_date': review_date,
                                'review_rating': review_rating 

                            } 
                            # print(data)
                            # print()
                            final_data.append(data)
                            time.sleep(5)
                wait = WebDriverWait(browser, 10, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))      
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="pagination-item pagination-item--next"]//a[@class="pagination-link"]')))
                next_page = browser.find_element(By.XPATH, '//li[@class="pagination-item pagination-item--next"]//a[@class="pagination-link"]') 
                time.sleep(5)
                next_page.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(10)
                
            except (NoSuchElementException, TimeoutException):
                review = "No review"
                data = {
                            'product_brand': product_brand,
                            'product_name': product_name,
                            'product_ingredients': product_ingredients,
                            'product_function': product_function,
                            'review_topic': "",
                            'reviewer_name': "",
                            'review_comment': "",
                            'review_date': "",
                            'review_rating': ""
                    }
                final_data.append(data)
                next_page = False
                    
        else:
            data_list[prod_name] = final_data
            print(f"Reviews for {prod_name} successfully saved")
            print()
        time.sleep(10)
        browser.close()
        browser.switch_to.window(home)
        time.sleep(10)
    
    return data_list


if __name__ == '__main__':
     data = scrape()
     print(data)
     
     


