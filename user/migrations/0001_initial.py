# Generated by Django 3.2.6 on 2021-10-19 09:09

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Given phone number is not valid', regex='^(\\+?998)?([. \\-])?((\\d){2})([. \\-])?(\\d){3}([. \\-])?(\\d){2}([. \\-])?(\\d){2}$')])),
                ('full_name', models.CharField(max_length=150, verbose_name='Ismi:')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ro‘yxatdan o‘tgan sanasi')),
                ('is_superuser', models.BooleanField(default=False, help_text='Administrator huquqini beradi', verbose_name='Administratormi?')),
                ('is_staff', models.BooleanField(default=False, help_text='Admin qismiga kirish huquqini beradi.', verbose_name='Moderatormi?')),
                ('is_active', models.BooleanField(default=True, help_text='Saytga kirish huquqini beradi.', verbose_name='Aktivmi?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
    ]
