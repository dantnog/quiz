from django.shortcuts import render
from .models import Question, Challenge, Score, User

def index(request):
	challenges = Challenge.objects.order_by('-id')
	return render(
		request, 'pages/index.html',
		{'challenges': challenges, 'id': 1}
	)