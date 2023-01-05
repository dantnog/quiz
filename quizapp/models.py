from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField()

	def __str__(self):
		return self.name

class Challenge(models.Model):
	title = models.CharField(max_length=200)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()

	def __str__(self):
		return self.title

class Question(models.Model):
	text = models.CharField(max_length=200)
	option_1 = models.CharField(max_length=200)
	option_2 = models.CharField(max_length=200)
	option_3 = models.CharField(max_length=200)
	option_4 = models.CharField(max_length=200)
	right = models.IntegerField(default=0)
	challenge_id = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	created_at = models.DateTimeField()

	def __str__(self):
		return self.text

class Score(models.Model):
	user = models.CharField(max_length=100)
	tries = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	challenge_id = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()

	def __str__(self):
		return self.user