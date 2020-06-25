from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from aerolinksma.shuttle.models import Client, Reservation, Place, Driver

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('first_name', wrapper_class='col-md-6'),
                Field('last_name', wrapper_class='col-md-6'),
                css_class='form-row',
            ),
            Div(
                Field('email', wrapper_class='col-md-6'),
                Field('phone_number', wrapper_class='col-md-6'),
                css_class='form-row',
            ),
        )


class ReservationForm(forms.ModelForm):
    direction = forms.ChoiceField(choices=Reservation.DIRECTION_CHOICES,
                                  initial=Reservation.DIRECTION_CHOICES[0],
                                  help_text='Going to or from SMA?')
    fare_type = forms.ChoiceField(choices=Reservation.FARE_TYPES,
                                  initial=Reservation.FARE_TYPES[0])
    place = forms.ModelChoiceField(queryset=Place.objects.all().filter(enabled=True),
                                   empty_label='Choose a place')
    luggage = forms.IntegerField(min_value=0, max_value=6, initial=0)
    passengers = forms.IntegerField(min_value=1, max_value=4, initial=1)
    payment_method = forms.ChoiceField(choices=Reservation.PAYMENT_OPTIONS,
                                       initial=Reservation.PAYMENT_OPTIONS[0])

    class Meta:
        model = Reservation
        fields = ('fare_type', 'direction', 'place', 'place_details',
                  'sma_address', 'luggage', 'passengers', 'payment_method',
                  'pickup_date', 'return_date')
        widgets = {
            'place_details': forms.TextInput(
                attrs={
                    'placeholder': 'Specify the address or flight number',
                },
            ),
            'sma_address': forms.TextInput(
                attrs={
                    'placeholder': 'Specify the address in San Miguel de Allende',
                },
            ),
            'pickup_date': forms.DateTimeInput(
                attrs={
                    'placeholder': 'yyyy-mm-dd hh:mm',
                },
            ),
            'return_date': forms.DateTimeInput(
                attrs={
                    'placeholder': 'yyyy-mm-dd hh:mm',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('direction', wrapper_class='col-md-4',
                      css_class='custom-select'),
                Field('place', wrapper_class='col-md-8',
                      css_class='custom-select'),
                css_class='form-row',
            ),
            Div(
                Field('fare_type', wrapper_class='col-md-4',
                      css_class='custom-select'),
                Field('pickup_date', wrapper_class='col-md-4'),
                Field('return_date', wrapper_class='col-md-4'),
                css_class='form-row',
            ),
            Field('place_details'),
            Field('sma_address'),
            Div(
                Field('payment_method', wrapper_class='col-md-4',
                      css_class='custom-select'),
                Field('luggage', wrapper_class='col-md-4'),
                Field('passengers', wrapper_class='col-md-4'),
                css_class='form-row',
            ),
        )

    def clean_pickup_date(self):
        """Fail if pickup date is earlier than current datetime."""
        now = timezone.now()
        pickup_date = self.cleaned_data['pickup_date']

        if pickup_date < now:
            raise forms.ValidationError(
                'Pickup date cannot be earlier than current time.'
            )

        return pickup_date

    def clean_return_date(self):
        """
        Fail if fare type is 'Round trip' and return date is empty.

        Also, fail if return date is earlier than pickup date.
        """
        return_date = self.cleaned_data['return_date']
        fare_type = self.cleaned_data['fare_type']

        if fare_type == 'RT':
            if return_date is None:
                raise forms.ValidationError(
                    'Return date is required for round trips'
                )
            else:
                pickup_date = self.cleaned_data['pickup_date']

                if return_date < pickup_date:
                    raise forms.ValidationError(
                        'Return date cannot be earlier pickup date'
                    )
        else:
            return_date = None

        return return_date


class ReservationAssignForm(forms.ModelForm):
    driver = forms.ModelChoiceField(queryset=Driver.objects.all().filter(is_active=True),
                                    empty_label='Not assigned', required=False)
    class Meta:
        model = Reservation
        fields = ['driver']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].widget.attrs.update({
            'class': 'custom-select',
        })
