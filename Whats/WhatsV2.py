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

def new_chat(user_name):
    # Selecting the new chat search textbox
    new_chat = driver.find_element_by_xpath('//div[@class="ZP8RM"]')
    new_chat.click()

    # Enter the name of chat
    new_user = driver.find_element_by_xpath('//div[@class="_3u328 copyable-text selectable-text"]')
    new_user.send_keys(user_name)

    time.sleep(1)

    try:
        # Select for the title having user name
        user = driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user.click()
    except NoSuchElementException:
        print('No se encontro el numero "{}"'.format(user_name))
    except Exception as e:
        # Close the browser
        driver.close()
        print(e)
        sys.exit()
        
time.sleep(9)        
new_chat("5521934486")
name = input("Enter name or group name:")
msg = input("Enter message:")
count = int(input("Enter count:"))

input("Enter anything after scan QR code")

user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
user.click()

msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")

for index in range(count):
    msg_box.send_keys(msg)
    driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()

print("Success")

driver.close()
