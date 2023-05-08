# Generated by Django 4.2.1 on 2023-05-08 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=64)),
                ('order', models.IntegerField()),
                ('day_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.dayname')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.plan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.RecipePlan', to='jedzonko.recipe'),
        ),
    ]
