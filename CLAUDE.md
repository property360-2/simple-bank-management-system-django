# CLAUDE.md - Simple Bank Management System

## Project Overview

This is a **Django-based Bank Management System** designed to manage customer accounts, transactions, savings, investments, loans, and bill payments. The project emphasizes modularity, reusability, and modern UX/UI patterns.

### Purpose
Provide a comprehensive banking solution with features for:
- Account management (checking, savings, business accounts)
- Transaction processing (deposits, withdrawals, transfers)
- Savings accounts with interest calculation and goal tracking
- Investment portfolio management
- Loan management with EMI calculations
- Bill payment and tracking

### Tech Stack
- **Framework**: Django 5.2.7
- **Language**: Python 3
- **Database**: SQLite (development) - designed to be PostgreSQL-ready for production
- **Frontend**: Bootstrap 5, Django Templates
- **Authentication**: Django built-in auth with custom User model

---

## Directory Structure

```
simple-bank-management-system-django/
├── bank_system/                 # Main Django project directory
│   ├── config/                  # Project configuration
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL configuration
│   │   └── wsgi.py             # WSGI configuration
│   │
│   ├── users/                   # User authentication and profiles
│   │   ├── models.py           # Custom User model (extends AbstractUser)
│   │   ├── views.py            # Registration, profile views
│   │   └── forms.py            # User forms
│   │
│   ├── accounts/                # Bank account management
│   │   ├── models.py           # Account model
│   │   ├── views.py            # CRUD views for accounts
│   │   ├── forms.py            # Account forms
│   │   └── urls.py             # Account routes
│   │
│   ├── transactions/            # Transaction processing
│   │   ├── models.py           # Transaction model
│   │   ├── views.py            # Deposit, withdrawal, transfer views
│   │   └── forms.py            # Transaction forms
│   │
│   ├── savings/                 # Savings accounts and goals
│   │   ├── models.py           # SavingsProduct, SavingsAccount, SavingsGoal, InterestTransaction
│   │   ├── views.py            # Savings management views
│   │   └── urls.py             # Savings routes
│   │
│   ├── investments/             # Investment portfolio management
│   │   ├── models.py           # InvestmentPlatform, InvestmentProduct, Portfolio, InvestmentHolding, InvestmentTransaction
│   │   ├── views.py            # Portfolio and investment views
│   │   └── urls.py             # Investment routes
│   │
│   ├── loans/                   # Loan management
│   │   ├── models.py           # LoanProduct, Loan, LoanPayment
│   │   └── views.py            # Loan application and payment views
│   │
│   ├── bills/                   # Bill payment tracking
│   │   ├── models.py           # BillerCategory, Biller, Bill, BillReminder
│   │   └── views.py            # Bill payment views
│   │
│   ├── dashboard/               # Main dashboard
│   │   └── views.py            # Dashboard aggregation and display
│   │
│   ├── settings/                # User settings and preferences
│   │   ├── views.py            # Settings management
│   │   └── urls.py             # Settings routes
│   │
│   ├── core/                    # Shared utilities and base templates
│   │   ├── models.py           # Shared models and mixins
│   │   └── utils.py            # Helper functions
│   │
│   ├── templates/               # Django templates
│   │   ├── base.html           # Base template (shared layout)
│   │   ├── includes/           # Reusable template components
│   │   │   ├── _navbar.html    # Navigation bar
│   │   │   ├── _alerts.html    # Django messages display
│   │   │   ├── atoms/          # Atomic design components (button, icon, input)
│   │   │   └── molecules/      # Molecular components (modal)
│   │   ├── accounts/           # Account templates
│   │   ├── transactions/       # Transaction templates
│   │   ├── savings/            # Savings templates
│   │   ├── investments/        # Investment templates
│   │   ├── dashboard/          # Dashboard templates
│   │   └── users/              # User templates
│   │
│   ├── static/                  # Static files (CSS, JS, images)
│   │   └── css/                # Custom CSS files
│   │
│   ├── db.sqlite3              # SQLite database (development)
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
│
├── plan.md                      # Project planning document
├── readme.md                    # Project README
└── CLAUDE.md                    # This file

```

---

## Django Apps Architecture

### 1. **users** - User Management
- **Purpose**: Handle user authentication, registration, and profiles
- **Models**:
  - `User` (extends AbstractUser): username, email, phone
- **Key Features**: Custom user model with phone field

### 2. **accounts** - Bank Accounts
- **Purpose**: Manage user bank accounts
- **Models**:
  - `Account`: account_number, account_type (savings/checking/business), balance, is_active
- **Relationships**: One User → Many Accounts
- **Key Features**:
  - Auto-generated account numbers
  - Balance tracking
  - Account type categorization

