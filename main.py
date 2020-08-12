from flask import Flask, render_template, session, g, request
from tempfile import mkdtemp
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import *
from datetime import datetime
from flask_socketio import SocketIO, send
import sqlite3 as sql
import os
import random
import string

app = Flask(__name__)

DATABASE = 'mydb.db'

# Set the filesystem folder for saving uploaded images
app.config["IMAGE_UPLOADS"] = "./static/images"

# List of allowed extensions for uploaded images
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

# Set maximum upload size to about 16 MB
app.config['MAX_CONTENT_LENGTH'] = 4032 * 4032

def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

# Function get_db to get to the current database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db


# Function to be called when the application context ends and closes the db with it
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Query function that combines getting the cursor, executing and fetching the results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

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


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    # Forget any previous user session
    session.clear()

    if request.method == 'POST':
        email = request.form.get("email")

        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("login.html", msg="You forgot to enter your email") 

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("login.html", msg="You forgot to password") 

        with sql.connect("mydb.db") as con:
            cur = con.cursor()
            
            #  Query the db for the user email
            user = query_db('select * from users where email = ?', [email], one=True)
            print(user)

            # Ensure user (email) exists and the password is correct
            if user is None or check_password_hash(user[4], request.form.get("password")) == False:
                return render_template("login.html", msg="Wrong email address or password")                
            
            # Remember which user has logged in
            session["user_id"] = user[0]
            session["email"] = user[3]

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    # Logout the current user
    session.clear()

    if request.method == 'POST':
        try:            
            firstname = request.form.get("firstname")
            secondname = request.form.get("secondname")
            email = request.form.get("email1")
            city = request.form.get("city")
            country = request.form.get("country")
            hash = generate_password_hash(request.form.get("password1"))
            created = datetime.now().isoformat()
            
            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (firstname, secondname, email, hash, city, country, created) VALUES (?,?,?,?,?,?,?)", (firstname, secondname, email, hash, city, country, created))
                
                if check(email) == False:
                    raise Exception("Invalid email")
                print("all good")
                con.commit()
                msg = "Record successfully added"

            return render_template("/login.html")
            con.close()
        except Exception as e:
            print(e)
            con.rollback()
            return render_template("/register.html", msg = e)
            con.close()
        except:
            con.rollback()
            return render_template("/register.html", msg = "There was an error in database")
            con.close()
    else:
        return render_template("register.html")

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if session.get("user_id") is None:
        return render_template("register.html")

    if request.method == 'POST':
        print(request)
        try:            
            brand = request.form.get("brand")
            model = request.form.get("model")
            condition = request.form.get("condition")
            gender = request.form.get("gender")
            year = request.form.get("year")
            movement = request.form.get("movement")
            price = request.form.get("price")
            description = request.form.get("description") 
            created = datetime.now().isoformat()
        
            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (brand, model, condition, gender, year, movement, price, description, created, item_owner) VALUES (?,?,?,?,?,?,?,?,?,?)", (brand, model, condition, gender, year, movement, price, description, created, session["user_id"]))
                file_entry = query_db('SELECT last_insert_rowid()')
                image = request.files['file']

                # flask image upload procedure from https://pythonise.com/series/learning-flask/flask-uploading-files
                if image:                
                    # Check if the image has a name
                    if image.filename == "":
                        return render_template("/sell.html", msg = "Selected image has no name")

                    if allowed_image(image.filename):
                        filename = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8)) + secure_filename(image.filename) 
  
                        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))


                    cur.execute("INSERT INTO images (item, user, date, path) VALUES (?,?,?,?)", (1, session["user_id"], created, "/static/images/{}".format(filename)))

            
            con.commit()

            return render_template("watch.html", item_id = 14)
            con.close()

        except Exception as e:
            print("some success end")
            print(e)
            con.rollback()
            return render_template("/sell.html", msg = e)
            con.close()
        except:
            con.rollback()
            return render_template("/sell.html")
            con.close()
    else:
        return render_template("sell.html", watchBrands = watchBrands)
                
@app.route("/watch/<int:item_id>")
def watch(item_id):
    return render_template('watch.html', item_id = item_id)

@app.route("/account")
@login_required
def account():
    return render_template("account.html", countryList = countryList)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"
    
if __name__ == "__main__":
    app.run(debug=True)

