from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:challenge_id>', views.challenge, name = 'challenge'),
	path('solved', views.solved, name = 'solved'),
	path('scores/<int:challenge_id>', views.scores, name = 'scores'),
	path('auth', views.auth, name = 'auth'),
	path('auth/logout', views.logout, name = 'logout'),
	path('new/challenge', views.new_challenge, name = 'new_challenge'),
	path('new/question/<int:challenge_id>', views.new_question, name = 'new_question'),
	path('mychallenges', views.my_challenges, name = 'my_challenges'),
	path('delete/challenge/<int:challenge_id>', views.delete_challenge, name = 'delete_challenge'),
	path('delete/question/<int:question_id>', views.delete_question, name = 'delete_question'),
	path('edit/challenge/<int:challenge_id>', views.edit_challenge, name = 'edit_challenge'),
	path('edit/selectquestion/<int:challenge_id>', views.select_question, name = 'select_question'),
	path('edit/question/<int:question_id>', views.edit_question, name = 'edit_question'),
	path('search', views.search, name='search'),
]