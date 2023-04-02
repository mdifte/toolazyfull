from tkinter import messagebox
def error(text,title='Error'):
	messagebox.showerror(title=title,message=text)
def info(text,title='Info'):
	messagebox.showinfo(title=title,message=text)