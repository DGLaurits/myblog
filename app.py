import os
from flask import Flask
from extensions import db
from routes.blog import blog_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = os.environ['SECRET_CODE']

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)