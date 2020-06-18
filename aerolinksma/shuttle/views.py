from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.utils import timezone

from aerolinksma.shuttle.models import Reservation, Place
from aerolinksma.shuttle.forms import ClientForm, ReservationForm


class CreateReservationView(generic.View):
    template_name = 'shuttle/index.html'
    client_form = ClientForm()
    reservation_form = ReservationForm()

    def get(self, request, *args, **kwars):
        places = Place.objects.all().filter(enabled=True)
        context = {
            'client_form': self.client_form,
            'reservation_form': self.reservation_form,
            'places': places,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        client_form = ClientForm(request.POST)
        reservation_form = ReservationForm(request.POST)

        if all((client_form.is_valid(), reservation_form.is_valid())):
            client = client_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.client = client
            reservation.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'client_form': client_form,
                'reservation_form': reservation_form,
            }

            return render(request, self.template_name, context)


class AdminView(generic.ListView):
    model = Reservation
    paginate_by = 20
    template_name = 'shuttle/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_reservations'] = Reservation.objects.all().filter(
            pickup_date__gte=timezone.now()
        ).order_by('pickup_date')[:5]
        return context


class ReservationDetailView(generic.DetailView):
    model = Reservation
