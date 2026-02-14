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

        if story.start_page_id is None:
            story.start_page_id = page.id
            db.session.commit()

        previous_page = Page.query.filter_by(story_id=story_id).filter(Page.id != page.id).order_by(Page.id.desc()).first()
        if previous_page and not previous_page.is_ending:

            existing_choice = Choice.query.filter_by(page_id=previous_page.id).first()
            if not existing_choice:

                choice = Choice(page_id=previous_page.id, text="Continue", next_page_id=page.id)
                db.session.add(choice)
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


    @staticmethod
    def get_story_pages(story_id):

        pages = Page.query.filter_by(story_id=story_id).all()
        if not pages:
            return []

        page_id_to_seq = {page.id: idx for idx, page in enumerate(pages, 1)}

        pages_with_seq = []
        for idx, page in enumerate(pages, 1):
            page_dict = {
                'id': page.id,
                'story_id': page.story_id,
                'text': page.text,
                'is_ending': page.is_ending,
                'ending_label': page.ending_label,
                'sequence': idx,
                'choices': [{
                    'id': c.id,
                    'text': c.text,
                    'next_page_id': c.next_page_id,
                    'next_page_sequence': page_id_to_seq.get(c.next_page_id, '?')  # Add this
                } for c in page.choices]
            }
            pages_with_seq.append(page_dict)

        return pages_with_seq
    
    
    @staticmethod
    def delete_page(page_id):

        page = Page.query.get(page_id)
        if not page:
            return False

        story_id = page.story_id


        story = Story.query.get(story_id)
        if story and story.start_page_id == page_id:

            next_start_page = Page.query.filter_by(story_id=story_id).filter(Page.id != page_id).order_by(Page.id).first()
            story.start_page_id = next_start_page.id if next_start_page else None

        db.session.delete(page)
        db.session.commit()
        return True
    
    @staticmethod
    def delete_choice(choice_id):

        choice = Choice.query.get(choice_id)
        if choice:
            db.session.delete(choice)
            db.session.commit()
            return True
        return False