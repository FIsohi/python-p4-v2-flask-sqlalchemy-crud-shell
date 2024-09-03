from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Pet

# Create a Flask application instance 
app = Flask(__name__)

# Configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# Initialize the Flask application to use the database
db.init_app(app)

# Route to create a new pet
@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    name = data.get('name')
    species = data.get('species')
    if not name or not species:
        return jsonify({'error': 'Name and species are required'}), 400
    pet = Pet(name=name, species=species)
    db.session.add(pet)
    db.session.commit()
    return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species}), 201

# Route to get all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets]), 200

# Route to get a specific pet by ID
@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species}), 200

# Route to update a pet
@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    pet.name = data.get('name', pet.name)
    pet.species = data.get('species', pet.species)
    db.session.commit()
    return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species}), 200

# Route to delete a pet
@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message': 'Pet deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
