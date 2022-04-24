from flask import Flask, url_for, redirect, render_template, request, flash
import datetime

from AccountDatabase import AccountDatabase
from EmployeeAuthentication import EmployeeAuthentication

app = Flask(__name__)
app.secret_key = b'D=%C/zsY-P>wK5TwyL\\&Mu"/>r(}K@D~&z@8BmpL!,H\"\'Q`*VjZ]e^"6C%r7kw""YC+zh' \
                 b'T"CQRE]r;K;&#a2fe9vf\\%#)8L;8gd^7FU!eGQ,$!%azwAy>Td&nsJ.a"a'

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

@app.route('/accountlookup/', methods=['GET','POST'])
def accountlookup():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        dob = request.form["dob"]
        if fname != '' and lname != '' and dob != '':
            accountname = fname + " " + lname
            result = AccountDatabase.getNumber(accountname, dob)
            return redirect(url_for("account"))

    return render_template('account_look_up.html')


@app.route('/account/', methods=['GET','POST'])
def account():
    return render_template('account.html')

if __name__ == "__main__":
    app.run(debug=True)