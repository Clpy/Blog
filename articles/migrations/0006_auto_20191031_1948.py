# Generated by Django 2.2.6 on 2019-10-31 11:48

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20191031_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
    ]