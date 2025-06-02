from flask import Flask, jsonify, request
from flask_cors import CORS
import pathlib as pl
import pandas as pd

app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

@app.route('/api/alive', methods=['GET'])
def check_alive():
    return jsonify(message="Alive"), 200

@app.route('/api/associations', methods=['GET'])
def get_associations():
    return jsonify(associations_df['id'].tolist()), 200

@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if not association.empty:
        return jsonify(association.to_dict(orient='records')[0]), 200
    return jsonify({"error": "Association not found"}), 404

@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    return jsonify(evenements_df['id'].tolist()), 200

@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    evenement = evenements_df[evenements_df['id'] == id]
    if not evenement.empty:
        return jsonify(evenement.to_dict(orient='records')[0]), 200
    return jsonify({"error": "Event not found"}), 404

@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_association_evenements(id):
    association_evenements = evenements_df[evenements_df['association_id'] == id]
    if not association_evenements.empty:
        return jsonify(association_evenements.to_dict(orient='records')), 200
    return jsonify({"error": "No events found for this association"}), 404

@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    associations_by_type = associations_df[associations_df['type'] == type]
    if not associations_by_type.empty:
        return jsonify(associations_by_type['id'].tolist()), 200
    return jsonify({"error": "No associations found for this type"}), 404

if __name__ == '__main__':
    app.run(debug=False)
