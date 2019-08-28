from django.db import models

# Create your models here.


class ConferenceHall(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector_available = models.BooleanField()


class Booking(models.Model):
    date = models.DateField()
    hall = models.ForeignKey(ConferenceHall, on_delete=models.CASCADE)
    comment = models.TextField()
