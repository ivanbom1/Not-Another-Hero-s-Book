from flask import request, jsonify
from services.flaskServices import StoryService


class StoryController:

    @staticmethod
    def get_published_stories():

        try:
            stories = StoryService.get_all_published_stories()
            return jsonify([{
                'id': s.id,
                'title': s.title,
                'description': s.description,
                'status': s.status,
                'start_page_id': s.start_page_id
            } for s in stories]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def get_story(story_id):

        try:
            story = StoryService.get_story_by_id(story_id)
            if not story:
                return jsonify({'error': 'Story not found'}), 404
            return jsonify({
                'id': story.id,
                'title': story.title,
                'description': story.description,
                'status': story.status,
                'start_page_id': story.start_page_id
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def get_story_start(story_id):

        try:
            page = StoryService.get_story_start_page(story_id)
            if not page:
                return jsonify({'error': 'Story or start page not found'}), 404
            return jsonify({
                'id': page.id,
                'story_id': page.story_id,
                'text': page.text,
                'is_ending': page.is_ending,
                'ending_label': page.ending_label,
                'choices': [{
                    'id': c.id,
                    'text': c.text,
                    'next_page_id': c.next_page_id
                } for c in page.choices]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def get_page(page_id):
        
        try:
            page = StoryService.get_page_by_id(page_id)
            if not page:
                return jsonify({'error': 'Page not found'}), 404
            return jsonify({
                'id': page.id,
                'story_id': page.story_id,
                'text': page.text,
                'is_ending': page.is_ending,
                'ending_label': page.ending_label,
                'choices': [{
                    'id': c.id,
                    'text': c.text,
                    'next_page_id': c.next_page_id
                } for c in page.choices]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def create_story():

        try:
            data = request.get_json()
            if not data or not data.get('title') or not data.get('description'):
                return jsonify({'error': 'title and description required'}), 400
            
            story = StoryService.create_story(data['title'], data['description'])
            return jsonify({
                'id': story.id,
                'title': story.title,
                'description': story.description,
                'status': story.status,
                'message': 'Story created'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
   
    
    @staticmethod
    def update_story(story_id):
        
        try:
            story = StoryService.get_story_by_id(story_id)
            if not story:
                return jsonify({'error': 'Story not found'}), 404
            
            data = request.get_json()
            updated_story = StoryService.update_story(
                story_id,
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status')
            )
            return jsonify({
                'id': updated_story.id,
                'title': updated_story.title,
                'description': updated_story.description,
                'status': updated_story.status,
                'message': 'Story updated'
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def delete_story(story_id):
        
        try:
            story = StoryService.get_story_by_id(story_id)
            if not story:
                return jsonify({'error': 'Story not found'}), 404
            
            StoryService.delete_story(story_id)
            return jsonify({'message': 'Story deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def create_page(story_id):
        
        try:
            story = StoryService.get_story_by_id(story_id)
            if not story:
                return jsonify({'error': 'Story not found'}), 404
            
            data = request.get_json()
            if not data or not data.get('text'):
                return jsonify({'error': 'text required'}), 400
            
            page = StoryService.create_page(
                story_id,
                text=data['text'],
                is_ending=data.get('is_ending', False),
                ending_label=data.get('ending_label')
            )
            return jsonify({
                'id': page.id,
                'story_id': page.story_id,
                'text': page.text,
                'is_ending': page.is_ending,
                'ending_label': page.ending_label,
                'message': 'Page created'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

    @staticmethod
    def create_choice(page_id):
        
        try:
            page = StoryService.get_page_by_id(page_id)
            if not page:
                return jsonify({'error': 'Page not found'}), 404
            
            data = request.get_json()
            if not data or not data.get('text') or not data.get('next_page_id'):
                return jsonify({'error': 'text and next_page_id required'}), 400
            
            choice = StoryService.create_choice(
                page_id,
                text=data['text'],
                next_page_id=data['next_page_id']
            )
            return jsonify({
                'id': choice.id,
                'page_id': choice.page_id,
                'text': choice.text,
                'next_page_id': choice.next_page_id,
                'message': 'Choice created'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500