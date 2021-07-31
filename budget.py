import matplotlib.pyplot as plt
import pandas as pd


def gettotals(categories):
    """
    Gets total expenditure for each category.
    """
    breakdown = []
    for category in categories:
        breakdown.append(category.get_withdrawals())
    final_breakdown = [*map(lambda x:x*(-1), breakdown)]
    return final_breakdown


def create_spend_chart(categories):
    """
    Plots a simple bar chart to display total expenditure for each category.
    """
    spending_breakdown = gettotals(categories)
    category_name = [i.name for i in categories]
    df = pd.DataFrame({'Categories': category_name, 'Spending': spending_breakdown})
    df.plot.bar(x='Categories', ylabel='Spending in dollars', rot=0, legend=False)
    plt.show()


class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = (20 * '*') + self.name + (20 * '*') + '\n'
        items = ""
        total = 0
        for item in self.ledger:
            items += item['description'] + (
                        (len(title) - len(item['description']) - len(str(item['amount']))) * ' ') + str(
                item['amount']) + '\n'

            total += item['amount']

        output = title + items + 'Total: ' + str(total)
        return output

    def deposit(self, amount, description=""):
        """
        Deposit method that accepts an amount and description, and appends these information to a ledger list.
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Withdraw method that is similar to the deposit method, but amount passed to it is a negative number,
        since it is a withdrawal. If not enough funds, add nothing to the ledger. Returns True if withdrawal
        took place, and false if otherwise.
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        """
        Get_balance method that returns current balance of the budget category based on the deposits and withdrawals
        that have occurred.
        """
        current_balance = 0
        for i in self.ledger:
            current_balance += i["amount"]
        return current_balance

    def transfer(self, amount, category):
        """
        Transfer method that accepts an amount and another budget category as arguments. This method allows for
        valid transfers between budget categories.
        """
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    def check_funds(self, amount):
        """
        Check_funds method that is used by both the withdraw and transfer method, to validate whether logical
        withdrawals and transfers can actually be allowed to take place.
        """
        if self.get_balance() >= amount:
            return True
        return False

    def get_withdrawals(self):
        """
        Gets the total amount of withdrawals.
        """
        total = 0
        for item in self.ledger:
            if item["amount"] < 0:
                total += item["amount"]
        return total





