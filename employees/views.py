from django.views.generic import TemplateView
from .models import QabulKomissiya

class KomissiyaView(TemplateView):
    template_name = "komissiya.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rais'] = QabulKomissiya.objects.filter(
            lavozim_turi='rais',
            is_active=True
        ).first()

        context['azolar'] = QabulKomissiya.objects.filter(
            is_active=True
        ).exclude(lavozim_turi='rais')

        return context
    