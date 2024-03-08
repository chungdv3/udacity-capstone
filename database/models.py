import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine, ForeignKey, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


'''
Actor
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    casts = db.relationship('Cast', backref='actor', lazy='joined', cascade="all, delete")
    movies = db.relationship('Movie', secondary='casts', back_populates='actors')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.short() for movie in self.movies]
        }


'''
Movie
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)

    casts = db.relationship('Cast', backref='movie', lazy='joined', cascade="all, delete")
    actors = db.relationship('Actor', secondary='casts', back_populates='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'actors': [actor.short() for actor in self.actors]
        }


'''
Cast
'''


class Cast(db.Model):
    __tablename__ = 'casts'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    __table_args__ = (UniqueConstraint('movie_id', 'actor_id', name='_movie_actor_uc'),)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'movie_id': self.movie_id,
            'movie': self.movie.short(),
            'actor_id': self.actor_id,
            'actor': self.actor.short()
        }
