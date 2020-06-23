from django.views import generic

from aerolinksma.shuttle.models import Place


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class PricingView(generic.ListView):
    model = Place
    template_name = 'pricing.html'
