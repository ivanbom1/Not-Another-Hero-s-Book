from django.urls import path
from game.views import (
    StoriesListView,
    StoryDetailView,
    PlayStoryView,
    StatsView,
    CreateStoryView,
    EditStoryView,
    DeleteStoryView,
    AddPageView,
    AddChoiceView,
    DeletePageView,
    DeleteChoiceView
)

urlpatterns = [

    path('', StoriesListView.as_view(), name='stories_list'),
    path('stories/<int:story_id>/', StoryDetailView.as_view(), name='story_detail'),

    path('play/<int:story_id>/', PlayStoryView.as_view(), name='play_story'),
    path('play/<int:story_id>/<int:page_id>/', PlayStoryView.as_view(), name='play_page'),

    path('stats/', StatsView.as_view(), name='stats'),

    path('author/create/', CreateStoryView.as_view(), name='create_story'),
    path('author/edit/<int:story_id>/', EditStoryView.as_view(), name='edit_story'),
    path('author/delete/<int:story_id>/', DeleteStoryView.as_view(), name='delete_story'),
    path('author/page/<int:story_id>/', AddPageView.as_view(), name='add_page'),
    path('author/choice/<int:story_id>/<int:page_id>/', AddChoiceView.as_view(), name='add_choice'),
    path('author/delete-page/<int:story_id>/<int:page_id>/', DeletePageView.as_view(), name='delete_page'),
    path('author/delete-choice/<int:story_id>/<int:page_id>/<int:choice_id>/', DeleteChoiceView.as_view(), name='delete_choice'),
]