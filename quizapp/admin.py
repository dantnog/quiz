from django.contrib import admin
from .models import Question, Challenge, Score, User

admin.site.register(Challenge)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(User)