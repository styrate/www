# Generated by Django 4.1.7 on 2023-03-08 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='overview',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
