
import winsound
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

class MultilingualATM:
    def __init__(self, balance=0):
        self.balance = balance
        self.logged_in = False
        self.user_pin = None
        self.admin_password = 'admin1234'
        self.user_id = None
        self.admin_id = 'admin1234'
        self.transaction_history = []
        self.admin_transaction_history = []
        self.users = []

    def select_language(self):
        print("\nSelect your preferred language:")
        print("1. English")
        print("2. Hindi")
        print("3. Other")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            return 'en'
        elif choice == "2":
            return 'hi'
        else:
            return 'auto'  # 'auto' will detect the language automatically

    def process_input(self, input_text, target_language='en'):
        # For simplicity, we'll assume the input language is the same as the target language
        return input_text.lower()

    def create_account(self, user_id, initial_balance=0, target_language='en'):
        if not self.logged_in:
            # Check if the user ID is unique
            if user_id not in [user['user_id'] for user in self.users]:
                self.users.append({'user_id': user_id, 'balance': initial_balance, 'pin': None})
                return f"{self.translate_input('Account created successfully!', target_language)}"
            else:
                return f"{self.translate_input('User ID already exists. Please choose a different one.', target_language)}"
        else:
            return f"{self.translate_input('You are already logged in. Logout to create a new account.', target_language)}"

    def user_login(self, entered_pin, user_id, target_language='en'):
        if not self.logged_in:
            actual_pin = '1234'

            if actual_pin == entered_pin:
                self.logged_in = True
                self.user_pin = entered_pin
                self.user_id = user_id
                return f"{self.translate_input('User login successful!', target_language)}"
            else:
                return f"{self.translate_input('Invalid PIN. Please try again.', target_language)}"
        else:
            return f"{self.translate_input('You are already logged in.', target_language)}"

    def admin_login(self, entered_password, admin_password, target_language='en'):
        if not self.logged_in:
            if entered_password == self.admin_password:
                self.logged_in = True
                return f"{self.translate_input('Admin login successful!', target_language)}"
            else:
                return f"{self.translate_input('Invalid password. Please try again.', target_language)}"
        else:
            return f"{self.translate_input('You are already logged in.', target_language)}"

    def logout(self, target_language='en'):
        if self.logged_in:
            self.logged_in = False
            self.user_pin = None
            return f"{self.translate_input('Logout successful!', target_language)}"
        else:
            return f"{self.translate_input('You are not logged in.', target_language)}"

    def check_balance(self, target_language='en'):
        if self.logged_in:
            return f"{self.translate_input(f'Your balance is Rs{self.balance}', target_language)}"
        else:
            return f"{self.translate_input('Please log in first.', target_language)}"

    def deposit(self, amount, target_language='en'):
        if self.logged_in:
            self.balance += amount
            self.transaction_history.append(f"Deposited Rs{amount}. New balance: Rs{self.balance}")
            user = next((user for user in self.users if user['user_id'] == self.user_id), None)
            if user:
                user['balance'] += amount
            return f"{self.translate_input(f'Deposited Rs{amount}. New balance: Rs{self.balance}', target_language)}"
        else:
            return f"{self.translate_input('Please log in first.', target_language)}"

    def withdraw(self, amount, target_language='en'):
        if self.logged_in:
            if amount <= self.balance:
                self.balance -= amount
                self.transaction_history.append(f"Withdraw Rs{amount}. New balance: Rs{self.balance}")

                user = next((user for user in self.users if user['user_id'] == self.user_id), None)
                if user:
                    user['balance'] -= amount
                return f"{self.translate_input(f'Withdraw Rs{amount}. New balance: Rs{self.balance}', target_language)}"
            else:
                return f"{self.translate_input('Insufficient funds', target_language)}"
        else:
            return f"{self.translate_input('Please log in first.', target_language)}"

    def get_transaction_history(self, target_language='en'):
        if self.logged_in:
            return [self.translate_input(transaction, target_language) for transaction in self.transaction_history]
        else:
            return f"{self.translate_input('Please log in first.', target_language)}"

    def notify_low_balance(self, target_language='en'):
        if self.balance < 75000:
            send_email("Low Balance Alert", f"Your balance is below Rs75,000. Current balance: Rs{self.balance}")
            return f"{self.translate_input('Low balance notification sent.', target_language)}"
        else:
            return f"{self.translate_input('Balance is not below Rs75,000. No notification sent.', target_language)}"

    def total_balance_admin(self, admin_password, target_language='en'):
        print(f"Provided admin password: {admin_password}")
        print(f"Expected admin password: {self.admin_password}")
        print(f"Logged in: {self.logged_in}")
        print(f"Users: {self.users}")

        if self.logged_in and admin_password == self.admin_password:
            total_balance = sum(user.get('balance', 0) for user in self.users)
            return f"{self.translate_input(f'Total balance: Rs{total_balance}', target_language)}"
        else:
            return f"{self.translate_input('Admin access required.', target_language)}"

    def translate_input(self, input_text, target_language='en'):
        translation_dict_hi = {
            'Account created successfully!': 'खाता सफलतापूर्वक बनाया गया!',
            'User login successful!': 'उपयोगकर्ता लॉगिन सफल!',
            'Invalid PIN. Please try again.': 'अमान्य पिन। कृपया पुनः प्रयास करें।',
            'You are already logged in.': 'आप पहले ही लॉग इन कर चुके हैं।',
            'Admin login successful!': 'एडमिन लॉगिन सफल!',
            'Invalid password. Please try again.': 'अमान्य पासवर्ड। कृपया पुनः प्रयास करें।',
            'Logout successful!': 'लॉगआउट सफल!',
            'You are not logged in.': 'आप लॉग इन नहीं हैं।',
            'Your balance is Rs': 'आपका शेष राशि है रु',
            'Please log in first.': 'कृपया पहले लॉग इन करें।',
            'Deposited Rs': 'रु जमा हो गया',
            'New balance: Rs': 'नया संतुलन: रु',
            'Withdraw Rs': 'रु निकाला गया',
            'Insufficient funds': 'अपर्याप्त धन',
            'Total Balance: Rs': 'कुल शेष: रु',
            'Balance is not below Rs75,000. No notification sent.': 'शेष ₹75,000 से कम नहीं है। कोई सूचना नहीं भेजी गई है।',
            'Low balance notification sent.': 'कम शेष सूचना भेजी गई है।',
        }

        if target_language == 'hi':
            return translation_dict_hi.get(input_text, input_text)
        else:
            return input_text


