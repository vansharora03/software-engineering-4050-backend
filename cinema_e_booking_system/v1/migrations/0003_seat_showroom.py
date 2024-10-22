# Generated by Django 4.2.16 on 2024-10-22 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0002_movie_release_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Showroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Showrooms',
                'db_table': 'Showroom',
            },
        ),
    ]
