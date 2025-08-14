import json
from hashlib import sha256

class User:
    def __init__(self):
        pass





    def load_users(self):
        try:
            with open("users.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
        



    
    def store_users(self, name, password):
        users = self.load_users()

        if name in users:
            print(f"Username '{name}' already exists. Please choose a different one.")
            return False 

        hashed_pwd = hashed_password = sha256(password.encode()).hexdigest()  
          
        users[name] = {"username" : name,
                       "password" : hashed_pwd}
        
        with open("users.json", 'w') as file:
            json.dump(users, file, indent = 4)




        
    def authenticate_user(self, name, password):
        users = self.load_users()

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