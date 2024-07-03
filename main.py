import logging
from csvFileReader import CsvFileReader as csv
from jsonFileReader import JsonFileReader as json
from account import Account

# Program start #

# Add logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

logger.info("Starting to run SupportBank")


imported_file = False

logger.info("Starting to enter commands")
new_input = input("Enter command: ")

while new_input != "exit":

    if new_input.split()[0] == "Import" and new_input.split()[1] == "File":
        imported_file = True

        fileName = new_input.split()[2]

        logger.info("Reading from " + fileName + " file")

        accounts = []

        if fileName.split('.')[-1] == "csv":
            accounts = csv.read_csv_file(fileName)
        elif fileName.split('.')[-1] == "json":
            accounts = json.read_json_file(fileName)

        logger.info("Finished reading file")

    elif new_input == "List All":
        if imported_file is False:
            print("No file imported!")
            continue

        for acc in accounts:
            print(acc)

    elif new_input.split()[0] == "List":
        if imported_file is False:
            print("No file imported!")
            continue

        acc = Account.find_account(new_input.split()[1] + " " + new_input.split()[2], accounts)
        if acc != False:
            acc.print_transactions()
        else:
            print("Account not found")

    else:
        print("Command not found")

    new_input = input("Enter command: ")

logger.info("Finished entering commands")
