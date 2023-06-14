from django.contrib import admin
from .models import Profile, Class, StudySession, DiscussionBoard
# Register your models here.

admin.site.register(Profile)
admin.site.register(Class)
admin.site.register(StudySession)
admin.site.register(DiscussionBoard)