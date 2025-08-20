from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.contrib import messages
from django.utils.cache import add_never_cache_headers




EXEMPT_NAMES = ['landingpage', 'login', 'logout', 'signup', 'admin:index', 'setup_profile']
NO_CACHE_VIEWS = ['landingpage', 'signup', 'login'] # Views where back button should not work

class ForceProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        user = request.user
        path = request.path

        # Get current view name (e.g., 'feed', 'setup_profile', etc.)
        try:
            current_view = resolve(path).view_name
        except:
            current_view = None

        #  Redirect authenticated users away from login/signup/setup_profile
        if user.is_authenticated and current_view in NO_CACHE_VIEWS:
            return redirect('feed')  # Or whatever your main page is

        # Skip middleware if user is not logged in, or is on exempt view/static
        if(
            not user.is_authenticated or
            current_view in EXEMPT_NAMES or
            (current_view and current_view.startswith('admin:')) or
            path.startswith('/static/') or
            path.startswith('/admin/') or
            (path.startswith('/media/') and user.is_staff)  # ← allow media for admin only
        ):
            response = self.get_response(request)

            # Disable caching for important views
            if current_view in NO_CACHE_VIEWS:
                add_never_cache_headers(response)
            return response


        # Redirect if profile exists and is not complete
        profile = getattr(user, 'profile', None)
        if profile and not profile.is_complete:
                messages.info(request, "Please complete your profile before continuing.")
                return redirect('setup_profile')
            
        # Block completed users from accessing setup_profile manually
        if current_view == 'setup_profile' and profile and profile.is_complete:
            return redirect('feed')

        return self.get_response(request)
        