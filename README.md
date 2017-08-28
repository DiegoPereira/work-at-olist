Hi, welcome to my implementation of the olist challenge.

First, we need to install and configure postgrees.

Install dependencies for PostgreSQL to work with Django with this command:
```
sudo apt-get install libpq-dev python-dev
```
Install postgres
```
sudo apt-get install postgresql postgresql-contrib
```
- Create db and user 
```
sudo su - postgres
createdb <mydb>
createuser -P <myuser>
```

Grant privileges to your user
```
psql
GRANT ALL PRIVILEGES ON DATABASE <mydb> TO <myuser>;
ALTER USER <myuser> CREATEDB;
```

In the file work-at-olist/workatolist/settings.py, change the database configuration using postgres credentials.
```
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mydb',                      # Or path to database file if using sqlite3.
            'USER': 'myuser',
            'PASSWORD': 'password',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
```

Install the requirements
```
pip install -r requirements.txt
```

Create the tables and migrations
```
python manage.py makemigrations
python manage.py migrate
```

Now we can import the channel's csv, each parent channel must be referenced before its descendent.

```
Books
Books / National Literature
Books / National Literature / Science Fiction
```

Run the import command
```
python manage.py importcategories <channel_name> <csv_filename>
```

Run Web Aplication
```
python manage.py runserver
```

Heroku link

https://diegopereiraolist.herokuapp.com/

## Application API

List all the channels
```
your_host + /channels/channels/
```
List all categories of a channel
```
your_host + /channels/categories?channel=<channel_name>
```
Retrieve ancestors and descendants of a category, even if exists two with the same name
```
your_host + /channels/relatives?category=<category_name>
```
