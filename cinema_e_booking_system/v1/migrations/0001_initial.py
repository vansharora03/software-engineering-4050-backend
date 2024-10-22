# Generated by Django 4.2.16 on 2024-10-22 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('trailer_link', models.CharField(max_length=500)),
                ('img_link', models.CharField(max_length=500)),
                ('duration', models.PositiveIntegerField()),
                ('release_date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Movies',
                'db_table': 'Movie',
            },
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
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.movie')),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.showroom')),
            ],
            options={
                'db_table': 'Showtime',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.showroom')),
            ],
            options={
                'db_table': 'Seat',
            },
        ),
    ]
