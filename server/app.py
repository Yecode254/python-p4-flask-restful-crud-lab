#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ROUTES

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price'],
                is_in_stock=data.get('is_in_stock', True)
            )
            db.session.add(new_plant)
            db.session.commit()
            return make_response(new_plant.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 400)


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)
        return make_response(plant.to_dict(), 200)


    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)

        data = request.get_json()
        for attr in data:
            if hasattr(plant, attr):
                setattr(plant, attr, data[attr])
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)

        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
