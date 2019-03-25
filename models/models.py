"""Modules used by the class definition,
SQLAchelmy db representation
datetime library to retrieve date"""
from datetime import datetime
from app import db

class Weather_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(8), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'{{"date":"{self.date}", "address":"{self.address}", "weather":"{self.weather}"}}'