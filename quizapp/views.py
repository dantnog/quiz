from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Challenge, Score, User

def index(request):
	try:
		challenges = Challenge.objects.order_by('-id')
		return render(
			request, 'pages/index.html',
			{'challenges': challenges, 'id': 1}
		)
	except Challenge.DoesNotExist:
		print('*****\n[ERROR] Getting challenges\n*****')
		return HttpResponse(status=404)
		#raise Http404('Challenge not found')

def challenge(request, challenge_id):
	try:
		questions = Question.objects.filter(challenge_id=challenge_id)
		return render(
			request, 'pages/challenge.html',
			{'questions': questions, 'challenge_id': challenge_id}
		)
	except Question.DoesNotExist:
		print('*****\n[ERROR] Getting questions\n*****')
		return HttpResponse(status=404)
		#raise Http404('Questions not found')

def solved(request):
	try:
		if request.method != "POST":
			return HttpResponse(status=400)

		questions = Question.objects.filter(challenge_id=request.POST['challenge_id'])

		answers = {}
		for item in questions:
			answers[item.id] = item.right

		points = 0
		for id, res in request.POST.items():
			if id == "csrfmiddlewaretoken" or id == "id" or id == "challenge_id":
				continue
			if int(id) in answers.keys() and int(res) == answers[int(id)]:
				points += 1

		print(points)
		return HttpResponse(status=200)
	except:
		print('*****\n[ERROR] Saving solved challenges\n*****')
		return HttpResponse(status=500)
		#raise Http404('Questions not found')