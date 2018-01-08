from django.conf import settings
from django.shortcuts import redirect
import re

EXEMPT_URL = re.compile(settings.LOGIN_URL.lstrip('/'))

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request,'user')
        path = request.path_info.lstrip('/')
        print(request.user.is_authenticated)
        print("login redirect url: ", settings.LOGIN_URL)
        print("path: ", path)

        if not request.user.is_authenticated:
            if not path.lstrip('/') == settings.LOGIN_URL.lstrip('/'):
                return redirect(settings.LOGIN_URL)