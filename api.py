
from flask_cors import CORS
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from flask import Flask, make_response,request
import json

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "http://localhost:3000"}})

# Connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://lakkilakshman12:WpOKni2QVKHJRAFr@rental.x1c06wu.mongodb.net/')
db = client['test'] 
collection = db['cars'] 


data = list(collection.find({}))  # Retrieve all documents in the collection

# Check if the retrieved data is not empty
if not data:
    raise ValueError("No data found in the collection.")

# Filter out entries with non-empty fuelType and rentPerHour
fuel_rent_types = [(x['fuelType'], x['rentPerHour']) for x in data if x.get('fuelType') and x.get('rentPerHour')]

if not fuel_rent_types:
    raise ValueError("No valid fuelTypes and rentPerHour found in the data. Please check the 'fuelType' and 'rentPerHour' fields in your MongoDB documents.")

# TF-IDF matrix based on fuelType
fuel_types = [x[0] for x in fuel_rent_types]
tfidf = TfidfVectorizer(stop_words='english', lowercase=True, max_features=5000)
tfidf_matrix = tfidf.fit_transform(fuel_types)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

@app.route('/recommend', methods=['GET','POST'])
def get_recommendations():
    if request.method == 'POST':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    user_preferences = {'fuel_type': 'Petrol', 'seating_capacity':4, 'max_rent_per_hour': 2000}  # Example user preferences
    
    # Filter data based on user preferences
    filtered_data = [x for x in data if user_preferences['fuel_type'] in x['fuelType'] 
                     and x['capacity'] >= user_preferences['seating_capacity']
                     and x['rentPerHour'] <= user_preferences['max_rent_per_hour']]

    # Compute similarity scores and generate recommended vehicles
    recommended_vehicles = []
    for item in filtered_data:
        idx = data.index(item)  # or some other identifier
        similar_items = list(enumerate(cosine_sim[idx]))
        similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
        similar_items = similar_items[1:6]  # select top 5 similar items

        recommendations = [data[i[0]] for i in similar_items]

        # Convert ObjectId to string for JSON serialization
        for rec in recommendations:
            rec['_id'] = str(rec['_id'])

        recommended_vehicles.extend(recommendations)

    # Return the recommended vehicles as JSON data
    response= make_response(json.dumps({'recommended_vehicles': recommended_vehicles},default=str))
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return  response



if __name__ == '__main__':
    app.run(debug=True)
