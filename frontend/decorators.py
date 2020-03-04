from datetime import datetime

from django.contrib.auth.views import redirect_to_login


def LAW_login_required(func, login_url="/login/"):
    def decorator(request, *args, **kwargs):
        sessions = request.session
        if "access_token" in sessions.keys() and "expires_in" in sessions.keys():
            if datetime.now() >= datetime.strptime(
                sessions["expires_in"], "%m/%d/%y %H:%M:%S"
            ):
                del request.session["access_token"]
                del request.session["expires_in"]
                return redirect_to_login(
                    next=request.get_full_path(), login_url=login_url
                )
            else:
                return func(request, *args, **kwargs)
        else:
            return redirect_to_login(next=request.get_full_path(), login_url=login_url)

    return decorator
