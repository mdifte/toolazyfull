import tkinter as tk

class EntryWP(tk.Entry):
	def __init__(self, master=None, text=None,label=None,width=None,bd=None):
		super().__init__(master)
		self['width']=width
		self['bd']=bd

		if text is not None:
			self.placeholder=text
			self.placeholder_color = 'black'
			self.default_fg_color = self['fg']
			self.label=0
			self.entrys=True
			self.bind("<FocusIn>", self.foc_in)
			self.bind('<Key>',self.key_event)
			self.put_placeholder()


	def put_placeholder(self):
		self.insert(0, self.placeholder)
		self['fg'] = self.placeholder_color

	def foc_in(self,*args):
		if self.label:
			if self.label['text']!='Add':
				pass

	def key_event(self,*args):
		if self.label:
			if self.label['text']!='Add':

				text=self.label['text'].replace('*','')
				self.label['text']=text+'*'
				
	def set(self,data):
		self.delete('0', 'end')
		self.placeholder=data
		self.put_placeholder()
