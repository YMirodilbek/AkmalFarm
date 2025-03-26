from django.shortcuts import render

# Create your views here.


def Operator(request):
    return render(request,'operator.html')


def Vacancy(request):
    return render(request,'vacancy.html')


def Pharm(request):
    return render(request,'farmaset.html')