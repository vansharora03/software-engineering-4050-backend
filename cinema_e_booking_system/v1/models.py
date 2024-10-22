from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    trailer_link = models.CharField(max_length=500)
    img_link = models.CharField(max_length=500)
    duration = models.PositiveIntegerField() 
    release_date = models.DateTimeField(editable=True)

    class Meta:
        db_table = 'Movie'
        verbose_name_plural = 'Movies'
    
    def __str__(self):
        return self.title

class Showroom(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Showroom'
        verbose_name_plural = 'Showrooms'
    
    def __str__(self):
        return self.name

class Seat(models.Model):
    number = models.PositiveIntegerField()
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)

class Showtime(models.Model):
    time = models.DateTimeField(editable=True)
    duration = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
