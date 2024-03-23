"""
importing necessary libraries
"""
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
    url = "https://www.girlandhair.com/collections/g-h-system"
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
    time.sleep(5)

    product_list = []
    data_list = {}
    i = 0
    while i < 3:
        items = browser.find_elements(By.XPATH, '//div[@class="grid-view-item--desc-wrapper"]//p[@class="product-grid--title"]/a')
        last_item = items[-1]
        browser.execute_script("arguments[0].scrollIntoView();", last_item)
        browser.implicitly_wait(10)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="grid-view-item--desc-wrapper"]//p[@class="product-grid--title"]/a')))
        # time.sleep(10)
        [product_list.append(item) for item in items if item not in product_list]
        i+=1
    
    home = browser.current_window_handle
    action = ActionChains(browser)
    product_brand = "girlandhair"

    for product in product_list:
        product_name = product.get_attribute('innerHTML')
        print(f"Getting data for {product_name}")
        product.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[-1])
        product_page = browser.current_window_handle
        print(browser.current_url)
        try:
            browser.execute_script("let element = getElementByClassName('needsclick klaviyo-form klaviyo-form-version-cid_1 kl-private-reset-css-Xuajs1');element.remove()")
        except JavascriptException:
            pass
        text = browser.find_element(By.XPATH, '//div[@id="accordion"]').get_attribute('innerHTML')
        soup = BeautifulSoup(text, 'html.parser')
        product_details = soup.find_all('p')
        product_desc = "".join(str((product_details[0]))).join(str((product_details[1])))
        product_ingredients = product_details[-4]
        product_directions = product_details[-2]
        print()
        print(product_desc)
        print()
        print(product_ingredients)
        print()
        print(product_directions)
        time.sleep(10)

        # show_reviews = browser.find_element(By.XPATH, '//div[@class="loox-float-toggler loox-floating-widget-btn"]')
        break
        browser.switch_to.window(home)
        time.sleep(10)
        

scrape()
