"""PIN-based single-user authentication helpers."""

from functools import wraps

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect

from .models import AppConfig

PIN_HASH_KEY = "pin_hash"
START_DATE_KEY = "start_date"
SESSION_KEY = "authenticated"


def get_config(key, default=None):
    try:
        return AppConfig.objects.get(key=key).value
    except AppConfig.DoesNotExist:
        return default


def set_config(key, value):
    AppConfig.objects.update_or_create(key=key, defaults={"value": value})


def pin_is_set():
    return get_config(PIN_HASH_KEY) is not None


def set_pin(raw_pin):
    set_config(PIN_HASH_KEY, make_password(raw_pin))


def check_pin(raw_pin):
    hashed = get_config(PIN_HASH_KEY)
    if not hashed:
        return False
    return check_password(raw_pin, hashed)


def is_authenticated(request):
    return request.session.get(SESSION_KEY, False) is True


def log_in(request):
    request.session[SESSION_KEY] = True
    request.session.set_expiry(60 * 60 * 24 * 30)


def log_out(request):
    request.session.flush()


def require_pin(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not pin_is_set():
            return redirect("system:setup")
        if not is_authenticated(request):
            return redirect("system:login")
        return view_func(request, *args, **kwargs)

    return wrapped
