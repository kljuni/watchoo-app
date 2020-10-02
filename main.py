from flask import Flask, render_template, session, g, request, jsonify
from tempfile import mkdtemp
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import *
from datetime import datetime
from flask_socketio import SocketIO, send
from PIL import Image
import sqlite3 as sql
import os
import threading
import time
import random
import string
import math
import PIL
import glob


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

app.config['SECRET_KEY'] = '7/(T)H76T8g/T&h8/Z/(hn)76tR85VR8gbuzt6rV&%R9(NGn9&/B)'

# Set cookies to be ephemeral
@app.before_request
def make_session_permanent():
    session.permanent = False

# Populate the brands variable with currently available (listed) brands
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            try:
                with sql.connect("mydb.db") as conn:
                    global brands
                    c = conn.cursor()
                    watches = []
                    brands = []
                    for row in c.execute('SELECT * FROM items ORDER BY created desc'):
                        watches.append(list(row))
                    for row in watches: 
                        if row[1] not in brands:
                            brands.append(row[1])
                conn.close()
            except Exception as e:
                conn.rollback()
                conn.close()
            time.sleep(5)
    thread = threading.Thread(target=run_job)
    thread.start()

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


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

        print(session)
        print("here it is printed _______________")
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
            country = request.form.get("country")
            seller = request.form.get("seller")
            hash = generate_password_hash(request.form.get("password1"))
            created = datetime.now().isoformat()

            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (firstname, secondname, email, hash, country, seller, created) VALUES (?,?,?,?,?,?,?)", (firstname, secondname, email, hash, country, seller, created))
                
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
            return render_template("/register.html", msg = e, countryList = countryList)
            con.close()
        except:
            con.rollback()
            return render_template("/register.html", msg = "There was an error in database", countryList = countryList)
            con.close()
    else:
        return render_template("register.html", countryList = countryList)

@app.route("/")
@app.route("/home")
def index():    
    if session.get("user_id") is None:
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                watches = []
                images = []
                for row in c.execute('SELECT * FROM items ORDER BY created desc LIMIT 4'):
                    watches.append(list(row))
                for row in c.execute('SELECT * FROM images ORDER BY date desc LIMIT 16'):
                    images.append(list(row))
                return render_template("index.html", watches=watches, images=images, user="Welcome to the world of watch collectors")
                conn.close()
        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
            conn.close()
    else:
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                name = c.execute('SELECT firstname FROM users WHERE user_id=?', (session.get("user_id"),))
                names = [lis[0] for lis in name][0]
                watches = []
                images = []
                for row in c.execute('SELECT * FROM items ORDER BY created desc LIMIT 4'):
                    watches.append(list(row))
                for row in c.execute('SELECT * FROM images ORDER BY date desc LIMIT 16'):
                    images.append(list(row))
            return render_template("index.html", watches=watches, images=images, user='Hello {}, welcome back'.format(names))
            conn.close()
        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
            conn.close()

@app.route("/api/search")
def search():
    print(request.args)
    try:            
        search = request.args["arg1"]
        print(search)
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
            print(items)
            print(images)
            print("up there you can find em")
            global brands
            print(brands)
        return jsonify(watches = items, images = images, brands = brands, num_pages=3)
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        return redirect('/shop')
        conn.close()

@app.route("/shop", defaults={'search': None}, methods=['GET', 'POST'])
def shop(search):
    if request.method == 'POST':
        if request.form:
            if "search1" in request.form: 
                search=request.form["search1"]
            elif "search2" in request.form:  
                search=request.form["search2"]
            elif "search3" in request.form:  
                search=request.form["search3"]
            elif "search4" in request.form:  
                search=request.form["search4"]
            return render_template("shop.html", search=search)
    return render_template("shop.html")

