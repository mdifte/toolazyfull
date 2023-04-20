import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys


def login(driver, mail,info,error):
    """Se connecter au site monster.fr"""
    info(f"Connexion avec {mail['mail']} sur www.monster.fr")
    try:
        driver.get("https://www.monster.fr/profile/detail")
        time.sleep(5)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'email')))

        email_input = driver.find_element(By.NAME,"email")
        email_input.send_keys(mail['mail'])
        password_input = driver.find_element(By.NAME,"password")
        password_input.send_keys(mail['websites']['monster']['password'])
        time.sleep(1)
        password_input.send_keys(Keys.ENTER)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Se déconnecter"]')))
        return True
    except TimeoutException:
        return False
    except WebDriverException:
        return False


def logout(driver,info,error):
    "Deconnexion"
    time.sleep(1)
    info("Déconnexion")
    driver.get("https://www.monster.fr/profile/detail")
    try:
        logout_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Se déconnecter"]')))
        driver.execute_script("arguments[0].click();", logout_button)
    except TimeoutException:
        driver.delete_all_cookies()


def recherche(driver, link,info,error):
    """Effectuer une recherche"""
    driver.get(link)
    time.sleep(5)

    # Cookies
    try:
        cookie_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
    except TimeoutException:
        pass

    # Séléction des résultats de recherches
    print("Séléction des résultats de recherches")
    try:
        jobs_selector = 'article[data-testid="svx_jobCard"]'
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, jobs_selector)))
        cards = driver.find_elements(By.CSS_SELECTOR, jobs_selector)
        print(f"{len(cards)} résultats trouvés")
    except TimeoutException:
        return False

    jobs = []
    try:
        cookie_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
    except TimeoutException:
        pass
    for card in cards:
        try:
            # Check if it's an on site apply job (Quick Apply)
            button_text = card.find_element(By.CSS_SELECTOR, 'button[data-testid="svx-job-apply-button"]').text

            if 'rapide' not in button_text.lower():
                continue

            jobs.append(card.get_attribute("data-job-id"))
        except NoSuchElementException:
            continue

    print(jobs)

    return jobs


def postuler(driver,job, link,info,error,mail):
    try:
        div = driver.find_element(By.CSS_SELECTOR, f'[data-job-id="{job}"]')
    except:
        return "Job non trouvé"

    try:
        # apply_button = div.find_element_by_css_selector('button[data-testid="svx-job-apply-button"]') Depreciated
        apply_button = div.find_element(By.CSS_SELECTOR, 'button[data-testid="svx-job-apply-button"]')
        driver.execute_script("arguments[0].click();", apply_button)
        # apply_button.click()
    except NoSuchElementException:
        return "Non postulé"

    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            break
        except:
            pass

    try:

        gender_input=WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/main/form[1]/div/div/div[3]/div[4]/div/div/div[3]/div[1]/div/div[2]/input")))
        gender_input.click()
        gender_select=WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/main/form[1]/div/div/div[3]/div[4]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[3]/ul/li[1]")))
        gender_select.click()

        ethnicity_input=WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/main/form[1]/div/div/div[3]/div[4]/div/div/div[3]/div[2]/div/div[2]/input")))
        ethnicity_input.click()
        ethnicity_select=WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/main/form[1]/div/div/div[3]/div[4]/div/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/ul/li[1]")))
        ethnicity_select.click()

        submit_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/main/form[1]/div/div/div[3]/div[5]/div/button")))
        submit_button.click()
    except:
        pass

    return_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/button")))
    return_btn.click()

    driver.switch_to.window(driver.window_handles[0])

    return "Postulé"
