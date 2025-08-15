# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    main_image = db.Column(db.String(255), nullable=False)  # store filename or key
    public = db.Column(db.Integer, default=0)
    date = db.Column(db.String(20), default=date.today().strftime('%d-%m-%Y'))

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)