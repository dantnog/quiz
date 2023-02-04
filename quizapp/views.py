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
			return HttpResponseRedirect('/mychallenges')
		except:
			print('*******\n[ERROR] Create challenge\n*******')
			return HttpResponse(status=500)
	else:
		return HttpResponseRedirect('/')

#
#	MY CHALLENGES
#
def my_challenges(request):
	user_id = request.session.get('user_id', None)
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		try:
			challenges = Challenge.objects.filter(user_id=user_id)
			return render(request, 'pages/mychallenges.html', {'challenges': challenges, 'authenticated': authenticated})
		except:
			print('*******\n[ERROR] My challenges\n*******')
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
			return render(request, 'pages/mychallenges.html', {'alert': alert})
	else:
		return HttpResponseRedirect('/')

#
#	EDIT CHALLENGE
#
def edit_challenge(request, challenge_id):
	authenticated = request.session.get('authenticated', False)
	user_id = request.session.get('user_id', None)
	if request.method == 'GET':
		try:
			challenge = Challenge.objects.get(id=challenge_id)

			return render(
				request, 'pages/edit.html',
				{'type': 'challenge', 'challenge': challenge, 'authenticated': authenticated}
			)

		except:
			alert = {'type': 'danger', 'message': 'Challenge not found'}
			return render(
				request, 'pages/edit.html',
				{'type': 'challenge', 'alert': alert, 'authenticated': authenticated}
			)


	elif request.method == 'POST':
		try:
			challenge = Challenge.objects.get(id=challenge_id)
			if challenge.user_id.id != user_id:
				alert = {'type': 'danger', 'message': 'That challenge is not yours.'}
				return render(request, 'pages/index.html', {'alert': alert})

			# challenge.update(title=request.POST.get('title')) # not working
			challenge.title = request.POST.get('title')
			challenge.save()
			return HttpResponseRedirect('/mychallenges')
		except:
			return HttpResponseRedirect('/mychallenges')

	else:
		return HttpResponseRedirect('/')

#
#	SELECT QUESTION
#
def select_question(request, challenge_id):
	authenticated = request.session.get('authenticated', False)
	if request.method == 'GET':
		try:
			questions = Question.objects.filter(challenge_id=challenge_id)
			print(questions)

			return render(
				request, 'pages/edit.html',
				{'type': 'select', 'questions': questions, 'challenge_id': challenge_id,'authenticated': authenticated}
			)
		except:
			alert = {'type': 'danger', 'message': 'Question not found'}
			return render(
				request, 'pages/edit.html',
				{'type': 'select', 'alert': alert, 'authenticated': authenticated}
			)

	else:
		return HttpResponseRedirect('/')


#
#	EDIT QUESTION
#
def edit_question(request, question_id):
	authenticated = request.session.get('authenticated', False)
	user_id = request.session.get('user_id', None)
	if request.method == 'GET':
		try:
			question = Question.objects.get(id=question_id)

			return render(
				request, 'pages/edit.html',
				{'type': 'question', 'question': question, 'authenticated': authenticated}
			)
		except:
			alert = {'type': 'danger', 'message': 'Question not found'}
			return render(
				request, 'pages/edit.html',
				{'type': 'question', 'alert': alert, 'authenticated': authenticated}
			)

	elif request.method == 'POST':
		try:
			question = Question.objects.get(id=question_id)
			if question.challenge_id.user_id.id != user_id:
				alert = {'type': 'danger', 'message': 'That question is not yours.'}
				return render(request, 'pages/index.html', {'alert': alert})

			question.text = request.POST.get('text')
			question.option_1 = request.POST.get('option1')
			question.option_2 = request.POST.get('option2')
			question.option_3 = request.POST.get('option3')
			question.option_4 = request.POST.get('option4')
			question.right = request.POST.get('right')
			question.save()
			return HttpResponseRedirect('/mychallenges')
		except:
			return HttpResponseRedirect('/mychallenges')

	else:
		return HttpResponseRedirect('/')

#
#	DELETE CHALLENGE
#
def delete_challenge(request, challenge_id):
	user_id = request.session.get('user_id', None)
	if request.method == 'GET':
		try:
			challenge = Challenge.objects.get(id=challenge_id)
			if challenge.user_id.id != user_id:
				alert = {'type': 'danger', 'message': 'That challenge is not yours.'}
				return render(request, 'pages/index.html', {'alert': alert})
				
			challenge.delete()
			return HttpResponseRedirect('/mychallenges')
		except:
			alert = {'type': 'danger', 'message': 'Failed to delete challenge. Try again later.'}
			print('*******\n[ERROR] Delete challenge\n*******')
			return render(request, 'pages/mychallenges.html', {'alert': alert})
	
	else:
		return HttpResponseRedirect('/')

#
#	DELETE QUESTION
#
def delete_question(request, question_id):
	user_id = request.session.get('user_id', None)
	if request.method == 'GET':
		try:
			question = Question.objects.get(id=question_id)
			if question.challenge_id.user_id.id != user_id:
				alert = {'type': 'danger', 'message': 'That question is not yours.'}
				return render(request, 'pages/index.html', {'alert': alert})
				
			question.delete()
			return HttpResponseRedirect(f'/edit/selectquestion/{question.challenge_id.id}')
		except:
			alert = {'type': 'danger', 'message': 'Failed to delete challenge. Try again later.'}
			print('*******\n[ERROR] Delete challenge\n*******')
			return render(request, 'pages/mychallenges.html', {'alert': alert})
	
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

#
#	404
#
def error_404(request, exception):
	authenticated = request.session.get('authenticated', False)
	return render(request, 'pages/404.html', {'authenticated': authenticated})