from abc import ABC
from numpy import random
from datetime import datetime

class User(ABC):
    def __init__(self, name, email, phone, address, password) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.password = password

class Holder(User):
    def __init__(self, name, email, phone, address, password, account_number, account_type) -> None:
        super().__init__(name, email, phone, address, password)
        self.account_number = account_number
        self.account_type = account_type
        self.balance = 0
        self.loan_amount = 0
        self.loan_time = 0
        self.active_status = False
        self.trans_history = []
    
    def deposit(self, amount):
        self.balance += amount
        cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.trans_history.append(f"\tDeposited {amount} BDT on {cur_time}. New Balance: {self.balance} BDT")
    
    def withdraw(self, amount):
        self.balance -= amount
        cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.trans_history.append(f"\tWithdral {amount} BDT on {cur_time}. New Balance: {self.balance} BDT")
    
    def money_transfer(self, recipient, amount):
        if self.balance <= 500 or self.balance - amount < 500:
            print("\tInsufficient balance")
            return
        if amount <= 0:
            print("\tInvalid transfer amount")
            return
        if recipient.active_status == False:
            print("\tThis account is inactive")
            return
        else:
            self.balance -= amount
            recipient.balance += amount
            cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.trans_history.append(f"\tTransferred {amount} BDT to {recipient.name} on {cur_time}. New Balance: {self.balance}")
            recipient.trans_history.append(f"\tReceived {amount} BDT from {self.name} on {cur_time}. New Balance:  {recipient.balance}")
            print("\tAmount transferred successfully")
    
    def transaction_history(self):
        print("\tTransection History")
        for trans in self.trans_history:
            print(trans)
                           
class Admin(User):
    def __init__(self, name, email, phone, address, password) -> None:
        super().__init__(name, email, phone, address, password)

