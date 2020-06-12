from django.urls import path

from aerolinksma.shuttle import views

app_name = 'shuttle'
urlpatterns = [
    path('',
         views.CreateReservationView.as_view(),
         name='create_reservation'),
    path('admin/', views.AdminView.as_view(), name='admin'),
    path('admin/reservation/<int:pk>',
         views.ReservationDetailView.as_view(),
         name='reservation-detail'),
]