### 3. **transactions** - Financial Transactions
- **Purpose**: Process and record all financial transactions
- **Models**:
  - `Transaction`: transaction_type (deposit/withdrawal/transfer), amount, from_account, to_account
- **Relationships**:
  - Many Transactions → One Account (from_account)
  - Many Transactions → One Account (to_account)
- **Key Features**:
  - Support for deposits, withdrawals, and transfers
  - Transaction history tracking

### 4. **savings** - Savings Accounts & Goals
- **Purpose**: Manage high-yield savings accounts with interest calculation and savings goals
- **Models**:
  - `SavingsProduct`: Product templates with interest rates and compounding frequency
  - `SavingsAccount`: Individual savings accounts linked to main accounts
  - `SavingsGoal`: User-defined savings goals with progress tracking
  - `InterestTransaction`: Track interest accrual
- **Key Features**:
  - Interest calculation with configurable compounding
  - Withdrawal limits
  - Goal tracking with progress percentage
  - Automatic interest application

### 5. **investments** - Investment Portfolio
- **Purpose**: Manage investment portfolios across different asset types
- **Models**:
  - `InvestmentPlatform`: Investment platforms (stocks, bonds, ETF, crypto, etc.)
  - `InvestmentProduct`: Individual investment products with risk levels
  - `Portfolio`: User portfolios with performance tracking
  - `InvestmentHolding`: Individual holdings within portfolios
  - `InvestmentTransaction`: Buy/sell/dividend transactions
- **Key Features**:
  - Multi-platform support
  - Portfolio performance tracking (profit/loss, ROI%)
  - Risk level categorization
  - Automatic portfolio value calculation

### 6. **loans** - Loan Management
- **Purpose**: Handle loan applications, approvals, and payments
- **Models**:
  - `LoanProduct`: Loan types (personal, auto, home, education, business)
  - `Loan`: Individual loan instances with EMI calculation
  - `LoanPayment`: Track loan payments
- **Key Features**:
  - EMI (Equated Monthly Installment) calculation
  - Loan status tracking (pending, approved, active, completed, rejected, defaulted)
  - Payment history
  - Maturity date tracking

### 7. **bills** - Bill Payment
- **Purpose**: Track and manage recurring bills and one-time payments
- **Models**:
  - `BillerCategory`: Bill categories (electricity, water, internet, insurance, etc.)
  - `Biller`: Saved billers with account details
  - `Bill`: Individual bills to pay
  - `BillReminder`: Payment reminders
- **Key Features**:
  - Recurring bill support
  - Due date tracking
  - Overdue detection
  - Favorite billers

### 8. **dashboard** - Main Dashboard
- **Purpose**: Aggregate and display user's financial overview
- **Features**:
  - Total account balances
  - Recent transactions
  - Savings summary with interest earned
  - Investment portfolio performance
  - Savings goals progress
  - Total net worth calculation

### 9. **settings** - User Settings
- **Purpose**: User preferences and settings management
- **Features**: User-specific configuration options

### 10. **core** - Shared Utilities
- **Purpose**: Shared logic, base templates, and utilities
- **Features**: Reusable components and helper functions

---

## Database Models: Key Relationships

```
User (users.User)
├── accounts (ForeignKey) → Account
│   ├── outgoing_transactions → Transaction
│   ├── incoming_transactions → Transaction
│   ├── savings_account → SavingsAccount
│   ├── portfolios → Portfolio
│   └── loans → Loan
│
├── savings_accounts → SavingsAccount
│   ├── product → SavingsProduct
│   ├── goals → SavingsGoal
│   └── interest_transactions → InterestTransaction
│
├── portfolios → Portfolio
│   ├── holdings → InvestmentHolding
│   │   └── product → InvestmentProduct
│   └── transactions → InvestmentTransaction
│
├── loans → Loan
│   ├── product → LoanProduct
│   ├── account → Account
│   └── payments → LoanPayment
│
└── billers → Biller
    ├── category → BillerCategory
    └── bills → Bill
        ├── transaction → Transaction
        └── reminder → BillReminder
```

---

## URL Routing Structure

### Main URLs (`config/urls.py`)
```python
/admin/                  # Django admin
/register/               # User registration
/login/                  # User login
/logout/                 # User logout
/                        # Dashboard (requires login)
/accounts/               # Account management
/transactions/           # Transaction processing
/savings/                # Savings accounts and goals
/investments/            # Investment portfolios
/settings/               # User settings
```

---

## Common Patterns and Conventions

### 1. **Views Pattern**
All views follow a consistent pattern:
- Use `@login_required` decorator
- Filter data by `request.user` for security
- Use `get_object_or_404` for fetching single objects
- Add `messages` for user feedback
- Redirect after successful POST operations

