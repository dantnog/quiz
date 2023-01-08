from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Challenge, Score, User
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

#
#	INDEX
#
def index(request):
	authenticated = request.session.get('authenticated', False)
	try:
		challenges = Challenge.objects.order_by('-id')

		return render(
			request, 'pages/index.html',
			{'challenges': challenges, 'authenticated': authenticated}
		)
	except Challenge.DoesNotExist:
		print('*******\n[ERROR] Getting challenges\n*******')
		return HttpResponse(status=404)
		#raise Http404('Challenge not found')

#
#	CHALLENGE
#
def challenge(request, challenge_id):
	authenticated = request.session.get('authenticated', False)
	try:
		questions = Question.objects.filter(challenge_id=challenge_id)
		return render(
			request, 'pages/challenge.html',
			{'questions': questions, 'challenge_id': challenge_id, 'authenticated': authenticated}
		)
	except Question.DoesNotExist:
		print('*******\n[ERROR] Getting questions\n*******')
		return HttpResponse(status=404)
		#raise Http404('Questions not found')

#
#	SOLVED
#
def solved(request):
	if request.method == 'POST':
		challenge_id = request.POST['challenge_id']
		try:
			questions = Question.objects.filter(challenge_id=challenge_id)

			answers = {}
			for item in questions:
				answers[item.id] = item.right

			points = 0
			for id, res in request.POST.items():
				if id == 'csrfmiddlewaretoken' or id == 'id' or id == 'challenge_id':
					continue
				if int(id) in answers.keys() and int(res) == answers[int(id)]:
					points += 1

			challenge = Challenge.objects.get(id=challenge_id)
			user = User.objects.get(id=request.session.get('user_id'))
			Score.objects.create(
					user = request.session.get('user_name'),
					tries = 1,
					points = points,
					challenge_id = challenge,
					user_id = user,
					created_at = datetime.now()
				)
			return HttpResponseRedirect(f'/scores/{challenge_id}')
		except:
			print('*******\n[ERROR] Saving points\n*******')
			return HttpResponse(status=500)
	else:
		return HttpResponse(status=400)

#
#	SCORES
#
def scores(request, challenge_id):
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		try:
			scores = Score.objects.filter(challenge_id=challenge_id)
			return render(request, 'pages/score.html', {'scores': scores, 'authenticated': authenticated})
		except:
			print('*******\n[ERROR] Load scores\n*******')
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#
#	NEW CHALLENGE
#
def new_challenge(request):
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		return render(request, 'pages/new.html', {'type': 'challenge', 'authenticated': authenticated})

	elif request.method == 'POST':
		try:
			user = User.objects.get(id=request.session.get('user_id'))
			Challenge.objects.create(
					title =	request.POST['title'],
					user_id = user,
					created_at = datetime.now()
				)
			return HttpResponseRedirect('/select')
		except:
			print('*******\n[ERROR] Create challenge\n*******')
			return HttpResponse(status=500)
	else:
		return HttpResponseRedirect('/')

#
#	SELECT CHALLENGE
#
def select(request):
	user_id = request.session.get('user_id', None)
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		try:
			challenges = Challenge.objects.filter(user_id=user_id)
			return render(request, 'pages/select.html', {'type': 'question', 'challenges': challenges, 'authenticated': authenticated})
		except:
			print('*******\n[ERROR] Select challenge\n*******')
			return HttpResponse(status=500)

	else:
		return HttpResponseRedirect('/')

#
#	NEW QUESTION
#
def new_question(request, challenge_id):
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		try:
			challenge = Challenge.objects.get(id=challenge_id)
			return render(request, 'pages/new.html', {'type': 'question', 'challenge': challenge, 'authenticated': authenticated})
		except:
			print('*******\n[ERROR] Get new question\n*******')
			return HttpResponse(status=500)


	elif request.method == 'POST':
		print(request.POST)
		try:
			challenge = Challenge.objects.get(id=challenge_id)
			Question.objects.create(
				text =  request.POST['text'],
				option_1 = request.POST['option1'],
				option_2 = request.POST['option2'],
				option_3 = request.POST['option3'],
				option_4 = request.POST['option4'],
				right = request.POST['right'],
				challenge_id = challenge,
				created_at = datetime.now()
			)
			alert = {'type': 'success', 'message': 'New question saved.'}
			return render(request, 'pages/new.html',
			{'type': 'question', 'challenge': challenge, 'alert': alert, 'authenticated': authenticated})
		except:
			alert = {'type': 'danger', 'message': 'Failed to save question. Try again later.'}
			print('*******\n[ERROR] Post new question\n*******')
			return render(request, 'pages/select.html', {'alert': alert})
	else:
		return HttpResponseRedirect('/')


#
#	AUTH
#
def auth(request):
	if request.method == 'GET':
		return render(request, 'pages/auth.html') 

	elif request.method == 'POST':
		username = request.POST['username'].strip()
		password = request.POST['password'].strip()
		if username == '' or password == '':
			alert = {'type': 'warning', 'message': 'The data was empty.'}
			return render(request, 'pages/auth.html', {'alert': alert})

		if request.POST['action'] == 'register':
			try:
				hashed = make_password(password, 'SuperSalt')
				User.objects.create(name=username, password=hashed, created_at=datetime.now())

				alert = {'type': 'success', 'message': 'User created. You can login now.'}
				return render(request, 'pages/auth.html', {'alert': alert})
			except:
				print('*******\n[ERROR] Register\n*******')
				alert = {'type': 'danger', 'message': 'Failed to create user. Try again later.'}
				return render(request, 'pages/auth.html', {'alert': alert})

		elif request.POST['action'] == 'login':
			try:
				user = User.objects.get(name=username)
				if not user:
					alert = {'type': 'danger', 'message': 'User not found.'}
					return render(request, 'pages/auth.html', {'alert': alert})

				if not check_password(password, user.password):
					alert = {'type': 'danger', 'message': 'Wrong password.'}
					return render(request, 'pages/auth.html', {'alert': alert})
					
				request.session['authenticated'] = True
				request.session['user_id'] = user.id
				request.session['user_name'] = user.name
				# Set session as modified to force data updates/cookie to be saved.
				request.session.modified = True
				return HttpResponseRedirect('/')
			except:
				print('*******\n[ERROR] Login\n*******')
				alert = {'type': 'danger', 'message': 'Failed to login. Try again later.'}
				return render(request, 'pages/auth.html', {'alert': alert})
		else:
			return render(request, 'pages/auth.html')

	else:
		return render(request, 'pages/auth.html')

#
#	LOGOUT
#
def logout(request):
	del request.session['authenticated']
	del request.session['user_id']
	del request.session['user_name']
	return HttpResponseRedirect('/auth')