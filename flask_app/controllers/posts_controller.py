from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.restaurant_model import Restaurant
from flask_app.models.post_model import Post
from flask_app.models.sushi_model import Sushi
from flask_app.models.average_model import Average
from flask_app.models.count_model import Count

#ROUTE for CREATE POST/RATE SUSHI
@app.route('/sushi/<int:sushi_id>/rate/<int:user_id>')
def rate_sushi(sushi_id,user_id):
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    sushi=Sushi.get_by_id({'id':sushi_id})
    all_restaurants=Restaurant.get_all()
    restaurant=Restaurant.get_restaurant_by_sushi({'sushi_id':sushi_id})
    average=Average.average_sushi_rating({'id':sushi_id})
    if average.average:
        average.average=round(average.average)
    count=Count.count_sushi_rating({'id':sushi_id})
    if not count.counter:
        count.counter=0
    return render_template(
        'sushi_rate.html', 
        logged_user=logged_user, 
        sushi=sushi,restaurant=restaurant, 
        all_restaurants=all_restaurants,
        average=average,
        count=count
    )

#PROCESS for CREATE POST
@app.route('/sushi/<int:sushi_id>/post/<int:user_id>', methods=['POST'])
def create_post(sushi_id,user_id):
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    if logged_user.id!=user_id:
        return('/')
    sushi=Sushi.get_by_id({'id':sushi_id})
    data={
        **request.form,
        'user_id':user_id,
        'sushi_id':sushi_id
    }
    Post.create(data)
    return redirect('/')

#ROUTE for EDIT POST
@app.route('/sushi/<int:sushi_id>/post/<int:user_id>/edit')
def edit_post(sushi_id,user_id):
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    if logged_user.id!=user_id:
        return('/')
    sushi=Sushi.get_by_id({'id':sushi_id})
    all_restaurants=Restaurant.get_all()
    return render_template('post_edit.html', logged_user=logged_user, sushi=sushi, all_restaurants=all_restaurants)