import json
from hashlib import sha256

class Credentials:
    def __init__(self):
        pass




    def load_credentials(self):
        try:
            with open("credentials.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
        


           
    def store_credentials(self, name, password):
        credentials = self.load_credentials()

        if name in credentials:
            print(f"Username '{name}' already exists. Please choose a different one.")
            return False  

        hashed_pwd = hashed_password = sha256(password.encode()).hexdigest() 

        credentials[name] = {"username" : name,
                             "password" : hashed_pwd}
        with open("credentials.json", 'w') as file:
            json.dump(credentials, file, indent = 4)



            

    def authenticate_credentials(self, name, password):
        users = self.load_credentials()

        if name not in users:
            print("Username not found.")
            return False

        hashed_input = sha256(password.encode()).hexdigest()
        stored_hash = users[name]["password"]

        if hashed_input == stored_hash:
            print("Authentication successful.")
            return True
        else:
            print("Incorrect password.")
            return False
        