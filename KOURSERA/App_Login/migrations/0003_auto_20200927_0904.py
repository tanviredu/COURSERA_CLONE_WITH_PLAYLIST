# Generated by Django 3.1 on 2020-09-27 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Login', '0002_video_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_content',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_content', to=settings.AUTH_USER_MODEL),
        ),
    ]
