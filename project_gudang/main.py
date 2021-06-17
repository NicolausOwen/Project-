import sys
import tkinter as tk

from tkinter import messagebox
from settings import Settings
from appPage import AppPage
from login_page import LoginPage


class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable(0,0)

		self.create_menu()
		self.create_container()
		self.pages = {}

		self.create_appPage()
		self.create_login_page()

	def create_menu(self):
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label="About", command=self.clicked_about_menu)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

	def create_menu_after(self):
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label="Exit", command=self.clicked_exit_menu)

		self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label="About", command=self.clicked_about_menu)

		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def change_page(self, page):
		page = self.pages[page]
		page.tkraise()

	def auth_login(self):
		username = self.pages['login_page'].var_username.get()
		password = self.pages['login_page'].var_password.get()
		
		granted = self.settings.login(username, password)
		
		granted = self.settings.login(username, password)
		try:
			if granted:
				self.create_menu()
				self.create_menu_after()
				self.change_page('appPage')
		except:
			return auth_login()

	def create_appPage(self):
		self.pages["appPage"] = AppPage(self.container, self.app)

	def create_login_page(self):
		self.pages['login_page'] = LoginPage(self.container, self)

	def clicked_about_menu(self):
		messagebox.showinfo("About this Program", "This Program created by Delvin Alvian and Nicolaus Owen")

	def clicked_exit_menu(self):
		respond = messagebox.askyesnocancel("Exit Program", "Are you sure to close the program?")
		if respond:
			sys.exit()


class ContactApp:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	myContactApp = ContactApp()
	myContactApp.run()