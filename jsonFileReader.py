import json
import logging
from account import Account
from datetime import datetime
import dateutil.parser


class JsonFileReader:

    @staticmethod
    def read_json_file(jsonFileName):

        accounts = []

        logger = logging.getLogger(__name__)

        # Opening JSON file
        f = open(jsonFileName)

        # JSON object
        data = json.load(f)

        for values in data:

            dateString = values['Date']
            from_acc = values['FromAccount']
            to_acc = values['ToAccount']
            narrative = values['Narrative']
            amount = values['Amount']

            # Substract money from sender

            # Check if the amount is a float
            try:
                float(amount)
            except ValueError:
                logger.warning("Amount on line " + str(data.index(values) + 1) + " is not a number!!")
                continue

            # Check if the date is correct
            if JsonFileReader.correct_date(dateString) is False:
                logger.warning("Date on line " + str(data.index(values) + 1) + " is not valid!!")
                continue

            acc_from = Account.find_account(from_acc, accounts)
            if acc_from != False:  # found account
                acc_from.substract_money(float(amount))
            else:  # create new account
                acc_from = Account(from_acc)
                accounts.append(acc_from)
                acc_from.substract_money(float(amount))

            # Add money to receiver
            acc_to = Account.find_account(to_acc, accounts)
            if acc_to != False:
                acc_to.add_money(float(amount))
            else:
                acc_to = Account(to_acc)
                accounts.append(acc_to)
                acc_to.add_money(float(amount))

            # Add transaction to each account
            acc_from.add_transaction(dateString, narrative, amount, True)
            acc_to.add_transaction(dateString, narrative, amount, False)

        f.close()

        return accounts

    @staticmethod
    def correct_date(dateString):
        try:
            dateutil.parser.parse(dateString)
        except ValueError:
            return False

        return True
