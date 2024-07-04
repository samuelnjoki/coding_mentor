# Generated by Django 5.0.3 on 2024-04-24 12:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=15000)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('image', models.ImageField(default='default1.png', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('fromT', models.TimeField()),
                ('toT', models.TimeField()),
                ('description', models.TextField(max_length=15000)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('', 'Your Gender?'), ('male', 'Male'), ('female', 'Female')], max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('interest', models.CharField(choices=[('', 'Your Interest?'), ('mentor', 'mentor'), ('mentee', 'mentee')], max_length=50)),
                ('bio', models.TextField(max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, default='default.png', null=True, upload_to='', verbose_name='photo')),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(choices=[('', 'Experience Period'), ('None', 'None'), ('1-6 months', '1-6 months'), ('6-12 months', '6-12 months'), ('1-2 yrs', '1-2 yrs'), ('2-4 yrs', '2-4 yrs'), ('above 4yrs', 'above 4yrs')], max_length=20)),
                ('interest', models.CharField(choices=[('', 'Your Interest?'), ('mentor', 'mentor'), ('mentee', 'mentee')], max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorclub.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=15000)),
                ('date', models.DateField()),
                ('fromT', models.TimeField()),
                ('toT', models.TimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorclub.course')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorclub.member')),
            ],
        ),
        migrations.AddConstraint(
            model_name='member',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course'),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('course', 'mentor'), name='unique_course_mentor'),
        ),
    ]
