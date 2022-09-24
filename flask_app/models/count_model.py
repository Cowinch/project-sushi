from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Count:
    def __init__(self, data) -> None:
        self.counter=data['counter']
    
    @classmethod
    def count_sushi_rating(cls,data):
        query="select count(rating) as counter from posts join sushi on sushi_id=sushi.id where sushi.id=%(id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def count_restaurant_rating(cls,data):
        query='select count(rating) as counter from posts join sushi on sushi_id=sushi.id join restaurants on restaurants.id=restaurant_id where restaurants.id=%(id)s;'
        results=connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])