from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Contains definitions of tables and associated schema constructs
metadata = MetaData()

# Create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# Define a model class by inheriting from db.Model.
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Pet {self.id}, {self.name}, {self.species}>'
