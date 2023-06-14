from django.conf import settings
from django.test import TestCase

from django.contrib import auth

# Create your tests here.
from django.contrib.auth import get_user
from home.models import Profile, Class

from home.views import makeFriend

class TestCaseTest(TestCase):
    def test_user(self):
        user = auth.get_user(self.client)
        self.assertEqual(self.client.session.get('value', None), user.pk)

    def test_login(self):

        self.client.login(username="jess", password="123")
        self.assertTrue(get_user(self.client))



    def test_ProfiletestYear(self):
        Profile.objects.create(year="FirstYear")
        user1 = Profile.objects.get(id=1)
        label = user1.year
        self.assertEqual(label, 'FirstYear')

    def test_ProfiletestYearLength(self):
        Profile.objects.create(year="FirstYear")
        user1 = Profile.objects.get(id=1)
        length = user1._meta.get_field('year').max_length
        self.assertEqual(length, 20)
    #def assertHTML(self, resp):
        #pass
    def test_HTML(self):
        self.assertHTMLEqual('<input type="text" class="form-control form-control-lg" name="major" checked="checked" />',
                             '<input name="major" class="form-control form-control-lg" type="text" checked> ')



    def test_ManyToManyCLassTest(self):
        person = Profile.objects.create(year="FirstYear")
        first_class = Class.objects.create(catalog_number="1110")
        second_class = Class.objects.create(catalog_number="1111")
        person.classes.set([first_class.pk, second_class.pk])
        self.assertEqual(person.classes.count(), 2)