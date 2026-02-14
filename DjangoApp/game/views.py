from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Count, Q
from game.services import FlaskAPIService
from game.models import Play
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from game.models import UserProfile
from django.http import HttpResponseForbidden
from game.models import UserProfile


class StoriesListView(View):

    def get(self, request):

        all_stories = FlaskAPIService.get_all_stories()

        if request.user.is_staff:

            stories = all_stories
        else:

            stories = [s for s in all_stories if s.get('status') == 'published']

        published = [s['id'] for s in all_stories if s.get('status') == 'published']
        if published:
            Play.objects.exclude(story_id__in=published).delete()

        for story in stories:
            story['plays'] = Play.objects.filter(story_id=story['id']).count()
        
        return render(request, 'stories/list.html', {
            'stories': stories,
        })

@method_decorator(login_required, name='dispatch')
class StoryDetailView(View):

    def get(self, request, story_id):
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        plays = Play.objects.filter(story_id=story_id)
        total_plays = plays.count()

        endings = plays.values('ending_label').annotate(count=Count('id'))

        return render(request, 'stories/detail.html', {
            'story': story,
            'total_plays': total_plays,
            'endings': endings
        })

@method_decorator(login_required, name='dispatch')
class PlayStoryView(View):

    
    def get(self, request, story_id, page_id=None):

        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('status') == 'suspended':
            return render(request, 'play/suspended.html', {
                'story': story
            })

        if page_id is None:
            page = FlaskAPIService.get_story_start(story_id)
        else:
            page = FlaskAPIService.get_page(page_id)
        
        if not page:
            return redirect('story_detail', story_id=story_id)

        request.session['current_story'] = story_id
        request.session['current_page'] = page['id']
        
        return render(request, 'play/page.html', {
            'story': story,
            'page': page,
            'is_ending': page.get('is_ending', False)
        })
    
    def post(self, request, story_id, page_id=None):
        story = FlaskAPIService.get_story(story_id)

        if story and story.get('status') == 'suspended':
            return render(request, 'play/suspended.html', {
                'story': story
            })
        
        next_page_id = request.POST.get('next_page_id')
        
        if not next_page_id:
            return redirect('play_story', story_id=story_id)

        next_page = FlaskAPIService.get_page(int(next_page_id))
        if not next_page:
            return redirect('play_story', story_id=story_id)

        if next_page.get('is_ending', False):
            Play.objects.create(
                user=request.user if request.user.is_authenticated else None,
                story_id=story_id,
                ending_page_id=next_page['id'],
                ending_label=next_page.get('ending_label', 'Unknown Ending')
            )

            request.session.pop('current_story', None)
            request.session.pop('current_page', None)
            
            return render(request, 'play/ending.html', {
                'story': story,
                'page': next_page
            })

        request.session['current_page'] = next_page['id']
        return render(request, 'play/page.html', {
            'story': story,
            'page': next_page,
            'is_ending': False
        })


class StatsView(View):

    def get(self, request):

        stories = FlaskAPIService.get_all_stories()
        
        stats_data = []
        for story in stories:
            plays = Play.objects.filter(story_id=story['id'])
            total_plays = plays.count()
            
            if total_plays > 0:

                endings = plays.values('ending_label').annotate(count=Count('id'))

                for ending in endings:
                    ending['percentage'] = round((ending['count'] / total_plays) * 100, 1)
                
                stats_data.append({
                    'story': story,
                    'total_plays': total_plays,
                    'endings': list(endings)
                })
        
        total_plays_overall = Play.objects.count()
        
        return render(request, 'stats/index.html', {
            'stats_data': stats_data,
            'total_plays': total_plays_overall
        })

@method_decorator(login_required, name='dispatch')
class EditStoryView(View):

    def get(self, request, story_id):
        if not request.user.is_authenticated:
            return redirect('login')

        user_profile = request.user.userprofile
        if user_profile.role not in ['author', 'admin'] and not request.user.is_staff:
            return HttpResponseForbidden("Only authors can edit stories")
        
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        pages = FlaskAPIService.get_story_pages(story_id)
        
        return render(request, 'author/edit_story.html', {
            'story': story,
            'pages': pages
        })

    def post(self, request, story_id):
        if not request.user.is_authenticated:
            return redirect('login')

        user_profile = request.user.userprofile
        if user_profile.role not in ['author', 'admin'] and not request.user.is_staff:
            return HttpResponseForbidden("Only authors can edit stories")

        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'draft')
        
        story = FlaskAPIService.update_story(story_id, title, description, status)
        if story:
            return redirect('edit_story', story_id=story_id)
        else:
            return render(request, 'author/edit_story.html', {
                'story': FlaskAPIService.get_story(story_id),
                'pages': FlaskAPIService.get_story_pages(story_id),
                'error': 'Failed to update story'
            })

