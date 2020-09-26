from selenium import webdriver
import os, time




options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\raxo_\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Default')


driver = webdriver.Chrome(executable_path='C:\\Users\\raxo_\\Desktop\\Whats\\chromedriver.exe',
                          options=options)
driver.get("https://web.whatsapp.com/")
driver.maximize_window()

name = 'Ana'###USAR UNA COMILLA
msg = "Hola añu pupi pupi pu" 
count = 7000

user = driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")

user.send_keys(name)
time.sleep(2)

user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
user.click()
time.sleep(3)
msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
for index in range(count):
    msg_box.send_keys(msg)
    driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()

print("Success")

driver.close()
