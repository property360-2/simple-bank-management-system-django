from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse
from .forms import UserRegisterForm
from .models import User


class CustomLoginView(DjangoLoginView):
    """Custom login view that redirects based on user role"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect to different dashboards based on user role"""
        user = self.request.user

        try:
            # Admin users go to admin dashboard
            if user.is_admin_user():
                return reverse('admin_panel:dashboard')

            # Managers go to manager dashboard (can be same as admin or separate)
            elif user.is_manager():
                return reverse('admin_panel:dashboard')

            # Customers go to regular dashboard
            else:
                return reverse('dashboard')
        except:
            # Fallback to home if URL pattern is not found
            return '/'


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # New users default to 'customer' role
            user.role = 'customer'
            user.save()

            login(request, user)
            messages.success(request, f'Account created for {user.username}! Welcome!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})