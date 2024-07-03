import csv
import logging


class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []

    def add_money(self, amount):
        self.balance += amount

    def substract_money(self, amount):
        self.balance -= amount

    def add_transaction(self, date, narrative, amount, paid): # if paid is True -> person sent amount
                                                               # if paid is False -> person received amount
        self.transactions.append((date, narrative, amount, paid))
        self.transactions.sort()

    def print_transactions(self):
        for transaction in self.transactions:
            if transaction[3]:
                print(self.name + " sent amount " + str(transaction[2]) + " on " + transaction[0] + "\nnarrative : " + transaction[1] + "\n")
            else:
                print(self.name + " received amount " + str(transaction[2]) + " on " + transaction[0] + "\nnarrative : " + transaction[1] + "\n")

    def __str__(self):
        if self.balance >= 0:
            return "Name: " + self.name + "\nhas money : " + str(self.balance) + "\n"
        else:
            return "Name: " + self.name + "\nhas debt of : " + str(abs(self.balance)) + "\n"

# Program start

# Add logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

logger.info("Starting to run SupportBank")

accounts = []


def find_account(acc_name):
    for acc in accounts:
        if acc.name == acc_name:
            return acc
    return False


def correct_date(date):
    date_values = date.split('/')

    # Check if the values are int type
    try:
        day = int(date_values[0])
        month = int(date_values[1])
        year = int(date_values[2])
    except ValueError:
        return False

    # Check if the values are physically possible
    if day < 1 or day > 31 or month < 1 or month > 12:
        return False

    return True



csvFileName = input("Enter the name of the csv file: ")

# Read from csv file
logger.info("Reading from " + csvFileName + " file")

with open(csvFileName, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    csvlist = list(csvreader)

    first = True

    for row in csvlist:
        # Skip the first line in the CSV
        if first is True:
            first = False
            continue

        # Substract money from sender

        # Check if the amount is a float
        try:
            float(row[4])
        except ValueError:
            logger.warning("Amount on line " + str(csvlist.index(row) + 1) + " is not a number!!")
            continue

        # Check if the date is correct
        if correct_date(row[0]) is False:
            logger.warning("Date on line " + str(csvlist.index(row) + 1) + " is not valid!!")
            continue

        acc_from = find_account(row[1])
        if acc_from != False:   # found account
            acc_from.substract_money(float(row[4]))
        else:                   # create new account
            acc_from = Account(row[1])
            accounts.append(acc_from)
            acc_from.substract_money(float(row[4]))

        # Add money to receiver
        acc_to = find_account(row[2])
        if acc_to != False:
            acc_to.add_money(float(row[4]))
        else:
            acc_to = Account(row[2])
            accounts.append(acc_to)
            acc_to.add_money(float(row[4]))

        # Add transaction to each account
        acc_from.add_transaction(row[0], row[3], row[4], True)
        acc_to.add_transaction(row[0], row[3], row[4], False)

    csvfile.close()

logger.info("Finished reading from CSV file")

logger.info("Starting to enter commands")
new_input = input("Enter command: ")

while new_input != "exit":
    if new_input == "List All":
        for acc in accounts:
            print(acc)

    elif new_input.split()[0] == "List":
        acc = find_account(new_input.split()[1] + " " + new_input.split()[2])
        if acc != False:
            acc.print_transactions()
        else:
            print("Account not found")

    else:
        print("Command not found")

    new_input = input("Enter command: ")

logger.info("Finished entering commands")
