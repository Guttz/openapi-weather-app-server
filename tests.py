import unittest
from app import app
import requests

class BaseTestCase(unittest.TestCase):
    # Setting up the application to be tested
    def setUp(self):
        app.config['SECRET_KEY'] = 'bookatruckinseconds'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_weather_log.db'
        self.app = app.test_client()

    # Executed after each test, nothing necessary for now
    def tearDown(self):
        pass

    def test_get_searches(self):
        """Testing get all searches EndPoint"""
        # Send a request to the API server and store the response.
        response = self.app.get('/searches', follow_redirects=True)
        
        # Confirm that the request-response cycle completed successfully.
        assert response.status_code is 200
        print(". \n The test test_get_searches was sucessful...")

    def test_post_searches(self):
        """Testing POST a serach to /searches EndPoint"""
        # Send a request to the API server and store the response.
        response = self.app.post('/searches', data='{\n  "address": "New York, NY - United States"\
            , \n  "date": "27/03/2019",\n  "icon": "01n",\n  "weather": 10\n}')

        # Confirm that the request-response cycle completed successfully.
        assert response.status_code is 200
        print("\n The test test_get_searches was sucessful...")

    def test_get_weather(self):
        """Testing POST a serach to /searches EndPoint"""
        # Send a request to the API server and store the response.
        response = self.app.get('/weather?zipCode=88000-000&countryCode=br')

        # Confirm that the request-response cycle completed successfully.
        assert response.status_code is 200
        print("\n The test test_get_weather was sucessful...")

if __name__ == '__main__':
    unittest.main()
    