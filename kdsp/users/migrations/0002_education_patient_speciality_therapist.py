# Generated by Django 3.2.7 on 2021-09-19 07:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('age', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(6.5), django.core.validators.MinValueValidator(0)], verbose_name='Age')),
                ('parent_name', models.CharField(max_length=100, verbose_name='Parent Name')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('sessions', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)], verbose_name='Therapy Sessions')),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('code', models.CharField(max_length=6, verbose_name='Short Code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('fees', models.IntegerField(default=0, verbose_name='Fees')),
            ],
            options={
                'verbose_name_plural': 'Specialities',
            },
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('work_experience', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(60), django.core.validators.MinValueValidator(0)])),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='therapists', to='users.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('degree', models.CharField(max_length=100, verbose_name='Education Degree')),
                ('institution', models.CharField(max_length=100, verbose_name='Institution')),
                ('completion_year', models.CharField(blank=True, max_length=4, verbose_name='Completion Year')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='users.therapist')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
