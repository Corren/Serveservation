from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reservation(models.Model):
  reservation_title = models.CharField(max_length=150, blank=True)
  reserved_by = models.ForeignKey(User)
  start_date = models.DateField('date reserved', null=True)
  end_date = models.DateField('reservation end', null=True)

  def __unicode__(self):
    return self.reservation_title

class Server(models.Model):
  reservation = models.ForeignKey(Reservation, blank=True, null=True)
  name = models.CharField(max_length=150)
  operatingSystem = models.CharField(max_length=150)
  cpu = models.CharField(max_length=150)
  memory = models.IntegerField()
  operational = models.BooleanField()
  notes = models.CharField(max_length=300)

  def __unicode__(self):
    return self.name
