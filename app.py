from flask import Flask, url_for, redirect, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login/', methods=['GET','POST'])
def login():
    return render_template('login.html', name=update_date())

@app.route('/home/')
def home():
    return render_template('home.html', name=update_date())


def update_date():
    date = datetime.datetime.now().strftime("Date: %d/%m/%Y Time: %H:%M:%S")
    return date

if __name__ == "__main__":
    app.run(debug=True)