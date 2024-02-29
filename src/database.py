from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import unique
from sqlalchemy.orm import backref
import string
import random

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.Text(),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookmarks = db.relationship('Bookmark', backref='user')
    def __repr__(self) -> str:
        return f'User>>> {self.username}'


class Categories(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    title = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=False)
    bookmarks = db.relationship('Bookmark', backref='categories')

    def __repr__(self) -> str:
        return f'Categories>>> {self.title}'

class Bookmark(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    body = db.Column(db.Text,nullable=True)
    title = db.Column(db.Text,nullable=False)
    url = db.Column(db.Text,nullable=True)
    short_url = db.Column(db.String(3),nullable=False)
    visits = db.Column(db.Integer, default=0)
    piriority = db.Column(db.Text,nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_short_characters(self):
        charcters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(charcters, k=3))

        link=self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()


    def __repr__(self) -> str:
        return 'Bookmark>>> {self.url}'