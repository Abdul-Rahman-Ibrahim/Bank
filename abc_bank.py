### A class to model ABCBank

#BUGS THAT NEED FIXING
############################################################################################
# Do sth so as to store customers phone number in the columns of 'ABCBank_Customers' file. #
# solve customers with same last name issue.                                               #
############################################################################################

# FEATURES TO BE ADDED
############################################################################################
# Store all available bank acoounts in a folder/file. DONE!                                #
# A function that allows customers to check their balance. DONE!                           #
# A function that allows customers to access their financial transactions. DONE!           #
# Create a seperate python file to interact with customers. DONE!                          #
# Allow transactions with different banks. DONE!                                           #
# Consider exchange rates with different currencies during transfer of money to others.    #
# Modify 'transact' to accept 'checkBalance' and 'getUserTransactions'                     #
############################################################################################

import datetime as dt
import random
import os
import pandas as pd

try:
    os.mkdir('UsersTransactions')
except OSError:
    pass
try:
    os.mkdir('EmptyBankAccountsNumber')
except OSError:
    pass

class ABCBank():
    numbersList = list(str(number) for number in range(1,10)) #generate integers from 1 to 9
    users = {}  #this dictionary stores all the data of customers in a dictionary of dictionaries

    # get the data of costumers from bank path and store in users everytime the ABCBank() is instantized
    folder = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/UsersTransactions/'   #path to all customers transactions.

    # This path of the code assumes that 'ABCBank_Customers.csv' already exists in the desired directory
    try:
        file = open('ABCBank_Customers.csv', 'r')  #'ABCBank.csv' is the filename that stores the information of newly added customers
        firstLine = file.readline()
        for line in file:
            user = {}  #user is a dictionary of each customer.
            line = line.strip().split(',')
            user['Customer Number'] = line[1]
            user['First Name'] = line[3]
            user['Last Name'] = line[4]
            user['Other Name'] = line[5]
            user['Account Type'] = line[6]
            user['Currency'] = line[7]
            user['Phone Number'] = line[-2]
            phoneNumber = line[-2]
            user['Date Joined'] = line[0]
            user['Path'] = line[-1]

            # Opens each customer's transaction file to get their balance and bank account number and store in the user dictionary accordingly.
            # This part of the code assumes that the customer's transaction file already exist in the desired directory.
            try:
                tmpPath = folder + user['Last Name']+user['Customer Number']+'.csv'
                tmpFile = open(tmpPath, 'r')
                balance = tmpFile.readlines()[-1].strip().split(',')[-1]
                user['Balance'] = balance
                tmpFile.close()
            except IOError:
                pass
            users[line[2]] = user  #line[2] = the bank account number of customer
        file.close()
    except IOError:
        pass
    
    def __init__(self):
        print('WELCOME TO ABC BANK')

    def addUser(self, firstName, lastName, otherName='None', phoneNumber='None', accountType='Current', currency='USD', tmpDeposit='5'):
        """
        Initializing new customer to ABC Bank.
        Each new customer is given a customer number in addition to the their bank account number
        Customers are advised to keep their customer and bank account numbers secured
        
        Fields with '*' are required fields.
        
        PARAMETERS
            *firstName
            *lastName
             otherName
             phoneNumber
             accountType
                 default account type is 'Current'
             currency
                 default currency is United States Dollars (USD)
             tmpDeposit
                 an initial deposit minimum of 5 in the desired currency
        """
        
        self.accountNumbersList = [random.choices(self.numbersList, k=13) for _ in range(15000)] #create 15,000 lists of 9 digits numbers
        self.customerNumber = '1' #initialize first customer's number
        self.firstName = firstName
        self.lastName = lastName
        self.otherName = otherName
        self.fullName = firstName +' '+ str(otherName) +' '+ lastName
        if otherName == 'None':
            self.fullName = firstName +' '+ lastName
        self.phoneNumber = str(phoneNumber)
        
        self.accountType = accountType
        self.currency = currency
        self.accountNumber = self.initializeCustomerAccountNumber() #get account number for new customer
        
        self.balance = 0.00
        
        date = str(dt.datetime.now().year) + '-' + str(dt.datetime.now().month) + '-' + str(dt.datetime.now().day)
        self.path = self.lastName + self.customerNumber + '.csv'
        
        accNumber = self.accountNumber
        #print(self.firstName+'\'s account number is '+''.join(accNumber)) #print account number for customer

        # Add customer to 'ABCBank_Customers.csv'
        try:
            file = open('ABCBank_Customers.csv', 'r')
            lastLine = file.readlines()[-1].strip()
            lastLine = lastLine.split(',')
            self.customerNumber = str(int(lastLine[1])+1)
            self.path = self.lastName + self.customerNumber +'.csv'
        except IOError:
            file = open('ABCBank_Customers.csv', 'a')
            file.write('Date,'+'Customer number,'+'Account number,'+'First name,'+'Last name,'+'Other name,'+'Account type,'+
                        'Currency,'+'Phone Number,'+'Path'+'\n')
            file.write(date +','+ str(1) +','+ accNumber +','+ self.firstName +','+ self.lastName +','+ str(self.otherName)
                            +','+ self.accountType +','+ self.currency +','+self.phoneNumber+','+self.path+ '\n')
        else:
            file = open('ABCBank_Customers.csv', 'a')
            self.path = self.lastName + self.customerNumber +'.csv'
            file.write(date +','+ self.customerNumber +','+ accNumber +','+ self.firstName +','+ self.lastName +','+ str(self.otherName)
                            +','+ self.accountType +','+ self.currency +','+self.phoneNumber+','+self.path+ '\n')
        finally:
            file.close()
            print(self.firstName+' succesfully added to ABCBank_Customers')
            self.usersDataBase(currency+' '+str(self.balance))

        # Make first transaction for user.
        # This allows the customer to be added to the 'Customers Transactions' path
        self.transact(self.accountNumber, tmpDeposit, 'Deposit', reference='ABC Bank',reason='Account Fee')
        
    def initializeCustomerAccountNumber(self):
        '''
        Gets account Number for new customer
        Method not accessible to staff or customers.
        This method is controlled internally by the program to assign bank account to new customer.
        '''

        # This part of code opens the path to all available unused bank account numbers and assign one to the new customer.
        # Create a temporary file to copy the content of unused bank accounts after assigning an account to the new customer.
        
        folder = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/EmptyBankAccountsNumber/'  #path to all available unused account numbers
        fileName = 'Available_Bank_Accounts.csv'
        filePath = folder + fileName
        tmpFileName = 'Available_Bank_Accounts.tmp' 
        tmpFilePath = folder + tmpFileName
        
        try:
            file = open(filePath, 'r')
            tmpFile = open(tmpFilePath, 'w')
            firstLine = file.readline()
            
            for line in file:
                tmpFile.write(line)

            file.close()
            tmpFile.close()
            os.remove(filePath)
            os.rename(tmpFilePath, filePath)
            accNumber = firstLine.strip()
            return accNumber #returns bank account number to new customer
        
        except IOError:
            file = open(filePath, 'w')
            # Get first ever bank account number to first ever customer. This customer is special. :)
            # Once ABCBank is launched and a first customer is registered, this part of the progrma won't be used again.
            count = 1
            for accNumber in self.accountNumbersList:
                if count == 1:
                    count += 1
                    continue
                accNumber.append('\n')
                file.write(''.join(accNumber))
            file.close()

            accNumber = self.accountNumbersList[0] #here, accNumber is a list of one element containg the bank account number
            return ''.join(accNumber)              #accNumber is changed to string by using the '.join' method and then returned.
                
    def usersDataBase(self, balance):
        '''
        Updates a customer's data after every successful transaction
        This method is neither accesible to customers nor staffs.
        This method is controlled internally by the program after every transaction.
        
        PARAMETERS

        *balance
            get the remaining balance from whoever call this method.
            'balance' is a string with the currency and number. e.g USD 3900.00
        '''
        
        user = {}
        user['Customer Number'] = self.customerNumber
        user['First Name'] = self.firstName
        user['Last Name'] = self.lastName
        user['Other Name'] = self.otherName
        user['Account Type'] = self.accountType
        user['Currency'] = self.currency
        user['Phone number'] = self.phoneNumber
        user['Date Joined'] = date = str(dt.datetime.now().year) + '-' + str(dt.datetime.now().month) + '-' + str(dt.datetime.now().day)
        user['Path'] = self.lastName+self.customerNumber+'.csv'
        user['Balance'] = balance
        self.users[self.accountNumber] = user  #updates the main dictionary, 'users' by assigning the updated user's dictionary
        return self.users

    def getData(self, accountNumber):
        '''
        'getData' updates customer's data after transaction. This is quite similar to 'usersDataBase' method
        but the 'getData' accepts accountNumber of customer as parameter. This method is neither accesible to
        customers nor staffs. This method is controlled internally by the program after transactions.

        PARAMETERS

        *accountNumber
            bank account number of customer
        '''
        
        self.accountNumber = accountNumber
        self.firstName = self.users[accountNumber]['First Name']
        self.lastName = self.users[accountNumber]['Last Name']
        self.otherName = self.users[accountNumber]['Other Name']
        self.fullName = self.firstName + ' ' + self.lastName
        if self.otherName != 'None':
            self.fullName += ' '+self.otherName
        self.customerNumber = self.users[accountNumber]['Customer Number']
        self.accountType = self.users[accountNumber]['Account Type']
        self.currency = self.users[accountNumber]['Currency']
        #self.phoneNumber = self.users[accountNumber]['Phone Number']
        self.balance = float(self.users[accountNumber]['Balance'][len(self.currency)+1:])

    def transact(self, accountNumber, amount, transactionType, toAccountNumber='N/A', reference='None', reason='None'):
        self.getData(str(accountNumber))
        '''
        Interacts with customers to carry out transactions such as making deposit('Deposit'),
        withdrawing funds('Withdraw'), and transfering funds('Transfer')
        # This will be updated in the future to allow customers to check their remaining balance
        # and check their transactions

        PARAMETERS

        *accountNumber
            account Number
        *amount
            amount of money to deposit, withdraw, or transfer
        *transactionType
            'Deposit', 'Withdraw', or 'Transfer'
        toAccountNumber
            bank account number of the recepient
            default value = 'N/A'
            if transaction is 'Transfer', 'toAccountNumber' becomes a required field.
        reference
            default value = 'N/A'
        reason
            default value = 'N/A'
        '''
        
        if transactionType.lower() == 'withdraw':
            self.withdraw(accountNumber, amount, toAccountNumber, reference, reason) #calls the withdraw method
        elif transactionType.lower() == 'deposit':
            self.makeDeposit(accountNumber, amount, toAccountNumber, reference, reason) #calls the makeDeposit method
        elif transactionType.lower() == 'transfer':
            while toAccountNumber == 'N/A':
                toAccountNumber = input('Please enter recepient\'s account number ')
            if str(toAccountNumber)  in self.users:
                reason = 'Sent to '+self.users[str(toAccountNumber)]['Last Name']
            self.transfer(accountNumber, amount, toAccountNumber, reference, reason) #calls the transfer method

    def withdraw(self, accountNumber, amount, toAccountNumber, reference, reason):
        '''
        'withdraw' is neither accesible by staff nor customers. The sytem runs this methode during
        successive withdrawal.
        '''
        date = str(dt.datetime.now())
        i = date.index('.')
        date = date[:i]
        
        if float(amount) > float(self.balance):
            print('Can\'t withdraw due to insufficient balance.')
        else:
            self.balance -= float(amount)
            self.userTransactions(date, 'Withdrawal', amount, accountNumber, toAccountNumber, reference, reason)

    def makeDeposit(self, accountNumber, amount, toAccountNumber, reference, reason):
        '''
        'makeDeposit' is neither accesible by staff nor customers. The sytem runs this methode during
        successive bank deposit.
        '''
        date = str(dt.datetime.now())
        i = date.index('.')
        date = date[:i]
        self.balance += float(amount)
        self.userTransactions(date, 'Deposit', amount, accountNumber, toAccountNumber, reference, reason)

    def transfer(self, accountNumber, amount, toAccountNumber, reference='None', reason='None'):
        '''
        'transfer' is neither accesible by staff or customers. The sytem runs this methode during
        successive funds transfer.
        '''
        date = str(dt.datetime.now())
        i = date.index('.')
        date = date[:i]

        if float(amount) > float(self.balance):
            print('Can\'t transfer due to insufficient balance.')
        else:
            self.balance -= float(amount)
            self.userTransactions(date, 'Transfer', amount, accountNumber, toAccountNumber, reference, reason)
            self.updateRecepient(date, amount, str(accountNumber), str(toAccountNumber), str(reference))

    def checkBalance(self, customerNumber):
        for accNum, data in self.users.items():
            if str(customerNumber) == data['Customer Number']:
                convertedBalance = data['Balance']
                print('CURRENT BALANCE      ', convertedBalance)
                break

    def getUserTransactions(self, accountNumber, num=30):
        print('Getting your last {0} transactions'.format(num))
        accountNumber = str(accountNumber)
        folder = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/UsersTransactions/'
        fileName = self.users[accountNumber]['Last Name'] + self.users[accountNumber]['Customer Number'] + '.csv'
        filePath = folder + fileName

        def splitDate(row):
            row['Date'] = row['Transaction Date'][:10]
            row['Time'] = row['Transaction Date'][11:16]
            return row
        
        try:
            df = pd.read_csv(filePath)
            df = df.apply(splitDate, axis=1)
            df = df[['Date','Time','Reason','Transaction Type','Balance']]
            df = df.rename(columns={'Transaction Type':'Transaction'})
            df = df.set_index('Date')
            print(df[-num:])
        except IOError:
            print('Sorry no customer with account number {0} exist in our system'.format(accountNumber))

    def updateRecepient(self, date, amount, accountNumber, toAccountNumber, reference):
        '''
        Updates recepient's data if a customer in ABC bank receives funds.
        Inacessible to customers and staff
        '''
        folder = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/UsersTransactions/'
        toFilePath = folder + self.users[toAccountNumber]['Path']
        
        reason = 'None'
        if reason == 'None':
            reason = 'From '+self.users[accountNumber]['Last Name']
        try:
            file = open(toFilePath, 'r')
            balance = float(file.readlines()[-1].strip().split(',')[-1][len(self.currency)+1:])
            balance += float(amount)
        except IOError:
            pass
        else:
            file = open(toFilePath, 'a')
            currency = self.users[str(toAccountNumber)]['Currency']
            convertedAmount = currency + ' ' + str('%.2f'%float(amount))
            balance = currency+' '+str(balance)
            reason = 'From '+self.users[accountNumber]['Last Name']
            file.write(str(date)+','+'Payment'+','+convertedAmount+','+'My Account'+
                       ','+str(reference)+','+reason+','+str(balance)+'\n')
            self.getData(toAccountNumber)
            self.usersDataBase(balance)
        finally:
            file.close()

    def userTransactions(self, date, transactionType, amount, accountNumber, toAccountNumber, reference, reason):
        """
        Innaccesible method.
        """
        
        folderName = 'C:/Users/Abdul-Rahman/Desktop/Python/Bank/UsersTransactions/'
        fileName = self.lastName
        
        # Getting customer number
        for accNumber, data in self.users.items():
            if str(accNumber) == str(accountNumber):
                customerNumber = str(data['Customer Number'])
                break
        fileName += customerNumber+'.csv'
        filePath = folderName + fileName
        #filePath = folderName + self.path
        currency = self.currency
        convertedAmount = currency+' '+'%.2f'%float(amount)
        balance = currency+' '+'%.2f'%self.balance
        recepient = 'N/A'
        if transactionType.lower() == 'transfer':
            recepient = self.users[str(toAccountNumber)]['Last Name']
            if reason == 'None':
                reason = 'To '+ recepient
        
        try:
            file = open(filePath, 'r')
        except IOError:
            file = open(filePath, 'w')
            file.write('Transaction Date,'+'Transaction Type,'+'Amount,'+'Recepient,'+'Reference,'+'Reason,'+'Balance'+'\n')
            file.write(str(date)+','+transactionType+','+str(convertedAmount)+','+str(recepient)+','+str(reference)+
                       ','+reason+','+str(balance)+'\n')
        else:
            file = open(filePath, 'a')
            file.write(str(date)+','+transactionType+','+str(convertedAmount)+','+str(recepient)+','+str(reference)+
                       ','+reason+','+str(balance)+'\n')
        finally:
            file.close()
            self.printReceipt(transactionType, float(amount), accountNumber, toAccountNumber)
            self.usersDataBase(balance)

    def getReceiptNumber(self):
        try:
            file = open("receiptNumber.txt")  
        except IOError:
            file = open("receiptNumber.txt", "w")
            number = 1
            file.write(str(1))
            file.close()
            return str(number)
        else:
            tmp_file = open("receiptNumber.tmp", "w")
            number = int(file.readline()) + 1
            tmp_file.write(str(number))
            tmp_file.close()
            file.close()
            os.remove("receiptNumber.txt")
            os.rename("receiptNumber.tmp", "receiptNumber.txt")
            return number
        
    def printReceipt(self, transactionType, amount, accountNumber, toAccountNumber):
        print('-'*38)
        print()
        print("\a")
        print("ABC BANK")
        print("Plot 54 Block H, Tafo, Kumasi-Ghana")
        print()
        date = str(dt.datetime.now())[:10]
        time = str(dt.datetime.now())[11:19]
        receiptNumber = self.getReceiptNumber()
        print(date,"\t\t" + "Receipt NO:" + str(receiptNumber))
        print("TIME: {0}".format(time))
        print()
        print('FULL NAME', ' '*13, self.fullName)
        print('ACCOUNT NUMBER' + ' '*10 + '*'*(len(self.accountNumber)-4)+ str(self.accountNumber[-4:]))
        print('TRANSACTION TYPE' +' '*8 + transactionType)
        print('AMOUNT' + ' '*18 + self.currency+' '+'%.2f'%amount)
        
        if transactionType.lower() == 'transfer':
            if str(toAccountNumber) not in self.users:
                recepientName = 'Random Person'
            else:
                recepientName = self.users[str(toAccountNumber)]['First Name'] + ' '+ self.users[str(toAccountNumber)]['Last Name']
                if self.users[str(toAccountNumber)]['Other Name'] != 'None':
                    recepientName += ' '+ self.users[str(toAccountNumber)]['Other Name']
            print()
            print('RECEPIENT\'S INFORMATION')
            print('-'*23)
            print('RECEPIENT NO.', ' '*9, str(toAccountNumber))
            print('RECEPIENT NAME', ' '*8, recepientName)
        print('-'*38)

        

b = ABCBank()

### AFTER THIS PROGRAM, FOCUS ON APPLYING YOUR PYTHON SKILLS TO AREAS IN ENGINEERING.
### MAY GOD BE WITH YOU.
