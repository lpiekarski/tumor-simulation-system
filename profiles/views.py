from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.request
import os
import hashlib

from profiles.models import Profile

from core.utils import is_valid_username, is_valid_email, is_valid_password, media_file_path, render_with_context


def profile_detail(request, username, template_name="profiles/profile.html"):
    try:
        profile = get_object_or_404(Profile, user__username=username)
    except MultipleObjectsReturned:
        profile = Profile.objects.filter(user__username=username).latest('pk')
    return render_with_context(request, template_name, {'profile': profile})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request, template_name="profiles/register.html"):
    context = {}
    if request.method == 'POST':
        context['username'] = request.POST.get('username')
        context['email'] = request.POST.get('email')
        context['password'] = request.POST.get('password')

        if User.objects.filter(username=context['username']).count() != 0:
            context['register_status'] = 'username_taken'
        elif not is_valid_username(context['username']):
            context['register_status'] = 'invalid_username'
        elif not is_valid_email(context['email']):
            context['register_status'] = 'invalid_email'
        elif not is_valid_password(context['password']):
            context['register_status'] = 'invalid_password'
        else:
            user = User()
            user.username = context['username']
            user.email = context['email']
            user.set_password(context['password'])
            user.save()

            avatar_filename = user.username + "_avatar.svg"
            avatar_media_path = media_file_path(user, avatar_filename)
            avatar_system_path = os.path.join(settings.MEDIA_ROOT, avatar_media_path)
            if not os.path.exists(os.path.dirname(avatar_system_path)):
                os.makedirs(os.path.dirname(avatar_system_path))

            avatar_generator_url = \
                'https://www.tinygraphs.com/labs/isogrids/hexa/{0}?theme=berrypie&numcolors=4&size=220&fmt=svg' \
                .format(avatar_filename)

            urllib.request.urlretrieve(avatar_generator_url, avatar_system_path)

            profile = Profile()
            profile.user = user
            profile.avatar = avatar_media_path
            profile.save()
            context['register_status'] = 'registered'
    else:
        context['register_status'] = 'registering'
    return render_with_context(request, template_name, context)


def user_login(request, template_name="profiles/login.html"):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                context['login_status'] = 'account inactive'
        else:
            context['login_status'] = 'invalid details'
    else:
        context['login_status'] = 'logging in'
    return render(request, template_name, context)
