import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def login(driver, mail,info,error):
    """Se connecter au site monster.fr"""
    info(f"Connexion avec {mail['mail']} sur www.indeed.com")

    driver.get("https://www.indeed.com/")

    try:
        cokie_btn=WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/button[2]')))
        cokie_btn.click()
    except:
        pass

    login_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/nav/div/div/div[2]/div[2]')))
    login_btn.click()

    time.sleep(2)

    email_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div/span/input')))
    email_input.send_keys(mail['mail'])
    email_input.send_keys(Keys.ENTER)

    try:
        cokie_btn=WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/a')))
        cokie_btn.click()
    except:
        pass

    password_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/span/input')))
    password_input.send_keys(mail['websites']['indeed']['password'])
    password_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/nav/div/div/div[2]/div[2]/div/div/button')))
    
    time.sleep(4)
    
    return True

def logout(driver,info,error):
    time.sleep(1)
    info("Déconnexion")
    try:
        menu_button = driver.find_element(By.XPATH,"/html/body/app-root/app-meteo/app-layout-view/app-layout/cc-layout/cc-candidate-header/cc-meteojob-candidate-header/header/div/div[2]/ul/li[6]/cc-header-link/div/a")
        menu_button.click()
        logout_button = driver.find_element(By.XPATH,"/html/body/app-root/app-meteo/app-layout-view/app-layout/cc-layout/cc-candidate-header/cc-meteojob-candidate-header/header/div/div[2]/ul/li[6]/cc-header-link/div/div/cc-header-link[4]/a")
        logout_button.click()
    except:
        driver.delete_all_cookies()
        driver.refresh()
    time.sleep(1)


def recherche(driver, link,info,error):

    driver.get(link)
    time.sleep(3)

    amount=35
    index=0

    jobs = []

    frame = driver.find_element(By.CLASS_NAME,"jobsearch-ResultsList css-0")

    try:

        cards=list(frame.find_elements(By.TAG_NAME, 'span'))
        for card in cards:
            jobs.append(link+"&vjk="+card.get_attribute('id').replace('jobTitle-',''))

    except TimeoutException:
        return False

    return jobs


def postuler(driver, url,info,error):

    driver.get(url)

    current_window = driver.current_window_handle

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    try:
        button=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="indeedApplyButton"]')))
        button.click()

        select=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[2]/div/button')))
        select.click()

        select=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[1]/div[1]/div/fieldset/label[3]/span[1]')))
        select.click()
        
        select=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[1]/div[2]/div/fieldset/label[2]/span[1]')))
        select.click()
        
        select=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[1]/div[3]/div/fieldset/label[1]/span[1]')))
        select.click()

        button=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[2]/div/button')))
        button.click()

        button=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div/div[2]/div/button')))
        button.click()
        button=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/main/div[5]/button')))
        button.click()
        time.sleep(2)

        for handle in driver.window_handles:
            if driver.switch_to.window(handle) != current_window:
                driver.close()

        return "Postulé"
    except TimeoutException:
        return "Non Postulé"