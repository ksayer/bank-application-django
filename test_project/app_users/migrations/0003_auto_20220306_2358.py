# Generated by Django 2.2 on 2022-03-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_auto_20220306_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='number',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
    ]