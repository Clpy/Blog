# Generated by Django 2.2.6 on 2019-12-07 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likerecord',
            old_name='liked_user',
            new_name='user',
        ),
    ]
