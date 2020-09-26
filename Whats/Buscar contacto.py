# comenta
from selenium import webdriver
import sys
import time

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\raxo_\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Default')


driver = webdriver.Chrome(executable_path='C:\\Users\\raxo_\\Desktop\\Whats\\chromedriver.exe',
                          options=options)
driver.get("https://web.whatsapp.com/")
driver.maximize_window()

time.sleep(9)

user = driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")
user.send_keys('Gus')
time.sleep(4)




print("Success")

driver.close()
