# Generated by Django 4.0.4 on 2022-07-26 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_alter_review_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]
