# SALTY

## Objective
Implement salting + password hashing with a simple login system

## Build and Run

1. Install dependencies with package manager of your choice. For pipenv run:

        $ pipenv install -r requirements.txt

2. Activate your virtual environment. For pipenv, run:

        $ pipenv shell

3. Set FLASK_APP environment variable:

        (flask_salty) $ export FLASK_APP=salty

4. Build database:

        (flask_salty) $ flask init_db

5. Run app:
   
        (flask_salty) $ flask run

## NOTE
It is not advisable to roll-your-own hashing + salting. Please do not use this code for your security needs. There are several Flask-specific libraries for handling login. Check out [Flask-Login](https://github.com/maxcountryman/flask-login)