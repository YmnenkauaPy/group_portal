# Generated by Django 5.0.6 on 2024-10-11 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_alter_material_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to='materials_media/'),
        ),
    ]