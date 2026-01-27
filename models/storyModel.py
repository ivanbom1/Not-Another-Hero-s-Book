from . import db

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), unique=True, nullable=False)
    status = db.Column(db.String(9), unique=False, nullable=False)
    start_page_id = db.Column(db.Integer, default=1, nullable=False)