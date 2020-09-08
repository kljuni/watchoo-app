from flask import Flask, render_template, session, g, request, jsonify
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import *
from datetime import datetime
from flask_socketio import SocketIO, send
import sqlite3 as sql
import os
import random
import string
import math


app = Flask(__name__)


# from blueprints import main
# app.register_blueprint(main)


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

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:            
            search = request.form.get("search")
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                items = []
                list_items = []
                images = []
                for row in c.execute("SELECT * FROM items WHERE items.brand LIKE '%'||?||'%' OR items.model LIKE '%'||?||'%' OR items.description LIKE '%'||?||'%' ORDER BY created desc", (search, search, search)):
                    items.append(list(row))
                for item in items:
                    list_items.append(item[0])
                for item in list_items:
                    image = query_db('SELECT * FROM images WHERE images.item=? ORDER BY date desc', (item,))
                    for img in image:
                        images.append(list(img))
                return render_template('shop.html', watches=items, images=images, search=search)
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            return redirect('/shop')
            conn.close()

@app.route("/shop")
def shop():
    with sql.connect("mydb.db") as conn:
        c = conn.cursor()
        watches = []
        images = []
        brands = []
        for row in c.execute('SELECT * FROM items ORDER BY created desc'):
            watches.append(list(row))
        for row in c.execute('SELECT * FROM images ORDER BY date desc'):
            images.append(list(row))
        for row in watches: 
            if row[1] not in brands:
                brands.append(row[1])
    return render_template("shop.html", watches=watches, images=images, brands=brands)
    conn.close()

@app.route("/testing")
def testing():
    return render_template("testing.html")

@app.route('/api/shop/<int:order>/<int:page>')
def watches_list(order, page):
    try:
        with sql.connect("mydb.db") as conn:
            c = conn.cursor()
            watches = []
            images = []
            brands = []
            item_ids = []

            # Get number of all listed items by counting all rows in items table
            num_items = 0
            for row in c.execute('SELECT COUNT(*) FROM items'):
                num_items = row[0]

            # Get number of pages by deviding the number of listed items and ceil the result.
            num_pages = math.ceil(num_items / 12)

            # If requested page does not exist, redirect user to "shop" page
            if page < 1 or page > num_pages or order < 1 or order > 4:
                return redirect('/shop')
            # Select 12 items from items with the offset for the selected page and the selected order
            if order == 1:
                for row in c.execute('SELECT * FROM items ORDER BY created desc LIMIT 12 OFFSET (?)', ((page - 1) * 12,)):
                    watches.append(list(row))
            elif order == 2:
                for row in c.execute('SELECT * FROM items ORDER BY created asc LIMIT 12 OFFSET (?)', ((page - 1) * 12,)):
                    watches.append(list(row))
            elif order == 3:
                for row in c.execute('SELECT * FROM items ORDER BY price asc LIMIT 12 OFFSET (?)', ((page - 1) * 12,)):
                    watches.append(list(row))
            elif order == 4:
                for row in c.execute('SELECT * FROM items ORDER BY price desc LIMIT 12 OFFSET (?)', ((page - 1) * 12,)):
                    watches.append(list(row))
            # Populate item_ids with the ids from watches list
            for row in watches:
                item_ids.append(row[0])
            # Select rows from images table if the image is in the watches list (i.e. has the same id as one of the items in watches list)
            for row in item_ids:
                for img in c.execute('SELECT * FROM images WHERE item IN (?) ORDER BY date desc', (row,)):
                    images.append(list(img))
            num_pages = list(range(1, num_pages + 1))
        conn.close()
        return jsonify(watches = watches, images = images, num_pages=num_pages)
    except Exception as e:
        print(e)
        conn.rollback()
        return redirect('/shop')
        conn.close()

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
            category = request.form.get("category")

            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (brand, model, condition, gender, year, movement, price, description, created, item_owner, category) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (brand, model, condition, gender, year, movement, price, description, created, session["user_id"], category))
                con.commit()
                file_entry = query_db('SELECT MAX(item_id) FROM items')
                
                # Save uploaded image to image. 
                # Save the uploaded item_id
                uploaded_files = request.files.getlist("input-fa[]")
                print(uploaded_files)
                item_id = [lis[0] for lis in file_entry][0]
                for image in uploaded_files:
                    if image:                
                        # Check if the image has a name
                        if image.filename == "":
                            return render_template("/sell.html", msg = "Selected image has no name")

                        if allowed_image(image.filename):
                            filename = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8)) + secure_filename(image.filename) 
    
                            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))


                        cur.execute("INSERT INTO images (item, user, date, path) VALUES (?,?,?,?)", (item_id, session["user_id"], created, "/static/images/{}".format(filename)))

                
                # # image = request.files['input-fa[]']
                # # print(image)
                # item_id = [lis[0] for lis in file_entry][0]

                # # Flask image upload procedure from https://pythonise.com/series/learning-flask/flask-uploading-files
                # if image:                
                #     # Check if the image has a name
                #     if image.filename == "":
                #         return render_template("/sell.html", msg = "Selected image has no name")

                #     if allowed_image(image.filename):
                #         filename = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8)) + secure_filename(image.filename) 
  
                #         image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))


                #     cur.execute("INSERT INTO images (item, user, date, path) VALUES (?,?,?,?)", (item_id, session["user_id"], created, "/static/images/{}".format(filename)))

            
            con.commit()

            # return render_template("watch.html", item_id = item_id)
            return redirect(url_for('watch', item_id = item_id))
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
    with sql.connect("mydb.db") as conn:
        c = conn.cursor()
        watch = []
        image = []
        for row in c.execute('SELECT * FROM items WHERE items.item_id == ?', (item_id,)):
            watch.append(list(row))
        for row in c.execute('SELECT * FROM images WHERE images.item == ?', (item_id,)):
            image.append(list(row))
        print(watch)
        print(image)
        return render_template('watch.html', item_id = item_id, watch=watch, image=image)
        conn.close()

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
    app.run()

