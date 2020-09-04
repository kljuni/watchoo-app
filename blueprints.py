# from flask import Blueprint, jsonify
# import sqlite3 as sql

# main = Blueprint('main', __name__)

# @main.route('/shop/<int:order>')
# def watches_list(order):
#     if order == 1:
#         with sql.connect("mydb.db") as conn:
#             c = conn.cursor()
#             watches = []
#             images = []
#             brands = []
#             for row in c.execute('SELECT * FROM items ORDER BY created desc'):
#                 watches.append(list(row))
#             for row in c.execute('SELECT * FROM images ORDER BY date desc'):
#                 images.append(list(row))
#             for row in watches: 
#                 if row[1] not in brands:
#                     brands.append(row[1])
#         conn.close()
#         return jsonify(watches = watches, images = images)
#     else:
#         print("this is change!")


# @main.route('/search/<str:order>')
# def search(order, type):
#     if request.method == 'POST':
#         try:            
#             search = request.form.get("search")
#             with sql.connect("mydb.db") as conn:
#                 c = conn.cursor()
#                 items = []
#                 list_items = []
#                 images = []
#                 for row in c.execute("SELECT * FROM items WHERE items.brand LIKE '%'||?||'%' OR items.model LIKE '%'||?||'%' OR items.description LIKE '%'||?||'%' ORDER BY created desc", (search, search, search)):
#                     items.append(list(row))
#                 for item in items:
#                     list_items.append(item[0])
#                 for item in list_items:
#                     image = query_db('SELECT * FROM images WHERE images.item=? ORDER BY date desc', (item,))
#                     for img in image:
#                         images.append(list(img))
#                 return render_template('shop.html', watches=items, images=images, search=search)
#                 conn.close()
#         except Exception as e:
#             print(e)
#             conn.rollback()
#             return redirect('/shop')
#             conn.close()
