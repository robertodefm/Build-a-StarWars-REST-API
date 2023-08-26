
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="user", uselist=True)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    @classmethod
    def new_registro_users(cls, email, password, is_active):
        new_registro_users = cls( email, password, is_active)
       
        db.session.add(new_registro_users)
        try:
            db.session.commit()
            return new_registro_users
        except Exception as error:
            print(error)
            return None
        
class People(db.Model):
    id = db.Column(db.Integer,primary_key=True)  
    name = db.Column(db.String(100), nullable=False)
    url_address = db.Column(db.String(300), nullable=False)
    
   
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "url_address": self.url_address,
            
        }

    @classmethod
    def new_registro_people(cls, uid, name, url_address):
        new_registro_people = cls( uid, name, url_address)
       
        db.session.add(new_registro_people)
        try:
            db.session.commit()
            return new_registro_people
        except Exception as error:
            print(error)
            return None
        
class Planets(db.Model):
    id = db.Column(db.Integer,primary_key=True)  
    name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(400), nullable=False)
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "info": self.info,
        }    

    @classmethod
    def new_registro_planets(cls, name, info):
        new_registro_planets = cls( name, info)
       
        db.session.add(new_registro_planets)
        try:
            db.session.commit()
            return new_registro_planets
        except Exception as error:
            print(error)
            return None    
     
        
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer,db.ForeignKey('planets.id'))
    __table_args__ =(db.UniqueConstraint(
        'user_id', 
        'people_id',
        name = 'unique_favorites'
    ),)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def __init__(self, name, user_id, planet_id, people_id):
        self.name = name
        self.user_id = user_id
        self.planet_id = planet_id
        self.people_id = people_id

    def serialize(self):
        return{
           "id": self.id,
           "user_id": self.user_id,
           "people_id": self.people_id,
           "planet_id": self.planet_id,
             
           
        }
        
    @classmethod
    def new_registro_favorites(cls, name, user_id, planet_id, people_id):
        new_registro_favorites = cls(name, user_id, planet_id, people_id)
       
        db.session.add(new_registro_favorites)
        try:
            db.session.commit()
            return new_registro_favorites
        except Exception as error:
            print(error)
            return None

    def update(self, name):
        self.name = name
        try:
            db.session.commit()
            return self
        except Exception as error:
            print(error)
            return False

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False