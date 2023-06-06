import pyperclip
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def getOneTimeLink(links_arr, amount_of_links):
    
    for iterations in range(amount_of_links+1):
        today = date.today()
        
        driver = webdriver.Chrome()
        
        driver.get("https://singleuse.link/")
        
        # Secret Message Box
        driver.find_element("id", "data").send_keys(f"CONFIRMED {today}")
        
        # Link Pass
        #driver.find_element("id", "inputPassword").send_keys("ha23")
        
        #Email Alert
        driver.find_element("id", 'inputEmail').send_keys(" ")
        
        #Drop down for link expirey
        grade_dropdown = Select(driver.find_element("id", "select"))
        grade_dropdown.select_by_visible_text("3 month")
        
        #Radio Button selection
        driver.find_element("id", 'optionsRadios1').click()
        
        #Create Button click
        driver.find_element("id", "createbtn2").click()
        
        #Copy to CLipboard
        driver.find_element(By.XPATH, "/html/body/div[2]/button").click();
        
        link = pyperclip.paste()
        
        links_arr.append(link)
        
        print(iterations)
        
        driver.close()
        
    return links_arr;
