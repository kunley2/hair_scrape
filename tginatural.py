"""
importing necessary libraries
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
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
import traceback
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrape():
    url = "https://tginatural.com/product-category/hair/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)

    try:
        page_products = []
        for i in range(1, 5):
            url = f"https://tginatural.com/product-category/hair/page/{i}"
            soup = BeautifulSoup(urlopen(url),'html.parser')
            products_links = soup.find_all('div',{"class":"nr-details"})
            links = [product.find('a') for product in products_links]
            [page_products.append(str(link).split('"')[3]) for link in links]
        print(len(page_products))
        data_list = {}
        product_brand = "tgin"
        i = 1
        for product_link in page_products:
            print()
            print(i)
            browser.get(product_link)
            time.sleep(5)
            final_data = []
            print(browser.current_url)
            product_page = browser.current_window_handle
            product_name = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//h1').text
            print(f"getting data for {product_name}...")
            if "Green Tea Super Moist Leave in Conditioner" in product_name:
                info = browser.find_element(By.XPATH, '//div[@class="product-info-content-column"]//div[@class="inner"]')
                product_desc = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//p').text
                product_directions = info.find_elements(By.TAG_NAME, 'p')[4].get_attribute("innerHTML").split("</span>")[1]
                product_ingredients = info.find_elements(By.TAG_NAME, 'p')[5].get_attribute("innerHTML").split("</span>")[1]
            else:
                info = browser.find_element(By.XPATH, '//div[@class="product-info-content-column"]//div[@class="inner"]')
                product_desc = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//p').text
                product_ingredients = info.find_elements(By.TAG_NAME, 'p')[3].get_attribute("innerHTML").split("</strong>")[1]
                try:
                    product_directions = info.find_elements(By.TAG_NAME, 'p')[2].get_attribute("innerHTML").split("</strong>")[1]
                except IndexError:
                    product_directions = info.find_elements(By.TAG_NAME, 'p')[2].get_attribute("innerHTML").split("</b>")[1]
                except Exception:
                    product_directions = ""
            reviews_button = browser.find_element(By.XPATH, '//button[@id="tab-3"]')
            browser.implicitly_wait(10)
            ActionChains(browser).move_to_element(reviews_button).click(reviews_button).perform()
            time.sleep(5)
            while product_page:
                try:
                    wait = WebDriverWait(browser, 10)
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="stamped-reviews"]//div[@class="stamped-review"]')))
                    reviews = browser.find_elements(By.XPATH, './/div[@class="stamped-reviews"]//div[@class="stamped-review"]')
                    for review in reviews:
                        header = review.find_element(By.XPATH, './/div[@class="stamped-review-header"]')
                        content = review.find_element(By.XPATH, './/div[@class="stamped-review-content"]')
                        review_topic = content.find_element(By.XPATH, './/h3').get_attribute('innerHTML')
                        reviewer_name = header.find_element(By.XPATH, './/strong[@class="author"]').get_attribute('innerHTML')
                        review_content = content.find_element(By.XPATH, './/p[@class="stamped-review-content-body"]').get_attribute('innerHTML')
                        review_date = header.find_element(By.XPATH, './/div[@class="created"]').get_attribute('innerHTML')
                        review_rating = str(content.find_element(By.XPATH, './/span').get_attribute("outerHTML").split(" ")[4]).split("=")[-1].split('"')[1].split('"')[0]
                        # break
                        data = {
                                'product_brand': product_brand,
                                'product_name': product_name,
                                'product_ingredients': product_ingredients,
                                'product_desc': product_desc,
                                'product_directions': product_directions,
                                'reviewer_name': reviewer_name,
                                'review_topic': review_topic,
                                'review_comment': review_content,
                                'review_date': review_date,
                                'review_rating': review_rating

                                }
                        if data not in final_data:
                            final_data.append(data)
                    wait = WebDriverWait(browser, 10, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="next"]/a')))
                    browser.implicitly_wait(10)
                    ActionChains(browser).move_to_element(reviews_button).click(reviews_button).perform()
                    next_rev_page = browser.find_element(By.XPATH, '//li[@class="next"]/a')
                    print(next_rev_page.get_attribute('outerHTML'))
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="next"]/a')))
                    browser.implicitly_wait(10)
                    next_rev_page.click()
                    time.sleep(5)
                except (NoSuchElementException, TimeoutException):
                    print("Last Review Page")
                    print()
                    break
            try:
                print(final_data)
                print()
                print()
            except UnicodeEncodeError:
                print(str(final_data).encode('cp1252', errors='ignore'))

            data_list[product_name] = final_data
            i += 1

    except(NoSuchElementException, StaleElementReferenceException):
            print("Last Product")
    except Exception as error:
        print(error)
        traceback.print_exc()

    browser.quit()

scrape()