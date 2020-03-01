from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.request
import os
import hashlib

from profiles.models import Profile

from core.decorators import check_recaptcha
from core.utils import \
    is_valid_full_name,\
    is_valid_username, \
    is_valid_email, \
    is_valid_password, \
    media_file_path, \
    render_with_context


def profile_edit(request, template_name="profiles/edit.html"):
    return render_with_context(request, template_name, {})


def profile_detail(request, username, template_name="profiles/profile.html"):
    try:
        profile = get_object_or_404(Profile, user__username=username)
    except MultipleObjectsReturned:
        profile = Profile.objects.filter(user__username=username).latest('pk')
    return render_with_context(request, template_name, {'profile': profile})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@check_recaptcha
def register(request, template_name="profiles/register.html"):
    context = {
        'recaptcha_key': settings.GOOGLE_RECAPTCHA_PUBLIC_KEY,
    }
    if request.method == 'POST':
        context['full_name'] = request.POST.get('full_name')
        context['username'] = request.POST.get('username')
        context['email'] = request.POST.get('email')
        context['password'] = request.POST.get('password')
        context['accept_terms'] = (request.POST.get('accept_terms') == 'on')

        if not context['accept_terms']:
            context['register_status'] = 'invalid_terms'
        elif not request.recaptcha_is_valid:
            context['register_status'] = 'invalid_recaptcha'
        elif User.objects.filter(username=context['username']).count() != 0:
            context['register_status'] = 'username_taken'
        elif User.objects.filter(email=context['email']).count() != 0:
            context['register_status'] = 'email_taken'
        elif not is_valid_full_name(context['full_name']):
            context['register_status'] = 'invalid_full_name'
        elif not is_valid_username(context['username']):
            context['register_status'] = 'invalid_username'
        elif not is_valid_email(context['email']):
            context['register_status'] = 'invalid_email'
        elif not is_valid_password(context['password']):
            context['register_status'] = 'invalid_password'
        else:
            with transaction.atomic():
                user = User()
                user.username = context['username']
                user.set_password(context['password'])
                user.save()

                group, created = Group.objects.get_or_create(name='DOCTOR_GROUP')
                user.groups.add(group)

                avatar_filename = user.username + "_avatar.svg"
                avatar_media_path = media_file_path(user, avatar_filename)
                avatar_system_path = os.path.join(settings.MEDIA_ROOT, avatar_media_path)
                if not os.path.exists(os.path.dirname(avatar_system_path)):
                    os.makedirs(os.path.dirname(avatar_system_path))

                avatar_generator_url = \
                    settings.AVATAR_PROVIDER + '{0}?theme=berrypie&numcolors=4&size=220&fmt=svg' \
                    .format(avatar_filename)

                urllib.request.urlretrieve(avatar_generator_url, avatar_system_path)

                profile = Profile()
                profile.full_name = context['full_name']
                profile.user = user
                profile.email = context['email']
                profile.avatar = avatar_media_path
                profile.save()
                context['register_status'] = 'registered'
            
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        context['register_status'] = 'registering'
    return render_with_context(request, template_name, context)


def user_login(request, template_name="profiles/login.html"):
    context = {}
    if request.method == 'POST':
        username = None
        username_or_email = request.POST.get('username_or_email')
        if "@" in username_or_email:
            try:
                username = User.objects.all().get(email=username_or_email)
            except MultipleObjectsReturned:
                username = User.objects.filter(email=username_or_email).latest('pk')
        else:
            username = username_or_email
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
