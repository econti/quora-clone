# Quora clone
Quora clone written in Django.

![alt tag](http://i.imgur.com/vj4TQFg.jpg)

### Installation
```
# clone repo
git clone https://github.com/econti/quora-clone.git
# go into repo
cd repo_name
# make a virtual environment
virtualenv env
# start the env
. env/bin/activate
# install the requirements
pip install -r requirements.txt
```
Now set up your db. Install postgres and make sure you are running it.
```
psql
create database quora;
```

Now set up the environment variables.
```
# make .env file in root of directory with following variables
DEBUG=True
SECRET_KEY='mys3cr3tk3y'
DATABASE_URL='postgres://<your_pg_username>:p4ssw0rd@localhost:5432/quora'
```

Now run the database migrations
```
python manage.py migrate
```
Create superuser for admin site
```
python manage.py createsuperuser
```
Now run the server
```
python manage.py runserver
```
### Fb Auth & Authenticating users
There are two ways to create users. One via fb authentication and the other via the app's authentication.

For the app's native authentication vist `localhost:8000/hidden_login`. To set up fb auth simply create a new fb app and modify the following variables in `settings.py`.
```
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET =''
```
