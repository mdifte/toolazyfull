from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import InvalidArgumentException

from urllib.parse import urlparse, parse_qs
import pickle 
import os,inspect


dir_path = os.path.dirname(os.path.realpath(__file__))

def get_data(path):
	with open(path, 'rb') as file:
		try:
			data = pickle.load(file)
		except EOFError as e:
			print(e)
			data=[]
		file.close()

	if path==db_links_path:
		for index,mail in enumerate(data):
			try:
				with open(dir_path+'/logs/'+data[index]['mail']+'.txt','r') as f:
					pass
			except:
				del(data[index])
		set_data(data,db_links_path)

	return data

def set_data(data,path):

	try:
		if path==dir_path+'/data/links.pickle':
			files=os.listdir(dir_path+'/logs')
			data=links
			for index,file in enumerate(files):
				os.remove(dir_path+'/logs/'+file)

			for index,mail in enumerate(data):
				with open(dir_path+'/logs/'+data[index]['mail']+'.txt','w+') as f:
					for link in data[index]['links']:
						f.write(link+'\n')
	except:
		pass

	try:
		with open(path, 'wb') as file:
			pickle.dump(data, file)
			file.close()
	except Exception as e:
			pass

db_mails_path=dir_path+'/data/mails.pickle'

db_links_path=dir_path+'/data/links.pickle'


try:
	links=get_data(db_links_path)
except:
	links=[]
	set_data(links,db_links_path)

def get_driver(state):

	chrome_options = webdriver.ChromeOptions()

	chrome_options.add_argument('start-maximized')
	chrome_options.add_argument("--log-level=3")

	if 'selected' not in state:
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument("--log-level=3")
		chrome_options.add_argument("--output=/dev/null")

	driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

	return driver


def get_parameters(url):
	parse_result = urlparse(url)
	dict_result = parse_qs(parse_result.query)

	return dict_result

