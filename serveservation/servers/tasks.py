from celery.task.schedules import crontab
from celery.decorators import periodic_task
from servers.models import Reservation, check_expired, check_upcoming

@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def check_reservations():
  all_reservations = Reservation.objects.all()
  for res in all_reservations:
    check_expired(res) 
    check_upcoming(res)
