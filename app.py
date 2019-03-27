from datetime import datetime
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flasgger import Swagger
from requests import get
import json

#Declaring our Flask application
app = Flask(__name__)

#Setting CORS so it allows requests from our Angular app in localhost:4200
CORS(app, resources={r"*": {"origins": "http://localhost:4200"}})

#SQL Database configuration 
app.config['SECRET_KEY'] = 'bookatruckinseconds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_log.db'

#Starting the database engine variable and Swagger API Docs endpoint
db = SQLAlchemy(app)
swagger = Swagger(app)

#Weather API informaton and credentials
API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "b65335b39eb9189980121a51c105c90a"

"""MODELS Section, below you can find all the database models used in this application """
class Weather_Log(db.Model):
    """Model that represents a Weather Log inserted in the database"""
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(8), nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'{{"date":"{self.date}", "address":"{self.address}",\
          "weather":"{self.weather}", "icon":"{self.icon}"}}'

#Create the database with the above classes
db.create_all()

"""ENDPOINTS Section, below you can find all the database models used in this application """
@app.route("/weather", methods=['GET'])
def get_weather():
    """Endpoint that returns the weather for given Zip Code and Country Code as input
    ---
    parameters:
      - name: zipCode
        in: query
        type: string
        required: true
        default: '88000-000'
      - name: countryCode
        in: query
        type: string
        required: true
        default: 'br'
    definitions:
      Weather:
        type: object
        properties:
          temp:
            type: number
          pressure:
            type: number
          humidity:
            type: number
          temp_min:
            type: number
          temp_max:
            type: number
      Failed:
        type: object
        properties:
          cod:
            type: number
          message:
            type: string
    responses:
      200:
        description: Successfully retrieved the weather for given Zip Code
        schema:
          $ref: '#/definitions/Weather'
        examples:
          weather: {"temp": 21.17, "pressure": 1015, "humidity": 83,
          "temp_min": 15.56, "temp_max": 24, "icon": "01d"}
      404:
        description: The specified city wasn't found
        schema:
          $ref: '#/definitions/Failed'
        examples:
          failed: {"cod":"404","message":"city not found"}
    """
    params = {'zip': "88000-000,br", 'APPID': API_KEY, 'units': "imperial", }

    if not request.args.get('zipCode') or not request.args.get('countryCode'):
        return '{"cod":"403", "message":"invalid request"}', 400
    else:
        params['zip'] = request.args.get(
            'zipCode') + "," + request.args.get('countryCode')

    weather_response = get(url=API_URL, params=params).json()

    if weather_response['cod'] == 200:
        weather_response['main']['icon'] = weather_response['weather'][0]['icon']
        return json.dumps(weather_response['main']), 200
    else:
        return json.dumps(weather_response), 404


@app.route("/searches", methods=['GET', 'OPTIONS'])
def get_searches():
    """Endpoint that returns the searches already executed
    ---    
    definitions:
      WeatherLogs:
        type: array
        items:
          $ref: '#/definitions/WeatherLog'
      WeatherLog:
        type: object
        properties:
          date:
            type: string
          address:
            type: string
          weather:
            type: number
          icon:
            type: string
    responses:
      200:
        description: Successfully retrieved the weather for given Zip Code
        schema:
          $ref: '#/definitions/WeatherLogs'
        examples: [{"date":"2019-03-16 19:50:50.155235", "address":"Florianopólis",
        "weather":21.23, "icon":"04d.png"}]
    """
    return str(Weather_Log.query.order_by(Weather_Log.date.desc()).all())


@app.route("/searches", methods=['POST'])
def post_searches():
    """Endpoint that inserts data to the search history
    ---
    parameters:
      - name: WeatherLog
        description: Object with the searched elements
        in: body
        required: true
        schema:
            $ref: '#/definitions/WeatherLog'
    definitions:
      WeatherLog:
        type: object
        required:
          - address
          - weather
          - icon
        properties:
          date:
            type: string
          address:
            type: string
          weather:
            type: number
          icon:
            type: string
      Failed:
        type: object
        properties:
          cod:
            type: number
          message:
            type: string
    responses:
      200:
        description: Successfully inserted the Weather Log in the Database
        schema:
          $ref: '#/definitions/WeatherLog'
        examples:
          weather: {"temp": 21.17, "pressure": 1015, "humidity": 83,
          "temp_min": 15.56, "temp_max": 24}
      400:
        description: Invalid request, please check the body of your request
        schema:
          $ref: '#/definitions/Failed'
        examples:
          failed: {"cod":"400", "message":"invalid request"}
      404:
        description: Server internal error when inserting into Database
        schema:
          $ref: '#/definitions/Failed'
        examples:
          failed: {"cod":"500","message":"internal error"}
    """

    try:
        body = request.get_data()
        body = body.decode('utf8').replace("'", '"')
        body = json.loads(body)
    except Exception as exception:
        print(exception)
        return '{"cod":"400", "message":"invalid body format"}', 400

    if not body['weather'] or not body['icon'] or not body['address']:
        return '{"cod":"400", "message":"invalid or missing parameters"}', 400

    new_weatherLog = Weather_Log(weather=body['weather'], icon=body['icon'], address=body['address'])
    db.session.add(new_weatherLog)
    
    try:
        db.session.commit()
        return str(new_weatherLog), 200
    except Exception as exception:
        print(exception)
        return '{"cod":"500", "message":"internal server error when commiting to Database"}', 500

    return str(Weather_Log.query.all())


if __name__ == '__main__':
    app.run(debug=True)
