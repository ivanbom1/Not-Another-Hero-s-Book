from models import db

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(20), default='draft', nullable=False)
    start_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    author_id = db.Column(db.String(255), nullable=True)  # Store Django username or ID
    
    def __str__(self):
        return self.title

class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(4096), nullable=False)
    is_ending = db.Column(db.Boolean, default=False, nullable=False)
    ending_label = db.Column(db.String(255))
    
    choices = db.relationship('Choice', backref='page', cascade='all, delete-orphan', foreign_keys='Choice.page_id')

class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)