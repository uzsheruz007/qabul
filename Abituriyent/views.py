from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .models import PrivilegeCategory, Privilege
from django.shortcuts import render
from .models import QabulKvotasi

class PrivilegeListView(TemplateView):
    template_name = "privileges.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = PrivilegeCategory.objects.filter(is_active=True)
        privileges = Privilege.objects.filter(is_active=True).order_by('id')

        paginator = Paginator(privileges, 4)  # 🔥 2x2
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["categories"] = categories
        context["page_obj"] = page_obj
        context["total_count"] = privileges.count()

        return context


def qabul_kvotasi(request):
    kvota = QabulKvotasi.objects.last()
    return render(request, 'qabul_kvotasi.html', {'kvota': kvota})
