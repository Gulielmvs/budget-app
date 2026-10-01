class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        cat_title = f'{self.name:*^30}\n'
        cat_list = ''
        cat_total = f'Total: {self.get_balance()}'
        for i in range(len(self.ledger)):
            if self.ledger[i]['amount'] >= 10000 or self.ledger[i]['amount'] <= -1000:
                ledger_amount = f"{self.ledger[i]['amount']:.0e}"
            else:
                ledger_amount = f"{self.ledger[i]['amount']:.2f}"
            cat_list += f"{self.ledger[i]['description'][:23]:<23}{ledger_amount:>7}\n"
        display = cat_title + cat_list + cat_total
        return display

    def deposit(self, amount, description=''):
        if amount > 0:
            d = {'amount': amount, 'description': description}
            self.ledger.append(d)

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            w = {'amount': amount * -1, 'description': description}
            self.ledger.append(w)
            return True
        else:
            return False

    def get_balance(self):
        amount_total = 0
        for i in range(len(self.ledger)):
            amount_total += self.ledger[i]['amount']
        return amount_total

    def transfer(self, amount, cat_obj):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {cat_obj.name}')
            cat_obj.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance() or amount <= 0:
            return False
        else:
            return True


def create_spend_chart(categories):

    category_spent = []
    percentage_spent = []
    title = 'Percentage spent by category\n'
    labels = ''
    largest = 0
    limit = len(categories)
    # if limit > 4:
    #    limit = 4
    dashes = '    ' + '-' * (limit * 3 + 1) + '\n'
    names = ''
    spent_total = 0
    for item in range(limit):
        # largest name
        if len(categories[item].name) > largest:
            largest = len(categories[item].name)
        # withdrawals per Category
        withdrawals = 0
        for i in range(len(categories[item].ledger)):
            if categories[item].ledger[i]['amount'] < 0:
                withdrawals += categories[item].ledger[i]['amount']
        withdrawals *= -1
        category_spent.append(withdrawals)
        # spent total
        spent_total += withdrawals
    # percentage
    for n in range(len(category_spent)):
        if spent_total > 0:
            percentage = category_spent[n] / spent_total * 100
        else:
            percentage = 0
        percentage_spent.append(percentage)
    # labels - bars
    for n in reversed(range(0, 110, 10)):
        labels += f'{n:3}|'
        for i in range(len(percentage_spent)):
            bar = ' '
            if percentage_spent[i] != 0 and percentage_spent[i] >= n:
                bar = 'o'
            # only first loop
            if i == 0:
                labels += f'{bar:>2}'
            else:
                labels += f'{bar:>3}'
        labels += '  \n'
    # vertically names
    for n in range(largest):
        names += '   '
        for i in range(limit):
            try:
                letter = categories[i].name[n]
            except:
                letter = ' '
            names += f'{letter:>3}'
        names += '  \n'
    chart = title + labels + dashes + names.rstrip('\n')
    return chart
