from json import load, dump
import json

class Settings:

	def __init__(self):

		self.title = "Gudang Mie Instan"

		base = 75
		ratio =(16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]
		self.screen = f"{self.width}x{self.height}"

		self.logo = "img/Gudang.jpg"
		self.users_path = "data/users.json"

		self.contacts = None
		self.load_data_from_json()


	def load_data_from_json(self):
		with open("data/contacts.json", "r") as json_file:
			self.contacts = load(json_file)


	def save_data_to_json(self):
		with open("data/contacts.json", "w") as json_file:
			dump(self.contacts, json_file)


	def load_data(self, path):
		with open(path, "r") as json_data:
			data = json.load(json_data)
		return data


	def login(self, username, password):
		user = self.load_data(self.users_path)
		if username in user:
			if password == user[username]["password"]:
				return True
			else:
				return False
		else:
			return False
