from flask import Flask, render_template, session, g, request
from tempfile import mkdtemp
from flask_session import Session
from helpers import *
import sqlite3 as sql

app = Flask(__name__)

# auto-reloads templates on change
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/register", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:            
            name = request.form.get("name")
            email = request.form.get("email")
            surname = request.form.get("surname")
            city = request.form.get("city")
            pin = request.form.get("pin")

            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, email, surname, city, pin) VALUES (?,?,?,?,?)", (name, email, surname, city, pin))
                
                if pin.isnumeric() == False:
                    raise Exception("No letter characters in PIN")

                if check(email) == False:
                    raise Exception("Invalid email")

                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            print(e)
            con.rollback()
            msg = "Error in insert operation"
            return render_template("home.html", msg = msg)
            con.close()
        finally:
            return redirect("/")
            con.close()
    else:
        return render_template("register.html")

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"
    
if __name__ == "__main__":
    app.run(debug=True)