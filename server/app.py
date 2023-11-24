#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        p_list = []
        plants = Plant.query
        for plant in plants:
            p_list.append(plant.to_dict())
        return make_response(p_list, 200)
    
    def post(self):
        try:
            data = json.loads(request.data)
            new_plant = Plant(
                name=data["name"],
                image=data["image"],
                price=data["price"],
            )
            db.session.add(new_plant)
            db.session.commit()
            return make_response(new_plant.to_dict(), 201)
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"error": [str(e)]}, 400
            )

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        try:
            plant = db.session.get(Plant, id)
            return make_response(plant.to_dict(), 200)
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"error": [str(e)]}, 404
            )


api.add_resource(PlantByID, '/plants/<int:id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
