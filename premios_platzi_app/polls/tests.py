import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question


# Create your tests here.
# se van a testear modelos y vistas
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor Course Director de Platzi", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="Quien es el mejor Course Director de Platzi", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        
    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now()
        present_question = Question(question_text="Quien es el mejor Course Director de Platzi", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    
    def test_no_question(self):
        """If no question exist, an appropiate message is display"""
        response = self.client.get(reverse("polls:index")) # client es un modulo de django que nos deja hacer peticiones http
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
        
    def test_no_future_question_are_display(self):
        """ If a future question is create in the database,
            this question is not shown until his pub_date is equal to the present     
        """
        response = self.client.get(reverse("polls:index"))
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor Course Director de Platzi", pub_date=time)
        self.assertNotIn(future_question, response.context["latest_question_list"])