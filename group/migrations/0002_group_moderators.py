# Generated by Django 5.0.6 on 2024-10-04 11:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='moderators',
            field=models.ManyToManyField(related_name='moderators_of_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]