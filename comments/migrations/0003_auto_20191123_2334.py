# Generated by Django 2.2.6 on 2019-11-23 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20191117_2157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_time'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]