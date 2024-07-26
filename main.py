import login

def main():
    while True:
        print("0. Quit")
        print("1. Login")
        print("2. Create New User")

        choice = input("Enter choice (0-2): ")

        if choice == "1":
            login.Login.login()
        elif choice == "2":
            login.Login.create_user()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please enter a valid option.")

if __name__ == "__main__":
    main()