@method_decorator(login_required, name='dispatch')
class DeleteStoryView(View):

    def post(self, request, story_id):
        if not request.user.is_authenticated:
            return redirect('login')

        user_profile = request.user.userprofile
        if user_profile.role not in ['author', 'admin'] and not request.user.is_staff:
            return HttpResponseForbidden("Only authors can delete stories")

        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only delete your own stories")

        if FlaskAPIService.delete_story(story_id):
            Play.objects.filter(story_id=story_id).delete()
            return redirect('stories_list')
        else:
            return redirect('edit_story', story_id=story_id)

@method_decorator(login_required, name='dispatch')
class CreateStoryView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        user_profile = request.user.userprofile
        if user_profile.role not in ['author', 'admin'] and not request.user.is_staff:
            return HttpResponseForbidden("Only authors can create stories")
        
        return render(request, 'author/create_story.html')
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        user_profile = request.user.userprofile
        if user_profile.role not in ['author', 'admin'] and not request.user.is_staff:
            return HttpResponseForbidden("Only authors can create stories")
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if not title or not description:
            return render(request, 'author/create_story.html', {
                'error': 'Title and description are required'
            })

        story = FlaskAPIService.create_story(title, description, author_id=request.user.username)
        if story:

            if not story.get('author_id'):
                story['author_id'] = request.user.username
            return redirect('edit_story', story_id=story['id'])
        else:
            return render(request, 'author/create_story.html', {
                'error': 'Failed to create story'
            })

@method_decorator(login_required, name='dispatch')
class DeleteStoryView(View):

    def post(self, request, story_id):
        if FlaskAPIService.delete_story(story_id):
            return redirect('stories_list')
        else:
            return redirect('edit_story', story_id=story_id)

@method_decorator(login_required, name='dispatch')
class AddPageView(View):

    def get(self, request, story_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        return render(request, 'author/add_page.html', {'story': story})
    
    def post(self, request, story_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        text = request.POST.get('text')
        is_ending = request.POST.get('is_ending') == 'on'
        ending_label = request.POST.get('ending_label') if is_ending else None
        
        if not text:
            return render(request, 'author/add_page.html', {
                'story': story,
                'error': 'Page text is required'
            })
        
        page = FlaskAPIService.create_page(story_id, text, is_ending, ending_label)
        if page:
            return redirect('edit_story', story_id=story_id)
        else:
            return render(request, 'author/add_page.html', {
                'story': story,
                'error': 'Failed to create page'
            })

    def post(self, request, story_id):
        text = request.POST.get('text')
        is_ending = request.POST.get('is_ending') == 'on'
        ending_label = request.POST.get('ending_label') if is_ending else None

        if not text:
            return render(request, 'author/add_page.html', {
                'story': FlaskAPIService.get_story(story_id),
                'error': 'Page text is required'
            })

        page = FlaskAPIService.create_page(story_id, text, is_ending, ending_label)
        if page:
            return redirect('edit_story', story_id=story_id)
        else:
            return render(request, 'author/add_page.html', {
                'story': FlaskAPIService.get_story(story_id),
                'error': 'Failed to create page'
            })

@method_decorator(login_required, name='dispatch')
class AddChoiceView(View):

    def get(self, request, story_id, page_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        page = FlaskAPIService.get_page(page_id)
        
        if not story or not page:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        return render(request, 'author/add_choice.html', {
            'story': story,
            'page': page,
            'story_pages': FlaskAPIService.get_story_pages(story_id)
        })
    
    def post(self, request, story_id, page_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        page = FlaskAPIService.get_page(page_id)
        
        if not story or not page:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        text = request.POST.get('text')
        next_page_id = request.POST.get('next_page_id')
        
        if not text or not next_page_id:
            story_pages = FlaskAPIService.get_story_pages(story_id)
            return render(request, 'author/add_choice.html', {
                'story': story,
                'page': page,
                'story_pages': story_pages,
                'error': 'Text and next page are required'
            })
        
        choice = FlaskAPIService.create_choice(page_id, text, int(next_page_id))
        if choice:
            return redirect('edit_story', story_id=story_id)
        else:
            story_pages = FlaskAPIService.get_story_pages(story_id)
            return render(request, 'author/add_choice.html', {
                'story': story,
                'page': page,
                'story_pages': story_pages,
                'error': 'Failed to create choice'
            })

@method_decorator(login_required, name='dispatch')
class DeletePageView(View):

    def post(self, request, story_id, page_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        if FlaskAPIService.delete_page(page_id):
            return redirect('edit_story', story_id=story_id)
        else:
            return redirect('edit_story', story_id=story_id)

@method_decorator(login_required, name='dispatch')
class DeleteChoiceView(View):

    def post(self, request, story_id, page_id, choice_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        story = FlaskAPIService.get_story(story_id)
        if not story:
            return redirect('stories_list')

        if story.get('author_id') != request.user.username and not request.user.is_staff:
            return HttpResponseForbidden("You can only edit your own stories")
        
        if FlaskAPIService.delete_choice(choice_id):
            return redirect('edit_story', story_id=story_id)
        else:
            return redirect('edit_story', story_id=story_id)