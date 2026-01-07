from django.shortcuts import render
from .models import TeamMember





def about(request):
    about = TeamMember.objects.all()
    
    return render(request, 'about.html', {'about': about})



from django.shortcuts import render
from .models import QabulJadvali

def qabul_kunlari(request):
    qabul_list = QabulJadvali.objects.all()
    return render(request, 'qabul.html', {'qabul_list': qabul_list})



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q, Count
from .models import  Document, ImportantNote, AdmissionRule, Deadline
import os

class RegulatoryDocumentsView(TemplateView):
    template_name = 'meyor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
     
        # Barcha hujjatlar
        context['documents'] = Document.objects.filter(is_active=True).order_by('order')
        
        # Muhim eslatmalar
        context['important_notes'] = ImportantNote.objects.filter(is_active=True).order_by('order')
        
        # Qabul qoidalari
        context['bachelor_rules'] = AdmissionRule.objects.filter(
            rule_type='bakalavr',
            is_active=True
        ).order_by('order')

        context['master_rules'] = AdmissionRule.objects.filter(
            rule_type='magistr',
            is_active=True
        ).order_by('order')

        context['steps'] = AdmissionRule.objects.filter(
            rule_type='step',
            is_active=True
        ).order_by('order')

        
        # Joriy muddat
        context['current_deadline'] = Deadline.objects.filter(is_active=True).first()
        
        return context

class DocumentListView(ListView):
    model = Document
    template_name = 'meyor.html'
    context_object_name = 'documents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_active=True).order_by('order')
        
        # Filtr by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Qidiruv
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    

class DocumentDetailView(DetailView):
    model = Document
    template_name = 'meyor.html'
    context_object_name = 'document'
    
    def get_object(self):
        obj = super().get_object()
        # Ko'rishlar sonini oshirish
        obj.view_count += 1
        obj.save()
        return obj

def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk, is_active=True)
    
    # Yuklab olishlar sonini oshirish
    document.download_count += 1
    document.save()
    
    # Faylni yuklab olish uchun yuborish
    response = FileResponse(document.file.open('rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{document.name}.{document.get_file_extension()}"'
    
    return response

def view_document(request, pk):
    document = get_object_or_404(Document, pk=pk, is_active=True)
    
    # Ko'rishlar sonini oshirish
    document.view_count += 1
    document.save()
    
    # Faylni ko'rsatish (PDF uchun)
    if document.file_format == 'PDF':
        response = FileResponse(document.file.open('rb'))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = f'inline; filename="{document.name}.pdf"'
        return response
    else:
        # Boshqa formatlar uchun yuklab olish sahifasiga yo'naltirish
        return download_document(request, pk)

def get_documents_by_category(request):
    category_id = request.GET.get('category_id')
    
    if category_id:
        documents = Document.objects.filter(category_id=category_id, is_active=True).order_by('order')
    else:
        documents = Document.objects.filter(is_active=True).order_by('order')
    
    data = []
    for doc in documents:
        data.append({
            'id': doc.id,
            'name': doc.name,
            'description': doc.description,
            'format': doc.file_format,
            'size': doc.file_size,
            'download_count': doc.download_count,
            'download_url': doc.get_download_url(),
        })
    
    return JsonResponse({'documents': data})

def increment_download_count(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
        try:
            document = Document.objects.get(id=doc_id)
            document.download_count += 1
            document.save()
            return JsonResponse({'success': True, 'download_count': document.download_count})
        except Document.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Document not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_admission_info(request):
    # Bakalavriat qoidalari
    bachelor_rules = AdmissionRule.objects.filter(
        rule_type='bakalavr', is_active=True
    ).order_by('order')
    
    # Magistratura qoidalari
    master_rules = AdmissionRule.objects.filter(
        rule_type='magistr', is_active=True
    ).order_by('order')
    
    # Bosqichlar
    steps = AdmissionRule.objects.filter(
        rule_type='step', is_active=True
    ).order_by('order')
    
    data = {
        'bachelor': [{'title': r.title, 'content': r.content, 'icon': r.icon} for r in bachelor_rules],
        'master': [{'title': r.title, 'content': r.content, 'icon': r.icon} for r in master_rules],
        'steps': [{'title': r.title, 'content': r.content, 'order': r.order} for r in steps],
    }
    
    return JsonResponse(data)