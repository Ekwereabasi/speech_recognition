from django.http import HttpResponseRedirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('register'))  # Redirect authenticated users to the home page
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


