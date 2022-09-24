from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.restaurant_model import Restaurant
from flask_app.models.post_model import Post
from flask_app.models.sushi_model import Sushi
from flask_app.models.friend_model import Friend
from flask_app import DATABASE
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

#this is a reroute to home page
@app.route('/')
def index():
    if 'user_id' in session:
        print('makin my way downtown')
        return redirect(f'/users/{session["user_id"]}')
    return redirect('/login')

#this is just so when we're logging in the URL reflects the stage we're at
@app.route('/login')
def home():
    return render_template('index.html')

#process form route for NEW USERS
@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pass=bcrypt.generate_password_hash(request.form['password'])
    data={
        **request.form,
        'password': hashed_pass
    }
    id=User.create(data)
    session['user_id']=id
    return redirect('/')

#process form route for ACTIVE USERS
@app.route('/users/login', methods=['POST'])
def login():
    data={'email': request.form['email']}
    user_in_db=User.get_by_email(data)
    if not user_in_db:
        flash('Invalid login info','log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid login info','log')
        return redirect('/')
    session['user_id']=user_in_db.id
    return redirect('/')

#DASHBOARD
@app.route('/users/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        print('ur not logged in buddy')
        return redirect('/')
    user_data={
        'id':session['user_id']
    }
    all_posts=Post.get_by_id({'user_id':id})
    # print("\nline 64 users_controller, all_posts: ")
    # print(all_posts)
    
    all_restaurants=Restaurant.get_all()
    # print("\nline 66 users_controller, all_restaurants: ")
    # print(all_restaurants)
    all_sushi=Sushi.get_all_with_restaurants()
    
    logged_user=User.get_by_id(user_data)
    page_user=User.get_by_id({'id':id})
    all_friends=User.get_friends({"id":id})
    return render_template(
        'dashboard.html', 
        logged_user=logged_user,
        all_posts=all_posts,
        all_restaurants=all_restaurants,
        page_user=page_user,
        all_friends=all_friends,
        all_sushi=all_sushi
    )

#UPDATE PROFILE PICTURE
@app.route('/users/profile/<int:id>', methods=['POST'])
def update_pfp(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'profile_picture':request.form['profile_picture'],
        'id':id
    }
    User.create_pfp(data)
    return redirect('/')


#PROCESS to LOG OUT
@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')

#404 error PAGE
@app.errorhandler(404)
def page_not_found(e): #as far as I can tell this parameter literally exists just to stop a positional argument error.
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404