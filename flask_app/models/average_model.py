from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE



class Average:
    def __init__(self,data) -> None:
        self.average=data['average']
        
    @classmethod
    def average_sushi_rating(cls,data):
        query="select avg(rating) as average from posts join sushi on sushi_id=sushi.id where sushi.id=%(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def average_restaurant_rating(cls, data):
        query="select avg(rating) as average from posts join sushi on sushi_id=sushi.id join restaurants on restaurants.id=restaurant_id where restaurants.id=%(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])