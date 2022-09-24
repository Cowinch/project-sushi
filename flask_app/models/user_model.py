from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask import Flask
from flask_app import app
import re
EMAIL_REGEX=re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-0._-]+\.[a-zA-Z]+$")
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.profile_picture=data['profile_picture']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    
    #create NEW USER
    @classmethod
    def create(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def create_pfp(cls, data):
        query="UPDATE users SET profile_picture=%(profile_picture)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #this method is used when logging in a returning user
    @classmethod
    def get_by_email(cls,data):
        query="SELECT * FROM users WHERE email = %(email)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_friends(cls,data):
        query='select * from users where id!=%(id)s;'
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) >0:
            all_friends=[]
            for row in results:
                this_friends=cls(row)
                all_friends.append(this_friends)
            return all_friends
        return []
    
    
    @classmethod
    def get_by_id(cls,data):
        #the two commented out lines are what was originally written before linked to another table
        query="SELECT * FROM users WHERE users.id = %(id)s;"
        # query="SELECT * FROM users LEFT JOIN recipes on users.id=recipes.user_id WHERE users.id = %(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
        # user =cls(results[0])
        # list_of_recipes=[]
        # for row in results:
        #     if row['recipes.id']==None:
        #         break
        #     recipe_data={
        #         **row,
        #         'id':row['recipes.id'],
        #         'created_at':row['recipes.created_at'],
        #         'updated_at':row['recipes.updated_at'],
        #     }
        #     this_recipe=recipe_model.Recipe(recipe_data)
        #     list_of_recipes.append(this_recipe)
        # user.recipes=list_of_recipes
        # return user
    
    #validates for both registering and returning users
    @staticmethod
    def validate(user_data):
        is_valid=True
        if len(user_data['first_name']) <1:
            flash('First name required', 'reg')
            is_valid=False
        if len(user_data['last_name']) <1:
            flash('Last name required', 'reg')
            is_valid=False
        if len(user_data['email']) <1:
            flash('email required', 'reg')
            is_valid=False
        elif not EMAIL_REGEX.match(user_data['email']):
            flash('Invalid email format', 'reg')
            is_valid=False
        else:
            data={
                'email':user_data['email']
            }
            potenial_user=User.get_by_email(data)
            if potenial_user:
                flash('Email already registered (hope it was you!)', 'reg')
                is_valid=False
        if len(user_data['password'])<8:
            flash("Passes must be more than 8 characters", 'reg')
            is_valid=False
        elif not user_data['password']==user_data['confirm_pass']:
            flash("passes don't match", 'reg')
            is_valid=False
        return is_valid