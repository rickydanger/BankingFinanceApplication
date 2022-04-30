from flask import Flask, url_for, redirect, render_template, request, flash, session
#from flask.ext.login import LoginManager
import datetime
import string

from AccountDatabase import AccountDatabase
from EmployeeAuthentication import EmployeeAuthentication

app = Flask('GRJ Credit Union')
app.secret_key = b'D=%C/zsY-P>wK5TwyL\\&Mu"/>r(}K@D~&z@8BmpL!,H\"\'Q`*VjZ]e^"6C%r7kw""YC+zh' \
                 b'T"CQRE]r;K;&#a2fe9vf\\%#)8L;8gd^7FU!eGQ,$!%azwAy>Td&nsJ.a"a'

currentAccountName = None
currentAccountNumber = None

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
    currentAccountBalance = AccountDatabase.getBalance(currentAccountNumber)
    currentAccountHistory = formatHistory(AccountDatabase.getHistory(currentAccountNumber))

    return render_template('account.html', employee_name=session.get("username"), account_name=currentAccountName,
                           account_number = currentAccountNumber, account_balance = currentAccountBalance,
                           account_history = currentAccountHistory)

def formatHistory(historyString):
    historyArray = historyString.split(';')
    historyString = ""
    currentAccountHistory = ""

    while len(historyArray) != 0:
        for x in range(0, 4):
            historyString = historyString + "<td>" + historyArray[x] + "</td>"
        for x in range(0, 4):
            historyArray.pop(0)
        currentAccountHistory = historyString + currentAccountHistory
    return currentAccountHistory

if __name__ == "__main__":
    app.run(debug=True)