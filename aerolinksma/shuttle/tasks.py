from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from aerolinksma.shuttle.models import Reservation


@shared_task
def notify_new_reservation(email, reservation_pk):
    if email is None or email == '':
        raise AttributeError('Email is blank')

    try:
        r = Reservation.objects.get(pk=reservation_pk)
    except Reservation.DoesNotExist:
        raise Exception('Reservation not found')

    context = {'reservation': r}
    subject = render_to_string('emails/clients/new_reservation_subject.txt',
                               {'id': r.get_id()})
    message = render_to_string('emails/clients/new_reservation_body.txt',
                               context)
    from_email = 'contact@aerolinksma.com'

    send_mail(subject, message, from_email, [email])
