from django.test import TestCase
from ..models import User, Questions


class QuestionModelTest(TestCase):
    """
    Test case for Questions Model
    """
    @classmethod
    def setUpTestData(cls):
        # Create test credential to imitate new user
        credentials = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'secret',
            'first_name': 'test',
            'last_name': 'user',
        }
        # Register user in the postgres database
        User.objects.create(**credentials)
        Questions.objects.create(user = User.objects.get(id=1),
                                 title = 'Here is my first question',
                                 description = 'Here is what I wanted to ask')

    
    def test_field_labels(self):
        question = Questions.objects.get(id=1)
        user_field = question._meta.get_field('user').verbose_name
        self.assertEqual(user_field, 'user')

    def test_title_field_label(self):
        question = Questions.objects.get(id=1)
        title_field = question._meta.get_field('title').verbose_name
        self.assertEqual(title_field, 'title')
    
    def test_description_field_label(self):
        question = Questions.objects.get(id=1)
        description_field = question._meta.get_field('description').verbose_name
        self.assertEqual(description_field, 'description')

    def test_slug_field_label(self):
        question = Questions.objects.get(id=1)
        slug_field = question._meta.get_field('slug').verbose_name
        self.assertEqual(slug_field, 'slug')

    def test_user_content(self):
        question = Questions.objects.get(id=1)
        username = question.user.username
        email = question.user.email
        password = question.user.password
        first_name = question.user.first_name
        last_name = question.user.last_name
        self.assertEqual(username, 'test')
        self.assertEqual(email, 'test@gmail.com')
        self.assertEqual(password, 'secret')
        self.assertEqual(first_name, 'test')
        self.assertEqual(last_name, 'user')

    def test_title_content(self):
        question = Questions.objects.get(id=1)
        title = question.title
        self.assertEqual(title, 'Here is my first question')

    def test_description_content(self):
        question = Questions.objects.get(id=1)
        description = question.description
        self.assertEqual(description, 'Here is what I wanted to ask')

    def test_slug_content(self):
        question = Questions.objects.get(id=1)
        slug = question.slug
        self.assertEqual(slug, 'here-is-my-first-question')