# brain-tec Assignment

## Contact

Project by: José Carlos Rodríguez Cortés

Email: josecarlosrodriguezcortes@gmail.com

Phone: +34 694479093

## Description

This is a project of a book of contacts wrote in Python with Flask for the assignment of brain-tec.

## How to run

To run this program you're gonna need to install some libraries of Python and set some environment variables.

### First steps

Open a Linux Shell (or Windows PowerShell) inside the folder of the project and write the next command:

````
pip install -r requirements.txt
````
Now you need to set the environment variables to config Flask.
Write the next commands:

If you use Linux or Mac:

````
export FLASK_APP=rodriguez_cortes_jose_carlos
export FLASK_ENV=development
````

If you use Windows CMD:

````
set FLASK_APP=rodriguez_cortes_jose_carlos
set FLASK_ENV=development
````

If you use Windows PowerShell:

````
$env:FLASK_APP = "rodriguez_cortes_jose_carlos"
$env:FLASK_ENV = "development"
````

### Change the config.py file

Open the config.py file with your prefered editor and change the next fields to fit your data:

````
PORT = 3306 # The DB port
DATABASE = "exercise" # The DB Name
USER = "root" # Your user in the DB
PASSWORD = "1111" # DB password
````

Do the same in the test_config.py file to configure the database for the tests:

````
PORT = 3306 # The DB port
DATABASE = "test_exercise" # The test DB Name
USER = "root" # Your user in the DB
PASSWORD = "1111" # DB password
````

### Init the database

Now, we've finished the work inside the assignment folder so go back:

````
cd ..
````

And now execute the following commands:

````
flask init-db
````

This will initialize the database with the next SQL code (written here for most readability):

````
CREATE DATABASE IF NOT EXISTS exercise CHARACTER SET utf8;
USE exercise;
DROP TABLE IF EXISTS contact;
CREATE TABLE contact (
    contact_id  MEDIUMINT NOT NULL AUTO_INCREMENT,
    firstname   VARCHAR(100) NOT NULL,
    lastname    VARCHAR(100) NOT NULL,
    address     VARCHAR(200),
    /* Since this is a contact-book, the email can't be repeated... */
    email       VARCHAR(100) NOT NULL UNIQUE,
    /* [...] neither the phone number. */
    phone       VARCHAR(30) UNIQUE,
    PRIMARY KEY (contact_id)
);
````

### Running the test and coverage

To run the tests:

````
pytest -sv
````

To run the coverage report:

````
coverage run -m pytest
coverage report
````

### Running the application

To run the application just execute:

````
flask run -p 80
````