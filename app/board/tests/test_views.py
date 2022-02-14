from django.test import TestCase
from ..models import User


class SignUpTest(TestCase):
    """
    Test case for webpage sign up and account creation.
    User login functionality is also tested here.
    """
    def setUp(self):
        # Create test credential to imitate new user
        self.credentials = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'secret',
            'first_name': 'test',
            'last_name': 'user',
        }
        # Register user in the postgres database
        User.objects.create_user(**self.credentials)

    def test_signup(self):
        """
        Tests sign up through web page with valid credentials
        """
        response = self.client.post('/signup/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_created(self):
        """
        Tests that sign up form successfully updates database with user credentials
        """
        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')

    def test_user_login(self):
        """
        Tests that signed up user with valid credentials can successfully log in to the web application
        """
        wanted_keys = ['username', 'password']
        # Dictionary comprehension to select only username and password from credentials
        login_info = {k: self.credentials[k] for k in set(wanted_keys) & set(self.credentials.keys())}
        response = self.client.post('/accounts/login/', login_info, follow=True)
        # Assert that user is logged in after passing of correct credentials
        self.assertTrue(response.context['user'].is_active)

    def test_user_login_bad_credentials(self):
        """
        Tests that non signed up user cannot authenticate in the web application
        """
        login_info = {'username': 'gr8user', 'password': 'weak'}
        # Send response to login form with fake credentials
        response = self.client.post('/accounts/login/', login_info, follow=True)
        # Assert user is not logged in after submitting fake credentials
        self.assertFalse(response.context['user'].is_active)

    def test_user_login_bad_password(self):
        """
        Tests that a signed up user using an incorrect password cannot authenticate in the web application
        """
        wanted_keys = ['username', 'password']
        # Dictionary comprehension to select only username and password from credentials
        login_info = {k: self.credentials[k] for k in set(wanted_keys) & set(self.credentials.keys())}
        # Change password variable to incorrect value
        login_info['password'] = 's3cret'
        response = self.client.post('/accounts/login/', login_info, follow=True)
        # Ensure that user is not authenticated following incorrect password
        self.assertFalse(response.context['user'].is_active)