from django.shortcuts import redirect
from functools import wraps
from .models import User

def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.role in allowed_roles:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return redirect("dashboard")

        return wrapper

    def admin_required(view_func):
        return role_required(
            [User.Role.ADMIN]
        )(view_func)

    def manager_required(view_func):
        return role_required(
            [
                User.Role.ADMIN,
                User.Role.MANAGER
            ]
        )(view_func)

    def employee_required(view_func):
        return role_required(
            [
                User.Role.ADMIN,
                User.Role.MANAGER,
                User.Role.EMPLOYEE
            ]
        )(view_func)
    return decorator