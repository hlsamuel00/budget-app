class Category:
    def __init__(self, name):
        self.name = name
        self.balance = 0.00
        self.ledger = []
    
    def __repr__(self):
        line_width = 30
        stars = '*' * int((line_width - len(self.name)) / 2)
        string = stars + self.name + stars + '\n'
        for transaction in self.ledger:
            description = transaction['description'][:23]
            amount = f"{transaction['amount']:.2f}"[:7].rjust(int(line_width - len(description) - 1))
            string += f'{description} {amount}\n'
        string += f'Total: {self.str_balance()}'
        return string

    def deposit(self, amount, description = ''):
        self.ledger.append({ 'amount': amount, 'description': description })
        self.balance += amount
    
    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({ 'amount': -amount, 'description': description })
            self.balance -= amount
            return True
        else:
            return False
    
    def get_balance(self):
        return round(self.balance, 2)
    
    def str_balance(self):
        return f'{self.balance:.2f}'

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.ledger.append({ 'amount': -amount, 'description': f'Transfer to {other_category.name}' })
            self.balance -= amount
            other_category.ledger.append({ 'amount': amount, 'description': f'Transfer from {self.name}' })
            other_category.balance += amount
            return True
        else:
            return False

    def check_funds(self, amount):
        return self.balance >= amount

    def get_expenses(self):
        return round(sum([ -transaction['amount'] for transaction in self.ledger if transaction['amount'] < 0 ]), 2)


def create_spend_chart(categories):
    total = sum( [ category.get_expenses() for category in categories ])
    percentages = [ int((category.get_expenses() / total)* 100)  for category in categories ]
    labels = [ category.name for category in categories ]
    string = 'Percentage spent by category\n'

    label_length = max([len(label) for label in labels])

    for column in range(100,-1,-10):
        string += f'{str(column).rjust(3)}|'
        for i in range(len(percentages)):
            string += ' o ' if percentages[i] >= column else ' ' * 3
        string += ' \n'
    
    string += ('    ' + '-' * 10 + '\n')
    
    for i in range(label_length):
        string += '    '
        
        for label in labels:
            string += f' {label[i]} ' if i < len(label) else '   '      
        
        if i < label_length - 1:
            string += ' \n'
        else:
            string += ' ' 
    
    return string
