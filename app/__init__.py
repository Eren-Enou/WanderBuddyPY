from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.template_folder = 'templates'
    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)



if __name__ == '__main__':
    app.run(debug=True)

from app import routes