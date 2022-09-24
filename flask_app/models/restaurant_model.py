from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask import Flask
from flask_app import app
from flask_app.models import user_model, sushi_model

class Restaurant:
    def __init__(self,data) -> None:
        self.id=data['id']
        self.name=data['name']
        self.address=data['address']
        self.phone_number=data['phone_number']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
    
    @classmethod
    def create(cls, data):
        query="INSERT INTO restaurants (name, address, phone_number, user_id) VALUES (%(name)s,%(address)s,%(phone_number)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query="SELECT * FROM restaurants;"
        results=connectToMySQL(DATABASE).query_db(query)
        if len(results) >0:
            all_restaurant=[]
            for row in results:
                this_restaurant=cls(row)
                all_restaurant.append(this_restaurant)
            return all_restaurant
        return []
    
    
    @classmethod
    def get_all_with_sushi(cls):
        query="SELECT * FROM restaurants LEFT JOIN sushi on restaurants.id=restaurant_id;"
        results=connectToMySQL(DATABASE).query_db(query)
        if len(results) >0:
            all_restaurant=[]
            for row in results:
                this_restaurant=cls(row)
                sushi_data={
                    **row,
                    'id': row['sushi.id'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at']
                }
                this_sushi=sushi_model.Sushi(sushi_data)
                this_restaurant.creator=this_sushi
                all_restaurant.append(this_restaurant)
            return all_restaurant
        return []
    
    @classmethod
    def get_restaurant_by_sushi(cls,data):
        query="SELECT * FROM restaurants join sushi on restaurants.id=sushi.restaurant_id WHERE sushi.id = %(sushi_id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        #the two commented out lines are what was originally written before linked to another table
        # query="SELECT * FROM restaurants WHERE restaurants.id = %(id)s;"
        query="SELECT * FROM restaurants LEFT JOIN sushi on restaurants.id=sushi.restaurant_id WHERE restaurants.id = %(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        # return cls(results[0])
        user =cls(results[0])
        list_of_sushi=[]
        for row in results:
            if row['sushi.id']==None:
                break
            sushi_data={
                **row,
                'id':row['sushi.id'],
                'name':row['sushi.name'],
                'created_at':row['sushi.created_at'],
                'updated_at':row['sushi.updated_at'],
                'user_id':row['sushi.user_id']
            }
            this_sushi=sushi_model.Sushi(sushi_data)
            list_of_sushi.append(this_sushi)
        user.sushi=list_of_sushi
        return user
    
    @classmethod
    def delete(cls,data):
        query='DELETE FROM restaurants WHERE id=%(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update(cls,data):
        query="UPDATE restaurants SET name=%(name)s, address=%(address)s, phone_number=%(phone_number)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validator(form_data):
        is_valid=True
        if len(form_data['name'])<2:
            flash('name of restaurant required', 'reg')
            is_valid=False
        if len(form_data['address'])<5:
            flash('valid address required', 'reg')
            is_valid=False
        if len(form_data['phone_number'])<1 and len(form_data['phone_number'])>11:
            flash('valid phone-number required', 'reg')
            is_valid=False
        return is_valid