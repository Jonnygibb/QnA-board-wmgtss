from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

from .forms import SignUpForm

def home(request):
    return render(request, "users/home.html")

class SignUpView(FormView):

    def get(self, request):
        content = {}
        content['form'] = SignUpForm
        return render(request, 'registration/register.html', content)

    def post(self, request):
        content = {}
        form = SignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect(reverse('home'))
        content['form'] = form
        template = 'registration/register.html'
        return render(request, template, content)
