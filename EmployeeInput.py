from flask import Flask, url_for, redirect, render_template, request, flash, session
import re
from datetime import timedelta
import time

from AccountDatabase import AccountDatabase
from EmployeeAuthentication import EmployeeAuthentication

app = Flask('GRJ Credit Union')
app.secret_key = b'D=%C/zsY-P>wK5TwyL\\&Mu"/>r(}K@D~&z@8BmpL!,H\"\'Q`*VjZ]e^"6C%r7kw""YC+zh' \
                 b'T"CQRE]r;K;&#a2fe9vf\\%#)8L;8gd^7FU!eGQ,$!%azwAy>Td&nsJ.a"a'
app.permanent_session_lifetime = timedelta(minutes=5)

currentAccountName = None
currentAccountNumber = None

AccountDatabase.startTimer()

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        auth_info = EmployeeAuthentication.auth(request.form["username"], request.form["password"])

        if auth_info[0]:
            return redirect(url_for("accountlookup"))
        else:
            flash(auth_info[1])

    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session["username"] = None
    return redirect(url_for('login'))

@app.route('/switchaccount', methods=['GET','POST'])
def switchaccount():
    global currentAccountName, currentAccountNumber
    currentAccountName = None
    currentAccountNumber = None
    return redirect(url_for("accountlookup"))
    

@app.route('/accountlookup/', methods=['GET','POST'])
def accountlookup():
    if not session.get("username"):
        return redirect(url_for('login'))
    elif request.method == "POST":
        global currentAccountName, currentAccountNumber
        fname = request.form["fname"]
        lname = request.form["lname"]
        dob = request.form["dob"]
        accountnumber = request.form["accountnumber"]
        error = None

        if fname != '' and lname != '' and dob != '':
            accountname = fname + " " + lname
            data = AccountDatabase.getNumber(accountname, dob)
            accountnumber = data[0]
            error = data[1]
            if error == None:
                currentAccountName = accountname
                currentAccountNumber = accountnumber
                return redirect(url_for("accountprompt"))
        elif (accountnumber !='' and len(accountnumber) != 6):
            error = "account number is not the correct length"
        elif (accountnumber != ''):
            data = AccountDatabase.getHolder(accountnumber)
            accountname = data[0]
            error = data[1]
            if error == None:
                currentAccountName = accountname
                currentAccountNumber = accountnumber
                return redirect(url_for("accountprompt"))
        if error == None:
            error = "You missed one or more forms"
        flash(error)

    return render_template('account_look_up.html', employee_name=session.get("username"))

@app.route('/accountprompt/', methods=['GET','POST'])
def accountprompt():
    if not session.get("username"):
        return redirect(url_for('login'))
    else:
        global currentAccountName, currentAccountNumber
        if request.method == "POST":
            return redirect(url_for("account"))
    return render_template('accountprompt.html', name=currentAccountName, number=currentAccountNumber)

@app.route('/account', methods=['GET','POST'])
def account():
    global currentAccountName, currentAccountNumber
    if not session.get("username"):
        return redirect(url_for('login'))
    elif currentAccountName == None or currentAccountNumber == None:
        return redirect(url_for("accountlookup"))

    if request.method == "POST":
        deposit = request.form["deposit"]
        withdraw = request.form["withdraw"]
        if deposit != '':
            AccountDatabase.makeDeposit(currentAccountNumber, deposit)
            flash("Deposit of $" + str("%.2f" % float(deposit)) + " was successful")
        if withdraw != '':
            data = AccountDatabase.makeWithdrawal(currentAccountNumber, withdraw)
            error = data[1]
            if error == None:
                flash("Withdrawal of $" + str("%.2f" % float(withdraw)) + " was successful")
                return redirect(url_for("account"))
            else:
                flash(error)
        return redirect(url_for("account"))


    currentAccountBalance = AccountDatabase.getBalance(currentAccountNumber)
    currentAccountHistory = formatHistory(AccountDatabase.getHistory(currentAccountNumber))

    return render_template('account.html', employee_name=session.get("username"), account_name=currentAccountName,
                           account_number = currentAccountNumber, account_balance = currentAccountBalance,
                           account_history = currentAccountHistory)

def formatHistory(historyString):
    historyArray = re.split(';|:', historyString)
    currentAccountHistory = ""

    while len(historyArray) != 0:
        historyString = ""
        for x in range(0, 4):
            historyString = historyString + "<td>" + historyArray[x] + "</td>"
        for x in range(0, 4):
            historyArray.pop(0)
        currentAccountHistory = currentAccountHistory + "<tr align\"center\">" + historyString + "</tr>"
    return currentAccountHistory

@app.route('/forceinterest', methods=['GET','POST'])
def forceinterest():
    AccountDatabase.simulateMonth()
    return redirect(url_for("account"))


if __name__ == "__main__":
    app.run(debug=False)