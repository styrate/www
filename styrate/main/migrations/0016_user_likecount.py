# Generated by Django 4.1.7 on 2023-03-13 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_user_ranking_alter_user_biotext'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likeCount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]