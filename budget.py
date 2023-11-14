class Category:
    # Initialize the instance with its name, the balance starting at 0.00, and a list of dictionaries for the ledger.
    def __init__(self, name: str) -> None:
        self.name = name
        self.balance = 0.00
        self.ledger = []
    
    # Construct the string representation of each Category class. This string representation shows all transactions within the category and the current balance. 
    def __repr__(self) -> str:
        line_width = 30
        return_string = [self.name.center(line_width, '*')]

        for transaction in self.ledger:
            amount = self._stringify_amount(transaction['amount'])
            truncated_max_length = line_width - len(amount) - 1
            trunc_description = transaction['description'][:truncated_max_length]
            spacing = ' ' * (line_width - len(amount) - len(trunc_description))
            return_string.append(f'{trunc_description}{spacing}{amount}')
        
        return_string.append(f'Total: {self._stringify_amount(self.balance)}')
        
        return '\n'.join(return_string)

    # The deposit method adds the amount specified to the balance and keeps track of all the transactions that occur within the ledger.
    def deposit(self, amount: int | float, description = '') -> None:
        self.ledger.append({ 'amount': amount, 'description': description })
        self.balance += amount
    
    # The withdrawal method determines if the amount of the withdrawal is less than or equal to the current balance in the account; if so, it reduces the ledger by the specified amount, adds the transaction to the ledger, and returns True. If the amount of the withdrawal is larger than the balance, the transaction is not processed and False is returned. 
    def withdraw(self, amount: int | float, description = '') -> bool:
        if self.check_funds(amount):
            self.ledger.append({ 'amount': -amount, 'description': description })
            self.balance -= amount
            return True

        return False
    
    # The get_balance method returns the balance rounded to two decimal places. 
    def get_balance(self) -> float:
        return round(self.balance, 2)
    
    # The transfer method determines whether the requested transfer amount is less than or equal to the balance in the account; if so it withdraws funds from one category and deposits the funds into the other category. Both transactions are logged on their respective category's ledger and True is returned. If the transfer amount is larger than the balance, the transaction is not processed and False is returned.
    def transfer(self, amount: int | float, other_category: 'Category') -> bool:
        if self.check_funds(amount):
            self.ledger.append({ 'amount': -amount, 'description': f'Transfer to {other_category.name}' })
            self.balance -= amount
            other_category.ledger.append({ 'amount': amount, 'description': f'Transfer from {self.name}' })
            other_category.balance += amount
            return True

        return False

    # The check_funds method returns a boolean value of whether the balance in the account is greater than or equal to the amount passed in as an argument. 
    def check_funds(self, amount: int | float) -> bool:
        return self.balance >= amount

    # The get_expenses method returns the sum total of all debit transactions on the account rounded to two decimal places.
    def get_expenses(self) -> float:
        return round(sum([ -transaction['amount'] for transaction in self.ledger if transaction['amount'] < 0 ]), 2)
    
    # The _stringify_amount helper method converts an integer or float value passed in as an argument to its two-digit decimal string representation
    def _stringify_amount(self, num: int | float) -> str:
        return f'{num:.2f}'


def create_spend_chart(categories: list[Category]) -> str:
    # Preprocess constants and lists of values that will be used for later calculations
    total_spending = sum(category.get_expenses() for category in categories)
    percentages = []
    labels = []
    max_label_length = 0
    col_width = 3
    space = ' '.center(col_width)
    indent = 4
    printout = ['Percentage spent by category']

    # Iterate through each category in the list of categories and obtain the percentage each category contributes to the total expenses, the category names, and the max length of the label for later processing. 
    for category in categories:
        percentages.append(int(category.get_expenses() / total_spending * 100))
        labels.append(category.name)
        max_label_length = max(max_label_length, len(category.name))
    
    # CREATE THE GRAPH 
    # Iterate from 100 to 0 by 10's and create the 
    for row in range(100,-1,-10):
        point = 'o'.center(col_width)
        temp_row = [f'{row}|'.rjust(indent)]
        
        # Determine if the percentage for each category is greater than or equal to the current value of the iterator; if so, add the 'o' character to simulate the graph, otherwise, leave it blank by adding the adequate amount of spacing. 
        for percentage in percentages:
            graph_row = point if percentage >= row else space
            temp_row.append(graph_row)

        temp_row.append(' ')
        printout.append(''.join(temp_row))

    # ADD THE BOTTOM ROW OF THE GRAPH
    divider_row = ''.rjust(indent).ljust(len(printout[-1]), '-')
    printout.append(divider_row)
    
    # ADD THE LABELS
    # Iterate up to the max_label_length value calculated earlier. Add the corresponding letter to each row (as applicable) on each iteration so that the label is written vertically.
    for i in range(max_label_length):
        temp_row = [''.rjust(indent)]
        
        for label in labels:
            temp_row.append(label[i].center(col_width) if i < len(label) else space)
        
        temp_row.append(' ')
        printout.append(''.join(temp_row))

    # Return the string representation of the graph created with each row on a new line. 
    return '\n'.join(printout)
