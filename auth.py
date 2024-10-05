import csv
import bcrypt
import re

class Auth:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.attempts = 0
        self.max_attempts = 5

    def _load_users(self):
        users = {}
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
                    users[row['email']] = row
        except FileNotFoundError:
            print("User data file not found.")
        return users

    def _validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password):
        if (len(password) < 8 or
                not re.search(r'[A-Z]', password) or
                not re.search(r'[a-z]', password) or
                not re.search(r'[0-9]', password) or
                not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
            return False
        return True
    
    def register_user(self, email, password):
        if not self._validate_email(email):
            print("Invalid email format.")
            return

        if self._validate_password(password):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            security_question = input("Enter a security question: ")
            security_answer = input("Enter the answer to the security question: ")
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['email', 'hashed_password', 'security_question', 'security_answer'])
                writer.writerow({'email': email, 'hashed_password': hashed_password, 'security_question': security_question, 'security_answer': security_answer})
            print("Account created successfully!")
            return True
        else:
            print("Password does not meet the requirements.")
            return False

    def login(self):
        users = self._load_users()

        while self.attempts < self.max_attempts:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            if not self._validate_email(email):
                print("Invalid email format.")
                continue

            if email in users:
                if bcrypt.checkpw(password.encode('utf-8'), users[email]['hashed_password'].encode('utf-8')):
                    print("Login successful!")
                    return True
                else:
                    self.attempts += 1
                    print(f"Incorrect password. Attempts remaining: {self.max_attempts - self.attempts}. Do you want to reset the password? (y/n)")
                    reset_password = input()
                    if reset_password.lower() == 'y':
                        self.reset_password()
                        return True
            else:
                print("Email not found. Do you want to create a new account? (y/n)")
                create_account = input()
                if create_account.lower() == 'y':
                    created = self.register_user(email, password)
                    if created:
                        return True
                else:
                    print("Exiting application.")
                    return False

        print("Too many failed attempts. Please restart the application.")
        return False

    def reset_password(self):
        email = input("Enter your registered email: ")
        users = self._load_users()
        
        if email in users:
            security_question = users[email]['security_question']
            answer = input(f"Security Question: {security_question}\nYour answer: ")

            # In a real application, you'd check this answer against a stored value.
            # For simplicity, we will assume it's correct here.
            # check if the answer matches the stored answer
            if answer != users[email]['security_answer']:   
                print("Wrong answer. Exiting!")
                return
            new_password = input("Enter your new password: ")

            if self._validate_password(new_password):
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                users[email]['hashed_password'] = hashed_password

                # Write back to CSV
                with open(self.csv_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['email', 'hashed_password', 'security_question', 'security_answer'])
                    writer.writeheader()
                    for user_email, user_data in users.items():
                        writer.writerow(user_data)
                
                print("Password has been reset successfully!")
            else:
                print("New password does not meet the requirements.")
        else:
            print("Email not found.")

