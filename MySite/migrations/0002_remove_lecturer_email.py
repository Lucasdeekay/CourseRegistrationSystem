# Generated by Django 5.0.6 on 2024-06-22 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='email',
        ),
    ]
