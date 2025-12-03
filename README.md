# Fwittewr_flask

A simple **Twitter-like social network** built with **Flask**.

---

## 🚀 Features

- User registration and login  
- Posting short messages
- liking posts
- commenting posts
- commenting other comments

---

## 🧱 Project Structure
```
/Fwittewr_flask
│
├── app/ # Main Flask application package
│ ├── routes/ # urls with request implementation
│ ├── static/ # html dependencies (bootstrap) and images
|  ├── bootstrap/
|  └── icons/
│ ├── templates/ # all html + jinja templates
|  ├── authentication/
|  ├── errors/
|  ├── home/
|  └── base.html
│ ├── __init__.py # base setup
│ ├── extensions.py # db, app, bcrypt, login configurations
│ ├── forms.py #wtf forms
│ ├── models.py # entities definition
├── instance/
| └──database.db
├── app.py # Application entrypoint
└── README.md # This file
```
---

## 🛠️ Technologies Used (dependencies)

- Flask
- Flask Login
- SQLAlchemy
- Jinja2
- Flask-WTF
- Bcrypt
- SQLite (for dev purposes, should be changed if ever put into production)
