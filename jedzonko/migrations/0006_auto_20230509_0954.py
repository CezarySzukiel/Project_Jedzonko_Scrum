# Generated by Django 2.2.6 on 2023-05-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0005_auto_20230509_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
