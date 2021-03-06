# OpenAPI Weather Application
This is a Flask based application with a SQL Database, the interface between the two is made with SQLAlchemy, a ORM(Object Relational Mapping) tool for python. This app was published with Open API, so there's an Endpoint for documentation/api console.

## Requirements
- Python 3.6.7+

## To set up the dependencies follow:
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## To run the backend server:

```
python app.py
```

## Check Open API V3 auto generated EndPoint

Open: http://localhost:5000/apidocs/

- You can see all models used by the API, also the parameters and responses for every endpoint
- Also, it can be used as a console for trying the API

## To run the integration battery of tests:

```
python test_app.py
```

## Next steps
- Refactor Models as a package in a different directory
- Refactor Routes to a different folder and import them
- Implement testing on the same database or copy production database before testing
- Implement pagination mechanism for the API

### Observations
The Open Weather API Key is the backend for safety reasons as API Keys usually are. However, the Geocoding/Places api has to be on the frontend for a better user experience and it's safety is provided by refferrals, setting limits and other restrictions for each client in Google Cloud Platform.
