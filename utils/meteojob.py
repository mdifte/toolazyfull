import time

from pynput.mouse import Button, Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pyautogui

    

def login(driver, mail,info,error):
    """Se connecter au site monster.fr"""
    info(f"Connexion avec {mail['mail']} sur www.meteojob.com")


    driver.get("https://www.meteojob.com/")
  

    try:
        cokie_btn=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/button[2]')))
        cokie_btn.click()
        time.sleep(10)
        mouse = Controller()
        mouse.position = (300, 400)
        mouse.click(Button.left, 2)
        time.sleep(5)
    except:
        pass
        

    login_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-sticky-container"]/div[3]/div/ul/li[1]/span')))
    login_btn.click()

    pyautogui.click(x=100, y=200)
    time.sleep(6)

    email_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
    email_input.send_keys(mail['mail'])
    time.sleep(3)
    driver.implicitly_wait(10)
    try:
        email_input.send_keys(Keys.ENTER)
    except:
        pass
    time.sleep(3)

    password_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    password_input.send_keys(mail['websites']['meteojob']['password'])
    time.sleep(3)

    password_input.send_keys(Keys.ENTER)

    time.sleep(10)


    try:
        account_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-test="accountNavigation"]')))
        return True
    except:
        return False


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
    """Effectuer une recherche"""
    driver.get(link)
    time.sleep(3)

    # Séléction des résultats de recherches

    jobs = []


    while True:
        #If the element is not visible, break the loop
        try:
            show_more_element_xpath = "//a[@href=\"#show-more\"]"
            show_more_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, show_more_element_xpath)))
        except TimeoutException:
            break

        try:
            #click on <a> tag with href="#show-more"
            driver.execute_script("document.querySelector('a[href=\"#show-more\"]').click()")
            time.sleep(3)
        except:
            pass


    #Find all <li> with role="treeitem"
    li_elements = driver.find_elements(By.XPATH, "//li[@role=\"treeitem\"]")

    for elem in li_elements:
        if "Candidature facile".lower() in elem.text.lower():
            try:
                job_id = elem.get_attribute('id').split("-")[-1]
                job_url = f"https://www.meteojob.com/jobs/meteo?oid={job_id}"
                jobs.append(job_url)
            except:
                continue


    return jobs


def postuler(driver, url,info,error):

    driver.get(url)


    #Find the button with cceventcategory="APPLY_OFFER" and cceventlabel="APPLICATION"
    try:
        apply_button_xpath = "//button[@cceventcategory=\"APPLY_OFFER\" and @cceventlabel=\"APPLICATION\"]"
        apply_button = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, apply_button_xpath)))

    except TimeoutException:
        return "Non Postulé"

    try:

        time.sleep(1)
        driver.implicitly_wait(10)
        try:
            #Find mat-checkbox with id contains mat-checkbox
            checkbox_xpath = "//mat-checkbox[contains(@id, \"mat-checkbox\")]"
            checkbox = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
            checkbox.click()
        except:
            pass

        time.sleep(1)

        apply_button_xpath = "//button[@cceventcategory=\"APPLY_OFFER\" and @cceventlabel=\"APPLICATION\"]"
        apply_button = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, apply_button_xpath)))
        apply_button.click()
        time.sleep(10)

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, apply_button_xpath)))
            return "Non Postulé"

        except:
            time.sleep(3)
            return "Postulé"

    except Exception as e:
        print(e)
        return "Non Postulé"
