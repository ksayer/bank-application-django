# Generated by Django 2.2 on 2022-03-06 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='app_users.Transaction', verbose_name='Транзакция'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.PositiveIntegerField(default=0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
