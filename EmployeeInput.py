from flask import Flask, url_for, redirect, render_template, request, flash
import datetime

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
            return redirect(url_for("home"))
        else:
            flash(auth_info[1])

    return render_template('login.html', name=update_date())

@app.route('/home/')
def home():
    return render_template('home.html', name=update_date())


def update_date():
    date = datetime.datetime.now().strftime("Date: %d/%m/%Y Time: %H:%M:%S")
    return date

if __name__ == "__main__":
    app.run(debug=True)