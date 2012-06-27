import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Server(models.Model):
  name = models.CharField(max_length=150)
  operating_system = models.CharField(max_length=150, default='')
  ip_address = models.IPAddressField(default="0.0.0.0")
  cpu = models.CharField(max_length=150)
  memory = models.IntegerField()
  operational = models.BooleanField()
  notes = models.CharField(max_length=300)

  def __unicode__(self):
    return self.name

class Reservation(models.Model):
  server = models.OneToOneField(Server, primary_key=True)
  reserved = models.BooleanField()
  reserved_by = models.ForeignKey(User, blank=True, null=True)
  start_date = models.DateField('date reserved', default=datetime.date.today(), null=True)
  end_date = models.DateField('reservation end', default=datetime.date.today(), null=True)

  def __unicode__(self):
    return u"%s is reserved by this Reservation" % self.server.name

class ExpiredReservatation(models.Model):
  allReservations = list(Reservation.objects.all())
  expiredReservations = []
  for res in allReservations:
    if res.end_date == datetime.date.today():
      expiredReservations.append(res)

  def __unicode__(self):
    return u"A list of expired reservations is: %s" % expiredReservations
