# FEATURES TO ADD
# 1. After user enters information to sign up, create new window to make user confirm
# the correctness of the information entered. Update the addUser method to add this feature

# 2. Allow user to be able to go back to previous window. Try storing all opened windows in a 1D dictionary

# 3. Make proper positioning of frames in each window and add some formatting

import tkinter
import tkinter.messagebox
from PIL import ImageTk, Image

#get the directory of filepaths.py and abc_bank.py
import os
bankFilePath = os.getcwd()
bankFilePath = bankFilePath.split('\\')
bankFilePath = bankFilePath[:-1]
bankFilePath = '/'.join(bankFilePath)

#add path to this directory to import filepaths.py and abc_bank.py
import sys
sys.path.append(bankFilePath)
import filepaths
from abc_bank import ABCBank

#the sys module adds files and empty folders from Bank to Interface.
#these added files and empty folders are removed here.
currentFilePath = os.getcwd()
for filename in os.listdir(currentFilePath):
    if filename != 'bank_UI.py':
        try:
            os.remove(currentFilePath+'/'+filename)
        except:
            os.rmdir(currentFilePath+'/'+filename)



class BankInterface:
	def __init__(self):
		#get Bank's directory path from filepaths.py and instantiate
		bankFilePath = filepaths.mainPath
		bankFilePath = bankFilePath.split('/')
		i = bankFilePath.index('Bank') + 1
		self.bankFilePath = '/'.join(bankFilePath[:i])+'/'

		self.bank = ABCBank()
		self.firstName = ''
		self.lastName = ''
		self.otherName = ''
		self.phoneNumber = ''
		self.currency = ''
		self.accountType = ''

		#store every opened window in a dictionary
		self.all_windows = {}

		#get the homepage
		self.index = self.homepage()
		#creating the mainloop of the homepage
		self.index.mainloop()

	def homepage(self):
		#creating dimension of main window
		width = "800"
		height = "500"
		self.main_window_size = width + "x" + height

		#creating main window and setting its dimensions
		index = tkinter.Tk()
		index.geometry(self.main_window_size)
		index.title('ABC Bank')

		#create background image frame
		self.imgName = self.bankFilePath + 'imgs/logo.png'
		self.img_frame = tkinter.Frame(index)
		self.img = Image.open(self.imgName)
		self.img = self.img.resize((800,500))
		self.img = ImageTk.PhotoImage(self.img)
		self.img_label = tkinter.Label(self.img_frame, image=self.img)
		self.img_label.pack()


		#creating sign in frame
		sign_in_frame = tkinter.Frame(index)

		#creating the widgets for the sign in frame
		sign_in_msg = tkinter.Label(sign_in_frame,
										 text='\nEnter your bank account number to sign in')

		self.sign_in_entry = tkinter.Entry(sign_in_frame, width=40)
		

		#packing the widgets for the sign in frame
		sign_in_msg.pack()
		self.sign_in_entry.pack()

		#creating the forgot account number frame
		fgt_acc_frame = tkinter.Frame(index)

		#creating forgot account number widgets
		fgt_acc_msg = tkinter.Label(fgt_acc_frame, text='\nForgot Account Number? Click Below')
		fgt_acc_button = tkinter.Button(fgt_acc_frame, text='Click Here!', command=self.fgt_account_number)

		#packing widgets for forgot account number frame
		fgt_acc_msg.pack()
		fgt_acc_button.pack()



		#creating buttons (sign in and exit) frame
		buttons_frame = tkinter.Frame(index)

		#creating the widgets for the buttons_frame
		sign_in_button = tkinter.Button(buttons_frame, text='Sign in', command=self.sign_in)
		exit_button = tkinter.Button(buttons_frame, text='Exit', command=index.destroy)

		self.is_in = False #variable is updated when user is customer of the bank

		#packing the widgets for the buttons frame
		sign_in_button.pack(side='left')
		exit_button.pack(side='left')
		

		#creating sign up frame
		sign_up_frame = tkinter.Frame(index)

		#creating widgets for the sign up frame
		sign_up_msg = tkinter.Label(sign_up_frame, text="\nNew User? Click below to sign up")
		sign_up_button = tkinter.Button(sign_up_frame, text='Sign up', command=self.sign_up)

		#packing the widgets for the sign up frame
		sign_up_msg.pack(side='top')
		sign_up_button.pack(side='bottom')


		#packing the frames
		self.img_frame.place(x=0,y=0)
		sign_in_frame.pack(pady=0)
		buttons_frame.pack(pady=8)
		fgt_acc_frame.pack(pady=8)
		sign_up_frame.pack(side='bottom')

		return index
		
	def sign_in(self):

		accNumber = self.sign_in_entry.get()

		#check if user has account or user is already a customer of the bank
		filePath = self.bankFilePath + 'ABCBank_Customers.csv'
		file = open(filePath)
		header = file.readline()
		userName = ''
		for line in file:
			line = line.strip().split(',')
			if accNumber == line[2]:
				self.is_in = True
				userName = line[3]
				break
		file.close()

		if not self.is_in:
			tkinter.messagebox.showinfo('Error!', 
										'You do not have an account. Close dialog box and sign up for an account!')

		else:
			#self.index.destroy()
			self.is_in = False
			userWindow = self.createUserWindow(userName)
			
			
			userWindow.mainloop()

	def sign_up(self):
		#create a new window
		self.index.destroy()
		self.userWindow = self.createUserWindow()

		#create background image frame
		img_frame = tkinter.Frame(self.userWindow)
		img = Image.open(self.imgName)
		img = img.resize((800,500))
		img = ImageTk.PhotoImage(img)
		img_label = tkinter.Label(img_frame, image=img)
		img_label.pack()

		#create first name frame and widgets
		f_name_frame = tkinter.Frame(self.userWindow)
		f_name_label = tkinter.Label(f_name_frame, text='First name')
		self.f_name_entry = tkinter.Entry(f_name_frame, width=20)
		#packing the widgets
		f_name_label.pack(side='left')
		self.f_name_entry.pack(side='left')

		#create last name frame and widgets
		l_name_frame = tkinter.Frame(self.userWindow)
		l_name_label = tkinter.Label(l_name_frame, text='Last name')
		self.l_name_entry = tkinter.Entry(l_name_frame, width=20)
		#packing the widgets
		l_name_label.pack(side='left')
		self.l_name_entry.pack(side='left')

		#create other name frame and widgets
		o_name_frame = tkinter.Frame(self.userWindow)
		o_name_label = tkinter.Label(o_name_frame, text='Other name')
		self.o_name_entry = tkinter.Entry(o_name_frame, width=20)
		#packing the widgets
		o_name_label.pack(side='left')
		self.o_name_entry.pack(side='left')

		#create phone number frame and widgets
		phone_num_frame = tkinter.Frame(self.userWindow)
		phone_num_label = tkinter.Label(phone_num_frame, text='Phone number')
		self.phone_num_entry = tkinter.Entry(phone_num_frame, width=20)
		#packing the widgets
		phone_num_label.pack(side='left')
		self.phone_num_entry.pack(side='left')


		self.ccy_radio_b_var = tkinter.IntVar()
		self.ccy_radio_b_var.set(1)
		#create currency frame and widgets
		currency_frame = tkinter.Frame(self.userWindow)
		currency_label = tkinter.Label(currency_frame, text='Select type of currency')
		currency_radio_b_usd = tkinter.Radiobutton(currency_frame, text='USD', variable=self.ccy_radio_b_var, value=1, activeforeground='red')
		currency_radio_b_cedis = tkinter.Radiobutton(currency_frame, text='GHC', variable=self.ccy_radio_b_var, value=2, activeforeground='red')
		currency_radio_b_euro = tkinter.Radiobutton(currency_frame, text='EUR', variable=self.ccy_radio_b_var, value=3, activeforeground='red')
		currency_radio_b_tl = tkinter.Radiobutton(currency_frame, text='TLR', variable=self.ccy_radio_b_var, value=4, activeforeground='red')

		#packing widgets
		currency_label.pack(anchor='w')
		currency_radio_b_usd.pack(anchor='w')
		currency_radio_b_cedis.pack(anchor='w')
		currency_radio_b_euro.pack(anchor='w')
		currency_radio_b_tl.pack(anchor='w')



		self.acc_type_radio_var = tkinter.IntVar()
		self.acc_type_radio_var.set(1)
		#create account type frame
		account_type_frame = tkinter.Frame(self.userWindow)
		account_type_label = tkinter.Label(account_type_frame, text='Select bank account type to open')
		account_type_radio_b_current = tkinter.Radiobutton(account_type_frame, text='Current', variable=self.acc_type_radio_var, value=1)
		account_type_radio_b_savings = tkinter.Radiobutton(account_type_frame, text='Savings', variable=self.acc_type_radio_var, value=2)

		#packing widgets
		account_type_label.pack(anchor='w')
		account_type_radio_b_current.pack(anchor='w')
		account_type_radio_b_savings.pack(anchor='w')



		#creating the sign up button frame
		sign_up_button_frame = tkinter.Frame(self.userWindow)
		#creating widgets for the sign up frame
		sign_up_button = tkinter.Button(sign_up_button_frame, text='Sign up', command=self.addUser)
		#packing the widget
		sign_up_button.pack()


		#packing the frames
		img_frame.place(x=0,y=0)
		f_name_frame.pack(pady=10)
		l_name_frame.pack(pady=10)
		o_name_frame.pack(pady=10)
		phone_num_frame.pack(pady=10)
		currency_frame.pack(pady=10)
		account_type_frame.pack()
		sign_up_button_frame.pack(side='bottom')

		if not self.userWindow in self.all_windows:
			self.all_windows['user_up'] = self.userWindow
		
		tkinter.mainloop()


	def fgt_account_number(self):
		tkinter.messagebox.showinfo('Hello')

	def createUserWindow(self, userName='Create Account'):
		userWindow = tkinter.Tk()
		userWindow.geometry(self.main_window_size)
		userWindow.title(userName)
		return userWindow

	def addUser(self):
		self.firstName = self.f_name_entry.get()
		self.lastName = self.l_name_entry.get()
		self.otherName = self.o_name_entry.get()
		if self.otherName == '':
			self.otherName = 'None'
		self.phoneNumber = self.phone_num_entry.get()
		if self.phoneNumber == '':
			self.phoneNumber = 'None'
		#get currency
		if self.ccy_radio_b_var.get() == 1:
			self.currency = 'USD'
		elif self.ccy_radio_b_var.get() == 2:
			self.currency = 'GHC'
		elif self.ccy_radio_b_var.get() == 3:
			self.currency = 'EUR'
		elif self.ccy_radio_b_var.get() == 4:
			self.currency = 'TLR'

		#get account type
		if self.acc_type_radio_var.get() == 1:
			self.accountType = 'Current'
		elif self.acc_type_radio_var.get() == 2:
			self.accountType = 'Savings'

		#check if user entered empty first name and/or last name
		if self.firstName and self.lastName:
			#Now time to register our new user/customer to ABC bank and open an account for them
			accountNumber, customerNumber = self.bank.addUser(self.firstName,
										   self.lastName,
										   self.otherName,
										   self.phoneNumber,
										   self.accountType,
										   self.currency)

			#pop up dialog box to inform user that sign up is succesful
			message_title = 'Welcome to ABC Bank'
			message = """Hello {0},

You have successfully sign up for an account in ABC Bank.
Welcome to the best bank in the world.

You will be directed to the sign in page.
To sign in your account, you need your account number (see below). Also I have added your customer number below.

Secure these numbers and do not share to anyone!

Account Number: {1}
Customer Number: {2}
	""".format(self.firstName, accountNumber, customerNumber)
			
			#close the sign up window and open dialog box to welcome new customer
			tkinter.messagebox.showinfo(message_title, message)
			self.userWindow.destroy()
			index = self.homepage()
			index.mainloop()
		else:
			tkinter.messagebox.showinfo('Error!', 'First name and/or last name can\'t be empty')


		#confirm user's information by opening new window
		#feature to be added soon

bank = BankInterface()

