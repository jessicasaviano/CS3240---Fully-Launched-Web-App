

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Class(models.Model):
    class_name = models.CharField(max_length=150)
    department = models.CharField(max_length=10)
    catalog_number = models.CharField(max_length=10)
    instructor = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    days = models.CharField(max_length=20)
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)
    location = models.CharField(max_length=100)
    component = models.CharField(max_length=10)
    def __str__(self):
        courseStr = self.class_name + " /w " + self.instructor + " [" + self.days + " @ " + self.start_time + "] in " +self.location + " (" +self.component+")"
        return str(courseStr)
    def compare(self, other):
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        return values == other_values

""" class Friends(models.Model):
    username = models.CharField(max_length=150)
    def __str__(self):
        friendStr = self.username
        return str(friendStr)

    def compare(self, other):
        values = [(k, v) for k, v in self.__dict__.items() if k != '_state']
        other_values = [(k, v) for k, v in other.__dict__.items() if k != '_state']
        return values == other_values """
class DiscussionBoard(models.Model):
    #associatedSession = models.ForeignKey("StudySession", on_delete=models.CASCADE)
    sender = models.ForeignKey("Profile", related_name = "sender", on_delete=models.CASCADE)
    message = models.TextField(max_length=150, default="Remote")
    date = models.TextField(max_length=150, default="Remote")

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="Profile", null=True, on_delete=models.CASCADE)
    classesSet = models.BooleanField(default=False)
    preferencesSet = models.BooleanField(default=False)
    bioSet = models.BooleanField(default=False)
    classes = models.ManyToManyField(Class, blank=True)

    friendsList = models.ManyToManyField("self", blank=True)
    favorite_location = models.TextField(max_length=20, default="Not Specified")
    in_person = models.BooleanField(default=True)
    cramming = models.BooleanField(default=False)
    year = models.TextField(max_length=20, default="Not Specified")
    school = models.TextField(max_length=20, default="Not Specified")
    major = models.TextField(max_length=50, default ="Not Specified")
    about_you = models.TextField(max_length=100, default ="Not Specified")

    def __str__(self):
        firstName = self.user.first_name
        lastName = self.user.last_name
        fullName = firstName + " " + lastName
        if fullName != " ":
            return fullName
        return str(self.user)

class StudySession(models.Model):
    associatedClass = models.ForeignKey("Class", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Profile", related_name = "organizer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Profile, related_name = "attendees", blank=True)
    title = models.TextField(max_length=50)
    location = models.TextField(max_length=150, default="Remote")
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()
    messagess = models.ManyToManyField(DiscussionBoard, blank=True)






@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.Profile.save()