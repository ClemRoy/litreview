# Generated by Django 4.0.4 on 2022-07-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_ticket_review_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='review_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
