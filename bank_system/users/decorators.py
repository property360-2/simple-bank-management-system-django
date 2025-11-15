from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def role_required(allowed_roles):
    """
    Decorator to check if user has one of the allowed roles.

    Usage:
        @role_required(['admin', 'manager'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')

        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to restrict view to admin users only.

    Usage:
        @login_required
        @admin_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_admin_user():
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Admin access required.')
        return redirect('dashboard')

    return wrapper


def manager_required(view_func):
    """
    Decorator to restrict view to manager/staff and admin users.

    Usage:
        @login_required
        @manager_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_manager() or request.user.is_admin_user():
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Manager access required.')
        return redirect('dashboard')

    return wrapper


def customer_required(view_func):
    """
    Decorator to restrict view to customers only.

    Usage:
        @login_required
        @customer_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_customer():
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Customer access required.')
        return redirect('dashboard')

    return wrapper
