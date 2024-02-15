from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains



def scrape():
    """ this function returns the reviews of a product 
            Parameters:
                    None

            Returns:
                    reviews (list): the reviews along with their meta data
                    
    """
    url = "https://www.camillerose.com/collections/hair"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True,version_main=120)
    browser.get(url)
    time.sleep(2)
    views = []
    items = browser.find_elements(By.XPATH,'//div[@class="card "]/a')
    try:
        browser.execute_script("let element = document.getElementsByClassName('needsclick  kl-private-reset-css-Xuajs1');element[0].remove()")
        browser.execute_script("let element = document.getElementById('smile-ui-container');element.remove()")
    except JavascriptException:
        pass
    brand_name = "camille rose"
    main_browser = browser.current_window_handle
    for item in items:
        action = ActionChains(browser)
        try:
            browser.execute_script("let element = document.getElementsByClassName('needsclick  kl-private-reset-css-Xuajs1');element[0].remove()")
        except JavascriptException:
            pass
        time.sleep(2)
        try:
            browser.execute_script("document.getElementById('smile-ui-container').style.display='none';")
        except JavascriptException:
            pass
        action.move_to_element(item).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(2)
        product_name = browser.find_element(By.XPATH,'//div[@class="product-converter__title"]/div').text
        try:
            browser.execute_script("let element = document.getElementsByClassName('needsclick  kl-private-reset-css-Xuajs1');element[0].remove()")
            browser.execute_script("let element = document.getElementsById('smile-ui-container');element[0].remove()")
        except JavascriptException:
            pass
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        iframe = browser.find_element(By.ID,"roaReviewsIframe")
        browser.switch_to.frame(iframe)
        next_page = browser.find_elements(By.XPATH,'//div[@class="titania-159ouz7"]/button[2]')
        while len(next_page) > 0 and next_page[-1].is_enabled():
            try:
                browser.execute_script("let element = document.getElementsByClassName('needsclick  kl-private-reset-css-Xuajs1');element[0].remove()")
                browser.execute_script("let element = document.getElementsById('smile-ui-container');element[0].remove()")
            except JavascriptException:
                pass
            all_reviews = browser.find_elements(By.XPATH,".//div[@class='titania-1ank7hr-reviewWrapper']/div")
            if len(all_reviews) > 0:
                for review in all_reviews:
                    review_topic = review.find_element(By.CLASS_NAME,'titania-1oqpb4x').text
                    review_name = review.find_element(By.XPATH,'.//p[@class="titania-oshm15"]').text
                    date = review.find_element(By.CLASS_NAME,'titania-1if91g1').text
                    more = review.find_elements(By.CLASS_NAME,'titania-jcue9l-readMoreLessText')
                    if len(more) > 0:
                        browser.execute_script("arguments[0].click()", more[-1])
                    message = review.find_element(By.CLASS_NAME,'titania-2lt2bb').text
                    data = {
                        "brand": brand_name,
                        'product':product_name,
                        "review topic":review_topic,
                        "review author":review_name,
                        'date':date,
                        "message": message
                    }
                    views.append(data)
            try:
                browser.execute_script("let element = document.getElementsByClassName('needsclick  kl-private-reset-css-Xuajs1');element[0].remove()")
                browser.execute_script("let element = document.getElementsById('smile-ui-container');element[0].remove()")
            except JavascriptException:
                pass
            browser.execute_script("arguments[0].click()", next_page[-1])
            time.sleep(2)
            next_page = browser.find_elements(By.XPATH,'//div[@class="titania-159ouz7"]/button[2]')
        else:
            review = "no review"
            data = {
                "brand": brand_name,
                'product':product_name,
                "review topic":'',
                "review author":'',
                'date':'',
                "message": ''
            }
            views.append(data)
        browser.switch_to.default_content()
        browser.close()
        browser.switch_to.window(main_browser)
        time.sleep(2)
    return views

scrape()