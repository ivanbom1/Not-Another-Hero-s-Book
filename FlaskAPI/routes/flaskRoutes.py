from flask import Blueprint
from controllers.flaskControllers import StoryController

story_bp = Blueprint('stories', __name__, url_prefix='/api')

#story_bp.route('/stories', methods=['GET'])(StoryController.get_published_stories)
story_bp.route('/stories/<int:story_id>', methods=['GET'])(StoryController.get_story)
story_bp.route('/stories/<int:story_id>/start', methods=['GET'])(StoryController.get_story_start)
story_bp.route('/pages/<int:page_id>', methods=['GET'])(StoryController.get_page)
story_bp.route('/stories/<int:story_id>/pages', methods=['GET'])(StoryController.get_story_pages)
story_bp.route('/stories', methods=['GET'])(StoryController.get_all_stories)


story_bp.route('/stories', methods=['POST'])(StoryController.create_story)
story_bp.route('/stories/<int:story_id>', methods=['PUT'])(StoryController.update_story)
story_bp.route('/stories/<int:story_id>', methods=['DELETE'])(StoryController.delete_story)
story_bp.route('/stories/<int:story_id>/pages', methods=['POST'])(StoryController.create_page)
story_bp.route('/pages/<int:page_id>/choices', methods=['POST'])(StoryController.create_choice)
story_bp.route('/pages/<int:page_id>', methods=['DELETE'])(StoryController.delete_page)
story_bp.route('/choices/<int:choice_id>', methods=['DELETE'])(StoryController.delete_choice)
