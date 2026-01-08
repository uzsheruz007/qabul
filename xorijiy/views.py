from django.shortcuts import render
from .forms import ForeignStudentRequestForm
from .models import  Bakalaver, Magistratura, Shartnomalar, Kontrakt

def foreign_student_request(request):
    if request.method == "POST":
        form = ForeignStudentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = ForeignStudentRequestForm()

    return render(request, 'request.html', {'form': form})


def bakalaver(request):
    kvota = Bakalaver.objects.last()
    return render(request, 'bakalaver.html', {'kvota': kvota})


def magistr(request):
    kvota = Magistratura.objects.last()
    return render(request, 'magistratura.html', {'kvota': kvota})



def shartnoma(request):
    kvota = Shartnomalar.objects.last()
    return render(request, 'shartnoma.html', {'kvota': kvota})




def kontrakt(request):
    kvota = Kontrakt.objects.last()
    return render(request, 'kontrakt.html', {'kvota': kvota})