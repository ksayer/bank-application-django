# Generated by Django 2.2 on 2022-03-07 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_transaction_number_money'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='number',
            new_name='number_money',
        ),
    ]