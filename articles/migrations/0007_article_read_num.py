# Generated by Django 2.2.6 on 2019-10-31 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20191031_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]
