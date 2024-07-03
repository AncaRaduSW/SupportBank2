class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []

    def add_money(self, amount):
        self.balance += amount

    def substract_money(self, amount):
        self.balance -= amount

    def add_transaction(self, date, narrative, amount, paid):  # if paid is True -> person sent amount
        # if paid is False -> person received amount
        self.transactions.append((date, narrative, amount, paid))
        self.transactions.sort()

    def print_transactions(self):
        for transaction in self.transactions:
            paid = transaction[3]

            if paid is True:    # current account SENT amount
                print(self.name + " sent amount " + str(transaction[2]) + " on " + transaction[0] + "\nnarrative : " +
                      transaction[1] + "\n")
            else:               # current account RECEIVED amount
                print(
                    self.name + " received amount " + str(transaction[2]) + " on " + transaction[0] + "\nnarrative : " +
                    transaction[1] + "\n")

    @staticmethod
    def find_account(acc_name, accounts):
        for acc in accounts:
            if acc.name == acc_name:
                return acc
        return False

    def __str__(self):
        if self.balance >= 0:
            return "Name: " + self.name + "\nhas money : " + str(self.balance) + "\n"
        else:
            return "Name: " + self.name + "\nhas debt of : " + str(abs(self.balance)) + "\n"