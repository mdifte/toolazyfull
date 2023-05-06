from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from urllib.parse import urlparse, parse_qs
import pickle
import os, inspect
from . import hellowork, keljob, lefigaro,meteojob,monster,welcometothejungle, indeed
from email_config import gmail_sender_account,gmail_sender_password, email_body, email_subject, email_body_no_job, email_subject_no_job
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to, website, type='login'):
    try:
        msg = MIMEMultipart()

        msg['From'] = gmail_sender_account
        msg['To'] = to

        if type == 'login':
            msg['Subject'] = email_subject.format(website=website)
            msg.attach(MIMEText(email_body.format(website=website), 'plain'))

        elif type == 'no_job':
            msg['Subject'] = email_subject_no_job.format(website=website)
            msg.attach(MIMEText(email_body_no_job.format(website=website), 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_sender_account, gmail_sender_password)
        text = msg.as_string()
        server.sendmail(gmail_sender_account, to, text)
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print('Error: ', e)
        print('Failed to send email.')

def get_data(path):
    with open(path, 'rb') as file:
        try:
            data = pickle.load(file)
        except EOFError as e:
            print(e)
            data = []

    if path == db_links_path:
        data = [mail for mail in data if os.path.exists(os.path.join('logs', f"{mail['mail']}.txt"))]

    return data


def set_data(data, path):
    if path == db_links_path:
        for mail in data:
            with open(os.path.join('logs', f"{mail['mail']}.txt"), 'w+') as f:
                for link in mail['links']:
                    f.write(link + '\n')

    with open(path, 'wb') as file:
        pickle.dump(data, file)


db_mails_path= os.path.join('data', 'mails.pickle')
db_links_path = os.path.join('data', 'links.pickle')

try:
    links = get_data(db_links_path)
    print(len(links))
except:
    links = []
    set_data(links, db_links_path)


def get_driver(state):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("--log-level=3")

    if 'selected' not in state:
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--output=/dev/null")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_parameters(url):
    parse_result = urlparse(url)
    dict_result = parse_qs(parse_result.query)

    return dict_result


def run_mail(driver, mail, info, error, links, set_data, db_links_path,  website_main=''):

    try:
        mail_index = [link['mail'] for link in links].index(mail['mail'].replace('\n', ''))
    except:

        links.append({
            'mail': mail['mail'].replace('\n', ''),
            'links': []
        })

        mail_index = [link['mail'] for link in links].index(mail['mail'].replace('\n', ''))

        set_data(links, db_links_path)
    for website in mail['websites']:
        total_jobs = None

        if website_main and website_main != website:
            continue
        if mail['websites'][website]['research'] != '':
            if website == 'meteojob':

                if meteojob.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        try:
                            params = get_parameters(link)
                            try:
                                query = params['what'][0]
                            except:
                                query = ''
                            try:
                                where = params['where'][0]
                            except:
                                where = ''
                            info(f"Recherche : {query} en {where}")
                        except Exception as e:
                            pass

                        jobs = meteojob.recherche(driver, link, info, error)
                        total_jobs += len(jobs)

                        if jobs:

                            for job in jobs:
                                if job in links[mail_index]['links']:
                                    info(f"{mail['mail']} -- {job} déjà visité")
                                    pass_count += 1
                                    continue
                                status = meteojob.postuler(driver, job, info, error)
                                if status == "Postulé":
                                    count += 1

                                links[mail_index]['links'].append(job)
                                set_data(links, db_links_path)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            error("\tAucun job trouvé")
                            print("WARNING: Aucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.meteojob.com")
                    send_email(mail['mail'], 'meteojob')

            elif website == 'lefigaro':

                if lefigaro.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        try:
                            params = get_parameters(link)
                            try:
                                query = params['q'][0]
                            except:
                                query = ''

                            info(f"Recherche : {query}")
                        except Exception as e:
                            pass

                        jobs = lefigaro.recherche(driver, link, info, error)
                        total_jobs += len(jobs)
                        if jobs:

                            for job in jobs:
                                if job != None and job != link:
                                    if job in links[mail_index]['links']:
                                        info(f"{mail['mail']} -- {job} déjà visité")
                                        pass_count += 1
                                        continue
                                    try:
                                        status = lefigaro.postuler(driver, job, info, error, mail)
                                        if status == "Postulé":
                                            count += 1

                                        links[mail_index]['links'].append(job)
                                        set_data(links, db_links_path)

                                    except Exception as e:
                                        error(e)
                                        error(job)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            error("\tAucun job trouvé")
                            print("WARNING: Aucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.lefigaro.fr")
                    send_email(mail['mail'], 'lefigaro')

            elif website == 'hellowork':

                if hellowork.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        params = get_parameters(link)
                        try:
                            query = params['k'][0]
                        except:
                            query = ''
                        try:
                            where = params['l'][0]
                        except:
                            where = ''

                        info(f"Recherche : {query} en {where}")

                        print('looking for jobs')
                        jobs = hellowork.recherche(driver, link, info, error)
                        print('Jobs: ' + str(len(jobs)))
                        total_jobs += len(jobs)

                        if jobs:
                            for job in jobs:
                                if job != None:
                                    try:
                                        if job in links[mail_index]['links']:
                                            info(f"{mail['mail']} -- {job} déjà visité")
                                            pass_count += 1
                                            continue
                                        status = hellowork.postuler(driver, job, info, error, mail)
                                        if status == "Postulé":
                                            count += 1
                                        links[mail_index]['links'].append(job)
                                        set_data(links, db_links_path)
                                    except InvalidArgumentException:
                                        error(e)
                                        error(job)
                                    except Exception as e:
                                        error(e)
                                        error(job)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            error("\tAucun job trouvé")
                            info("WARNING: Aucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.hellowork.com")
                    send_email(mail['mail'], 'hellowork')

            elif website == 'monster':

                if monster.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        try:
                            params = get_parameters(link)
                            try:
                                query = params['q'][0]
                            except:
                                query = ''
                            try:
                                where = params['where'][0]
                            except:
                                where = ''

                            info(f"Recherche : {query} en {where}")
                        except Exception as e:
                            pass

                        jobs = monster.recherche(driver, link, info, error)
                        total_jobs += len(jobs)
                        if jobs:

                            for job in jobs:
                                if jobs != None:
                                    try:
                                        if job in links[mail_index]['links']:
                                            info(f"{mail['mail']} -- {job} déjà visité")
                                            pass_count += 1
                                            continue
                                        status = monster.postuler(driver, job, link, info, error, mail)
                                        if status == "Postulé":
                                            count += 1

                                        links[mail_index]['links'].append(job)
                                        set_data(links, db_links_path)
                                    except InvalidArgumentException:
                                        pass
                                    except Exception as e:
                                        error(e)
                                        error(job)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            info("\tAucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.monster.com")
                    send_email(mail['mail'], 'monster')

            elif website == 'welcometothejungle':

                if welcometothejungle.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        try:
                            params = get_parameters(link)
                            try:
                                query = params['query'][0]
                            except:
                                query = ''
                            try:
                                where = params['aroundQuery'][0]
                            except:
                                where = ''

                            info(f"Recherche : {query} en {where}")
                        except Exception as e:
                            pass

                        jobs = welcometothejungle.recherche(driver, link, info, error)
                        total_jobs += len(jobs)
                        if jobs:
                            info(f"\tNombre de jobs trouvés : {len(jobs)}")
                            for job in jobs:
                                print()
                                if jobs != None:
                                    try:
                                        if get_parameters(job)['o'][0] in [get_parameters(link_)['o'][0] for link_ in
                                                                           links[mail_index]['links'] if
                                                                           link_.startswith(
                                                                                   'https://www.welcometothejungle.com')]:
                                            info(f"{mail['mail']} -- {job} déjà visité")
                                            pass_count += 1
                                            continue
                                        status = welcometothejungle.postuler(driver, job, info, error, mail)
                                        if status == "Postulé":
                                            count += 1

                                        links[mail_index]['links'].append(job)
                                        set_data(links, db_links_path)
                                        print("JOB set to pickle")
                                    except InvalidArgumentException as e:
                                        print(e)
                                        pass
                                    except Exception as e:
                                        print(e)
                                        error(e)
                                        error(job)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            error("\tAucun job trouvé")
                            error("WARNING: Aucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.monster.com")
                    send_email(mail['mail'], 'welcometothejungle')

            elif website == 'indeed':

                if indeed.login(driver, mail, info, error):
                    total_jobs = 0
                    info(f"\tConnecté au compte {mail['mail']} sur {website}")

                    for link in mail['websites'][website]['research'].split(','):
                        count = 0
                        pass_count = 0

                        try:
                            params = get_parameters(link)
                            try:
                                query = params['query'][0]
                            except:
                                query = ''
                            try:
                                where = params['aroundQuery'][0]
                            except:
                                where = ''

                            info(f"Recherche : {query} en {where}")
                        except Exception as e:
                            pass

                        jobs = indeed.recherche(driver, link, info, error)
                        total_jobs += len(jobs)
                        if jobs:

                            for job in jobs:
                                if jobs != None:
                                    try:
                                        if get_parameters(job)['o'][0] in [get_parameters(link_)['o'][0] for link_ in
                                                                           links[mail_index]['links'] if
                                                                           link_.startswith(
                                                                                   'https://www.welcometothejungle.com')]:
                                            info(f"{mail['mail']} -- {job} déjà visité")
                                            pass_count += 1
                                            continue
                                        status = indeed.postuler(driver, job, info, error, mail)
                                        if status == "Postulé":
                                            count += 1

                                        links[mail_index]['links'].append(job)
                                        set_data(links, db_links_path)
                                    except InvalidArgumentException:
                                        pass
                                    except Exception as e:
                                        error(e)
                                        error(job)

                            info(f"\tNombre de jobs ignorés : {pass_count}")
                            info(f"\tNombre de jobs postulés : {count}")
                        else:
                            error("\tAucun job trouvé")
                            error("WARNING: Aucun job trouvé")

                    info(f"Déconnexion de {mail['mail']}")

                else:
                    error(f"Erreur de connexion avec {mail['mail']} sur www.monster.com")
                    send_email(mail['mail'], 'indeed')


        if total_jobs== 0:
            send_email(to=mail['mail'], website=website, type='no_job')

