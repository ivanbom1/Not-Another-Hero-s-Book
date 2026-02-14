from . import db

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(20), default='draft', nullable=False)  # draft/published/suspended
    start_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    
    pages = db.relationship('Page', backref='story', cascade='all, delete-orphan')

class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    text = db.Column(db.String(4096), nullable=False)
    is_ending = db.Column(db.Boolean, default=False, nullable=False)
    ending_label = db.Column(db.String(255))
    
    choices = db.relationship('Choice', backref='page', cascade='all, delete-orphan')

class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)