# flask-images-webapp
This repo is for a webapp which stores images

Database String for SQL Alchemy - mysql://username:password@localhost/db_name

### Steps to setup DB-
1. `mysql -u root -p`
2. `CREATE USER 'amogh'@'localhost' IDENTIFIED BY 'amogh'`
3. `GRANT ALL PRIVILEGES ON * . * TO 'amogh'@'localhost';`
4. `FLUSH PRIVILEGES;`
5. Exit and login using `mysql -u amogh -p`
6. `CREATE DATABASE flask_webapp`
7. `USE flask_webapp`

Start python interpreter from one level above project directory

### Commands -
cd to project directory
`source flask_env/bin/activate`
cd one level up
`export FLASK_APP=images_webapp`
`export FLASK_ENV=development`
`flask run`

### Libraries-
Flask
Flask Login
Flask WTF
flask-sqlalchemy

`pip install flask flask-sqlalchemy flask-login`
