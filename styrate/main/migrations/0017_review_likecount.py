# Generated by Django 4.1.7 on 2023-03-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_user_likecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='likeCount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
