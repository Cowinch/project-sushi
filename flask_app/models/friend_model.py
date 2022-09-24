from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Friend:
    def __init__(self,data) -> None:
        self.id=data['id']
    
        