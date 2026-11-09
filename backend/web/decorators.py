from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseNotAllowed
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme


def post_login_required(view):
    """
    For buttons that change data: accepts POST only. An anonymous visitor is
    sent to the login page and comes back to the page holding the button,
    because the action URL itself cannot be opened with GET after login.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        if not request.user.is_authenticated:
            target = request.META.get('HTTP_REFERER', '')
            if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
                target = resolve_url('/')
            return redirect_to_login(target, login_url=resolve_url('login'))
        return view(request, *args, **kwargs)
    return wrapper
