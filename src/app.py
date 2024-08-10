from flask import Flask
from database.database import db
from controllers.api import api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