@app.route("/shop/categories", methods=['POST'])
def categories():
    try:
        with sql.connect("mydb.db") as conn:

            if len(request.form["gender"]) == 0:
                gender = "noben"
            else:
                gender = request.form["gender"]
            # gender = request.form["gender"]
            category = request.form["category"]
            brand = request.form["brand"]
            print("here the brands")
            print(gender)
            print(category)
            print(brand)
            if gender == None:
                gender = ''
            if category == None:
                category = ''
            if brand == None:
                brand = ''

            c = conn.cursor()            
            items = []
            list_items = []
            images = []
            for row in c.execute("SELECT * FROM items WHERE brand LIKE ? AND gender LIKE ? AND category LIKE ? ORDER BY created desc", ('%' + brand + '%', '%' + gender + '%', '%' + category + '%')):
                items.append(list(row))
            for item in items:
                list_items.append(item[0])
            for item in list_items:
                image = query_db('SELECT * FROM images WHERE images.item=? ORDER BY date desc', (item,))
                for img in image:
                    images.append(list(img))
        print("printing items")
        print(list_items)
        print(items)
        return render_template("shop.html", watches=list_items)
        conn.close()

    except Exception as e:
        conn.rollback()
        print(e)
        return redirect('/')
        conn.close()

@app.route("/testing")
def testing():
    return render_template("testing.html")

@app.route('/api/shop/<int:order>/<int:page>')
def watches_list(order, page):
    print(request.args)
    arg1 = request.args["arg1"]
    arg2 = request.args["arg2"]
    arg3 = request.args["arg3"]
    print("here printing args")
    print(arg1)
    print(arg2)
    print(arg3)
    if (arg1 or arg2 or arg3):
        try:
            with sql.connect("mydb.db") as conn:
                gender = request.args["arg1"]
                category = request.args["arg2"]
                brand = request.args["arg3"]
                print("here the brands")
                print(gender)
                print(category)
                print(brand)
                if gender == None:
                    gender = ''
                if category == None:
                    category = ''
                if brand == None:
                    brand = ''
                print("hallelujah")
                c = conn.cursor()            
                items = []
                list_items = []
                images = []
                for row in c.execute("SELECT * FROM items WHERE brand LIKE ? AND gender LIKE ? AND category LIKE ? ORDER BY created desc", ('%'+brand+'%', '%'+gender+'%', '%'+category+'%')):
                    items.append(list(row))
                for item in items:
                    list_items.append(item[0])
                for item in list_items:
                    image = query_db('SELECT * FROM images WHERE images.item=? ORDER BY date desc', (item,))
                    for img in image:
                        images.append(list(img))
                print("printing items")
                print(list_items)
                print(items)            
            global brands
            return jsonify(watches = items, images = images, brands = brands)
            conn.close()

        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
            conn.close()
    else: 
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                watches = []
                images = []
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
            return jsonify(watches = watches, images = images, num_pages=num_pages, brands = brands)
            
        except Exception as e:
            print(e)
            conn.rollback()
            return redirect('/shop')
            conn.close()

