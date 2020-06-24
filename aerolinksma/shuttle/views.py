from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from aerolinksma.shuttle.models import Reservation, Place
from aerolinksma.shuttle.forms import ClientForm, ReservationForm


class CreateReservationView(generic.View):
    template_name = 'shuttle/index.html'
    client_form = ClientForm()
    reservation_form = ReservationForm()

    def get_places_prices(self, places):
        if places is None:
            places = Place.objects.all().filter(enabled=True)
        places_prices = dict()

        for place in places:
            # Use fare type model choices as keys for convenient
            # handling in JavaScript.
            places_prices[place.pk] = {
                'OW': {         # one way
                    'cash': place.display_price(),
                    'paypal': place.get_paypal_price(),
                },
                'RT': {         # round trip
                    'cash': place.get_round_trip_price(),
                    'paypal': place.get_paypal_round_trip_price(),
                }
            }

        return places_prices

    def get(self, request, *args, **kwars):
        places = Place.objects.all().filter(enabled=True)
        # Pass places so it is not queried twice.
        places_prices = self.get_places_prices(places)

        context = {
            'client_form': self.client_form,
            'reservation_form': self.reservation_form,
            'places': places,
            'places_prices': places_prices,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        client_form = ClientForm(request.POST)
        reservation_form = ReservationForm(request.POST)

        if all((client_form.is_valid(), reservation_form.is_valid())):
            client = client_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.client = client

            # Set cost in cash to reservation instance according to
            # fare type.
            if reservation.fare_type == Reservation.FARE_TYPES[0][0]:
                reservation.cost = reservation.place.price
            else:
                reservation.cost = reservation.place.get_round_trip_price(
                    add_dollar_sign=False,
                )
            reservation.save()
            reservation.send_email()

            return HttpResponseRedirect(reverse('index'))
        else:
            places = Place.objects.all().filter(enabled=True)
            places_prices = self.get_places_prices(places)
            context = {
                'client_form': client_form,
                'reservation_form': reservation_form,
                'places': places,
                'places_prices': places_prices,
            }

            return render(request, self.template_name, context)


class AdminReservationView(generic.ListView):
    model = Reservation
    paginate_by = 15
    template_name = 'shuttle/admin_reservations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_reservations'] = Reservation.objects.all().filter(
            pickup_date__gte=timezone.now()
        ).order_by('pickup_date')[:5]
        return context


class ReservationDetailView(generic.DetailView):
    model = Reservation


class ReservationDeleteView(generic.DeleteView):
    model = Reservation
    success_url = reverse_lazy('shuttle:admin')


class ReservationMarkAsPaidView(generic.View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if pk is not None:
            reservation = get_object_or_404(Reservation, pk=pk)
        else:
            raise AttributeError(
                'Reservation pk should be provided.'
            )

        reservation.paid = True
        reservation.paid_at = timezone.now()
        reservation.payment_method = Reservation.PAYMENT_OPTIONS[0][0]
        reservation.save()

        return HttpResponseRedirect(reservation.get_absolute_url())


class AdminPlaceView(generic.ListView):
    model = Place
    template_name = 'shuttle/admin_places.html'


class PlaceCreateView(generic.CreateView):
    model = Place
    fields = ['name', 'price', 'time', 'enabled']
    template_name = 'shuttle/place_form.html'
    success_url = reverse_lazy('shuttle:admin-places')


class PlaceUpdateView(generic.UpdateView):
    model = Place
    fields = ['name', 'price', 'time', 'enabled']
    template_name = 'shuttle/place_form.html'
    success_url = reverse_lazy('shuttle:admin-places')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update place'
        return context
