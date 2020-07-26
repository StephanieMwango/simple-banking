import random
import sqlite3

class CardSystem():
    def __init__(self):
        self.user_card = None
        self.user_pin = None
        self.card_details_dict = {}
        self.top_menu = None
        self.checksum = None
        self.login_input = None
        self.my_dict = {}
        self.conn = sqlite3.connect('card.s3db')
        self.create_table_arg = 'CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT NOT NULL, pin TEXT NOT NULL, balance INTEGER);'
        self.add_value = 'INSERT INTO card (number, pin, balance) VALUES (?, ?, 0);'
        self.ADD_INCOME = 'UPDATE card SET balance = balance + ? WHERE number = ?;'
        self.DELETE_ACCOUNT = 'DELETE FROM card WHERE number = ?;'
        self.CHECK_BALANCE = 'SELECT balance FROM card WHERE number = ?;'
        self.TRANSFER_MONEY = 'UPDATE card SET balance = balance - ? WHERE number = ?;'
        self.GET_CARD_DETAILS = 'SELECT number, pin FROM card WHERE number = ?;'






    def run_menu(self):
        self.connect()
        print('1. Create an account\n2. Log into account\n0. Exit')
        self.top_menu = input()
        if self.top_menu in ['1', '2', '0']:
            if self.top_menu == '0':
                print('Bye!')
                exit()

            if self.top_menu == '1':
                while True:
                    bin_number =  '400000'
                    account_identifier =  self.gen_ran_number_given_size(9)
                    card_number = bin_number + account_identifier
                    self.check_sum(card_number)
                    self.user_card = card_number + self.checksum
                    if self.card_exists(self.user_card) is None:
                        break

                self.user_pin = self.gen_ran_number_given_size(4)
                self.card_details_dict[self.user_card] = self.user_pin
                self.insert_value(self.conn)
                self.details = self.get_details(self.conn, self.user_card)
                print('Your card has been created')
                print('Your card number:')
                print(f'{self.details[0]}')
                print(f'Your card PIN:')
                print(f'{self.details[1]}')
                self.run_menu()

            elif self.top_menu == '2':
                self.login()
        else:
            self.run_menu()


    def login(self):
        
        user_card = input('Enter your card number:\n >')
        user_pin = input('Enter your PIN:\n >')
        self.mdetails = self.get_details(self.conn, user_card)
        
        if self.mdetails is None or user_pin != self.mdetails[1]:
            print('Wrong card number or PIN!')
            self.run_menu()
        elif user_card == self.mdetails[0] and user_pin == self.mdetails[1]:
            print('You have successfully logged in!')
            self.new_login_menu()
            


    def check_sum(self, number):
        num_list = [int(number[i]) for i in range(len(number))]
        num_list = [num_list[i] * 2 if i % 2 == 0 else num_list[i] for i in range(len(num_list))]
        num_list = [num_list[i] - 9 if num_list[i] > 9 else num_list[i] for i in range(len(num_list))]
        num_list = sum(num_list)
        if num_list % 10 == 0:
            self.checksum = '0'
        else:
            total = num_list % 10
            self.checksum = str(10 - total)

    def check_luhn_algorithm(self, number):
        num_list = [int(number[i]) for i in range(len(number))]
        num_list = [num_list[i] * 2 if i % 2 == 0 else num_list[i] for i in range(len(num_list))]
        num_list = [num_list[i] - 9 if num_list[i] > 9 else num_list[i] for i in range(len(num_list))]
        num_list = sum(num_list)
        if num_list % 10 == 0:
            return True
        else:
            return False



    def gen_ran_number_given_size(self, digit_size):
        self.digit_size = digit_size
        return "".join(['{}'.format(random.randint(0, 9)) for num in range(0, digit_size)])
    def connect(self):
        conn = sqlite3.connect('card.s3db')
        return self.create_table(conn)

    def create_table(self, conn):
        with conn:
            return conn.execute(self.create_table_arg)

    def insert_value(self, conn):
        with conn:
            return conn.execute(self.add_value,(self.user_card,self.user_pin))
    def get_details(self, conn, user_card):
        with conn:
            return conn.execute(self.GET_CARD_DETAILS, (user_card,)).fetchone()
    
    def update_income(self,conn, income, number):
        with conn:
            return conn.execute(self.ADD_INCOME, (income, number))

    def delete_account(self, conn):
        with conn:
            return conn.execute(self.DELETE_ACCOUNT, (self.mdetails[0],))
    def check_balance(self, conn):
        with conn:
            return conn.execute(self.CHECK_BALANCE, (self.mdetails[0],)).fetchone()

    def transfer_money(self, conn, money):
        with conn:
            return conn.execute(self.TRANSFER_MONEY, (money, self.mdetails[0]))

    def card_exists(self, transferred_card_number):
        """ Checks if card exists in database. """
        sql = 'SELECT 1 FROM card WHERE number = ?;'

        with self.conn as cur:
           return cur.execute(sql, (transferred_card_number,)).fetchone()

        

    def new_login_menu(self):
        #mydetails = self.get_details(self.conn, user_card)
        action = input('\n 1. Balance\n 2. Add income\n 3. Do transfer\n 4. Close account\n 5. Log out\n 0. Exit\n')
        if action == '1':
            balance = self.check_balance(self.conn)
            print(f'Balance: {balance[0]}')
            self.new_login_menu()
        elif action == '2':
            income = int(input("Enter income:"))
            self.update_income(self.conn,income, self.mdetails[0])
            print('Income was added!')
            self.new_login_menu()

        elif action == '3':
            user_card_transferred_to = input('Transfer\n Enter card number\n').strip()
            if user_card_transferred_to == self.mdetails[0]:
                print("You can't transfer money to the same account!")
                self.new_login_menu()
                
            elif self.check_luhn_algorithm(user_card_transferred_to) == False:
                print('Probably you made mistake in the card number. Please try again!')
                self.new_login_menu()
            else:
                value = self.card_exists(user_card_transferred_to)
                if value is None:
                    print('Such a card does not exist.')
                    self.new_login_menu()
                else:
                    money_transfer = int(input('Enter how much money you want to transfer:'))
                    balance = self.check_balance(self.conn)
                    bal = balance[0]
                    if money_transfer >= bal:
                        print('Not enough money!')
                        self.new_login_menu()
                    else:
                        self.transfer_money(self.conn,money_transfer)
                        self.update_income(self.conn, money_transfer, user_card_transferred_to)
                        print('Success')
                        self.new_login_menu()
       
        elif action == '4':
            self.delete_account(self.conn)
            print('The account has been closed!')
            self.run_menu()
        elif action == '5':
            self.run_menu()
        elif action == '0':
            print('Bye!')
            exit()
        else:
            self.new_login_menu()






cs = CardSystem()
cs.run_menu()
