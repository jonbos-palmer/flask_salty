# SALTY

## Objective
Implement salting + password hashing with a simple login system

## Build and Run

1. Install dependencies with package manager of your choice. For pipenv run:

        $ pipenv install -r requirements.txt

2. Set FLASK_APP environment variable:

        $ export FLASK_APP=salty

3. Build database:

        $ flask init_db

4. Run app:
   
        $ flask run

## NOTE
It is not advisable to roll-your-own hashing + salting. Please do not use this code for your security needs. There are several Flask-specific libraries for handling login. Check out [Flask-Login](https://github.com/maxcountryman/flask-login)