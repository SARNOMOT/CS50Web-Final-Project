# Generated by Django 4.0.2 on 2023-10-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_alter_quiz_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]
