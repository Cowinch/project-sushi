from pdb import Restart
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask import Flask
from flask_app import app
from flask_app.models import restaurant_model

class Sushi:
    def __init__(self,data) -> None:
        self.id=data['id']
        self.name=data['name']
        self.ingredients=data['ingredients']
        self.description=data['description']
        self.image=data['image']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.restaurant_id=data['restaurant_id']
        self.user_id=data['user_id']
    
    @classmethod
    def create(cls, data):
        query="INSERT INTO sushi (name, ingredients, description, image, restaurant_id, user_id) VALUES (%(name)s,%(ingredients)s,%(description)s, %(image)s, %(restaurant_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM sushi WHERE id = %(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query="SELECT * FROM sushi;"
        results=connectToMySQL(DATABASE).query_db(query)
        if len(results) >0:
            all_sushi=[]
            for row in results:
                this_sushi=cls(row)
                all_sushi.append(this_sushi)
            return all_sushi
        return []
    
    @classmethod
    def get_all_with_restaurants(cls):
        query="SELECT * FROM sushi join restaurants on sushi.restaurant_id=restaurants.id;"
        results=connectToMySQL(DATABASE).query_db(query)
        if len(results) >0:
            all_sushi=[]
            for row in results:
                this_sushi=cls(row)
                restaurant_data={
                    **row,
                    'id': row['restaurants.id'],
                    'name':row['restaurants.name'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at']
                }
                this_restaurant=restaurant_model.Restaurant(restaurant_data)
                this_sushi.restaurant=this_restaurant
                all_sushi.append(this_sushi)
            return all_sushi
        return []
    
    
    @classmethod
    def delete(cls,data):
        query='DELETE FROM sushi WHERE id=%(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update(cls,data):
        query="UPDATE sushi SET name=%(name)s, ingredients=%(ingredients)s, description=%(description)s, image=%(image)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validator(form_data):
        is_valid=True
        if len(form_data['name'])<2:
            flash('name of sushi required', 'reg')
            is_valid=False
        if len(form_data['ingredients'])<5:
            flash('please fillout ingredients', 'reg')
            is_valid=False
        return is_valid