from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reservation(models.Model):
  reserved_by = models.ForeignKey(User)
  start_date = models.DateField('date reserved')
  end_date = models.DateField('reservation end')

class Server(models.Model):
  reservation = models.ForeignKey(Reservation)
  name = models.CharField(max_length=150)
  operatingSystem = models.CharField(max_length=150)
  cpu = models.CharField(max_length=150)
  memory = models.IntegerField()
  operational = models.BooleanField()
  notes = models.CharField(max_length=300)
