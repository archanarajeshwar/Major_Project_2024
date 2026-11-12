from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
from address import gmaps

app = Flask(__name__)
CORS(app)

@app.route('/hospitals', methods=['POST'])
def hospitals():
    latitude = request.get_json()['latitude'] 
    longitude = request.get_json()['longitude'] 
    print(latitude,longitude)
    lat = 19.0443
    long = 72.8204
    # hospital_data = gmaps(latitude,longitude)
    hospital_data = gmaps(lat,long)
    return jsonify(hospital_data)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
