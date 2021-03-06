import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# database_name = "forum"

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "forum"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """
    drops the database tables and starts fresh
    can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(100))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return "<Category {} {}>".format(self.name, self.description)


class Post(db.Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    body = Column(String(1000))
    created_timestamp = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __init__(self, title, body, category_id):
        self.title = title
        self.body = body
        self.category_id = category_id
        self.created_timestamp = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_timestamp": self.created_timestamp
        }

    def long(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_timestamp": self.created_timestamp,
            "category_id": self.category_id
        }

    def __repr__(self):
        return "<Post {} {} {} {} {}>".format(
            self.id, self.title, self.body,
            self.created_timestamp, self.category_id)


class Comment(db.Model):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(String(1000), nullable=False)
    created_timestamp = Column(DateTime, default=datetime.now())
    post_id = Column(Integer, ForeignKey(Post.id), nullable=False)

    post = db.relationship(
        Post, backref=db.backref
        ("posts", cascade="save-update, merge, delete"))

    def __init__(self, post_id, body):
        self.post_id = post_id
        self.body = body
        self.created_timestamp = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "body": self.body,
            "created_timestamp": self.created_timestamp
        }

    def long(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "body": self.body,
            "created_timestamp": self.created_timestamp
        }

    def __repr__(self):
        return "<Comment {} {} {}>".format(
            self.post_id, self.body, self.created_timestamp)
