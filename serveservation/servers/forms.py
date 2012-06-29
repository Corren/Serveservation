from django import forms
from servers.models import Server, Reservation

# Form for Servers
class ServerForm(forms.ModelForm):
  class Meta:
    model = Server

# Form for Reservation
class ReservationForm(forms.ModelForm):
  class Meta:
    model = Reservation
