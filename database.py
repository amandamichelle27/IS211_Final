# Third-party imports.
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

# Local imports.
from config import app
from login import login_manager

# Basic configuration for the database to be re-used across components.
db = SQLAlchemy(app)
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # This will automatically create a new user if a unique username is given.
    @classmethod
    def get_user(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return user
        elif user.password == password:
            return user
        else:
            return None


    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String)
    author = db.Column(db.String)
    page_count = db.Column(db.Integer)
    avg_score = db.Column(db.Float)
    thumbnail = db.Column(db.String)

    @classmethod
    def get_books(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
        
        
# Directly execute this script to instantiate the database.
if __name__ == "__main__":
    # Initialize database.
    db.create_all()
    
    # Create some users.
    user_1 = User(username="joe", password="abc")
    user_2 = User(username="bob", password="123")
    
    # Insert them into the database and flush to generate IDs.
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.flush()
    
    # Hard-coded URLs for sample assets.
    url = ("http://books.google.com/books/content?id=i_SorqUvsOEC&"
           "printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")
    
    # Create books for the two users.
    db.session.add(Book(user_id=user_1.id, title="Some Book", author="Not Me",
                        page_count=100, avg_score=4.0, thumbnail=url))
    db.session.add(Book(user_id=user_2.id, title="My Own Book", author="Me",
                        page_count=666, avg_score=5/7, thumbnail=url))
    db.session.commit()