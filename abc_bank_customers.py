from random import choice
from abc_bank import ABCBank

newCustomersFilePath = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/NewCustomers/new_customers.csv'
newCustomersFileHandle = open(newCustomersFilePath, 'r')
newCustomersFileHandle.readline()

bank = ABCBank()
accountTypes = ['Current','Savings','Fixed-Deposit']
currencies = ['USD','GHC','GBP','EUR','YEN','CFA', 'TL']
bankAccountFee = '10'

for customerInfo in newCustomersFileHandle:
    customerInfo = customerInfo.strip().split(',')
    firstName = customerInfo[0]
    lastName = customerInfo[1]
    currency = choice(currencies)
    bank.addUser(firstName, lastName, accountType=choice(accountTypes), currency=choice(currencies), tmpDeposit=bankAccountFee)
    
newCustomersFileHandle.close()
