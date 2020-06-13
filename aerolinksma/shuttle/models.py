from django.db import models
from django.urls import reverse


class Place(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.FloatField(help_text='Time to get from SMA to this destination or viceversa, in hours')
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)


class Reservation(models.Model):
    DIRECTION_CHOICES = (
        ('TO', 'To SMA'),
        ('FR', 'From SMA'),
    )
    FARE_TYPES = (
        ('OW', 'One way'),
        ('RT', 'Rount trip'),
    )
    direction = models.CharField(max_length=2, choices=DIRECTION_CHOICES)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL,
                              null=True, related_name='reservations')
    place_details = models.CharField(max_length=255)
    sma_address = models.CharField('SMA Address', max_length=255)
    fare_type = models.CharField(max_length=2, choices=FARE_TYPES)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    luggage = models.IntegerField(default=0)
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Required if fare type is round trip')
    paid = models.BooleanField(default=False)
    notes = models.TextField(help_text='Extra information about your trip',
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """The str representation will be like: 'To Guadalajara (One way)'"""

        if self.direction == 'TO':
            direction = 'To'
        else:
            direction = 'From'
        return '{} {} ({})'.format(direction, self.place,
                                   self.get_fare_type_display())

    def get_absolute_url(self):
        return reverse('shuttle:reservation-detail', kwargs={'pk': self.pk})
