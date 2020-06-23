from django.urls import path

from aerolinksma.core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
]
