import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

from django.core.mail import send_mail

# Create your models here.

class Server(models.Model):
  name = models.CharField(max_length=150)
  ip_address = models.IPAddressField(default="0.0.0.0")
  operating_system = models.CharField(max_length=150, default='')
  cpu = models.CharField(max_length=150)
  memory = models.IntegerField()
  operational = models.BooleanField()
  reservable = models.BooleanField()
  notes = models.CharField(max_length=300, blank=True, null=True)

  def __unicode__(self):
    return self.name

class Reservation(models.Model):
  server = models.ForeignKey(Server, blank=True, null=True)
  reserved_by = models.ForeignKey(User, blank=True, null=True)
  start_date = models.DateField('start date', default=datetime.date.today(), blank=True, null=True)
  end_date = models.DateField('reservation end', default=datetime.date.today(), blank=True, null=True)
  started = False
  expired = False 
  upcoming_warn = False

  def clean(self):
    if (self.server.operational == False):
      raise ValidationError(u"%s claims to be unoperational." % self.server.name)


    start_overlap = False
    end_overlap = False
    if(self.start_date > self.end_date):
      raise ValidationError(u"Reservation End cannot come before the Start Date")
    all_reservations = Reservation.objects.all() 
    for reservation in all_reservations:
      if (self.server == reservation.server) and not (self == reservation):
        if (self.start_date == reservation.start_date):
          raise ValidationError(u"Start date on this server matches a reservation of this server by %s." % reservation.reserved_by)
        if (self.end_date == reservation.end_date):
          raise ValidationError(u"End date on this server matches a reservation of this server by %s." % reservation.reserved_by)
        if (reservation.start_date < self.start_date) and (self.start_date < reservation.end_date):
          start_overlap = True
        if (reservation.start_date < self.end_date) and (self.end_date < reservation.end_date):
          end_overlap = True

        if (start_overlap and end_overlap):
          raise ValidationError(u"You're reservation falls inside of another reservation by %s, which starts %s and ends %s." % (reservation.reserved_by, reservation.start_date, reservation.end_date))
        elif (start_overlap):
          raise ValidationError(u"You're reservation starts inside of %s's reservation of the same server, which starts %s and ends %s." % (reservation.reserved_by, reservation.start_date, reservation.end_date))
        elif (end_overlap):
          raise ValidationError(u"You're reservation ends inside of %s's reservation of the same server, which starts %s and ends %s." % (reservation.reserved_by, reservation.start_date, reservation.end_date))
    if(self.start_date != None):
      if(self.start_date == datetime.date.today()) or (self.start_date < datetime.date.today()):
        self.started = True

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

def check_upcoming(res):
  if res.started == False and res.start_date != None and res.upcoming_warn == False:
    time_delta = datetime.date.today() - res.start_date
    if time_delta < datetime.timedelta(7):
      email_subject = u"[Serveservation] Reservation for %s Coming Soon" % res.server
      email_body =u"Your reservation of a server is coming soon. \n\nReservation start date: %s\nReservation end date: %s\n\nServer Name: %s\nServer IP: %s\n" % (res.start_date, res.end_date, res.server.name, res.server.ip_address) 
      email_from="david.dropinski@unboundid.com"
      email_to=[]
      email_to.append(res.reserved_by.email)
      send_mail(email_subject, email_body, email_from, email_to, fail_silently=False) 
      res.upcoming_warn = True
      res.save()

def check_expired(res):
  if (res.end_date != None) :
    time_delta = res.end_date - datetime.date.today()
    if time_delta < datetime.timedelta(0):
      res.expired = True

  if res.expired:
    email_subject = u"[Serveservation] Reservation for %s Expired" % res.server
    email_body =u"Your reservation of a server has ended. \n\nReservation start date: %s\nReservation end date: %s\n\nServer Name: %s\nServer IP: %s\n" % (res.start_date, res.end_date, res.server.name, res.server.ip_address) 
    email_from="david.dropinski@unboundid.com"
    email_to=[]
    email_to.append(res.reserved_by.email)
    send_mail(email_subject, email_body, email_from, email_to, fail_silently=False)
    expire_data(res)

def expire_data(res):
  res.reserved_by = None 
  res.start_date = None
  res.end_date = None 
  res.expired = False
  res.save()
