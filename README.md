# Inkredo Assignment

Required functionalities are missing a dashboard though the backend for the dashboard has been built.

# Build Instructions.

You can do this with or without a venv but I am gonna try include usage of a venv in the instructions.

* Make sure you have python 3.6 installed.
* `pip3 install virtualenv`
* Extract the project zip I sent you and open up a terminal to the project folder location.
*  `virtualenv inkredo-venv` This will create a virtual env.
*  `source inkredo-venv/bin/activate`
*  `pip install -r requirements.txt`

### Create a database inside postgresql to be used in the app.
* Drop to psql shell. `psql`
* `CREATE DATABASE inkredo;`
* `CREATE USER inkredo WITH PASSWORD <password here>;`
* `ALTER ROLE inkredo SET client_encoding TO 'utf8';`
* `ALTER ROLE inkredo SET default_transaction_isolation TO 'read committed';`
* `ALTER ROLE inkredo SET timezone TO 'UTC';`
* `GRANT ALL PRIVILEGES ON DATABASE inkredo TO inkredo;`
* Create a secrets file at `/etc/inkredo/secrets.conf`
Use the following schema:
```
[secrets]
secret_key = <a secret key over here>
db_user = inkredo
db_userpassword = <password you set here>
```
* Migrate the database using `python manage.py migrate`.

To start a web server run `python manage.py runserver`. A web server will start up at `localhost:8000`.

# Code Documentation.

So code is basically a standard Django app with standard places to find things.
I am gonna go in order of assignment elements detailing stuff. I would mention over here which is going to apply to requests at every endpoint. Every request to a logged in endpoint would expect presence of a CSRF header. This is a header value which can be obtained by doing a get request and doing all subsequent requests by passing the value of CSRF-token in cookies in form of request header using `X-CSRFToken` header.

### Companies and Users

Both companies and users follow a similar pattern for CRUD. Basically we have a
`/company` and a `/user` endpoint POSTing to which results in a creation of new user.
The payload for the POST request would look like the following:

Company:
```
{
	"name": "Yo",
	"registered_name": "yo ltd",
	"address": "foobar",
	"type": "1",
	"email": "yo@yo.com"
}
```
User:
```
{
	"full_name": "Yo Yo",
	"username": "adnrs96",
	"email": "a@b.com",
	"company_id": "1",
	"password": "qwerty"
}
```

Next we have endpoints to GET the user and company info. We use REST paradigm over here and have the following two endpoints to which we want to make GET requests.

Companies: `/company/<company_id>`
Users: `/user/<user_id>`

Moving forward we can delete the Companies and Users. We would want to make a DELETE request to the same endpoints we use for the GET requests to achieve a delete.

Lastly to perform an update we do a PATCH request at the same endpoints as above with the payload that looks similar to the following:

Companies:
```
{
	"update_field": "name",
	"update_value": "yo"
}
```

Users:
```
{
	"update_field": "company_id",
	"update_value": 5
}
```
user and after doing all the sanity checks create a new account and login the user into it.
Expects two parameters:
```
{
"email": "a@b.com",
"password": "@1234",
"username": "adnrs96"
}
```

Notice only limited fields can be updated. These are limited to:
For Companies- `name`, `address`, `type`
For Users- `full_name`, `company_id`

### User login and logout (Session maintainance)

Since I could use the Django's internal session maintainance middleware I did.
For the login I think code is pretty much self explanatory and resides inside `views/accounts.py`

* `/login` Expects two parameters and a POST request.
```
{
    "email": "a@b.com",
    "password": "yoyo@1234"
}
```
