# Author: Sam Shenoi
# Description: This file web scrapes from ACR to output a bunch of cases for training


from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def delete_cache(driver):
    driver.execute_script("window.open('')")  # Create a separate tab than the main one
    driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
    driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
    perform_actions(driver, Keys.TAB * 1  + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
    driver.close()  # Close that window
    driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.


def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(2)
    actions.perform()

driver = webdriver.Chrome()

driver.get('https://cortex.acr.org/CiP/Pages/OpenArchive')

driver.find_element(By.CLASS_NAME,"cookie-consent-accept-button").click()

elem = driver.find_element(By.ID,"subspecialtiesData")  # Find the search box
elem.click()

time.sleep(1.5)

btn = driver.find_element(By.ID,"btnSelectAll")
btn.click()

finish = driver.find_element(By.XPATH,'//*[@id="ModalitiesAndSubSpecalitypopup"]/div/div/div[3]/button[1]')
finish.click()

time.sleep(1.5)
driver.find_element(By.ID,"btnSearch").click()
time.sleep(1.5)


# Im cheating and using a magic number...

MAX_PAGE = 40
current_page = 1

while(current_page < MAX_PAGE):
    # Get the data from the table
    odds = driver.find_elements(By.CLASS_NAME, "odd")
    evens =  driver.find_elements(By.CLASS_NAME, "even")
    data = odds + evens

    out = open("acrcasesdata.csv",'w')
    out.write("Hx,Question\n")

    for i,d in enumerate(data):


        e = d.find_element(By.CLASS_NAME,"spn-rbt-history")
        hx = e.text

        d.find_element(By.CLASS_NAME,"redirect-history-diagnosis").click()
        time.sleep(2)

        p = driver.current_window_handle
        chwd = driver.window_handles

        for w in chwd:
            if(w!=p):
                driver.switch_to.window(w)
                break
        time.sleep(3)
        try:
            elem = driver.find_element(By.CLASS_NAME,"QuestionStem")
            question = elem.text
        except:
            question="None"
        driver.close()


        driver.switch_to.window(p)

        # Every 10 or so lets clear the cache so that it doesn't crash
        if i %10 ==0:
            delete_cache(driver)
            driver.find_element(By.CLASS_NAME,"cookie-consent-accept-button").click()

        out.write(f"{hx}\t{question}\n")


    # Clear the cache so we don't get "request to long errors"

    current_page = current_page + 1
    wrap = driver.find_element(By.ID,"tblActivity_wrapper")
    for elem in wrap.find_elements(By.CLASS_NAME, "paginate_button "):
        if elem.text == str(current_page):
            elem.click()
            break
    time.sleep(1.5)
out.close()

#time.sleep(4)
driver.quit()

