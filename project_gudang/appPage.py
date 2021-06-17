import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_contact = self.settings.contacts[0]
		self.last_current_contact_index = []
		self.update_mode = False
		self.contacts_index = []

		super().__init__(parent)
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_right_frame()


	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.create_left_header()
		self.create_left_content()


	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()


	def config_left_right_frame(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_rowconfigure(0, weight=1)


	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio),int(i_h/ratio))
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_header, bg="white", width=frame_w, height=frame_h//4)
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), text="Find", command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.searchbox_frame.grid_columnconfigure(0, weight=3)
		self.searchbox_frame.grid_columnconfigure(1, weight=1)


	def update_contact_index_list(self):
		contacts = self.settings.contacts

		self.contacts_index = []
		counter_index = 0
		for contact in contacts:
			self.contacts_index.append(counter_index)
			counter_index += 1

		self.show_contacts_in_listbox()


	def show_contacts_in_listbox(self):
		contacts = self.settings.contacts

		for index in self.contacts_index:
			contact = contacts[index]
			for key, value in contact.items():
				full_name = f"{value['f_name']} {value['l_name']}"
				self.contact_listBox.insert("end", full_name)


	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5

		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.contact_listBox = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.contact_listBox.pack(side="left", fill="both", expand=True)

		self.contacts_scroll = tk.Scrollbar(self.left_content)
		self.contacts_scroll.pack(side="right", fill="y")

		contacts = self.settings.contacts
		counter_index = 0
		for contact in contacts:
			self.contacts_index.append(counter_index)
			counter_index += 1

		self.show_contacts_in_listbox()

		self.contact_listBox.configure(yscrollcommand=self.contacts_scroll.set)
		self.contacts_scroll.configure(command=self.contact_listBox.yview)

		self.contact_listBox.bind("<<ListboxSelect>>", self.clicked_item_in_Listbox)


	def clicked_item_in_Listbox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				index_item = selection[0]
			except IndexError:
				index_item = self.last_current_contact_index
			index = self.contacts_index[index_item]
			self.last_current_contact_index = index
			#print(index_item,"=>",index)
			self.current_contact = self.settings.contacts[index]
			for Merk, info in self.current_contact.items():
				merk = Merk
				full_name = info['f_name']+" "+info['l_name']
				harga = info['Harga']
				rasa = info['Rasa']
			self.full_name_label.configure(text=full_name)
			self.table_info[0][1].configure(text=merk)
			self.table_info[1][1].configure(text=harga)
			self.table_info[2][1].configure(text=rasa)


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_header.pack()
		self.create_detail_right_header()


	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_contact.values())[0]
		full_name = f"{data['f_name']} {data['l_name']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.full_name_label = tk.Label(self.detail_header, text=full_name, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.full_name_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)


	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True)
		self.create_detail_right_content()


	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for Merk, info in self.current_contact.items():
			info = [
				['Merk :', Merk],
				['Harga :', info['Harga']],
				['Rasa :', info['Rasa']]
			]

		self.table_info = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)


	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack()
		self.create_detail_right_footer()


	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)


	def recreate_right_frame(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()


	def recreate_right_frame_after_delete(self):
		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()


	def recreate_right_frame_after_add_new(self):
		self.detail_add_contact_header.destroy()
		self.detail_add_contact_content.destroy()
		self.detail_add_contact_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()


	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for Merk, info in self.current_contact.items():
			info = [
				['Nama Depan :', info['f_name']],
				['Nama Belakang :', info['l_name']],
				['Merk :', Merk],
				['Harga :', info['Harga']],
				['Rasa :', info['Rasa']]
			]

		self.table_info = []
		self.entry_update_contact_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					entry.insert(0, info[row][column])
					aRow.append(entry)
					self.entry_update_contact_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_contact_btn, self.clicked_cancel_contact_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)


	def clicked_delete_btn(self):
		confirmed = messagebox.askyesnocancel("Product Conrifmation", "Are you sure you want to delete this product?")

		if confirmed:
			#print(self.current_contact, self.last_current_contact_index)
			self.settings.contacts.pop(self.last_current_contact_index)
			
			self.update_contact_index_list()
			self.settings.save_data_to_json()

			self.last_current_contact_index = 0
			self.current_contact = self.settings.contacts[self.last_current_contact_index]
			self.recreate_right_frame_after_delete()
			self.contact_listBox.delete(0, 'end')
			self.show_contacts_in_listbox()


	def clicked_add_new_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_add_contact_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_add_contact_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.add_product_label = tk.Label(self.detail_add_contact_header, text="Tambah Produk Baru", font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.add_product_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_add_contact_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_add_contact_content.grid(row=0, column=0, sticky="nsew")

		info = [
				['Nama Depan :', None],
				['Nama Belakang :', None],
				['Merk :', None],
				['Harga :', None],
				['Rasa :', None]
			]

		self.table_info = []
		self.entry_update_contact_vars = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_add_contact_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_add_contact_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					aRow.append(entry)
					self.entry_update_contact_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_add_contact_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_add_contact_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_new_contact_btn, self.clicked_cancel_new_contact_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_add_contact_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)


	def clicked_save_contact_btn(self):
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("Product Conrifmation", "Are you sure you want to update this product?")
		if confirmed:
			f_name = self.entry_update_contact_vars[0].get()
			l_name = self.entry_update_contact_vars[1].get()
			merk = self.entry_update_contact_vars[2].get()
			harga = self.entry_update_contact_vars[3].get()
			rasa = self.entry_update_contact_vars[4].get()
			self.settings.contacts[self.last_current_contact_index] = {
				merk : {
					"f_name" : f_name,
					"l_name" : l_name,
					"Harga" : harga,
					"Rasa" : rasa
				}
			}
			self.current_contact = self.settings.contacts[self.last_current_contact_index]
			self.settings.save_data_to_json()

		self.recreate_right_frame()
		self.contact_listBox.delete(0, 'end')
		self.show_contacts_in_listbox()


	def clicked_cancel_contact_btn(self):
		self.update_mode = False

		self.recreate_right_frame()


	def clicked_search_btn(self):
		item_search = self.entry_search_var.get()
		if item_search:
			contacts = self.settings.contacts
			self.contacts_index = []
			counter_index = 0
			for contact in contacts:
				for phoneNumber, info in contact.items():
					if item_search in phoneNumber:
						self.contacts_index.append(counter_index)
					elif item_search in info['f_name']:
						self.contacts_index.append(counter_index)
					elif item_search in info['l_name']:
						self.contacts_index.append(counter_index)
				counter_index += 1
			self.contact_listBox.delete(0, 'end')
			self.show_contacts_in_listbox()
		else:
			self.contact_listBox.delete(0, 'end')
			self.update_contact_index_list()


	def clicked_save_new_contact_btn(self):
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("Product Conrifmation", "Are you sure you want to add this product?")
		if confirmed:
			f_name = self.entry_update_contact_vars[0].get()
			l_name = self.entry_update_contact_vars[1].get()
			merk = self.entry_update_contact_vars[2].get()
			harga = self.entry_update_contact_vars[3].get()
			rasa = self.entry_update_contact_vars[4].get()
			product = {
				merk : {
					"f_name" : f_name,
					"l_name" : l_name,
					"Harga" : harga,
					"Rasa" : rasa
				}
			}
			self.settings.contacts.append(product)
			self.last_current_contact_index = len(self.settings.contacts)-1
			self.current_contact = self.settings.contacts[self.last_current_contact_index]
			self.settings.save_data_to_json()

		self.recreate_right_frame_after_add_new()
		self.contact_listBox.delete(0, 'end')
		self.update_contact_index_list()


	def clicked_cancel_new_contact_btn(self):
		self.update_mode = False

		self.recreate_right_frame_after_add_new()

		self.update_contact_index_list()
		self.settings.save_data_to_json()

		self.last_current_contact_index = 0
		self.current_contact = self.settings.contacts[self.last_current_contact_index]
		self.recreate_right_frame_after_delete()
		self.contact_listBox.delete(0, 'end')
		self.show_contacts_in_listbox()