Example:
```python
@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})
```

### 2. **Forms Pattern**
Forms follow these conventions:
- Extend `forms.ModelForm`
- Use Bootstrap classes in widgets
- Accept `user` parameter in `__init__` when needed
- Handle auto-generation of unique identifiers (e.g., account numbers)

Example:
```python
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type']
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
```

### 3. **Model Conventions**
All models include:
- Timestamps: `created_at`, `updated_at`
- `__str__` method for admin display
- `Meta` class with ordering
- Related_name on ForeignKeys for reverse lookups

Example:
```python
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    # ... fields ...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
```

### 4. **Template Organization**
Templates use:
- **Atomic Design Pattern**: Components organized in `atoms/` and `molecules/`
- **Template Inheritance**: All templates extend `base.html`
- **Includes**: Reusable components in `includes/` directory
  - `_navbar.html` - Navigation bar
  - `_alerts.html` - Django messages display
  - `atoms/button.html` - Button components
  - `atoms/input.html` - Input fields
  - `atoms/icon.html` - Icons
  - `molecules/modal.html` - Modal dialogs

### 5. **Security Patterns**
- **Always filter by user**: `Model.objects.filter(user=request.user)`
- **Validate ownership**: Use `get_object_or_404(Model, pk=pk, user=request.user)`
- **CSRF protection**: All forms include `{% csrf_token %}`
- **Login required**: All views use `@login_required`
- **Balance validation**: Check account balance before withdrawals/transfers

### 6. **Calculation Methods**
Models with financial calculations use property methods or model methods:
- `SavingsAccount.calculate_interest()` - Calculate interest
- `Loan.calculate_monthly_payment()` - Calculate EMI
- `Portfolio.return_percentage` - Calculate ROI
- `SavingsGoal.progress_percentage` - Calculate goal progress

---

## Development Workflow

### Setting Up Development Environment

1. **Install Dependencies**:
   ```bash
   cd bank_system
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

### Making Changes

#### Adding a New Feature
1. Identify the appropriate Django app (or create new one)
2. Update/create models in `models.py`
3. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Create forms in `forms.py`
5. Create views in `views.py`
6. Add URL patterns in `urls.py`
7. Create templates in `templates/<app_name>/`
8. Register models in `admin.py` for admin access

#### Modifying Existing Models
1. Edit model in `models.py`
2. Create migration: `python manage.py makemigrations`
3. Review migration file
4. Apply migration: `python manage.py migrate`
5. Update forms and views as needed

#### Adding New URL Routes
1. Add URL pattern to app's `urls.py`
2. If new app, include app URLs in `config/urls.py`:
   ```python
   path('app_name/', include('app_name.urls'))
   ```

### Database Management

- **Current DB**: SQLite (`db.sqlite3`)
- **Production-ready**: Designed to switch to PostgreSQL
- **Custom User Model**: `AUTH_USER_MODEL = 'users.User'`

---

## Key Settings (`config/settings.py`)

```python
# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Login/Logout URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Templates
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Installed Apps (in order)
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our apps
    'users',
    'accounts',
    'transactions',
    'core',
    'dashboard',
    'settings',
    'loans',
    'bills',
    'savings',
    'investments',
]
```

---

## Common Tasks for AI Assistants

### 1. Adding a New Transaction Type
- Update `Transaction.TRANSACTION_TYPES` in `transactions/models.py`
- Create migration
- Add view logic in `transactions/views.py`
- Create form in `transactions/forms.py`
- Add URL route
- Create template

### 2. Creating a New Financial Product
- Create model in appropriate app (savings/loans/investments)
- Add product configuration fields
- Create admin interface
- Add CRUD views
- Create forms and templates

### 3. Adding Dashboard Widgets
- Update `dashboard/views.py` with new data aggregation
- Update `templates/dashboard/dashboard.html` with new widget
- Ensure queries are optimized (use `select_related`, `prefetch_related`)

### 4. Implementing New Calculations
- Add method to model (e.g., `def calculate_xyz(self)`)
- Use `@property` for derived values
- Use `Decimal` for financial calculations
- Test edge cases (zero values, negative values)

### 5. Adding User Notifications
- Consider using Django messages framework
- Add reminder models (like `BillReminder`)
- Create notification views
- Add notification display in templates

---

## Testing Guidelines

### Manual Testing Checklist
- [ ] User can register and login
- [ ] User can only access their own data
- [ ] Forms validate correctly
- [ ] Calculations are accurate
- [ ] Transactions update balances correctly
- [ ] Negative balances are prevented
- [ ] Messages display properly
- [ ] Templates render correctly

### Areas Requiring Automated Tests
- Transaction processing logic
- Interest calculations
- EMI calculations
- Portfolio value calculations
- Balance validation
- User data isolation

---

## Security Considerations

### Current Implementations
1. **Custom User Model**: Uses Django's AbstractUser
2. **Login Required**: All views require authentication
3. **User Data Isolation**: All queries filter by `request.user`
4. **CSRF Protection**: Enabled by default
5. **Password Validation**: Django's built-in validators

### Production Considerations
- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Switch to PostgreSQL
- [ ] Add HTTPS enforcement
- [ ] Implement rate limiting
- [ ] Add transaction logging/audit trail

---

## Code Style and Conventions

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to complex methods
- Use type hints where appropriate

### Templates
- Use consistent indentation (2 or 4 spaces)
- Use template tags for logic
- Keep templates DRY (Don't Repeat Yourself)
- Use includes for reusable components

### Forms
- Add Bootstrap classes to widgets
- Provide helpful help_text
- Validate data in clean methods
- Display errors clearly

---

## Known Patterns to Follow

### When Creating New Models
```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NewModel(models.Model):
    # Always include user relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_models')

    # Your fields here
    name = models.CharField(max_length=200)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
