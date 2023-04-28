import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys


def login(driver, mail,info,error):
    """Se connecter au site monster.fr"""
    info(f"Connexion avec {mail['mail']} sur www.emploi.lefigaro.fr")

    driver.get("https://emploi.lefigaro.fr/")

    try:
        frame= WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/iframe')))
        driver.switch_to.frame(frame)
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div/div[2]/aside/section/button[1]'))).click()

        driver.switch_to.default_content()
    except:
        pass

    a=list(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))))
    for btn in a:
        if btn.text=='Mon compte Figaro Emploi':
            btn.click()

    email_input=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-email"]')))
    password_input=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-password"]')))

    email_input.send_keys(mail['mail'])
    password_input.send_keys(mail['websites']['lefigaro']['password'])

    time.sleep(1)
    password_input.send_keys(Keys.ENTER)
    time.sleep(10)

    #If password_input is still here, it means that the login failed, return False
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-password"]')))
        return False
    except:
        pass

    return True

def logout(driver,info,error):
    time.sleep(1)
    info("Déconnexion")
    try:
        menu_button = driver.find_element(By.CSS_SELECTOR,"i.sc-kmASHI.inkvsG")
        driver.execute_script("arguments[0].click();", menu_button)
        logout_button = driver.find_element(By.NAME,"log_out")
        driver.execute_script("arguments[0].click();", logout_button)
    except:
        driver.delete_all_cookies()
        driver.refresh()
    time.sleep(1)


def recherche(driver, link,info,error):
    """Effectuer une recherche"""
    driver.get(link)
    time.sleep(3)

    # Séléction des résultats de recherches
    try:
        frame=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "job-search--bottom--body--items")))

        cards=list(frame.find_elements(By.TAG_NAME, 'a'))

    except TimeoutException:
        return False

    jobs = []

    for card in cards:
        try:
            jobs.append(card.get_attribute('href'))

        except:
            continue

    return jobs


def postuler(driver, url,info,error,mail):
    """Postuler pour un job"""
    driver.get(url)
    try:

        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
            time.sleep(10)
        try:
            apply_button = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div/div[2]/button")))
        except TimeoutException as tex:
            apply_button = None

        # Si le le formulaire est sur le site www.welcometothejungle.com
        if apply_button:
            apply_button.click()

            cover_letter = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/div/div[2]/div[2]/textarea")))
            cover_letter.clear()
            cover_letter.send_keys(mail['websites']['lefigaro']['letter'])

            submit_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "applyButton")))
            submit_button.click()

            try:
                time.sleep(3)
                return "Postulé"
            except TimeoutException:
                return "Non postulé"
            # time.sleep(1)
        else:
            return "Non postulé"

    except:
        return "Non postulé"
