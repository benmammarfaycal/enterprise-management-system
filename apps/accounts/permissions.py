from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and user.role == "ADMIN"


def is_manager(user):
    return user.is_authenticated and user.role == "MANAGER"


def is_employee(user):
    return user.is_authenticated and user.role == "EMPLOYEE"


def can_manage_projects(user):
    """
    Qui peut créer/modifier/supprimer des projets ?
    """
    return is_admin(user) or is_manager(user)


def can_view_all_projects(user):
    """
    Qui peut voir tous les projets ?
    """
    return is_admin(user)

from django.core.exceptions import PermissionDenied


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not is_admin(request.user):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper



def manager_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not is_manager(request.user):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper

def check_permission(condition):
    """
    Petit helper pour éviter de répéter PermissionDenied
    """
    if not condition:
        raise PermissionDenied