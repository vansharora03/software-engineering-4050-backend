# Generated by Django 4.2.16 on 2024-12-09 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_alter_booking_movie_title_alter_booking_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='show_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.showtime'),
        ),
    ]
