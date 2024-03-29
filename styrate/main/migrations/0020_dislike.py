# Generated by Django 4.1.7 on 2023-06-27 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_review_dislikecount_alter_review_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('createdByUser_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DisLikesOfUser_List', to=settings.AUTH_USER_MODEL)),
                ('onReview_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DisLikesOfPost_List', to='main.review')),
            ],
        ),
    ]
