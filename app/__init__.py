from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from . import routes

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    print(app)
    app.config.from_object('config.Config')
    db.init_app(app)
    return app

app = create_app()

migrate = Migrate(app, db)



if __name__ == '__main__':
    app.run(debug=True)

