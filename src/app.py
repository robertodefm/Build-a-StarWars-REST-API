"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import *
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET','POST'])
def handle_hello():
    
    if request.method == 'GET':

        all_user = User.query.all()
        return jsonify(
            [ users.serialize() for users in all_user]
        ), 200
    elif request.method == 'POST':
        body = request.json
        if "email" not in body:
            return 'Debe indicar el email', 400
        if "password" not in body:
            return 'Debe indicar una password', 400
        if "is_active" not in body:
            return 'Debe indicar is_active', 400
        new_row = User.new_registro_users(body["email"], body["password"], body["is_active"])
        if new_row == None:
            return 'Ha ocurrido un error!', 500
        else:
            return jsonify(new_row.serialize()), 200
    

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():

    all_favorites = Favorites.query.all()
    return jsonify(
        [ favorites.serialize() for favorites in all_favorites]
    ), 200



@app.route('/people', methods=['GET'])
def people_todos():
    all_people = People.query.all()
    return jsonify(
        [ people.serialize() for people in all_people]
    ), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def people_search(people_id):
    people=People.query.get(people_id)
    if not people:
        return 'No se encontro registro people con ese id ', 404
    return jsonify(
        people.serialize() 
    ), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST','DELETE'])
def post_people(people_id):
    search = People.query.get(people_id)


    if request.method == 'POST':
        body = request.json
        if "name" not in body:
            return 'Debe indicar la descripcion porque es favorito!', 400
        if "user_id" not in body:
            return 'Debe indicar el usuario', 400
        
        new_row = Favorites.new_registro_favorites(body["name"], body["user_id"], None, people_id)
        if new_row == None:
            return 'Ha ocurrido un error!!', 500
        else:
            return jsonify(new_row.serialize()), 200
    elif request.method == 'DELETE':
        searchdelete = Favorites.query.filter_by(people_id=people_id)

        result = searchdelete.delete()
        db.session.commit()
        if result == True:
            return f'El people {people_id} ha sido eliminado con exito!', 200
        else:
            return 'Ha ocurrido un error!!', 500

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    return jsonify(
        [ planets.serialize() for planets in all_planets]
    ), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_search(planet_id):
    planet=Planets.query.get(planet_id)
    if not planet:
        return 'No se encontro registro planet con ese id ', 404
    return jsonify(
        planet.serialize() 
    ), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST','DELETE'])
def post_planets(planet_id):
    search = Planets.query.get(planet_id)


    if request.method == 'POST':
        body = request.json
        if "name" not in body:
            return 'Debe indicar la descripcion porque es favorito!', 400
        if "user_id" not in body:
            return 'Debe indicar el usuario', 400
        
        new_row = Favorites.new_registro_favorites(body["name"], body["user_id"], search.id, None)
        if new_row == None:
            return 'Ha ocurrido un error!', 500
        else:
            return jsonify(new_row.serialize()), 200
    elif request.method == 'DELETE':
        searchdelete = Favorites.query.filter_by(planet_id=planet_id)

        result = searchdelete.delete()
        db.session.commit()
        if result == True:
            return f'El planeta {planet_id} ha sido eliminado con exito!', 200
        else:
            return 'Ha ocurrido un error!!', 500



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)