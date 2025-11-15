import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Account
from transactions.models import Transaction, FraudDetection
from savings.models import SavingsProduct, SavingsAccount
from investments.models import InvestmentPlatform, InvestmentProduct, Portfolio, InvestmentHolding
from loans.models import LoanProduct, Loan
from bills.models import BillerCategory, Biller

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with test data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting data seeding...'))

        # Create savings products
        self.create_savings_products()

        # Create investment platforms and products
        self.create_investment_data()

        # Create loan products
        self.create_loan_products()

        # Create biller categories
        self.create_biller_categories()

        # Create users and their data
        self.create_users_with_data()

        # Create fraud detection records
        self.create_fraud_detection_data()

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_savings_products(self):
        """Create savings product types"""
        products = [
            {
                'name': 'Premium Savings',
                'description': 'High yield savings account',
                'interest_rate': Decimal('4.50'),
                'min_balance': Decimal('1000'),
                'compounding_frequency': 'monthly',
                'withdrawal_limit': 6,
                'penalty_rate': Decimal('0.50'),
            },
            {
                'name': 'Standard Savings',
                'description': 'Regular savings account',
                'interest_rate': Decimal('3.00'),
                'min_balance': Decimal('500'),
                'compounding_frequency': 'monthly',
                'withdrawal_limit': 4,
                'penalty_rate': Decimal('0.25'),
            },
            {
                'name': 'Growth Savings',
                'description': 'Ideal for long-term growth',
                'interest_rate': Decimal('5.25'),
                'min_balance': Decimal('5000'),
                'compounding_frequency': 'daily',
                'withdrawal_limit': 2,
                'penalty_rate': Decimal('1.00'),
            },
        ]

        for product_data in products:
            SavingsProduct.objects.get_or_create(**product_data)

        self.stdout.write(self.style.SUCCESS('Created savings products'))

    def create_investment_data(self):
        """Create investment platforms and products"""
        platforms_data = [
            {
                'name': 'Stock Market Exchange',
                'platform_type': 'stocks',
                'description': 'Major stock trading platform',
                'icon': 'fa-chart-line',
                'color': '#00AA00',
            },
            {
                'name': 'Crypto Exchange',
                'platform_type': 'crypto',
                'description': 'Cryptocurrency trading',
                'icon': 'fa-coins',
                'color': '#FF9900',
            },
            {
                'name': 'Bond Market',
                'platform_type': 'bonds',
                'description': 'Government and corporate bonds',
                'icon': 'fa-file-contract',
                'color': '#0066CC',
            },
            {
                'name': 'Mutual Funds Hub',
                'platform_type': 'mutual_funds',
                'description': 'Mutual fund investments',
                'icon': 'fa-chart-pie',
                'color': '#9900CC',
            },
        ]

        for platform_data in platforms_data:
            platform, _ = InvestmentPlatform.objects.get_or_create(**platform_data)

            # Create products for each platform
            if platform.platform_type == 'stocks':
                products = [
                    ('AAPL', 'Apple Inc.', 'large-cap', Decimal('175.50')),
                    ('GOOGL', 'Alphabet Inc.', 'large-cap', Decimal('140.25')),
                    ('MSFT', 'Microsoft Corp.', 'large-cap', Decimal('380.00')),
                    ('AMZN', 'Amazon.com Inc.', 'large-cap', Decimal('180.75')),
                    ('TSLA', 'Tesla Inc.', 'large-cap', Decimal('245.50')),
                ]
            elif platform.platform_type == 'crypto':
                products = [
                    ('BTC', 'Bitcoin', 'volatile', Decimal('65000')),
                    ('ETH', 'Ethereum', 'volatile', Decimal('3500')),
                    ('ADA', 'Cardano', 'volatile', Decimal('0.98')),
                ]
            elif platform.platform_type == 'bonds':
                products = [
                    ('US10Y', '10-Year Treasury', 'low', Decimal('4.15')),
                    ('CORPBOND', 'Corporate Bond Fund', 'medium', Decimal('102.50')),
                ]
            else:
                products = [
                    ('VTSAX', 'Vanguard Total Stock', 'medium', Decimal('85.50')),
                    ('VTIAX', 'Vanguard Intl Stock', 'medium', Decimal('95.75')),
                ]

            for symbol, name, risk_level, price in products:
                InvestmentProduct.objects.get_or_create(
                    platform=platform,
                    symbol=symbol,
                    defaults={
                        'name': name,
                        'description': f'{name} investment product',
                        'current_price': price,
                        'risk_level': risk_level,
                        'min_investment': Decimal('100'),
                        'expected_return': Decimal('7.50'),
                    }
                )

        self.stdout.write(self.style.SUCCESS('Created investment platforms and products'))

    def create_loan_products(self):
        """Create loan product types"""
        products = [
            {
                'name': 'Personal Loan',
                'loan_type': 'personal',
                'min_amount': Decimal('1000'),
                'max_amount': Decimal('50000'),
                'interest_rate': Decimal('8.50'),
                'min_term': 12,
                'max_term': 60,
                'description': 'Flexible personal loans',
            },
            {
                'name': 'Home Loan',
                'loan_type': 'home',
                'min_amount': Decimal('50000'),
                'max_amount': Decimal('1000000'),
                'interest_rate': Decimal('4.25'),
                'min_term': 120,
                'max_term': 360,
                'description': 'Long-term home financing',
            },
            {
                'name': 'Auto Loan',
                'loan_type': 'auto',
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('100000'),
                'interest_rate': Decimal('5.75'),
                'min_term': 24,
                'max_term': 84,
                'description': 'Vehicle financing',
            },
            {
                'name': 'Business Loan',
                'loan_type': 'business',
                'min_amount': Decimal('25000'),
                'max_amount': Decimal('500000'),
                'interest_rate': Decimal('7.00'),
                'min_term': 12,
                'max_term': 120,
                'description': 'Business expansion and growth',
            },
        ]

        for product_data in products:
            LoanProduct.objects.get_or_create(**product_data)

        self.stdout.write(self.style.SUCCESS('Created loan products'))

    def create_biller_categories(self):
        """Create biller categories"""
        categories = [
            'electricity', 'water', 'internet', 'insurance',
            'credit_card', 'loan', 'shopping', 'utilities', 'subscription'
        ]

        for category in categories:
            BillerCategory.objects.get_or_create(category=category)

        self.stdout.write(self.style.SUCCESS('Created biller categories'))

    def create_users_with_data(self):
        """Create test users and their financial data"""
        # Create 50 test users
        for i in range(1, 51):
            username = f'user{i:03d}'

            # Create or get user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'User{i}',
                    'last_name': f'Test{i}',
                    'phone': f'+1555{i:06d}',
                    'role': 'customer',
                }
            )

            if created:
                user.set_password('Test@123456')
                user.save()

                # Create accounts for user
                self.create_user_accounts(user)

                # Create savings accounts
                self.create_user_savings(user)

                # Create transactions
                self.create_user_transactions(user)

                # Create investments
                self.create_user_investments(user)

                # Create loans
                self.create_user_loans(user)

                # Create billers
                self.create_user_billers(user)

                if i % 10 == 0:
                    self.stdout.write(f'Created {i} users with all data')

        self.stdout.write(self.style.SUCCESS('Created 50 users with complete financial data'))

    def create_user_accounts(self, user):
        """Create checking and savings accounts for user"""
        for account_type in ['checking', 'savings']:
            account_number = f'{user.id:06d}{random.randint(1000, 9999)}'
            Account.objects.get_or_create(
                user=user,
                account_number=account_number,
                defaults={
                    'account_type': account_type,
                    'balance': Decimal(random.randint(1000, 100000)),
                    'is_active': True,
                }
            )

    def create_user_savings(self, user):
        """Create savings accounts for user"""
        products = SavingsProduct.objects.all()
        for product in products[:2]:  # 2 savings products per user
            account_number = f'SAV{user.id:06d}{random.randint(1000, 9999)}'
            account = user.accounts.first()
            if account:
                SavingsAccount.objects.get_or_create(
                    user=user,
                    product=product,
                    account=account,
                    account_number=account_number,
                    defaults={
                        'balance': Decimal(random.randint(5000, 50000)),
                        'interest_earned': Decimal(random.uniform(10, 500)),
                        'status': 'active',
                    }
                )

    def create_user_transactions(self, user):
        """Create random transactions for user"""
        accounts = user.accounts.all()
        if accounts.count() < 2:
            return

        accounts_list = list(accounts)
        from_account = accounts_list[0]

        # Create 50-100 transactions per user from Oct 17 to Nov 24
        num_transactions = random.randint(50, 100)
        for _ in range(num_transactions):
            # Oct 17 to Nov 24 is approximately 38 days
            days_ago = random.randint(0, 38)
            created_at = timezone.now() - timedelta(days=days_ago)

            transaction_type = random.choice(['deposit', 'withdrawal', 'transfer'])
            amount = Decimal(random.uniform(10, 5000)).quantize(Decimal('0.01'))

            to_account = accounts_list[1] if len(accounts_list) > 1 and transaction_type == 'transfer' else None

            Transaction.objects.create(
                from_account=from_account if transaction_type != 'deposit' else None,
                to_account=to_account if transaction_type == 'transfer' else from_account,
                transaction_type=transaction_type,
                amount=amount,
                description=f'{transaction_type.title()} transaction',
                created_at=created_at,
            )

    def create_user_investments(self, user):
        """Create investment portfolio for user"""
        account = user.accounts.first()
        if not account:
            return

        portfolio, _ = Portfolio.objects.get_or_create(
            user=user,
            account=account,
            defaults={
                'name': f'{user.username} Portfolio',
                'description': 'Investment portfolio',
                'total_invested': Decimal(random.randint(10000, 100000)),
                'current_value': Decimal(random.randint(10000, 120000)),
                'status': 'active',
            }
        )

        # Add some holdings
        products = InvestmentProduct.objects.all()[:5]
        for product in products:
            InvestmentHolding.objects.get_or_create(
                portfolio=portfolio,
                product=product,
                defaults={
                    'quantity': Decimal(random.randint(1, 100)),
                    'purchase_price': product.current_price * Decimal(random.uniform(0.8, 1.2)),
                    'current_price': product.current_price,
                }
            )

    def create_user_loans(self, user):
        """Create loans for user"""
        account = user.accounts.first()
        if not account:
            return

        # Create 1-3 loans per user
        loan_products = LoanProduct.objects.all()
        for loan_product in random.sample(list(loan_products), k=min(random.randint(1, 3), len(list(loan_products)))):
            principal = Decimal(random.randint(int(loan_product.min_amount), min(50000, int(loan_product.max_amount))))
            loan_term = random.randint(loan_product.min_term, loan_product.max_term)

            loan, created = Loan.objects.get_or_create(
                user=user,
                product=loan_product,
                account=account,
                defaults={
                    'principal_amount': principal,
                    'interest_rate': loan_product.interest_rate,
                    'loan_term': loan_term,
                    'remaining_balance': principal,
                    'status': random.choice(['pending', 'approved', 'active']),
                }
            )

            # Calculate and set monthly payment if it's a new loan
            if created:
                loan.monthly_payment = loan.calculate_monthly_payment()
                loan.save()

    def create_user_billers(self, user):
        """Create billers for user"""
        categories = BillerCategory.objects.all()
        for category in random.sample(list(categories), k=min(random.randint(3, 6), len(list(categories)))):
            Biller.objects.get_or_create(
                user=user,
                name=f'{category.get_category_display()} - Bill {user.id}',
                category=category,
                defaults={
                    'account_number': f'ACC{random.randint(100000, 999999)}',
                    'phone': f'+1555{random.randint(1000000, 9999999)}',
                    'email': f'biller{user.id}@example.com',
                    'nickname': f'{category.get_category_display()}',
                    'due_date': random.randint(1, 28),
                    'is_active': True,
                    'is_favorite': random.choice([True, False]),
                }
            )

    def create_fraud_detection_data(self):
        """Create fraud detection records for demonstration"""
        try:
            accounts = Account.objects.all()[:30]  # Use first 30 accounts
            risk_levels = ['low', 'medium', 'high', 'critical']
            fraud_reasons = [
                'Unusual transaction amount detected',
                'Multiple rapid transactions detected',
                'Transaction at unusual time',
                'New recipient transaction',
                'Geographic anomaly detected',
                'Pattern deviation detected',
                'High-value withdrawal attempt',
                'Suspicious account access pattern',
            ]

            for account in accounts:
                # Create 0-3 fraud alerts per account
                for _ in range(random.randint(0, 3)):
                    risk_level = random.choices(
                        risk_levels,
                        weights=[60, 20, 15, 5],  # More low/medium, fewer critical
                        k=1
                    )[0]

                    detected_date = timezone.now() - timedelta(days=random.randint(1, 30))

                    FraudDetection.objects.create(
                        account=account,
                        risk_level=risk_level,
                        status=random.choice(['pending', 'reviewed', 'approved', 'rejected']),
                        unusual_amount=random.choice([True, False]),
                        rapid_transactions=random.choice([True, False]),
                        unusual_time=random.choice([True, False]),
                        new_recipient=random.choice([True, False]),
                        geographic_anomaly=random.choice([True, False]),
                        reason=random.choice(fraud_reasons),
                        detected_at=detected_date,
                    )

            self.stdout.write(self.style.SUCCESS('Created fraud detection records'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Fraud detection seeding skipped: {str(e)}'))
