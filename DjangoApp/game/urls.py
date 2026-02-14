from django.urls import path
from game.views import *
from game.auth_views import RegisterView, LoginView, LogoutView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Story browsing
    path('', StoriesListView.as_view(), name='stories_list'),
    path('stories/<int:story_id>/', StoryDetailView.as_view(), name='story_detail'),
    
    # Playing
    path('play/<int:story_id>/', PlayStoryView.as_view(), name='play_story'),
    path('play/<int:story_id>/<int:page_id>/', PlayStoryView.as_view(), name='play_page'),
    
    # Statistics
    path('stats/', StatsView.as_view(), name='stats'),
    
    # Author tools
    path('author/create/', CreateStoryView.as_view(), name='create_story'),
    path('author/edit/<int:story_id>/', EditStoryView.as_view(), name='edit_story'),
    path('author/delete/<int:story_id>/', DeleteStoryView.as_view(), name='delete_story'),
    path('author/page/<int:story_id>/', AddPageView.as_view(), name='add_page'),
    path('author/choice/<int:story_id>/<int:page_id>/', AddChoiceView.as_view(), name='add_choice'),
    path('author/delete-page/<int:story_id>/<int:page_id>/', DeletePageView.as_view(), name='delete_page'),
    path('author/delete-choice/<int:story_id>/<int:page_id>/<int:choice_id>/', DeleteChoiceView.as_view(), name='delete_choice'),
]