# Generated by Django 4.0.4 on 2022-06-01 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0002_userfollows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='following_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
