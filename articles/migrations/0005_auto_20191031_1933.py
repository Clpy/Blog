# Generated by Django 2.2.6 on 2019-10-31 11:33

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20191031_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=mdeditor.fields.MDTextField(verbose_name='内容'),
        ),
    ]