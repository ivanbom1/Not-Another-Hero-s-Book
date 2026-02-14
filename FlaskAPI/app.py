from flask import Flask
from dotenv import load_dotenv
import os
from config import Config
from models import db
from models.flaskModel import Story, Page, Choice
from routes.flaskRoutes import story_bp

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(story_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Tables created')
    app.run(debug=True)