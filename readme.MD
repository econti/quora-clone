# quora

How to get set up to dev.

```
# clone repo
git clone https://<bitbucket_username>@bitbucket.org/edoardoconti/quora.git
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
python manage.py syncdb
```
Create superuser for admin site
```
python manage.py createsuperuser
```
Seed the db with some fake data
```
python quora/scripts/seed_db.py
```
Now run the server
```
python manage.py runserver
```
