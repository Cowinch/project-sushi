from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.restaurant_model import Restaurant
from flask_app.models.post_model import Post
from flask_app.models.sushi_model import Sushi
from flask_app import DATABASE

#ROUTE for NEW SUSHI
@app.route('/sushi/<int:restaurant_id>/new')
def new_sushi(restaurant_id):
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    restaurant=Restaurant.get_by_id({'id':restaurant_id})
    all_restaurants=Restaurant.get_all()
    return render_template('sushi_new.html', logged_user=logged_user, restaurant=restaurant, all_restaurants=all_restaurants)

#PROCESS form for NEW SUSHI
@app.route('/sushi/<int:restaurant_id>/create', methods=['POST'])
def process_sushi(restaurant_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Sushi.validator(request.form):
        return redirect(f'/sushi/{restaurant_id}/new')
    restaurant=Restaurant.get_by_id({'id':restaurant_id})
    data = {
        **request.form,
        'user_id': session['user_id'],
        'restaurant_id': restaurant.id
    }
    id=Sushi.create(data)
    return redirect(f'/restaurant/{restaurant_id}')

#ROUTE for UPDATE
@app.route('/sushi/<int:sushi_id>/edit/<int:restaurant_id>')
def edit_sushi(sushi_id,restaurant_id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant=Restaurant.get_by_id({'id':restaurant_id})
    sushi=Sushi.get_by_id({'id':sushi_id})
    all_restaurants=Restaurant.get_all()
    return render_template('sushi_edit.html', restaurant=restaurant, sushi=sushi, all_restaurants=all_restaurants)

#PROCESS for UPDATE
@app.route('/sushi/<int:sushi_id>/update/<int:restaurant_id>', methods=['POST'])
def update_sushi(sushi_id,restaurant_id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant=Restaurant.get_by_id({'id':restaurant_id})
    sushi=Sushi.get_by_id({'id':sushi_id})
    if not Sushi.validator(request.form):
        return redirect(f'/sushi/{sushi_id}/edit/{restaurant_id}')
    data={
        **request.form,
        'id':sushi_id
    }
    Sushi.update(data)
    return redirect(f'/restaurant/{restaurant_id}')

#PROCESS for DELETE
@app.route('/sushi/<int:sushi_id>/delete/<int:restaurant_id>')
def del_sushi(sushi_id,restaurant_id):
    if 'user_id' not in session:
        return redirect('/')
    restaurant = Restaurant.get_by_id({'id':restaurant_id})
    sushi=Sushi.get_by_id({'id':sushi_id})
    if not int(session['user_id']) == restaurant.user_id or int(session['user_id'])==sushi.user_id:
        flash("Whoa there, that's not yours, hands off!")
        return redirect(f'/restaurant/{restaurant_id}')
    Sushi.delete({'id': sushi_id})
    return redirect(f'/restaurant/{restaurant_id}')