import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

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
  reserved_by = models.ForeignKey(User, blank=True, null=True)
  start_date = models.DateField('date reserved', default=datetime.date.today(), blank=True, null=True)
  end_date = models.DateField('reservation end', default=datetime.date.today(), blank=True, null=True)
  expired = False 

  def clean(self):
    time_delta = self.end_date - datetime.date.today()
    if (self.end_date == None) :
      self.expired = True
    elif time_delta < datetime.timedelta(0):
      self.expired = True

    if self.expired:
      self.reserved_by = None 
      self.start_date = None
      self.end_date = None 
      self.expired = False

  def __unicode__(self):
    if self.reserved_by != None:
      reserved_string = u"%s is reserved by %s" % (self.server.name, self.reserved_by)
    else:
      reserved_string = u"%s is not reserved" % self.server.name
    return reserved_string

@receiver(post_save, sender=Server)
def create_reservation(sender, instance, created, **kwargs):
  if(created):
    reservation = Reservation(server=instance, reserved_by=None, start_date=None, end_date=None)
    reservation.save()
