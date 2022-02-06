from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic.edit import FormView
from django.views.generic import (ListView, 
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import SignUpForm, LogInForm
from .models import Answer, User, Questions

class BoardView(FormView):
    def get(self, request):
        content = {}
        if request.user.is_authenticated:
            user = request.user
            user.backend = 'django.contrib.core.backends.ModelBackend'
            ques_obj = Questions.objects.filter(user=user)
            content['userdetail'] = user
            content['questions'] = ques_obj
            #ans_obj = Answers.objects.filter(question=ques_obj[0])
            #content['answers'] = ans_obj
            return render(request, 'users/home.html', content)
        else:
            return redirect(reverse('login'))

class BoardListView(ListView):
    
    model = Questions
    template_name = 'users/home.html'
    context_object_name = 'questions'
    ordering = ['created_at']
    
    # Adds protection to home page by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BoardListView, self).dispatch(request, *args, **kwargs)
    
class QuestionDetailView(DetailView):
    
    model = Questions
    template_name = 'users/questions_detail.html'
    
    # Adds protection to questions by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionDetailView, self).dispatch(request, *args, **kwargs)


class QuestionCreateView(CreateView):
    model = Questions
    template_name = 'users/questions_form.html'
    fields = ['title', 'description']
    success_url = '/'

    # Adds protection to questions by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding the form valid method to ensure that the logged in
        user is set as the questions creator automatically
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    model = Questions
    template_name = 'users/questions_form.html'
    fields = ['title', 'description']
    success_url = '/'

    # Adds protection to questions by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding the form valid method to ensure that the logged in
        user is set as the questions creator automatically
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """
        Uses a test to ensure that the creator of the question is only allowed to update
        questions created by themselves
        """
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False

class QuestionDeleteView(UserPassesTestMixin, DeleteView):
    
    model = Questions
    template_name = 'users/questions_confirm_delete.html'
    success_url = '/'
    
    # Adds protection to questions by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionDeleteView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        """
        Uses a test to ensure that the creator of the question is only allowed to delete
        questions created by themselves
        """
        question = self.get_object()
        if (self.request.user == question.user) or (self.request.user.is_superuser):
            return True
        else:
            return False

class AnswerCreateView(CreateView):
    model = Answer
    template_name = 'users/answer_form.html'
    fields = ['description']
    success_url = '/'

    # Adds protection to questions by ensuring that only authenticated users can access it
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.question = Questions.objects.get(slug=kwargs['slug'])
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding the form valid method to ensure that the logged in
        user is set as the questions creator automatically
        """
        form.instance.user = self.request.user
        form.instance.question = self.question
        return super().form_valid(form)

    

class SignUpView(FormView):
    """
    Class view for sign up page.
    Uses Django Forms to create a sign up page with first name,
    last name, email, username and password. 
    Django authentication module handles password hashing.
    User model is used to save users details to the database.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUpView, self).dispatch(request, *args, **kwargs)


    def get(self, request):
        """
        Method for get request of signup page
        """

        # Set website content equal to the sign up form
        content = {}
        content['form'] = SignUpForm
        # Return the form rendered into html
        return render(request, 'registration/register.html', content)

    def post(self, request):
        """
        Method for post request of signup page
        """
        # Set content to sign up form
        content = {}
        form = SignUpForm(request.POST, request.FILES or None)
        # If post content is valid, login the user and return them to the home page
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['username']
            user.save()
            login(request, user)
            messages.success(request, 'Account created for {}!'.format(user.username))
            return redirect(reverse('home'))
        # Else, re render the sign in form again
        content['form'] = form
        template = 'registration/register.html'
        messages.warning(request, 'Account could not be created')
        return render(request, template, content)

class LogInView(FormView):
    """
    Class view for login page.
    Uses Django Forms to create a Form with a username and password field 
    along with a login button.
    Django authentication module is used to log users in and out. 
    """

    # Set website content equal to the login form
    content = {}
    content['form'] = LogInForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LogInView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        Method for get request of login page
        """
        content = {}
        # If the user is already authenticated, redirect them to the home page
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        # Otherwise render the log in form
        content['form'] = LogInForm
        return render(request, 'login.html', content)

    def post(self, request):
        """
        Method for post request of login page
        """

        content = {}
        # Instanciate username and password from post request
        username = request.POST['username']
        password = request.POST['password']
        try:
            # Search for user object in User records for given username
            users = User.objects.filter(username=username)
            # Attempt to authenticate user 
            user = authenticate(request, username=users.first().username, password=password)
            # If successful, log the user in and redirect them to the home page
            login(request, user)
            return(redirect(reverse('home')))
        except Exception as e:
            # If an error occurs during authentication, reload the login page and display the error message
            content = {}
            content['form'] = LogInForm
            content['error'] = 'Could not login with provided information' + e
            return render(request, 'login.html', content)
