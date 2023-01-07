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
]