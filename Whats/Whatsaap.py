from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import os, time


import sys

from selenium.common.exceptions import NoSuchElementException


options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\raxo_\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Default')


driver = webdriver.Chrome(executable_path='C:\\Users\\raxo_\\Desktop\\Whats\\chromedriver.exe',
                          options=options)


driver.maximize_window()
driver.get("https://web.whatsapp.com/")
time.sleep(8)

celular = "525531043795"
mensaje2 ='''Hola bb 30 '''
mensaje ='''Hola, RDsolution esta a su servicio:
%0ADigite 1 para citas de instalación
%0ADigite 2 para soporte técnico
%0ADigite 3 para una cotización
%0ADigite 4 para baile privado'''

driver.get("https://wa.me/"+celular+"?text="+mensaje2)
time.sleep(7)

btn = driver.find_elements_by_xpath("//*[@id='action-button']")[0]
btn.click()
time.sleep(9)
btn = driver.find_elements_by_xpath("//*[@id='fallback_block']/div/div/a")[0]
btn.click()
time.sleep(13)

###

##  //*[@id="main"]/footer/div[1]/div[2]/div      CUADRO DE TEXTO
##  //*[@id="main"]/footer/div[1]/div[3]/button   BOTON DE ENVIAR
## //*[@id="main"]/footer/div[1]/div[2]/div/div[1]   texto dentro de codigo

###

#boton enviar                        //*[@id='main']/footer/div[1]/div[3]
btn = driver.find_elements_by_xpath("//*[@id='main']/footer/div[1]/div[3]")[0]
btn.click()
time.sleep(9)


message_box = driver.find_elements_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
TEXT="Hey, I am your whatsapp bot"
message_box.send_keys(TEXT)
time.sleep(9)
        # Click on send button
##message_box=driver.find_elements_by_xpath('//button[@class="_3M-N-"]')
##message_box.click()
##chrome_browser.close()


print("-- Fin de Bot--")


driver.close()
