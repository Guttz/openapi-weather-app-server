from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bookatruckinseconds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_log.db'
db = SQLAlchemy(app)
db.create_all()

class Weather_Log(db.Model):
    __tablename__ = 'Weather_Log'
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.String(5), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"User('{self.date}', '{self.address}', '{self.weather}')"

@app.route("/")
@app.route("/home")
def home():
    new_weatherLog = Weather_Log(address="asddsa", weather="asdasds")
    db.session.add(new_weatherLog)
    
    try:
        db.session.commit()
    except exc.IntegrityError as exception:
        print(exception)
        db.session.rollback() 

    return str(Weather_Log.query.all())

if __name__ == '__main__':
    app.run(debug=True)
