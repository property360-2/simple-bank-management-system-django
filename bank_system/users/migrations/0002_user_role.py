# Generated migration for adding role field to User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('customer', 'Customer'), ('manager', 'Manager/Staff'), ('admin', 'Administrator')],
                default='customer',
                help_text="User's role in the system",
                max_length=20
            ),
        ),
    ]
