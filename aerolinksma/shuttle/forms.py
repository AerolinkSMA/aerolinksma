from django import forms

from aerolinksma.shuttle.models import Client, Reservation

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('fare_type', 'direction', 'place', 'place_address',
                  'sma_address', 'luggage', 'pickup_date', 'return_date')