class Bank:
    def __init__(self, name) -> None:
        self.name = name
        self.holders = []
        self.users = []
        self.bank_balance = 0
        self.loan_total = 0
        self.loan_feature = False
        self.bankrupt = False
    
    def total_loan(self):
        print(f"\tTotal loan amount : {self.loan_total} BDT")
    
    def take_loan(self, holder, amount):
        if amount > self.bank_balance:
            print("\tLoan amount exceeded")
            return
        elif self.bank_balance - amount < 5000 or self.bank_balance <= 5000:
            print("\tInsufficient funds in the bank")
            return
        else:
                self.bank_balance -= amount
                self.loan_total += amount
                holder.loan_amount += amount
                holder.balance += amount
                holder.loan_time += 1
                cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                holder.trans_history.append(f"\tTaken Loan {amount} BDT on {cur_time}. New Balance: {holder.balance} BDT")
                print(f"\tLoan {amount} BDT successfully added to your account")
            
    def pay_loan(self, holder, amount):
        if holder.balance - 500 < amount:
            print("\tInsufficient funds. Please deposit to pay your loan")
            return

        if holder.loan_amount and holder.loan_amount >= amount:
            print(f"\tPay more {holder.loan_amount-amount} BDT to clear loan")
            holder.loan_amount -= amount
            holder.balance -= amount
            self.loan_total -= amount
            self.bank_balance += amount
            cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            holder.trans_history.append(f"\tLoan paid {amount} BDT on {cur_time}. New Balance: {holder.balance}")
            if holder.loan_amount == 0:
                holder.loan_time -= 1
                print("\tBank loan is paid successfully")
            return

        print("\tInvalid loan amount")

    def set_bank_balance(self, amount):
        if amount <= 0:
            print("\tInvalid amount")
            return
        elif amount < 5000:
            self.bank_balance += amount
            print(f"\t{amount} BDT added as bank balance")
            if self.bank_balance < 5000:
                print(f"\tAdd {5000-self.bank_balance} BDT more to on loan feature")
            if self.bank_balance >= 5000:
                self.loan_feature = True
                print(f"\tAdded {amount} BDT to the bank balance. Loan feature is on now")
            return
        elif amount >= 5000:
            self.loan_feature = True    
            self.bank_balance += amount
            print(f"\tSuccessfully added {amount} BDT to the bank balance. Loan feature is on now")

    def generate_account_number(self):
        bank_code = 4269
        branch_code = 2420
        current_year = datetime.now().year
        unique_code = random.randint(1000, 1000000)
        return f"{bank_code}-{branch_code}-{current_year}-{unique_code}"

    def add_user(self, name, email, phone, address, password):
        user = Admin(name, email, phone, address, password)
        self.users.append(user)
        print(f"\t{name.capitalize()}, your registration completed. Now {name.capitalize()} can login his account")

    def add_account_holder(self, name, email, phone, address, password, account_number, account_type):
        holder = Holder(name, email, phone, address, password, account_number, account_type)
        self.holders.append(holder)
        print(f"\t{name.capitalize()}, your registration completed. Now {name.capitalize()} can login his account")
        print(f"\tYour account number is {account_number}")
    
    def find_account_holder(self, phone, account_number):
        if not self.holders:
            print("\tThere are no account holder")
            return
        else:
            for holder in self.holders:
                if holder.phone == phone and holder.account_number == account_number:
                    return holder
            return None

    def remove_account_holder(self, phone, account_number):
        holder = self.find_account_holder(phone, account_number)
        if holder:
            self.holders.remove(holder)
            print(f"\t{holder.name} with account number : {holder.account_number} removed from the account holder list")
        else:
            print(f"\t{holder.name.capitalize()} with account number : {holder.account_number} is not found on the account holder list")
    
    def show_account_holders(self):
        if not self.holders:
            print("\tThere are no account holder")
            return
        else:
            print("\nHolders list")
            for holder in self.holders:
                print(f"\tAccount Holder Name : {holder.name}")
                print(f"\tAccount Holder Email : {holder.email}")
                print(f"\tAccount Holder Phone : {holder.phone}")
                print(f"\tAccount Holder address : {holder.address}")
                print(f"\tAccount Number : {holder.account_number}")
                print(f"\tAccount Type : {holder.account_type}")
                print(f"\tAvailable Balance : {holder.balance} BDT")
                print(f"\tAccount Status : {"Active" if holder.active_status else "Inactive"}\n")

    def menu_holder(self, client):
        while True:
            print("Your Options")
            print("1 : Check available balance")
            print("2 : Deposit amount")
            print("3 : Withdraw amount")
            print("4 : Take loan")
            print("5 : Check loan")
            print("6 : Pay loan")
            print("7 : Transfer amount")
            print("8 : Check transaction history")
            print("9 : Logout")
            try:
                option = int(input("Enter the option: "))
            except ValueError:
                print("\tInvalid value.Please enter an integer value")
                continue
            if option == 1:
                print(f"\tAccount Total Balance :{client.balance} BDT\n\tAccount Available Balance : {client.balance-500} BDT")
            elif option == 2:
                try:
                    amount = float(input("Enter the amount to deposit: "))
                except ValueError:
                    print("\tInvalid value.Please enter an float value")
                    continue
                client.deposit(amount)
                print(f"Deposited {amount} BDT. New Balance: {client.balance}")
            elif option == 3:
                if Programmers_Bank.bankrupt == True:
                    print("\tThe bank is bankrupt")
                    continue
                elif client.balance == 500:
                    print("\tWithdrawal amount exceeded")
                    print("Withdrawing your entire balance will deactivate your account.\nConfirm withdrawal Yes or No (Y?N)?")
                    option = input("Enter your choice: ")
                    if option == 'Y' or option == 'y':
                        try:
                            amount = float(input("Enter the amount to withdraw: "))
                        except ValueError:
                            print("\tInvalid value.Please enter an float value")
                            continue
                        if amount > client.balance:
                            print("\tWithdrawal amount exceeded\n")
                            continue
                        client.withdraw(amount)
                        client.active_status = False
                        print(f"Withdraw {amount} BDT. Account deactivated. Deposit at least {amount} BDT to reactivate.\n")
                        return
                    elif option == 'N' or option == 'n':
                        continue
                    else:
                        print(f"'{option}' is an invalid command!")
                        continue
                else:
                    try:
                        amount = float(input("Enter the amount to withdraw: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an float value")
                        continue
                    if amount > client.balance:
                        print("\tWithdrawal amount exceeded\n")
                        continue
                    elif amount == client.balance:
                        print("\n\tWithdrawal amount exceeded")
                        print("Withdrawing your entire balance will deactivate your account. Confirm withdrawal Yes or No (Y?N)?")
                        option = input("Enter your choice: ")
                        if option == 'Y' or option == 'y':
                            client.withdraw(amount)
                            client.active_status = False
                            print(f"Withdraw {amount} BDT. Account deactivated. Deposit at least 500 BDT to reactivate.\n")
                            return
                        elif option == 'N' or option == 'n':
                            continue
                        else:
                            print(f"'{option}' is an invalid command!")
                            continue
                    client.withdraw(amount)
                    print(f"Withdraw {amount} BDT. Total Balance: {client.balance} BDT\n\tAccount Available Balance : {client.balance-500} BDT")
            elif option == 4:
                if self.loan_feature == False:
                    print("\tLoan features is off. You cannot take loan\n")
                    continue
                if client.loan_time == 2:
                    print("\tYou take loan 2 times. Please pay previous loan\n")
                    continue
                try:
                    amount = float(input("Enter the amount to take loan: "))
                except ValueError:
                    print("\tInvalid value.Please enter an float value")
                    continue
                self.take_loan(client,amount)
            elif option == 5:
                print(f"\tTotal loan amount : {client.loan_amout} BDT")
            elif option == 6:
                if client.loan_time == 0 or client.loan_amount == 0:
                    print("\tYou have not taken any loan from the bank")
                    return
                try:
                    amount = float(input("Enter your amount to pay loan: "))
                except ValueError:
                    print("\tInvalid value.Please enter an integer value")
                    continue
                self.pay_loan(client, amount)
            elif option == 7:
                if Programmers_Bank.bankrupt == True:
                    print("\tThe bank is bankrupt")
                    continue
                try:
                    phone = int(input("Enter the recipient's phone number: "))
                except ValueError:
                    print("\tInvalid value.Please enter an integer value")
                    continue
                account_number = input("Enter the recipient's account number: ")
                recipient = self.find_account_holder(phone, account_number)
                try:
                    amount = int(input("Enter the transfer amount: "))
                except ValueError:
                    print("\tInvalid value.Please enter an integer value")
                    continue
                client.money_transfer(recipient, amount)
            elif option == 8:
                client.transaction_history()
            elif option == 9:
                return
            else:
                print("\tInvalid input")

Programmers_Bank = Bank("Bank of Programmer's")

def holder_menu():
    while True:
        print("\nOptions")
        print("1 : Create an account")
        print("2 : Login your account")
        print("3 : Exit")
        try:
            option = int(input("Enter the option: "))
        except ValueError:
            print("\tInvalid value.Please enter an integer value")
            continue
        if option == 1:
            name = input("Enter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            try:
                phone = int(input("Enter your phone number: "))
            except ValueError:
                print("\tInvalid value.Please enter an integer value")
                continue
            address = input("Enter your address: ")
            if not address.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            password = input("Enter your password: ")
            account_number = Programmers_Bank.generate_account_number()
            print("Choose account type")
            print("\t1 : Savings account")
            print("\t2 : Current account")
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("\tInvalid value.Please enter an integer value")
                continue
            if choice == 1:
                account_type = "Savings account"
            elif choice == 2:
                account_type = "Current account"
            else:
                print("Invalid choice")
                continue
            Programmers_Bank.add_account_holder(name, email, phone, address, password, account_number, account_type)
            continue
        elif option == 2:
            email = input("Enter you email: ")
            password = input("Enter your password: ")
            match = False
            for user in Programmers_Bank.holders:
                if user.email == email and user.password == password:
                    match = True
                    client = user
                    break
            if match == False:
                print("\tNo user found")
            else:
                while True:
                    if client.active_status == False:
                        print(f"\nPlease deposit minimum {500-client.balance} BDT to activate your account")
                        print("Options")
                        print("1 : Deposit and active account")
                        print("2 : Pay later and back")
                        try:
                            option = int(input("Enter the option: "))
                        except ValueError:
                            print("\tInvalid value.Please enter an integer value")
                            continue
                        if option == 1:
                            try:
                                amount = float(input("Enter your amount: "))
                            except ValueError:
                                print("\tInvalid value.Please enter an float value")
                                continue
                            if amount < 500:
                                if amount <= 0:
                                    print("\tInvalid deposit amount\n")
                                    continue
                                else:
                                    client.deposit(amount)
                                    print(f"Deposit {500-client.balance} more")
                                    if client.balance >= 500:
                                        client.active_status = True
                                        print(f"\tDeposited {amount} BDT.\n\tTotal balance: {client.balance} BDT\n\tAvailable balance: {client.balance-500} BDT")
                                        print("\tAccount Activated")
                                        print(f"\nWelcome {client.name.capitalize()}")
                                        Programmers_Bank.menu_holder(client)
                                    continue
                            elif amount >= 500:
                                client.deposit(amount)
                                client.active_status = True
                                print(f"\tDeposited {amount} BDT\n\tTotal balance: {client.balance} BDT\n\tAvailable balance: {client.balance-500} BDT")
                                print("\tAccount Activated")
                                print(f"\nWelcome {client.name.capitalize()}")
                                Programmers_Bank.menu_holder(client)
                                break
                        elif option == 2:
                            break
                        else:
                            print("\tInvalid option")
                            continue
                    else:
                        print(f"\nWelcome {client.name.capitalize()}")
                        Programmers_Bank.menu_holder(client)
                        break
        elif option == 3:
            break
        else:
            print("\tInvalid Input")

def admin_menu():
    while True:
        print("\nOptions: ")
        print("1 : Create an account")
        print("2 : Login your account")
        print("3 : Exit")
        try:
            option = int(input("Enter the option: "))
        except ValueError:
            print("\tInvalid value.Please enter an integer value")
            continue
        if option == 1:
            name = input("Enter your name: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            email = input("Enter your email: ")
            try:
                phone = int(input("Enter your phone number: "))
            except ValueError:
                print("\tInvalid value.Please enter an integer value")
                continue
            address = input("Enter your address: ")
            if not name.isalpha():
                print("\tInvalid value.Please enter alphabetic characters only")
                continue
            password = input("Enter your password: ")
            Programmers_Bank.add_user(name, email, phone, address, password)
            continue
        elif option == 2:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            match = False
            for user in Programmers_Bank.users:
                if user.email == email and user.password == password:
                    match = True
                    cur_user = user
                    break
            if match == False:
                print("\tNo user found")
                continue
            while True:
                print(f"\nWelcome {cur_user.name.capitalize()}")
                print("Your options")
                print("1 : Create account for client")
                print("2 : Delete account of client")
                print("3 : See all account holders")
                print("4 : Set the bank balance")
                print("5 : Total available balance")
                print("6 : Total loan amount")
                print("7 : Turn on/off loan feature")
                print("8 : Turn on/off bankrupt feature")
                print("9 : Logout")
                try:
                    option = int(input("Enter option: "))
                except ValueError:
                    print("\tInvalid value.Please enter an integer value")
                    continue
                if option == 1:
                    name = input("Enter your name: ")
                    if not name.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    email = input("Enter your email: ")
                    try:
                        phone = int(input("Enter your phone number: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    address = input("Enter your address: ")
                    if not address.isalpha():
                        print("\tInvalid value.Please enter alphabetic characters only")
                        continue
                    password = input("Enter your password: ")
                    account_number = Programmers_Bank.generate_account_number()
                    print("Choose account type")
                    print("\t1 : Savings account")
                    print("\t2 : Current account")
                    try:
                        choice = int(input("Enter your choice: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    if choice == 1:
                        account_type = "Savings account"
                    elif choice == 2:
                        account_type = "Current account"
                    else:
                        print("\tInvalid choice")
                        continue
                    Programmers_Bank.add_account_holder(name, email, phone, address, password, account_number, account_type)
                    continue
                elif option == 2:
                    if Programmers_Bank.holders == []:
                        print("\tThere are no account holder")
                        continue
                    else:
                        try:
                            phone = int(input("Enter the phone number: "))
                        except ValueError:
                            print("\tInvalid value.Please enter an integer value")
                            continue
                        account_number = input("Enter the account number: ")
                        Programmers_Bank.remove_account_holder(phone, account_number)
                elif option == 3:
                    Programmers_Bank.show_account_holders()
                elif option == 4:
                    try:
                        amount = float(input("Enter the amount to set the bank balance: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    Programmers_Bank.set_bank_balance(amount)
                elif option == 5:
                    if Programmers_Bank.bank_balance == 0 or Programmers_Bank.bank_balance < 5000:
                        print(f"\tAccount Total Balance :{Programmers_Bank.bank_balance} BDT")
                        print(f"\tAccount Available Balance : {Programmers_Bank.bank_balance} BDT")
                    else:
                        print(f"\tAccount Total Balance :{Programmers_Bank.bank_balance} BDT")
                        print(f"\tAccount Available Balance : {Programmers_Bank.bank_balance-5000} BDT")
                elif option == 6:
                    Programmers_Bank.total_loan()
                elif option == 7:
                    print(f"Loan feature is {"on" if Programmers_Bank.loan_feature else "off"}. If you want to {"off" if Programmers_Bank.loan_feature else "on"} loan feature enter option.")
                    print("Options")
                    print("1 : On")
                    print("2 : Off")
                    try:
                        option = int(input("Enter the option: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    if option == 1:
                        if Programmers_Bank.loan_feature == True:
                            print("\tLoan feature is already on")
                            continue
                        Programmers_Bank.loan_feature = True
                        print("\tLoan feature is successfully on")
                    elif option == 2:
                        if Programmers_Bank.loan_feature == False:
                            print("\tLoan feature is already off")
                            continue
                        Programmers_Bank.loan_feature = False
                        print("\tLoan feature is successfully off")
                    else:
                        print("\tInvalid input")
                        continue
                elif option == 8:
                    print(f"Bankrupt feature is {"on" if Programmers_Bank.bankrupt else "off"}. If you want to {"off" if Programmers_Bank.bankrupt else "on"} bankrupt feature enter option.")
                    print("Options")
                    print("1 : On")
                    print("2 : Off")
                    try:
                        option = int(input("Enter the option: "))
                    except ValueError:
                        print("\tInvalid value.Please enter an integer value")
                        continue
                    if option == 1:
                        if Programmers_Bank.bankrupt == True:
                            print("\tBankrupt feature is already on")
                            continue
                        Programmers_Bank.bankrupt = True
                        print("\tBankrupt feature is successfully on")
                    elif option == 2:
                        if Programmers_Bank.bankrupt == False:
                            print("\tBankrupt feature is already off")
                        Programmers_Bank.bankrupt = False
                        print("\tBankrupt feature is successfully off")
                    else:
                        print("\tInvalid input")
                        continue
                elif option == 9:
                    break
        elif option == 3:
            break
        else:
            print("\tInvlid input")
            continue
while True:
    print("""\t\t\t
        ************************************
        *                                  *
        *  Welcome to Bank of Programmer's *
        *                                  *
        ************************************
        \n""")
    print("Use this system as a account holder or as an admin")
    print("Options")
    print("1 : Account Holder")
    print("2 : Bank Admin")
    print("3 : Exit")
    try:
        option = int(input("Enter option: "))
    except ValueError:
        print("\tInvalid value.Please enter an integer value")
        continue
    if option == 1:
        holder_menu()
    elif option == 2:
        admin_menu()
    elif option == 3:
        print("\n\tExiting the system. Have a nice day!")
        break
    else:
        print("\tInvalid Input")