def send_email(subject, body):
    send_email = 'sharmapreetika72@gmail.com'
    receiver_email = '2022a6r035@mietjammu.in'
    password = "dpuolbheqsunygpt"
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = send_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(send_email, password)
        server.sendmail(send_email, receiver_email, message.as_string())


print("\t!!!!!WELCOME TO ATM!!!!!")
b = 0

def system_beep():
    winsound.Beep(1000, 1000)

def atm_simulator():
    correct_password = '1234'
    entered_password = input("Enter your password: ")

    if correct_password != entered_password:
        send_email("alert", "someone is trying to enter your password!!!!")
        system_beep()
        print("Alert!!!!!error")
    else:
        user_pin = "1234"
        admin_password = "admin1234"
        atm = MultilingualATM()

        # Prompt for language selection
        target_language = atm.select_language()

        while True:
            print("\n1. User Login\n2. Admin Login\n3. Create Account\n4. Exit")
            user_or_admin = input("Enter your choice (1-4): ")

            if user_or_admin == "1":
                user_id = input("Enter your User ID: ")
                while True:
                    print("\n1. Login\n2. Check Balance\n3. Deposit\n4. Withdraw\n5. Transaction History\n6. Password Change \n7. Logout\n8. Exit")
                    choice = input("Enter your choice (1-8): ")
                    if choice == "1":
                        pin = input("Enter your PIN: ")
                        processed_pin = atm.process_input(pin, target_language)
                        print(atm.user_login(processed_pin, user_id, target_language))
                    elif choice == "2":
                        print(atm.check_balance(target_language))
                    elif choice == "3":
                        amount = float(input("Enter the amount to deposit: Rs"))
                        print(atm.deposit(amount, target_language))
                    elif choice == "4":
                        amount = float(input("Enter the amount to withdraw: Rs"))
                        print(atm.withdraw(amount, target_language))
                    elif choice == "5":
                        print(atm.get_transaction_history(target_language))
                    elif choice == "6":
                        x = int(input("enter new password: "))
                        y = int(input("enter old password: "))
                        if user_pin == y:
                            user_pin = x
                            print("password changed")
                        else:
                            print("incorrect password!!!")
                    elif choice == "7":
                        print(atm.logout(target_language))
                    elif choice == "8":
                        print("Thank You Exiting from User Menu")
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 8.")

            elif user_or_admin == "2":
                admin_id = input("Enter your Admin ID: ")
                while True:
                    print("\n1. Login\n2. Total Balance\n3. Deposit\n4. Notify Low Balance\n5. Logout\n6. Exit")
                    admin_choice = input("Enter your choice (1-6): ")
                    if admin_choice == "1":
                        admin_password = input("Enter the admin password: ")
                        print(atm.admin_login(admin_password, admin_id, target_language))
                    elif admin_choice == "2":
                        print(atm.total_balance_admin(admin_id, target_language))
                    elif admin_choice == "3":
                        amount = float(input("Enter the amount to deposit: Rs"))
                        print(atm.deposit(amount, target_language))  
                    elif admin_choice == "4":
                            print(atm.notify_low_balance(target_language))
                    elif admin_choice == "5":
                            print(atm.logout(target_language))
                    elif admin_choice == "6":
                            print("Thank You Exiting from Admin Menu.")
                            break
                    else:
                            print("Invalid choice. Please enter a number between 1 and 6.")

            elif user_or_admin == "3":
                user_id = input("Enter your desired User ID: ")
                initial_balance = float(input("Enter the initial balance: Rs"))
                print(atm.create_account(user_id, initial_balance, target_language))
            
            elif user_or_admin == "4":
                print("Thank you for using the ATM. Goodbye!")
                return
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    atm_simulator()
  
                        