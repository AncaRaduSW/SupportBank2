import csv
import logging
from account import Account
from datetime import datetime


class CsvFileReader:

    @staticmethod
    def read_csv_file(csvFileName):

        accounts = []

        logger = logging.getLogger(__name__)

        with open(csvFileName, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            csvlist = list(csvreader)

            for row in csvlist[1:]:

                # Substract money from sender

                # Check if the amount is a float
                try:
                    float(row[4])
                except ValueError:
                    logger.warning("Amount on line " + str(csvlist.index(row) + 1) + " is not a number!!")
                    continue

                # Check if the date is correct
                if CsvFileReader.correct_date(row[0]) is False:
                    logger.warning("Date on line " + str(csvlist.index(row) + 1) + " is not valid!!")
                    continue

                acc_from = Account.find_account(row[1], accounts)
                if acc_from != False:  # found account
                    acc_from.substract_money(float(row[4]))
                else:  # create new account
                    acc_from = Account(row[1])
                    accounts.append(acc_from)
                    acc_from.substract_money(float(row[4]))

                # Add money to receiver
                acc_to = Account.find_account(row[2], accounts)
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

        return accounts

    @staticmethod
    def correct_date(dateString):
        try:
            datetime.strptime(dateString, '%d/%m/%Y')
        except ValueError:
            return False

        return True
