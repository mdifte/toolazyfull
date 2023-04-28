from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from entrywp import EntryWP
from tkinter import Button
from datetime import datetime
import pyautogui
import pickle
import os
import utils
from threading import Thread


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
            with open(os.path.join('logs', f"{mail['mail'].strip()}.txt"), 'w+') as f:
                for link in mail['links']:
                    f.write(link + '\n')

    with open(path, 'wb') as file:
        pickle.dump(data, file)


db_mails_path = os.path.join('data', 'mails.pickle')
db_links_path = os.path.join('data', 'links.pickle')

try:
    mails = get_data(db_mails_path)
except:
    mails = [{
        'mail': '',
        'websites': {
            'keljob': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            },
            'welcometothejungle': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            },
            'monster': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            },
            'lefigaro': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            },
            'hellowork': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            },
            'meteojob': {
                'password': '',
                'possition': '',
                'research': '',
                'letter': ''
            }
        }
    }]
    set_data(mails, db_mails_path)

try:
    links = get_data(db_links_path)
except:
    links = []
    set_data(links, db_links_path)


class ComboWP(ttk.Combobox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.bind('<Key>', self.key_event)

    def key_event(self, event):
        new_mails = []

        search_word = self.get()
        if event.char == '':
            search_word = search_word[:-1]
        else:
            search_word = search_word + event.char

        if search_word:
            for mail in self.root.mails:
                if mail.startswith(search_word):
                    new_mails.append(mail)
        else:
            new_mails = self.root.mails

        self.root.cb_all_mails.config(values=new_mails)


class Main(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title('Toolazyapp')
        self.geometry('440x830')
        self.minsize(440, 810)
        self.maxsize(800, 810)
        self.resizable(True, False)

        style = ttk.Style(self)
        style.layout('arrowless.Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough',
                       {'children': [('Vertical.Scrollbar.thumb',
                                      {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'ns'})])
        style.layout('arrowless.Horizontal.TScrollbar',
                     [('Horizontal.Scrollbar.trough',
                       {'children': [('Horizontal.Scrollbar.thumb',
                                      {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'we'})])

        self.mouse_coords = {
            'x': '',
            'y': ''
        }

        self.bind('<Motion>', self.click_mouse_coords)

        self.websites = ['keljob', 'welcometothejungle', 'monster', 'lefigaro', 'hellowork', 'meteojob', 'indeed']
        self.mails = [mail['mail'] for mail in mails]

        self.l1 = Frame(self)

        self.add_mail_btn = Button(self.l1, text='Ajouter nouveau mail', command=self.add_mail, relief=RIDGE, height=1,
                                   width=20, borderwidth=1, bg='#f5f5f5', highlightthickness=1)
        self.add_mail_btn.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.delete_mail_btn = Button(self.l1, text='Supprimer profil selectionne', command=self.delete_mail,
                                      relief=RIDGE, height=1, width=20, borderwidth=1, bg='#f5f5f5',
                                      highlightthickness=1)
        self.delete_mail_btn.config(highlightbackground="#b6b7b7", highlightcolor="#b6b7b7")

        self.add_mail_btn.pack(side=LEFT, ipadx=15, ipady=4, padx=(5, 17))
        self.delete_mail_btn.pack(side=RIGHT, ipadx=15, ipady=4, padx=(17, 5))

        self.cb_all_mails = ComboWP(self, values=self.mails, width=45, exportselection=0)
        self.cb_all_mails.current(0)
        self.cb_all_mails.bind("<<ComboboxSelected>>", self.select_mail)

        self.cb_all_websites = Combobox(self, values=self.websites, state='readonly', width=45)
        self.cb_all_websites.current(0)
        self.cb_all_websites.bind("<<ComboboxSelected>>", self.set_mail_settings)

        self.btn_save_mail = Button(self, text='Sauvegarder parametre', command=self.save_mail_website, relief=RIDGE,
                                    height=2, width=20, borderwidth=1, bg='#f5f5f5', highlightthickness=1)
        self.btn_save_mail.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")

        self.l_password = Frame(self)

        self.label_password = Label(self.l_password, text='Mot de passe', width=17)
        self.e_password = Text(self.l_password, bd=0, relief=GROOVE, height=1, font=('segoe', 9), bg='#ffffff',
                               highlightthickness=1)
        self.e_password.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")

        self.label_password.pack(side=LEFT, padx=(0, 24), anchor='n')
        self.e_password.pack(side=RIGHT, expand=True, fill=X)

        self.l_possition = Frame(self)

        self.label_possition = Label(self.l_possition, text='Poste actuel', width=17)
        self.e_possition = Text(self.l_possition, bd=0, relief=GROOVE, height=1, font=('segoe', 9), bg='#ffffff',
                                highlightthickness=1)
        self.e_possition.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")

        self.label_possition.pack(side=LEFT, padx=(0, 24), anchor='n')
        self.e_possition.pack(side=RIGHT, expand=True, fill=X)

        self.l_status = Frame(self)

        self.label_status = Label(self.l_status, text='Status', width=17)
        self.e_status = Text(self.l_status, bd=0, relief=GROOVE, height=1, font=('segoe', 9), state='disable',
                             bg='#f2f2f2', highlightthickness=1)
        self.e_status.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")

        self.label_status.pack(side=LEFT, padx=(0, 24), anchor='n')
        self.e_status.pack(side=RIGHT, expand=True, fill=X)

        self.l_research = Frame(self)

        self.label_research = Label(self.l_research, text='Recherche', width=17)
        self.e_research = Text(self.l_research, bd=0, relief=GROOVE, height=10, font=('segoe', 9), bg='#ffffff',
                               highlightthickness=1)
        self.e_research.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.vscroll_research = Scrollbar(self.l_research, orient=VERTICAL, style='arrowless.Vertical.TScrollbar')
        self.vscroll_research.config(command=self.e_research.yview)
        self.e_research.configure(yscrollcommand=self.vscroll_research.set)

        self.label_research.pack(side=LEFT, padx=(0, 24), anchor='n')
        self.vscroll_research.pack(side=RIGHT, fill=Y)
        self.e_research.pack(side=RIGHT, fill=BOTH, expand=True)

        self.l_letter = Frame(self)

        self.label_letter = Label(self.l_letter, text='Lettre de motivation', width=18)
        self.e_letter = Text(self.l_letter, bd=0, relief=GROOVE, height=10, font=('segoe', 9), bg='#ffffff',
                             highlightthickness=1)
        self.e_letter.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.vscroll_letter = Scrollbar(self.l_letter, orient=VERTICAL, style='arrowless.Vertical.TScrollbar')
        self.vscroll_letter.config(command=self.e_letter.yview)
        self.e_letter.configure(yscrollcommand=self.vscroll_letter.set)

        self.label_letter.pack(side=LEFT, padx=(0, 18), anchor='n')
        self.vscroll_letter.pack(side=RIGHT, fill=Y)
        self.e_letter.pack(side=RIGHT, fill=BOTH, expand=True)

        self.sep = Separator(self, orient='horizontal')

        self.check_btn_webdriver_visibility = Checkbutton(self, text='Visibilite du navigateur')
        self.check_btn_webdriver_visibility.state(['!alternate'])

        self.l2 = Frame(self)

        self.btn_l1 = Frame(self.l2)
        self.btn_l2 = Frame(self.l2)

        self.start_selected_mail_btn = Button(self.btn_l1, text='Lancer le site du profil', relief=RIDGE, height=2,
                                              width=20, borderwidth=1, bg='#f5f5f5', highlightthickness=1,
                                              command=self.start_selected_mail)
        self.start_selected_mail_btn.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.start_one_mail_btn = Button(self.btn_l1, text='Lancer profil selectionne', relief=RIDGE, height=2,
                                         width=20, borderwidth=1, bg='#f5f5f5', highlightthickness=1,
                                         command=self.start_mail)
        self.start_one_mail_btn.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.start_all_mails_btn = Button(self.btn_l2, text='Lancer tous les profils', relief=RIDGE, height=2, width=20,
                                          borderwidth=1, bg='#f5f5f5', highlightthickness=1,
                                          command=self.start_all_mails)
        self.start_all_mails_btn.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.start_from_mail_btn = Button(self.btn_l2, text='lancer à partir du profil', relief=RIDGE, height=2,
                                          width=20, borderwidth=1, bg='#f5f5f5', highlightthickness=1,
                                          command=self.start_from_mail)
        self.start_from_mail_btn.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")

        self.start_selected_mail_btn.pack(side=LEFT, ipadx=10, ipady=1, padx=(20, 5), pady=5)
        self.start_one_mail_btn.pack(side=LEFT, ipadx=10, ipady=1, padx=(5, 20), pady=5)
        self.start_all_mails_btn.pack(side=LEFT, ipadx=10, ipady=1, padx=(20, 5))
        self.start_from_mail_btn.pack(side=LEFT, ipadx=10, ipady=1, padx=(5, 20), pady=5)

        self.btn_l1.pack(side=TOP, fill=X)
        self.btn_l2.pack(side=TOP, fill=X)

        self.l3 = Frame(self)

        self.logs_listbox = Listbox(self.l3, bd=0, relief=GROOVE, height=15, font=('segoe', 9), bg='#ffffff',
                                    highlightthickness=1)
        self.logs_listbox.config(highlightbackground="#bfbfbf", highlightcolor="#bfbfbf")
        self.vscroll_logs = Scrollbar(self.l3, orient=VERTICAL, style='arrowless.Vertical.TScrollbar')
        self.vscroll_logs.config(command=self.logs_listbox.yview)
        self.xscroll_logs = Scrollbar(self.l3, orient=HORIZONTAL, style='arrowless.Horizontal.TScrollbar')
        self.xscroll_logs.config(command=self.logs_listbox.xview)
        self.logs_listbox.configure(xscrollcommand=self.xscroll_logs.set)
        self.logs_listbox.configure(yscrollcommand=self.vscroll_logs.set)

        self.xscroll_logs.pack(side=BOTTOM, fill=X)
        self.vscroll_logs.pack(side=RIGHT, fill=Y)
        self.logs_listbox.pack(side=RIGHT, fill=BOTH, expand=True)

    def click_mouse_coords(self, event):
        x, y = pyautogui.position()
        self.mouse_coords['x'] = x
        self.mouse_coords['y'] = y

    def add_mail(self):
        NewMail(self, self.mouse_coords['x'], self.mouse_coords['y'])

    def save_mail_website(self):

        mail = self.cb_all_mails.get()

        if mail != '':
            mail_index = self.mails.index(mail)
            website = self.cb_all_websites.get()

            mails[mail_index]['websites'][website]['password'] = self.e_password.get("1.0", END).replace('\n', '')
            mails[mail_index]['websites'][website]['possition'] = self.e_possition.get("1.0", END).replace('\n', '')
            mails[mail_index]['websites'][website]['research'] = self.e_research.get("1.0", END).replace('\n', '')
            mails[mail_index]['websites'][website]['letter'] = self.e_letter.get("1.0", END).replace('\n', '')

            set_data(mails, db_mails_path)

            self.info('Data saved')
            self.btn_save_mail['fg'] = 'green'

    def delete_mail(self):

        mail = self.cb_all_mails.get()
        if mail != '':
            mail_index = self.mails.index(mail)

            del (mails[mail_index])

            self.cb_all_mails.current(0)
            self.cb_all_websites.current(0)

            self.update_()

            set_data(mails, db_mails_path)

            self.set_mail_settings(None)

            self.info(mail + ' was deleted')

    def select_mail(self, event):
        self.clear()
        self.cb_all_websites.current(0)

        mail = self.cb_all_mails.get()
        mail_index = self.mails.index(mail)
        website = self.cb_all_websites.get()

        mail_settings = mails[mail_index]['websites'][website]

        self.e_password.insert(END, mail_settings['password'])
        self.e_possition.insert(END, mail_settings['possition'])
        self.e_research.insert(END, mail_settings['research'])
        self.e_letter.insert(END, mail_settings['letter'])

    def set_mail_settings(self, event):

        self.clear()
        self.mails = [mail['mail'] for mail in mails]

        mail = self.cb_all_mails.get()
        mail_index = self.mails.index(mail)
        website = self.cb_all_websites.get()

        mail_settings = mails[mail_index]['websites'][website]

        self.e_password.insert(END, mail_settings['password'])
        self.e_possition.insert(END, mail_settings['possition'])
        self.e_research.insert(END, mail_settings['research'])
        self.e_letter.insert(END, mail_settings['letter'])

    def update_(self):

        self.cb_all_mails['values'] = [mail['mail'] for mail in mails]
        self.set_mail_settings(None)

        self.l1.pack(side=TOP, pady=(13, 3), padx=10)
        self.cb_all_mails.pack(side=TOP, pady=2, padx=50)
        self.cb_all_websites.pack(side=TOP, pady=2, padx=50)
        self.btn_save_mail.pack(side=TOP, pady=2, padx=(80, 80))
        self.l_password.pack(side=TOP, fill=BOTH, pady=4, padx=(7, 12))
        self.l_possition.pack(side=TOP, fill=BOTH, pady=4, padx=(7, 12))
        self.l_status.pack(side=TOP, fill=BOTH, pady=4, padx=(7, 12))
        self.l_research.pack(side=TOP, fill=BOTH, pady=4, padx=(7, 12))
        self.l_letter.pack(side=TOP, fill=BOTH, pady=4, padx=(7, 12))
        self.sep.pack(side=TOP, fill=BOTH, pady=4, padx=(17, 35))
        self.check_btn_webdriver_visibility.pack(side=TOP, fill=BOTH, pady=4, padx=15)
        self.l2.pack(side=TOP, pady=4, padx=17)
        self.l3.pack(side=TOP, fill=BOTH, pady=(3, 13), padx=10)

    def clear(self):
        self.e_password.delete('1.0', END)
        self.e_possition.delete('1.0', END)
        self.e_research.delete('1.0', END)
        self.e_letter.delete('1.0', END)

    def info(self, text):

        time = str(datetime.now()).split('.')[0]

        error = '[INFO] - ' + time + ' - ' + str(text)

        self.logs_listbox.insert(END, error)
        self.logs_listbox.yview(END)

    def error(self, text):

        time = str(datetime.now()).split('.')[0]

        error = '[ERROR] - ' + time + ' - ' + str(text)

        self.logs_listbox.insert(END, error)
        self.logs_listbox.itemconfig(END, foreground="red")
        self.logs_listbox.yview(END)

    def start_mail(self):
        mail_index = self.mails.index(self.cb_all_mails.get())

        if mail_index != 0:
            threads = []
            state = self.check_btn_webdriver_visibility.state()
            mail = mails[mail_index]


            threads.append(
                self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                   'meteojob')))

            threads.append(
                self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                   'lefigaro')))

            threads.append(
                self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                   'hellowork')))

            threads.append(
                self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                   'monster')))

            threads.append(
                self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                   'welcometothejungle')))

            for thread in threads:
                thread.join()

            self.info('All Websites are done')

    def start_selected_mail(self):
        mail_index = self.mails.index(self.cb_all_mails.get())

        if mail_index != 0:

            state = self.check_btn_webdriver_visibility.state()
            mail = mails[mail_index]
            print(mail, mail_index)
            driver = utils.get_driver(state)
            website = self.cb_all_websites.get()

            new_task = Thread(target=utils.run_mail, args=(
                driver, mail, self.info, self.error, links, set_data, db_links_path,
                website))

            new_task.start()

            try:
                while new_task.is_alive():
                    self.update()
            except:
                pass

    def start_from_mail(self):
        mail_index = self.mails.index(self.cb_all_mails.get())
        for mail_ in mails[mail_index:]:
            if mail_ != '':
                mail_index = self.mails.index(mail_['mail'])

                if mail_index != 0:
                    threads = []
                    state = self.check_btn_webdriver_visibility.state()
                    mail = mails[mail_index]

                    threads.append(self.start_thread(utils.run_mail, (
                        utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                        'meteojob')))

                    threads.append(self.start_thread(utils.run_mail, (
                        utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                         'lefigaro')))

                    threads.append(self.start_thread(utils.run_mail, (
                        utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                         'hellowork')))

                    threads.append(self.start_thread(utils.run_mail, (
                        utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                         'monster')))

                    threads.append(self.start_thread(utils.run_mail, (
                        utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                         'welcometothejungle')))

                    # wait for all threads to finish
                    for t in threads:
                        t.join()


    def update_thread(self, thread):
        try:
            while thread.is_alive():
                self.update()
        except:
            pass

    def start_thread(self, function, args):
        print('starting thread', function)
        new_task = Thread(target=function, args=args)
        new_task.start()

        self.update_thread(new_task)

        return new_task

    def start_all_mails(self):

        for mail_ in mails:

            try:
                threads = []
                if mail_ != '':
                    mail_index = self.mails.index(mail_['mail'])

                    if mail_index != 0:

                        state = self.check_btn_webdriver_visibility.state()
                        mail = mails[mail_index]


                        threads.append(self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                                       'meteojob')))

                        threads.append(self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                                           'lefigaro')))

                        threads.append(self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                                             'hellowork')))

                        threads.append(self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                                             'monster')))

                        threads.append(self.start_thread(utils.run_mail, (utils.get_driver(state), mail, self.info, self.error, links, set_data, db_links_path,
                                                                           'welcometothejungle')))

                # wait for all threads to finish
                for t in threads:
                    t.join()

                print('all threads finished')

            except:
                pass




