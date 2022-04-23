import os
import pandas as pd
from flask import session


class EmployeeAuthentication:
    def auth(username, password):
        csv_path = os.path.join(os.getcwd() + "\\" + "Employee_Authentication_Database.csv")
        account_found = False
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            employee_db = pd.read_csv(csv_path)
            db_index = employee_db[employee_db['username'] == username].index.values

        if db_index >= 0:
            account_found = True
            db_password = employee_db.at[int(db_index[0]), 'password']
            del employee_db
            if db_password == password:
                session.permanent = True
                session["username"] = username
                return True, error
            if account_found:
                error = ("Password is incorrect.")
        else:
            error = ("User account not found")

        return False, error
