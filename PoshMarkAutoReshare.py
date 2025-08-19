from selenium import webdriver
import time
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
actions = ActionChains(driver)
def PoshLogin(): 
    loginUrl = 'https://poshmark.com/login'
    driver.get(loginUrl)

    driver.implicitly_wait(2)

    driver.find_element(By.NAME, value="login_form[username_email]").clear()
    driver.find_element(By.NAME, value="login_form[password]").clear()

    UsernameOrEmail = driver.find_element(by=By.NAME, value="login_form[username_email]")
    Password = driver.find_element(by=By.NAME, value="login_form[password]")

    UsernameOrEmail.send_keys("[Email Address Here]")
    Password.send_keys("[Password Here]")

    driver.find_element(By.CLASS_NAME, "btn--primary").click()
    driver.implicitly_wait(10)

 
def load_all_listings():
    scroll_pause_time = 10
    # These elements go to your closet
    driver.find_element(By.XPATH, '//*[@id="app"]/header/nav[1]/div/ul/li[5]/div').click()
    driver.find_element(By.XPATH,'//*[@id="app"]/header/nav[1]/div/ul/li[5]/div/div[2]/div/ul/li[1]').click()
    
    try:
        time.sleep(.5)
        driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div[2]/div[1]/button').click()  
        print("close pop-up")
    except:
        print(" didn't find pop-up of closet beta thing")

    # this element is to find the Available Items button and click it
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/div/div[2]/nav/div/div[9]/div/div[2]/ul/li[2]/div/label/div').click()
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for new content to load, TODO make this dynamic based on page response
        time.sleep(1.5)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def share_to_followers(share_btn):
    actions.move_to_element(share_btn).perform() 
    try:
        time.sleep(.7)
        share_btn.click()
        to_my_followers = driver.find_element(By.CLASS_NAME,"share-wrapper-container")
        to_my_followers.click()     
    except Exception as e:
        print(f"captcha block {e}") 
    time.sleep(.2)

def share_listings(share_buttons):
    print("There are: ", len(share_buttons), " listings")
    i = 0 
    for share_btn in share_buttons:
        share_to_followers(share_btn)
        i += 1
        print("Shared Listing: #", i)
  
if __name__ == '__main__':
    PoshLogin()
    load_all_listings()
    share_buttons = driver.find_elements(By.XPATH, '//div[@data-et-name="share"]')
    share_listings(share_buttons)
    driver.close()
