# Generated by Django 2.2.28 on 2023-06-19 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_tutorial', '0002_chatrecordsmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatrecordsmodel',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
