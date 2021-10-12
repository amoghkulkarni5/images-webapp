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
8. `INSERT INTO user(email,password,name) VALUES ('amoghkulkarni5@gmail.com','password','amogh');`

Start python interpreter from one level above project directory

### Commands -
cd to project directory
`source flask_env/bin/activate`
cd one level up
`export FLASK_APP=images_webapp`
`export FLASK_DEBUG=1`
`export FLASK_ENV=development`
`flask run`

### Libraries-
Flask <br>
Flask Login <br>
Flask WTF <br>
flask-sqlalchemy <br>
mysqlclient

`pip install flask flask-sqlalchemy flask-login`

### Setting UP DB interactions - 
sudo add-apt-repository 'deb http://archive.ubuntu.com/ubuntu bionic main'
sudo apt update
sudo apt install -y python-mysqldb

### Running UP DB interactions - 
Log onto python interpreter one level above project directory (make sure pymsql is there)
`from images_webapp import db, create_app, models`
`db.create_all(app=create_app())`

