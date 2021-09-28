# Write your code here
import random
import sqlite3

account_db = {}

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


CREATE_CARD_TABLE = """CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY, 
number TEXT, 
pin TEXT, 
balance INTEGER DEFAULT 0
);"""

INSERT_CARD = "INSERT INTO card (number, pin) VALUES (?, ?)"
UPDATE_BALANCE = "UPDATE card SET balance = ? WHERE number = ?"
GET_CARD_BY_PIN = "SELECT number FROM card WHERE pin = ?;"
GET_PIN_BY_CARD = "SELECT pin FROM card WHERE number = ?;"
GET_BALANCE_BY_NUMBER = "SELECT balance FROM card where number = ?;"
GET_CARD_NUMBER = "SELECT number FROM card WHERE number = ?;"
DELETE_ACCOUNT = "DELETE FROM card WHERE number = ?;"

cur.execute(CREATE_CARD_TABLE)


def creat_account():
    account_id = 0
    balance = 0
    print("Your card has been created")

    cust_num = ""
    for x in range(9):
        cust_num += str(random.randint(0, 9))
    account_num = "400000" + cust_num
    account_num = luhn_algorithm_check(account_num)

    pin = ""
    for x in range(4):
        pin += str(random.randint(0, 9))

    account_db[account_num] = pin
    account_id += 1

    cur.execute(INSERT_CARD, (account_num, pin))
    conn.commit()
    print("Your card number:")
    print(cur.execute(GET_CARD_BY_PIN, (pin,)).fetchone()[0])
    print()
    print("Your card PIN:")
    print(cur.execute(GET_PIN_BY_CARD, (account_num,)).fetchone()[0])
    print()


def luhn_algorithm_check(account_num):
    account_num_list = list(account_num)
    for x in range(15):
        account_num_list[x] = int(account_num_list[x])
        if x == 15:
            continue
        elif x % 2 == 0:
            account_num_list[x] = account_num_list[x] * 2
            if account_num_list[x] > 9:
                account_num_list[x] = account_num_list[x] - 9
    sum_account_num_list = sum(account_num_list)
    if sum_account_num_list % 10 != 0:
        check_sum = (10 - (sum_account_num_list % 10))
    else:
        check_sum = 0
    account_num += str(check_sum)
    return account_num


def login():
    print("Enter you card number:")
    acct_num = input()
    print("Enter your PIN:")
    pin = input()

    card_from_pin = cur.execute(GET_CARD_BY_PIN, (pin,)).fetchone()
    pin_from_card = cur.execute(GET_PIN_BY_CARD, (acct_num, )).fetchone()

    if card_from_pin is None or pin_from_card is None:
        print("Wrong card number or PIN!\n")

    elif card_from_pin[0] == acct_num and pin_from_card[0] == pin:
        print("You have successfully logged in!")
        while True:

            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")

            response = input()

            if response == "1":
                print(cur.execute(GET_BALANCE_BY_NUMBER, (acct_num,)).fetchone()[0])

            if response == "2":
                print("Enter income:")
                deposit = int(input())
                income = cur.execute(GET_BALANCE_BY_NUMBER, (acct_num,)).fetchone()[0] + deposit
                cur.execute(UPDATE_BALANCE, (income, acct_num))
                conn.commit()
                print("Income was added!")

            if response == "3":
                print("Transfer")
                print("Enter card number: ")
                acct_number = input()
                if acct_number[-1] != luhn_algorithm_check(acct_number[:15])[-1]:
                    print("Probably you made a mistake in the card number. Please try again!")
                elif cur.execute(GET_CARD_NUMBER, (acct_number,)).fetchone() is None:
                    print("Such a card does not exist.")
                elif acct_number == acct_num:
                    print("You can't transfer money to the same account!")
                else:
                    print("Enter how much money you want to transfer")
                    amt = int(input())
                    if cur.execute(GET_BALANCE_BY_NUMBER, (acct_num,)).fetchone()[0] < amt:
                        print("Not enough money!")
                    else:
                        debit_acc = cur.execute(GET_BALANCE_BY_NUMBER, (acct_num, )).fetchone()[0]
                        cur.execute(UPDATE_BALANCE, ((debit_acc - amt), acct_num))
                        conn.commit()

                        credit_acc = cur.execute(GET_BALANCE_BY_NUMBER, (acct_number, )).fetchone()[0]
                        cur.execute(UPDATE_BALANCE, ((credit_acc + amt), acct_number))
                        conn.commit()

                        print("Success!")

            if response == "4":
                cur.execute(DELETE_ACCOUNT, (acct_num,))
                conn.commit()

                print("The account has been closed!")

            if response == "5":
                print("You have successfully logged out!\n")
                break

            if response == "0":
                print("Bye!\n")
                exit(0)
    else:
        print("Wrong card number or PIN!\n")


if __name__ == "__main__":
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

        res = input()

        if res == "1":
            creat_account()
        if res == "2":
            login()
        if res == "0":
            print("Bye!")
            exit(0)
