from flask import Flask
from config import Config
from models import db
from models.flaskModel import Story, Page, Choice
from routes.flaskRoutes import story_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    app.register_blueprint(story_bp)
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)