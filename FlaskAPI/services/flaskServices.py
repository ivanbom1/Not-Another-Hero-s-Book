from models import db
from models.flaskModel import Story, Page, Choice

class StoryService:

    @staticmethod
    def get_all_published_stories():
        return Story.query.filter_by(status='published').all()
    

    @staticmethod
    def get_story_by_id(story_id):
        return Story.query.get(story_id)
    

    @staticmethod
    def get_story_start_page(story_id):
        story = Story.query.get(story_id)
        if not story:
            return None
        return Page.query.get(story.start_page_id)


    @staticmethod
    def get_page_by_id(page_id):
        return Page.query.get(page_id)
    

    @staticmethod
    def create_story(title, description):
        story = Story(title=title, description=description, status='draft')
        db.session.add(story)
        db.session.commit()
        return story
    
    
    @staticmethod
    def update_story(story_id, title=None, description=None, status=None):

        story = Story.query.get(story_id)
        if not story:
            return None
        if title:
            story.title = title
        if description:
            story.description = description
        if status:
            story.status = status
        db.session.commit()
        return story
    
    
    @staticmethod
    def delete_story(story_id):
        story = Story.query.get(story_id)
        if story:
            db.session.delete(story)
            db.session.commit()
        return story
    
    @staticmethod
    def create_page(story_id, text, is_ending=False, ending_label=None):
        story = Story.query.get(story_id)
        if not story:
            return None
        page = Page(story_id=story_id, text=text, is_ending=is_ending, ending_label=ending_label)
        db.session.add(page)
        db.session.commit()
        return page


    @staticmethod
    def create_choice(page_id, text, next_page_id):
        page = Page.query.get(page_id)
        if not page:
            return None
        choice = Choice(page_id=page_id, text=text, next_page_id=next_page_id)
        db.session.add(choice)
        db.session.commit()
        return choice