class NewMail(tk.Tk):
    def __init__(self, master, ws, hs, **kwargs):
        super().__init__(**kwargs)

        self.master = master

        screen_width = 180
        screen_height = 80

        self.title('New Mail')
        self.resizable(False, False)

        self.geometry('%dx%d+%d+%d' % (screen_width, screen_height, ws - 20, hs + 40))

        self.label_mail = Label(self, text='Mail', anchor='w')
        self.e_mail = EntryWP(self)
        self.add_mail_btn = Button(self, text='Ajouter', height=1, width=20, relief=GROOVE, borderwidth=4, anchor='n',
                                   command=self.add)

        self.label_mail.pack(fill=X, padx=5)
        self.e_mail.pack(fill=X, padx=5, pady=3)
        self.add_mail_btn.pack(fill=X, padx=5, pady=3)

    def add(self):
        mail = self.e_mail.get()
        mails.append({
            'mail': mail,
            'websites': {
                'keljob': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                },
                'welcometothejungle': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                },
                'monster': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                },
                'lefigaro': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                },
                'hellowork': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                },
                'meteojob': {
                    'password': '',
                    'possition': '',
                    'research': '',
                    'letter': ''
                }
            }
        })

        links.append({
            'mail': mail,
            'links': []
        })

        set_data(mails, db_mails_path)
        set_data(links, db_links_path)

        self.destroy()

        self.master.update_()
        self.master.cb_all_mails.current(END)
        self.master.set_mail_settings(None)
        self.master.info('New mail: ' + mail + ' was added')


if __name__ == '__main__':
    root = Main()
    root.update_()
    root.mainloop()
