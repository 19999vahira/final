# Generated by Django 5.0.4 on 2024-04-22 20:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Accountnew',
        ),
        migrations.RenameField(
            model_name='accountnew',
            old_name='balance',
            new_name='balancenew',
        ),
        migrations.RenameField(
            model_name='accountnew',
            old_name='user',
            new_name='usernew',
        ),
    ]