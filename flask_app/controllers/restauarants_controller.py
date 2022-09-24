from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.average_model import Average
from flask_app.models.count_model import Count
from flask_app.models.user_model import User
from flask_app.models.restaurant_model import Restaurant
from flask_app.models.post_model import Post
from flask_app.models.sushi_model import Sushi
from flask_app import DATABASE

#ROUTE for NEW restaurant
@app.route('/restaurant/new')
def new_restaurant():
    if 'user_id' not in session:
        print('ur not logged in buddy')
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    all_restaurants=Restaurant.get_all()
    return render_template('restaurant_new.html', logged_user=logged_user, all_restaurants=all_restaurants)

#PROCESS for NEW restaurant
@app.route('/restaurant/create', methods=['POST'])
def process_restaurant():
    if 'user_id' not in session:
        print('ur not logged in buddy')
        return redirect('/')
    if not Restaurant.validator(request.form):
        return redirect('/restaurant/new')
    data = {
        **request.form,
        'user_id':  session['user_id']
    }
    id=Restaurant.create(data)
    print('\nif you can see this, we should have a new restaruant\n')
    # return redirect('/')
    return redirect(f'/restaurant/{id}')

#ROUTE for ONE RESTAURANT
@app.route('/restaurant/<int:id>')
def display_restaurant(id):
    if 'user_id' not in session:
        print('ur not logged in buddy')
        return redirect('/')
    restaurant=Restaurant.get_by_id({'id':id})
    logged_user = User.get_by_id({'id': session['user_id']})
    all_restaurants=Restaurant.get_all()
    restaurant_average=Average.average_restaurant_rating({'id':id})
    if restaurant_average.average:
        restaurant_average.average=round(restaurant_average.average)
    restaurant_count=Count.count_restaurant_rating({'id':id})
    if not restaurant_count:
        restaurant_count=0
    return render_template(
        'restaurant_one.html',
        logged_user=logged_user, 
        restaurant=restaurant, 
        all_restaurants=all_restaurants,
        restaurant_average=restaurant_average,
        restaurant_count=restaurant_count
    )

#ROUTE for UPDATE RESTAURANT
@app.route('/restaurant/<int:id>/edit')
def edit_restaurant_form(id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant = Restaurant.get_by_id({'id': id})
    if not int(session['user_id']) == restaurant.user_id:
        flash("Whoa there, that's not yours, hands off!")
        return redirect('/')
    all_restaurants=Restaurant.get_all()
    return render_template('restaurant_edit.html', restaurant=restaurant, all_restaurants=all_restaurants)

#PROCESS for UPDATE RESTUARANT
@app.route('/restaurant/<int:id>/update', methods=['POST'])
def update_restaurant(id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant = Restaurant.get_by_id({'id': id})
    if not int(session['user_id']) == restaurant.user_id:
        flash("Whoa there, that's not yours, hands off!")
        return redirect('/')
    if not Restaurant.validator(request.form):
        return redirect(f'/restaurant/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    Restaurant.update(data)
    return redirect(f'/restaurant/{id}')


#PROCESS for DELETE RESTAURANT
@app.route('/restaurant/<int:id>/delete')
def del_restaurant(id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant = Restaurant.get_by_id({'id': id})
    if not int(session['user_id']) == restaurant.user_id:
        flash("Whoa there, that's not yours, hands off!")
        return redirect('/')
    Restaurant.delete({'id': id})
    return redirect('/')
