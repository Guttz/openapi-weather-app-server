python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt


##To check for code quality run
pylint main_flask.py