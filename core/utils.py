import hashlib
import os
import time
import re
from django.shortcuts import render
from django.template import RequestContext
import uuid


def media_file_path(instance, filename):
    ident = uuid.uuid4()
    _, ext = os.path.splitext(filename)
    return '{0}/{1}/{2}{3}'.format(ident[:2], ident[2:4], ident[4:], ext)


def is_valid_username(username):
    if len(username) > 20 or len(username) < 3:
        return False
    if not re.match(r"(^[a-zA-Z0-9]+([_-]?[a-zA-Z0-9])*$)", username):
        return False
    return True


def is_valid_email(email):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)


def is_valid_password(password):
    return len(password) >= 8


def is_valid_full_name(full_name):
    return 0 < len(full_name) <= 255


def render_with_context(request, template_name, context=None, content_type=None, status=None, using=None):
    global_context = RequestContext(request)
    global_context.update(context)
    return render(request, template_name, global_context.flatten(), content_type, status, using)
