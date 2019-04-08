from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
class HomePageTests(SimpleTestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class SignUpPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@qq.com'

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        newuser = get_user_model().objects.create_user(self.username,
                                                       self.email)
        all_user_objects = get_user_model().objects.all()
        self.assertEqual(all_user_objects.count(), 1)
        self.assertEqual(all_user_objects[0].username, self.username)
        self.assertEqual(all_user_objects[0].email, self.email)
