# Generated by Django 2.2.6 on 2023-05-11 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0013_auto_20230511_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', null=True, unique=True),
        ),
    ]