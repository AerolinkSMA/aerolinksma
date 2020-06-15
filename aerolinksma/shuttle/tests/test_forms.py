import datetime

from django.test import TestCase
from django.utils import timezone

from aerolinksma.shuttle.forms import ReservationForm
from aerolinksma.shuttle.models import Place, Reservation


class TestReservationForm(TestCase):
    def setUp(self):
        place = Place.objects.create(name='CDMX', price=100, time=2)

        self.initial_data = {
            'fare_type': 'OW',         # one way
            'direction': 'TO',         # to san miguel
            'place': place.pk,
            'place_details': 'Test details',
            'sma_address': 'Test address',
            'luggage': 0,
            'pickup_date': timezone.now() + datetime.timedelta(days=1)
        }

    def test_pickup_date_should_not_be_earlier_than_current_date(self):
        data = self.initial_data
        data['pickup_date'] = timezone.now() - datetime.timedelta(minutes=1)

        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('pickup_date' in form.errors)

        data['pickup_date'] = timezone.now() + datetime.timedelta(days=1)
        form = ReservationForm(data)
        self.assertTrue(form.is_valid())

    def test_return_date_should_not_be_earlier_than_pickup_date(self):
        data = self.initial_data
        data['fare_type'] = 'RT'  # round trip
        data['return_date'] = timezone.now() + datetime.timedelta(hours=12)

        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('return_date' in form.errors)

        data['return_date'] = timezone.now() + datetime.timedelta(days=2)
        form = ReservationForm(data)
        self.assertTrue(form.is_valid())

    def test_return_date_should_be_required_if_its_round_trip(self):
        data = self.initial_data
        data['fare_type'] = 'RT'  # round trip

        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('return_date' in form.errors)

        data['return_date'] = timezone.now() + datetime.timedelta(days=2)
        form = ReservationForm(data)
        self.assertTrue(form.is_valid())
