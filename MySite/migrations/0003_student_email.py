# Generated by Django 5.0.6 on 2024-06-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0002_remove_lecturer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(default='user@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
