# Generated by Django 4.1.7 on 2023-03-08 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_review_overview'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='itemCategory',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
