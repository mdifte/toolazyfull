import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys


def login(driver, mail,info,error):
    """Se connecter au site monster.fr"""
    info(f"Connexion avec {mail['mail']} sur www.hellowork.com")

    driver.get("https://www.hellowork.com/fr-fr")

    try:
        cokie_btn=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div/div[2]/button[2]')))
        cokie_btn.click()
    except:
        pass

    try:
        section=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div')))
        section.click()

        france_=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/ul/li[70]')))
        france_.click()

        ok_btn=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/button')))
        ok_btn.click()

        time.sleep(10)

    except:
        pass

    login_btn=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/header/nav/ul/li[6]/details/summary')))
    login_btn.click()

    login_btn=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/header/nav/ul/li[6]/details/div/ul/li[1]/span/span[1]')))
    login_btn.click()

    email_input=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'email2')))
    password_input=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'password2')))

    email_input.send_keys(mail['mail'])
    password_input.send_keys(mail['websites']['hellowork']['password'])

    time.sleep(5)

    submit_btn=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section/div[2]/section/button')))
    submit_btn.click()
    time.sleep(10)
    
    return True

def logout(driver,info,error):
    time.sleep(1)
    info("Déconnexion")
    try:
        menu_button = driver.find_element(By.XPATH,"/html/body/div[4]/header/nav/ul/li[5]/details/summary/span[2]")
        menu_button.click()
        logout_button = driver.find_element(By.XPATH,"/html/body/div[4]/header/nav/ul/li[5]/details/div/ul/li[7]/span")
        logout_button.click()
    except:
        driver.delete_all_cookies()
        driver.refresh()
    time.sleep(1)


def recherche(driver, link,info,error):
    """Effectuer une recherche"""
    time.sleep(3)
    driver.get(link)
    time.sleep(3)

    try:
        cokie_btn=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div/div/div/div[2]/button[2]')))
        cokie_btn.click()
    except:
        pass

    # Séléction des résultats de recherches

    jobs = []
    op=0

    try:

        while True:
            try:
                op+=1
                frame=WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/section[1]/div/section/ul[1]')))
                
                cards=list(frame.find_elements(By.TAG_NAME, 'div'))
                break
            except:
                if op==7:
                    error('Couldnt get jobs!')
                    return []

        for card in cards:
            id=card.get_attribute('id')
            if card.get_attribute('data-for') and id!='' and id!='infos':
                jobs.append(jobs.append('https://www.hellowork.com/fr-fr/emplois/'+id+'.html'))

    except TimeoutException:
        return []

    return jobs


def postuler(driver, url,info,error,mail):
    """Postuler pour un job"""

    driver.get(url)

    try:

        try:
            cokie_btn=WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div/div/div/div[2]/button[2]')))
            cokie_btn.click()
        except:
            pass

        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass

        # Si le le formulaire est sur le site www.welcometothejungle.com

        try:     

            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/section[2]/a'))).click()
            time.sleep(2)

            submit_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "progress-content")))
            submit_button.click()
            time.sleep(4)
            return "Postulé"

        except TimeoutException:

            return "Non postulé"

    except:
        return "Non postulé"
