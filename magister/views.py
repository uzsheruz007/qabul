from django.shortcuts import render
from .models import QabulRijasi, MagistraturaNatijalari

# Create your views here.

def hujjatlar_t(request):
    return render(request, 'hujjatlar_tuplami.html' )



def Qabul_Rijasi(request):
    kvota = QabulRijasi.objects.last()
    return render(request, 'qabul_rejasi.html', {'kvota': kvota})



def Magistratura_Natijalari(request):
    kvota = MagistraturaNatijalari.objects.last()
    return render(request, 'natijalarM.html', {'kvota': kvota})