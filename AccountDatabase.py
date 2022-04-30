#Will contain way to interact with CSV based database and contain functions to check against user information and retrieve account information.

import csv
import fileinput
from datetime import datetime

databasePath = "Accounts\Accounts.csv"
savingRate = 3 #3% interest rate for savings Accounts
checkingRate = 1.25 #1.25% interest rate for checking Accounts
daysInMonth = 30 #days in the month will need to be updated after the interest has been paid each month
now = datetime.now()
class AccountDatabase:
	def getNumber(accountName,accountDOB):
		"""This function will take the accountHolderName(column 2) and accountHolderDOB(column 3) and return the accountNumber(column 1) for use by EmployeeInput to allow access without the account Number"""
		with open(databasePath, newline='') as csvfile:
			database = csv.DictReader(csvfile, delimiter=',')
			for row in database:
				if (accountName == row['accountHolderName']) and (accountDOB == row['accountHolderDOB']):
					return row['accountNumber'], None
		return -1, "Account Holder Name and Date of Birth pair does not match any account in the system"

	def getHolder(accountNumber):
		"""This function will take the accountNumber(column 1) and return the accountHolderName(column 2) to the EmployeeInput to be displayed to the employee"""
		with open(databasePath, newline='') as csvfile:
			database = csv.DictReader(csvfile, delimiter=',')
			for row in database:
				if accountNumber == row['accountNumber']:
					return row['accountHolderName'], None
		return -1, "Account number does not match any account in the system"

	def getBalance(accountNumber):
		"""This function will take the accountNumber(column 1) and return the currentBalance(column 5) of the account"""
		with open(databasePath, newline='') as csvfile:
			database = csv.DictReader(csvfile, delimiter=',')
			for row in database:
				if accountNumber == row['accountNumber']:
					return row['accountBalance']

	def getHistory(accountNumber):
		"""This function will take the accountNumber(column 1) and return the accountHistory(column 7) of the account"""
		with open(databasePath, newline='') as csvfile:
			database = csv.DictReader(csvfile, delimiter=',')
			for row in database:
				if accountNumber == row['accountNumber']:
					return row['accountHistory']

	# Employee triggered Account Balance manipulation functions

	def makeDeposit(accountNumber,depositAmount):
		"""This function will take the accountNumber(column 1) and depositAmount, It will add the depositAmount to the currentBalance, record the transaction in the accountHistory(Column 7)
			then return the currentBalance(column 5) of the account"""
		depositAmount = float(depositAmount)
		newBalance = float(AccountDatabase.getBalance(accountNumber)) + depositAmount
		newHistory = now.strftime("%m/%d") + ";In Bank Deposit;" + str(depositAmount) + ";" + str(newBalance) + ":"
		with fileinput.FileInput(databasePath, inplace=True) as csvwrite:
			for row in csvwrite:
				data = row.split(',')
				if data[0] == accountNumber:
					print(data[0] + "," +
						data[1] + "," +
						data[2] + "," +
						data[3] + "," +
						str(newBalance) + "," +
						data[5] + "," +
						newHistory + data[6], end ='')
				else:
					print(row, end ='')
		return AccountDatabase.getBalance(accountNumber)

	def makeWithdrawal(accountNumber,withdrawalAmount):
		"""This function will take the accountNumber(column 1) and withdrawalAmount, It will check for sufficient funds then subtract the depositAmount from the currentBalance	record the transaction in the accountHistory(Column 7) then return the currentBalance(column 5) of the account"""
		error = None
		if float(getBalance(accountNumber)) >= withdrawalAmount:
			print("This account has the required funds")
			newBalance = float(getBalance(accountNumber)) - withdrawalAmount
			newHistory = now.strftime("%m/%d") + ";In Bank Withdrawal;" + str(withdrawalAmount) + ";" + str(newBalance) + ":"
			with fileinput.FileInput(databasePath, inplace=True, backup='.bak') as csvwrite:
				for row in csvwrite:
					data = row.split(',')
					test = row[0] + row[1] + row[2] + row[3] + row[4] + row[5]
					if data[0] == accountNumber:
						print(data[0] + "," +
							data[1] + "," +
							data[2] + "," +
							data[3] + "," +
							str(newBalance) + "," +
							data[5] + "," +
							newHistory + data[6], end ='')
					else:
						print(row, end ='')
		else:
			error = "This account does not have the required funds"
		return getBalance(accountNumber), error

	#Interest Functions

	def updateAverageBalance():
		"""This function will update the accountAverageBalance(column 5) based on the accountBalance and the number of days in the month"""
		with fileinput.FileInput(databasePath, inplace=True) as csvwrite:
			for row in csvwrite:
				data = row.split(',')
				if data[0] != "accountNumber":
					dailyAmount = float(data[4]) / daysInMonth
					print(data[0] + "," +
						data[1] + "," +
						data[2] + "," +
						data[3] + "," +
						data[4] + "," +
						str("%.2f" %(float(data[5]) + dailyAmount)) + "," +
						data[6], end ='')
				else:
					print(row, end ='')

	def makeInterestPayments():
		"""This function will loop through the accounts and add interest based on the interest rate of the account type and the accounts average balance for the month"""
		with fileinput.FileInput(databasePath, inplace=True) as csvwrite:
			for row in csvwrite:
				data = row.split(',')
				if data[0] != "accountNumber":
					rate = checkingRate

					if data[3] == 1: # Savings
						rate = savingsRate
					interestAmount = float(data[5]) * (rate / 12 / 100)
					newBalance = float(data[4]) + interestAmount
					newHistory = now.strftime("%m/%d") + ";Interest Payment;" + str("%.2f" % interestAmount) + ";" + str("%.2f" % newBalance) + ":"
					#Replace the dates here with dates pulled from the timer class or from datetime
					print(data[0] + "," +
						data[1] + "," +
						data[2] + "," +
						data[3] + "," +
						str("%.2f" % newBalance) + "," +
						"0" + "," +
						newHistory + data[6], end ='')
				else:
					print(row, end ='')
	#Update daysInMonth for the averageBalance updates
	
	
	#testing

	#makeInterestPayments()