```

### When Creating New Views
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def view_name(request):
    # Always filter by user
    objects = Model.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ModelForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Success message')
            return redirect('target_view')
    else:
        form = ModelForm(user=request.user)

    return render(request, 'app/template.html', {'form': form})
```

### When Creating New Forms
```python
from django import forms
from .models import Model

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['field1', 'field2']
        widgets = {
            'field1': forms.TextInput(attrs={'class': 'form-control'}),
            'field2': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
```

---

## Feature Flags and Configuration

Currently no feature flags are implemented. All features are enabled by default.

### Future Considerations
- Add settings for enabling/disabling modules (loans, investments, etc.)
- Add per-user feature access controls
- Add admin-configurable interest rates and fees

---

## Dependencies

Current dependencies (from `requirements.txt`):
```
asgiref==3.10.0
Django==5.2.7
sqlparse==0.5.3
tzdata==2025.2
```

Clean, minimal dependency footprint focusing on core Django functionality.

---

## Deployment Checklist

When deploying to production:
1. [ ] Update settings for production (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
2. [ ] Switch to PostgreSQL database
3. [ ] Set up static file serving (collectstatic)
4. [ ] Configure email backend for notifications
5. [ ] Set up HTTPS
6. [ ] Configure backup strategy for database
7. [ ] Set up logging
8. [ ] Configure environment variables
9. [ ] Run security checks: `python manage.py check --deploy`
10. [ ] Set up monitoring and error tracking

---

## Quick Reference: File Locations

| Task | File Location |
|------|---------------|
| Add URL route | `<app>/urls.py` or `config/urls.py` |
| Create model | `<app>/models.py` |
| Create view | `<app>/views.py` |
| Create form | `<app>/forms.py` |
| Create template | `templates/<app>/<name>.html` |
| Add CSS | `static/css/<name>.css` |
| Configure settings | `config/settings.py` |
| Register admin | `<app>/admin.py` |

---

## Notes for AI Assistants

### When Analyzing Code
- Check user data isolation in all queries
- Verify balance checks before transactions
- Ensure decimal precision for financial calculations
- Check for proper error handling

### When Adding Features
- Follow the existing app structure
- Use the same patterns for views, forms, and templates
- Add appropriate messages for user feedback
- Ensure mobile responsiveness (Bootstrap is used)
- Update this CLAUDE.md file if adding significant features

### When Fixing Bugs
- Check user permissions and data isolation
- Verify form validation
- Test edge cases (zero, negative, very large numbers)
- Check related transaction integrity

### When Refactoring
- Maintain backward compatibility with existing data
- Create migrations for model changes
- Update tests if they exist
- Keep code DRY but readable

---

## Project Status

**Current State**: Development/MVP
- Core features implemented
- Database schema established
- UI/UX framework in place
- Ready for testing and enhancement

**Next Steps** (Potential):
- Add comprehensive test suite
- Implement API endpoints (Django REST Framework)
- Add email notifications for bills and reminders
- Implement scheduled tasks (interest calculation, bill reminders)
- Add reporting and analytics features
- Implement two-factor authentication
- Add mobile app support via API

---

## Contact and Contribution

This is a learning/educational project. When making changes:
- Follow the established patterns
- Maintain code quality
- Add comments for complex logic
- Update documentation as needed
- Test thoroughly before committing

---

**Last Updated**: 2025-11-15
**Django Version**: 5.2.7
**Python Version**: 3.x
