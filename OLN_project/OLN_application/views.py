# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from OLN_application.models import UserProfileInfo
import OLN_application.validators as validators
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import models
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'OLN_application/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_register(request):
    context = {}
    if request.method == 'POST':
        context['username'] = request.POST.get('username')
        context['email'] = request.POST.get('email')
        context['password'] = request.POST.get('password')

        if User.objects.filter(username=context['username']).count() != 0:
            context['register_status'] = 'username_taken'
        elif not validators.is_valid_username(context['username']):
            context['register_status'] = 'invalid_username'
        elif not validators.is_valid_email(context['email']):
            context['register_status'] = 'invalid_email'
        elif not validators.is_valid_password(context['password']):
            context['register_status'] = 'invalid_password'
        else:
            user = User()
            user.username = context['username']
            user.email = context['email']
            user.set_password(context['password'])
            user.save()

            profile = UserProfileInfo()
            profile.user = user
            profile.save()
            context['register_status'] = 'registered'
    else:
        context['register_status'] = 'registering'
    print(context)
    return render(request, 'OLN_application/registration.html', context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context['login_status'] = 'account inactive'
        else:
            context['login_status'] = 'invalid details'
    else:
        context['login_status'] = 'logging in'
    return render(request, 'OLN_application/login.html', context)


def user_profile(request, username):
    requested_user = UserProfileInfo.objects.get(user__username=username)
    return render(request, 'OLN_application/user.html', {'requested_user': requested_user})
