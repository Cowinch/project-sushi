from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask import Flask
from flask_app import app
from flask_app.models import user_model, sushi_model, restaurant_model

class Post:
    def __init__(self,data) -> None:
        self.id=data['id']
        self.user_id=data['user_id']
        self.sushi_id=data['sushi_id']
        self.comment=data['comment']
        self.rating=data['rating']
        self.user_image=data['user_image']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    
    @classmethod
    def create(cls, data):
        query="INSERT INTO posts (user_id, sushi_id, comment, rating, user_image) VALUES (%(user_id)s, %(sushi_id)s, %(comment)s, %(rating)s, %(user_image)s)"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        # print('\nline 22 post model')
        # print(data)
        query="SELECT * FROM posts JOIN sushi on posts.sushi_id=sushi.id JOIN restaurants on restaurants.id=sushi.restaurant_id JOIN users on users.id = posts.user_id WHERE users.id = %(user_id)s order by posts.id desc;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        # print('\nline 24 post_model, results:')
        # print(results)
        if len(results) >0:
            all_post=[]
            for row in results:
                this_post=cls(row)
                sushi_data={
                    **row,
                    'id': row['sushi.id'],
                    # 'name':row['sushi.name'],
                    'created_at':row['sushi.created_at'],
                    'updated_at':row['sushi.updated_at'],
                }
                this_sushi=sushi_model.Sushi(sushi_data)
                this_post.sushi=this_sushi
                restaurant_data={
                    'id':row['restaurants.id'],
                    'name':row['restaurants.name'],
                    'address':row['address'],
                    'phone_number':row['phone_number'],
                    'created_at':row['restaurants.created_at'],
                    'updated_at':row['restaurants.updated_at'],
                    'user_id':row['restaurants.user_id'],
                }
                this_restaurant=restaurant_model.Restaurant(restaurant_data)
                this_post.restaurant=this_restaurant
                all_post.append(this_post)
            return all_post
        return []