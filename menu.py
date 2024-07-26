import EC2
import EBSStorage
import S3
import monitor

class Menu:
    def mainmenu(key, secret):
        while True:
            print("-------- Main Menu ---------")
            print("0. Back")
            print("1. Manage EC2")
            print("2. Manage EBS Storage")
            print("3. Manage S3")
            print("4. Monitor systems")
            

            choice = input("Enter choice (0-4): ")

            if choice == '1':
                EC2.EC2.menu(key, secret)
            elif choice == '2':
                EBSStorage.EBSStorage.menu(key, secret)
            elif choice == '3':
                S3.S3.menu(key, secret)
            elif choice == '4':
                monitor.Monitor.menu(key, secret)
            elif choice == '0':
                break
            else:
                print("Invalid choice, please select 1-5")
