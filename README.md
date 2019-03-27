This is the backend for an weather web application/coding task for Loadsmart. It's a Flask based application with a SQL Database, the interface between the two is made with SQLAlchemy, a ORM(Object Relational Mapping) tool for python. This app was publish with Open API, so there's an Endpoint for documentation/api console.

## To set up the dependencies follow:
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
(This code was built and tested for Python 3.6.7)

## To run the backend server 

```
python app.py
```
## Check Open API V3 auto generated EndPoint

Open: http://localhost:5000/apidocs/

-You can see all models used by the API, also the parameters and responses for every endpoint
-Also, it can be used as an console for trying the API

## To run the integration tests on the endpoints

```
python test_app.py
```

##Next steps
Separate Models in different folder and import them
Separate Routes in different folder an import them
Implement testing on the same database or copy production database before testing

## Observations
The Open Weather API Key is the backend for safety for safety reasons, however the Geocoding/Places api has to be on the frontend for a better user experience and it's safety is providing by refferrals and setting limits for each client in the Google Cloud Platform

# Pylint  was used to make the code quality better, unfortunatly due to timming reasons I couldn't fix all pylint warnings