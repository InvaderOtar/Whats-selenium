from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\raxo_\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Default')


driver = webdriver.Chrome(executable_path='C:\\Users\\raxo_\\Desktop\\Whats\\chromedriver.exe',
                          options=options)

# Navega a la URL

driver.get("http://www.google.com")

# Inserta el texto "Webdriver" y ejecuta la accion del teclado "ENTER"

driver.find_element(By.NAME, "q").send_keys("Star wars" + Keys.ENTER)
  
