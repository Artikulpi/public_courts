from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.core.exceptions import PermissionDenied
from urlparse import urlparse
import re

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    if login_url==None:
        login_url = settings.LOGIN_URL
    
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    if login_url==None:
        login_url = settings.LOGIN_URL
    
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def referer_matches_re(regex):
    """
    Decorator for views that checks that if the request's HTTP_REFERER matches
    the supplied regex pattern. Failure raises a PermissionDenied exception.
    """
    regex = re.compile(regex)
    def _dec(view_func):
        def _check_referer(request, *args, **kwargs):
            origin = request.META.get('HTTP_REFERER', '')
            partial = urlparse(origin)
            referer = partial.path
            if regex.match(referer):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied()
        _check_referer.__doc__ = view_func.__doc__
        _check_referer.__dict__ = view_func.__dict__        
        return _check_referer
    return _dec
