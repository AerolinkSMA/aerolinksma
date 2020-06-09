from django.urls import path

from aerolinksma.shuttle import views

app_name = 'shuttle'
urlpatterns = [
    path('',
         views.CreateReservationView.as_view(),
         name='create_reservation'),
]