@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if session.get("user_id") is None:
        reg = "Please register before posting a new listing"
        return render_template("register.html", reg=reg, countryList = countryList)

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
            location = request.form.get("location") 
            created = datetime.now().isoformat()
            category = request.form.get("category")

            with sql.connect("mydb.db") as con:
                cur = con.cursor()
                file_entry = query_db('SELECT MAX(item_id) FROM items')

                # Save uploaded image to image. 
                # Save the uploaded item_id
                uploaded_files = request.files.getlist("input-fas[]")
                print(uploaded_files)
                item_id = [lis[0] for lis in file_entry][0] + 1
                for image in uploaded_files:
                    print("here is the image")
                    print(image)
                    if image:                
                        # Check if the image has a name
                        print("it gets here 1")
                        if image.filename == "":
                            return render_template("/sell.html", msg = "Selected image has no name")

                        if allowed_image(image.filename):
                            print("it gets here 2")
                            filename = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8)) + secure_filename(image.filename) 
                            
                            # Open the image with Pillow "Image" class
                            im = Image.open(image)

                            # Convert the image to JPG and replace the background color to white if the image is PNG
                            fill_color = (255, 255, 255)  # your new background color

                            im = im.convert("RGBA")   # it had mode P after DL it from OP

                            if im.mode in ('RGBA', 'LA'):
                                background = Image.new(im.mode[:-1], im.size, fill_color)
                                background.paste(im, im.split()[-1]) # omit transparency
                                im = background

                            # Save image to file system and compress the image to aribitrary quality, here set to 20
                            im.convert('RGB').save(os.path.join(app.config["IMAGE_UPLOADS"], filename) + '.jpg', 'JPEG', optimize=True, quality=20)

                            cur.execute("INSERT INTO images (item, user, date, path) VALUES (?,?,?,?)", (item_id, session["user_id"], created, "/static/images/{}".format(filename + '.jpg')))
                        else: 
                            raise NameError('Wrong image format')

                cur.execute("INSERT INTO items (brand, model, condition, gender, year, movement, price, description, location, created, item_owner, category) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (brand, model, condition, gender, year, movement, price, description, location, created, session["user_id"], category))
                con.commit()

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

# form_id is meant to know which form is being submitted, form_id=1 is firstname, secondname etc form. Form_id=2 is password change.
@app.route("/account", methods=['GET', 'POST', 'DELETE'])
@login_required
def account():
    if request.method == 'DELETE':
        if session.get("user_id") is None:
            reg = "Please register before accessing your account"
            return render_template("register.html", reg=reg, countryList = countryList)
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                watches = []
                images = []
                user = session.get("user_id")
                for row in c.execute('SELECT * FROM items WHERE item_owner=? ORDER BY created desc', (user,)):
                    watches.append(list(row))
                for row in c.execute('SELECT * FROM images WHERE user=? ORDER BY date desc', (user,)):
                    images.append(list(row))
            return render_template("account.html", watches=watches, images=images, countryList = countryList)
        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
        conn.close()
    elif request.method == 'POST':
        if session.get("user_id") is None:
            reg = "Please register before accessing your account"
            return render_template("register.html", reg=reg, countryList = countryList)
        if "firstname" in request.form: 
            try:
                with sql.connect("mydb.db") as conn:
                    c = conn.cursor()
                    firstname = request.form.get("firstname") 
                    secondname = request.form.get("secondname") 
                    email = request.form.get("email") 
                    country = request.form.get("country") 
                    user = session.get("user_id")
                    c.execute('UPDATE users SET firstname = ?, secondname = ?, email = ?, country = ?  WHERE user_id = ?', (firstname, secondname, email, country, user))
                    msg = "You have successfully changed your personal information!"
                return render_template('account.html', msg=msg, alert="alert-success", countryList = countryList)
            except Exception as e:
                conn.rollback()
                print(e)
                return redirect('/')
            conn.close()
        elif "current_password" in request.form:        
            try:
                with sql.connect("mydb.db") as conn:
                    c = conn.cursor()
                    user_id = session.get("user_id")
                    user_data = query_db('select * from users where user_id = ?', [user_id], one=True)
                    
                    # Ensure user exists and the password is correct
                    if user_data is None or check_password_hash(user_data[4], request.form.get("current_password")) == False:
                        return render_template("account.html", msg="Wrong current password.", alert="alert-danger", countryList = countryList)

                    c.execute('UPDATE users SET hash = ? WHERE user_id = ?', (generate_password_hash(request.form.get("new_password")), user_id))
                    msg = "You have successfully changed your password!"
                return render_template('account.html', msg=msg, alert="alert-success", countryList = countryList)
            except Exception as e:
                conn.rollback()
                print(e)
                return redirect('/')
            conn.close()
    else:
        if session.get("user_id") is None:
            reg = "Please register before accessing your account"
            return render_template("register.html", reg=reg, countryList = countryList)
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                watches = []
                images = []
                user = session.get("user_id")
                for row in c.execute('SELECT * FROM items WHERE item_owner=? ORDER BY created desc', (user,)):
                    watches.append(list(row))
                for row in c.execute('SELECT * FROM images WHERE user=? ORDER BY date desc', (user,)):
                    images.append(list(row))
            return render_template("account.html", watches=watches, images=images, countryList=countryList)
            conn.close()
        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
            conn.close()

@app.route("/account/<int:item_id>", methods=['DELETE'])
@login_required
def del_item(item_id):
    if request.method == 'DELETE':
        if session.get("user_id") is None:
            reg = "Please register before accessing your data"
            return render_template("register.html", reg=reg, countryList = countryList)
        try:
            with sql.connect("mydb.db") as conn:
                c = conn.cursor()
                user = session.get("user_id")
                c.execute('DELETE FROM items WHERE item_id=?', (item_id,))
                c.execute('DELETE FROM images WHERE item=?', (item_id,))
            print("that was a success, congrats !!!")
            conn.close()
            return redirect('/account')
        except Exception as e:
            conn.rollback()
            print(e)
            return redirect('/')
            conn.close()
    else:
        return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"
    
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(threaded=True, port=5000)

