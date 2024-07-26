import os
import EC2
import menu

class Login:

    def file_exists_and_readable(file_path):
        return os.path.exists(file_path) and os.access(file_path, os.R_OK)

    def create_user():
        username = input("Enter username: ")
        password = input("Enter password: ")
        key = input("Enter key: ")
        secret_key = input("Enter secret key: ")

        with open("passwords.txt", "a") as file:
            file.write(f"{username}\t{password}\t{key}\t{secret_key}\n")
        print("User created successfully")

    def login():
        username = input("Enter username: ")
        password = input("Enter password: ")

        if not Login.file_exists_and_readable("passwords.txt"):
            print("User database is not accessible.")
            return

        with open("passwords.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                user, pwd, key, secret = line.strip().split("\t")
                if user == username and pwd == password:
                    menu.Menu.mainmenu(key, secret)
            print("Invalid username or password")