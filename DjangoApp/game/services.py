import requests
import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(ENV_PATH)

FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:5000/api')
FLASK_API_KEY = os.getenv('FLASK_API_KEY', 'nahb-secret-key-2026')

class FlaskAPIService:
    
    @staticmethod
    def _get_headers():
        return {
            'Content-Type': 'application/json',
            'X-API-KEY': FLASK_API_KEY
        }
    
    @staticmethod
    def get_published_stories():
        try:
            response = requests.get(f'{FLASK_API_URL}/stories', params={'status': 'published'})
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching stories: {e}")
            return []

    @staticmethod
    def get_story(story_id):
        try:
            response = requests.get(f'{FLASK_API_URL}/stories/{story_id}')
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            return None

    @staticmethod
    def get_story_start(story_id):
        try:
            response = requests.get(f'{FLASK_API_URL}/stories/{story_id}/start')
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching story start {story_id}: {e}")
            return None

    @staticmethod
    def get_page(page_id):
        try:
            response = requests.get(f'{FLASK_API_URL}/pages/{page_id}')
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching page {page_id}: {e}")
            return None

    @staticmethod
    def get_story_pages(story_id):
        try:
            response = requests.get(f'{FLASK_API_URL}/stories/{story_id}/pages')
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def create_story(title, description, author_id=None):
        try:
            data = {'title': title, 'description': description}
            if author_id:
                data['author_id'] = author_id
            response = requests.post(f'{FLASK_API_URL}/stories', json=data, headers=FlaskAPIService._get_headers())
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            print(f"Error creating story: {e}")
            return None

    @staticmethod
    def update_story(story_id, title=None, description=None, status=None):
        try:
            data = {}
            if title:
                data['title'] = title
            if description:
                data['description'] = description
            if status:
                data['status'] = status
            response = requests.put(f'{FLASK_API_URL}/stories/{story_id}', json=data, headers=FlaskAPIService._get_headers())
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error updating story {story_id}: {e}")
            return None
    
    @staticmethod
    def delete_story(story_id):
        try:
            response = requests.delete(f'{FLASK_API_URL}/stories/{story_id}', headers=FlaskAPIService._get_headers())
            return response.status_code == 200
        except Exception as e:
            print(f"Error deleting story {story_id}: {e}")
            return False
    
    @staticmethod
    def create_page(story_id, text, is_ending=False, ending_label=None):
        try:
            data = {
                'text': text,
                'is_ending': is_ending,
            }
            if ending_label:
                data['ending_label'] = ending_label
            response = requests.post(f'{FLASK_API_URL}/stories/{story_id}/pages', json=data, headers=FlaskAPIService._get_headers())
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            print(f"Error creating page: {e}")
            return None
    
    @staticmethod
    def create_choice(page_id, text, next_page_id):
        try:
            data = {'text': text, 'next_page_id': next_page_id}
            response = requests.post(f'{FLASK_API_URL}/pages/{page_id}/choices', json=data, headers=FlaskAPIService._get_headers())
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            print(f"Error creating choice: {e}")
            return None

    @staticmethod
    def delete_page(page_id):
        try:
            response = requests.delete(f'{FLASK_API_URL}/pages/{page_id}', headers=FlaskAPIService._get_headers())
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete_choice(choice_id):
        try:
            response = requests.delete(f'{FLASK_API_URL}/choices/{choice_id}', headers=FlaskAPIService._get_headers())
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    @staticmethod
    def get_all_stories():

        try:
            response = requests.get(f'{FLASK_API_URL}/stories')
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching stories: {e}")
            return []