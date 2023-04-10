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
        cokie_btn=WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/button[2]')))
        cokie_btn.click()
        time.sleep(20)
        mouse = Controller()
        mouse.position = (300, 400)
        mouse.click(Button.left, 2)
        time.sleep(10)
    except:
        pass
        

    login_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div/div[3]/div/ul/li[1]/a')))
    login_btn.click()
    pyautogui.click(x=100, y=200)
    time.sleep(6)

    email_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-signin/app-layout-funnel/cc-layout-funnel/cc-layout/main/div/main/div/cc-block/div/mat-tab-group/div/mat-tab-body[1]/div/div[1]/cc-candidate-signin/cc-candidate-signin-form/form/div[1]/div/mat-form-field/div/div[1]/div[4]/input')))
    email_input.send_keys(mail['mail'])
    time.sleep(5)

    ok_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-signin/app-layout-funnel/cc-layout-funnel/cc-layout/main/div/main/div/cc-block/div/mat-tab-group/div/mat-tab-body[1]/div/div[1]/cc-candidate-signin/cc-candidate-signin-form/form/div[1]/button')))
    ok_btn.click()
    time.sleep(5)

    password_input=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-signin/app-layout-funnel/cc-layout-funnel/cc-layout/main/div/main/div/cc-block/div/mat-tab-group/div/mat-tab-body[1]/div/div[1]/cc-candidate-signin/cc-candidate-signin-form/form/div[2]/div/mat-form-field/div/div[1]/div[4]/input')))
    password_input.send_keys(mail['websites']['meteojob']['password'])
    time.sleep(5)
  
    ok_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-signin/app-layout-funnel/cc-layout-funnel/cc-layout/main/div/main/div/cc-block/div/mat-tab-group/div/mat-tab-body[1]/div/div[1]/cc-candidate-signin/cc-candidate-signin-form/form/div[2]/button')))
    ok_btn.click()

    time.sleep(10)
    
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
    """Effectuer une recherche"""
    driver.get(link)
    time.sleep(3)

    # Séléction des résultats de recherches

    jobs = []
    
    try:

        while True and len(jobs):
            try:
                article=WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-meteo/app-criterias-on-top/app-layout-view/app-layout/cc-layout/main/div/aside/div/cc-block/div/div[2]/app-offer-list/ul'+str(index)+']')))
                link_=article.get_attribute('id')
                link_d=link+'#'+link_
                if 'job-offer' in link_d:
                    jobs.append(link_d)
            except:
                amount-=1

    except TimeoutException:
        return False

    return jobs


def postuler(driver, url,info,error):

    driver.get(url)

    try:
        a=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-search/app-layout-view/app-layout/cc-layout/main/div/main/div/div[2]/app-offer-view/app-offer/div/ng-scrollbar/div/div/div/div/cc-block[3]/div')))
    except TimeoutException:
        return "Non Postulé"

    try:
        cokie_btn=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/div/div/div/div[2]/button[2]')))
        cokie_btn.click()
    except:
        pass

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    try:

        time.sleep(1)

        try:
            toggle_btn=WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'd-inline-block align-middle ng-untouched ng-pristine ng-invalid')))
            driver.execute_script("arguments[0].click();",toggle_btn)
        except TimeoutException: 
            pass

        a=list(WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))))
        for btn in a:
            if btn.text=='POSTULER À CETTE OFFRE':

                action = ActionChains(driver)
                action.move_to_element(btn).perform()

                time.sleep(1)

                btn.click()

        try:
            
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-secondary')))
            return "Non Postulé"

        except:

            time.sleep(5)

            return "Postulé"

    except:
        return "Non Postulé"
