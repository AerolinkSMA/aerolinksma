from django.urls import path

from aerolinksma.shuttle import views

app_name = 'shuttle'
urlpatterns = [
    path('',
         views.CreateReservationView.as_view(),
         name='create_reservation'),
    path('admin/',
         views.AdminReservationView.as_view(),
         name='admin'),
    path('admin/reservation/<int:pk>/',
         views.ReservationDetailView.as_view(),
         name='reservation-detail'),
    path('admin/reservation/<int:pk>/mark-as-paid/',
         views.ReservationMarkAsPaidView.as_view(),
         name='reservation-mark-as-paid'),
    path('admin/reservation/<int:pk>/delete/',
         views.ReservationDeleteView.as_view(),
         name='reservation-delete'),
    path('admin/places/',
         views.AdminPlaceView.as_view(),
         name='admin-places'),
    path('admin/places/add/',
         views.PlaceCreateView.as_view(),
         name='place-add'),
    path('admin/places/<int:pk>/edit/',
         views.PlaceUpdateView.as_view(),
         name='place-edit'),
]
