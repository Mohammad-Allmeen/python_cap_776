from auth import Auth
from geo import Geo

def main():
    auth = Auth('regno.csv')
    login_success = auth.login()
    
    if login_success:
        geo = Geo()
        while True:
            geo.run()
            opt = input("Options:\n1. Check for another IP\n2. Logout\n")
            if opt == '1':
                continue
            elif opt == '2':
                break
            else:
                print("Invalid option. Exiting...")
                break
    else:
        print("Exiting application.")

if __name__ == "__main__":
    main()
