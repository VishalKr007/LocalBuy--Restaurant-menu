from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


#API endpoint
@app.route('/restaurant/JSON')
def restaurantJSON():
	restaurant = session.query(Restaurant).all()
	return jsonify(Rest = [i.serialize for i in restaurant])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def oneMenuJSON(restaurant_id, menu_id):
	items = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItems=[items.serialize])

#query to return list of all restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	restaurant = session.query(Restaurant)
	return render_template('restaurants.html', restaurant = restaurant)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
	restaurant = session.query(Restaurant)
	if request.method == 'POST':
		newRestro = Restaurant(name = request.form['name'])
		session.add(newRestro)
		session.commit()
		flash("new restaurant created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("restaurant name edited successfully!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant=editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash("restaurant deleted successfully!")
		return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleterestaurant.html', restaurant=deletedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = items, i = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("menu item edited successfully!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("menu item deleted successfully!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', i=deletedItem )

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)