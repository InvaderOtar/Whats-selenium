from selenium import webdriver
import time
import os, time


options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\raxo_\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Default')


driver = webdriver.Chrome(executable_path='C:\\Users\\raxo_\\Desktop\\Whats\\chromedriver.exe',
                          options=options)



driver.get("https://web.whatsapp.com/")
time.sleep(10)


nombre='505'

user= driver.find_element_by_xpath('//span[@title="{}"]'.format(nombre))

user.click()