def run_mail(driver,mail,info,error,links,set_data,db_links_path,website_module,website_main=''):
	try:
		mail_index=[link['mail'] for link in links].index(mail['mail'].replace('\n',''))
	except:


		links.append({
				'mail':mail['mail'].replace('\n',''),
				'links':[]
			})
		
		mail_index=[link['mail'] for link in links].index(mail['mail'].replace('\n',''))

		set_data(links,db_links_path)
		
	for website in mail['websites']:
		if website_main and website_main!=website:
			continue
		if mail['websites'][website]['research']!='':
			if website=='meteojob':
				
				if website_module[0].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")
					print(mail['websites'][website])

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0
						print(link)

						try:
							params=get_parameters(link)
							try:
								query=params['what'][0]
							except:
								query=''
							try:
								where = params['where'][0]
							except:
								where=''
							info(f"Recherche : {query} en {where}")
						except Exception as e:
							pass
							
						jobs = website_module[0].recherche(driver, link,info,error)

						if jobs:

							for job in jobs:
								if job in links[mail_index]['links']:
									info(f"{mail['mail']} -- {job} déjà visité")
									pass_count += 1
									continue
								status = website_module[0].postuler(driver, job,info,error,mail)
								if status == "Postulé":
									count += 1

								links[mail_index]['links'].append(job)
								set_data(links,db_links_path)

							info(f"\tNombre de jobs ignorés : {pass_count}")
							info(f"\tNombre de jobs postulés : {count}")
						else:
							error("\tAucun job trouvé")
							print("WARNING: Aucun job trouvé")

					info(f"Déconnexion de {mail['mail']}")

				else:
					error(f"Erreur de connexion avec {mail['mail']} sur www.meteojob.com")
			elif website=='lefigaro':
				
				if website_module[1].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0

						try:
							params=get_parameters(link)
							try:
								query=params['q'][0]
							except:
								query=''

							info(f"Recherche : {query}")
						except Exception as e:
							pass
							
						jobs = website_module[1].recherche(driver, link,info,error)

						if jobs:

							for job in jobs:
								if job!=None and job!=link:
									if job in links[mail_index]['links']:
										info(f"{mail['mail']} -- {job} déjà visité")
										pass_count += 1
										continue
									try:
										status = website_module[1].postuler(driver, job,info,error,mail)
										if status == "Postulé":
											count += 1

										links[mail_index]['links'].append(job)
										set_data(links,db_links_path)

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
			elif website=='hellowork':
				
				if website_module[2].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0

						params=get_parameters(link)
						try:
							query=params['k'][0]
						except:
							query=''
						try:
							where=params['l'][0]
						except:
							where=''

						info(f"Recherche : {query} en {where}")
						
						print('looking for jobs')
						jobs = website_module[2].recherche(driver, link,info,error)
						print('Jobs: '+str(len(jobs)))

						if jobs:

							for job in jobs:
								if job!=None:
									try:
										if job in links[mail_index]['links']:
											info(f"{mail['mail']} -- {job} déjà visité")
											pass_count += 1
											continue
										status = website_module[2].postuler(driver, job,info,error,mail)
										if status == "Postulé":
											count += 1

										links[mail_index]['links'].append(job)
										set_data(links,db_links_path)
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

			elif website=='monster':
				
				if website_module[3].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0

						try:
							params=get_parameters(link)
							try:
								query=params['q'][0]
							except:
								query=''
							try:
								where=params['where'][0]
							except:
								where=''

							info(f"Recherche : {query} en {where}")
						except Exception as e:
							pass
							
						jobs = website_module[3].recherche(driver, link,info,error)

						if jobs:

							for job in jobs:
								if jobs!=None:
									try:
										if job in links[mail_index]['links']:
											info(f"{mail['mail']} -- {job} déjà visité")
											pass_count += 1
											continue
										status = website_module[3].postuler(driver, job,link,info,error,mail)
										if status == "Postulé":
											count += 1

										links[mail_index]['links'].append(job)
										set_data(links,db_links_path)
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

			elif website=='welcometothejungle':
				
				if website_module[4].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0

						try:
							params=get_parameters(link)
							try:
								query=params['query'][0]
							except:
								query=''
							try:
								where=params['aroundQuery'][0]
							except:
								where=''

							info(f"Recherche : {query} en {where}")
						except Exception as e:
							pass
							
						jobs = website_module[4].recherche(driver, link,info,error)

						if jobs:

							for job in jobs:
								if jobs!=None:
									try:
										if get_parameters(job)['o'][0] in [get_parameters(link_)['o'][0] for link_ in links[mail_index]['links'] if link_.startswith('https://www.welcometothejungle.com')]:
											info(f"{mail['mail']} -- {job} déjà visité")
											pass_count += 1
											continue
										status = website_module[4].postuler(driver, job,info,error,mail)
										if status == "Postulé":
											count += 1

										links[mail_index]['links'].append(job)
										set_data(links,db_links_path)
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

			elif website=='indeed':
				
				if website_module[4].login(driver,mail,info,error):

					info(f"\tConnecté au compte {mail['mail']} sur {website}")

					for link in mail['websites'][website]['research'].split(','):
						count = 0
						pass_count = 0

						try:
							params=get_parameters(link)
							try:
								query=params['query'][0]
							except:
								query=''
							try:
								where=params['aroundQuery'][0]
							except:
								where=''

							info(f"Recherche : {query} en {where}")
						except Exception as e:
							pass
							
						jobs = website_module[4].recherche(driver, link,info,error)

						if jobs:

							for job in jobs:
								if jobs!=None:
									try:
										if get_parameters(job)['o'][0] in [get_parameters(link_)['o'][0] for link_ in links[mail_index]['links'] if link_.startswith('https://www.welcometothejungle.com')]:
											info(f"{mail['mail']} -- {job} déjà visité")
											pass_count += 1
											continue
										status = website_module[4].postuler(driver, job,info,error,mail)
										if status == "Postulé":
											count += 1

										links[mail_index]['links'].append(job)
										set_data(links,db_links_path)
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