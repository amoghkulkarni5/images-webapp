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
8. Insert one user with role 'admin' (Feature to be added based on 'admin' role later)

### Commands -
Start terminal from one level above project directory <br>
`source images_webapp/flask_env/bin/activate` <br>
`export FLASK_APP=images_webapp` <br>
`export FLASK_DEBUG=1` <br>
`export FLASK_ENV=development` <br>
`flask run` <br>

### Libraries-
Flask <br>
Flask Login <br>
Flask WTF <br>
flask-sqlalchemy <br>
mysqlclient <br>
Flask-Migrate <br>
Pillow
wand

`pip install flask flask-sqlalchemy flask-login`

### Setting UP DB interactions - 
sudo add-apt-repository 'deb http://archive.ubuntu.com/ubuntu bionic main' <br>
sudo apt update <br>
sudo apt install -y python-mysqldb <br>

### Running UP DB interactions - 
Log onto python interpreter one level above project directory (make sure pymsql is there)
`from images_webapp import db, create_app, models` <br>
`db.create_all(app=create_app())` <br>
`db.drop_all(app=create_app())` <br>

