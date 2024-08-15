import os
from flask import Flask
from database.database import db
from controllers.api import api
from controllers.template import template

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, '../database.db')}"

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api)
app.register_blueprint(template)

if __name__ == "__main__":
    app.run(debug=True)
