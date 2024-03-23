"""
importing necessary libraries
"""

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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)
    time.sleep(5)
    action = ActionChains(browser)
    wait = WebDriverWait(browser, 10)
    data_list = {}
    
    try:
        product_list = []
        for i in range(1, 4):
            url = f"https://edenbodyworks.com/collections/eden-hair?page={i}"
            soup = BeautifulSoup(urlopen(url),'html.parser')
            products_links = soup.find_all('div',{"class":"card-wrapper"})
            links = [product.find('a') for product in products_links]
            [product_list.append(str(link).split('"')[3]) for link in links]
    except Exception as e:
        print(e)
    main_page = "https://edenbodyworks.com"
    for product_link in product_list:
        final_data = []
        link = main_page + product_link
        print()
        browser.get(link)
        print(browser.current_url)
        product_name = browser.find_element(By.XPATH, '//div[@class="product__title"]//h1').get_attribute("innerHTML").strip()
        print(f"getting data for {product_name}...")
        info = browser.find_elements(By.XPATH, '//accordion-tab[@class="product__accordion accordion"]')
        try:
            try:
                product_desc = info[0].get_attribute("innerHTML").split("</strong>")[1].split("<br")[0].strip()
            except IndexError:
                product_desc = info[0].get_attribute("innerHTML").split("<p>")[1].split("</p")[0].strip()
            except Exception:
                product_desc = ""
            product_directions = info[1].find_element(By.XPATH, '//span[@class="metafield-multi_line_text_field"]').get_attribute("innerHTML")
            product_ingredients = info[2].find_element(By.XPATH, './/p//span[@class="metafield-multi_line_text_field"]').get_attribute("innerHTML")
        # except IndexError:
        #     info = browser.find_element(By.XPATH, '//accordion-tab[@class="product__accordion accordion"]')
        #     details = info.find_elements(By.TAG_NAME, 'p')
        #     product_desc = details[0].get_attribute("innerHTML").strip()
        #     product_directions = details[1].get_attribute("innerHTML").strip()
        #     product_ingredients = details[2].get_attribute("innerHTML").strip()
        except IndexError:
            product_desc = ""
            product_directions = ""
            product_ingredients = ""

        product_data = {
                            "product_name": product_name,
                            "product_desc": product_desc,
                            "product_ingredients": product_ingredients,
                            "product_directions": product_directions
                        }
        print(product_data)
        
        show_more = browser.find_element(By.XPATH, './/div[@class="kl_reviews__load_more_button"]//button')
        count = int(int(browser.find_element(By.XPATH, '//div[@class="kl_reviews__list__tab_buttons"]//small').get_attribute("innerHTML").strip())/5)
        i = 0
        while i < count:
            try:
                wait = WebDriverWait(browser, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, './/div[@class="kl_reviews__load_more_button"]//button')))
                browser.implicitly_wait(10)
                action.click(show_more).perform()
                i += 1                
            except(NoSuchElementException):
                print("reviews loaded completely")
                break
            except Exception:
                traceback.print_exc()
                break
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="kl_reviews__review_item"]')))
        reviews = browser.find_elements(By.XPATH, './/div[@class="kl_reviews__review_item"]')
        for review in reviews:
            review_data = {}
            review_topic = review.find_element(By.XPATH, './/div[@class="kl_reviews__review__title"]').get_attribute('innerHTML')
            reviewer_name = review.find_element(By.XPATH, './/div[@class="kl_reviews__review__author"]//div').get_attribute('innerHTML')
            review_content = review.find_element(By.XPATH, './/p[@class="kl_reviews__review__content"]').get_attribute('innerHTML')
            review_date = review.find_element(By.XPATH, './/div[@class="kl_reviews__review__timestamp"]').get_attribute('innerHTML')
            rating_count = review.find_elements(By.CLASS_NAME, 'kl_reviews__full_star')
            review_rating = (len(rating_count))

            review_data["review_topic"] = review_topic
            review_data["reviewer_name"] = reviewer_name
            review_data["review_content"] = review_content
            review_data["review_date"] = review_date
            review_data["review_rating"] = review_rating
            print(review_data)
            final_data.append(review_data)
            
        data_list[product_data] = final_data

scrape()
