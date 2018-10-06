from django.shortcuts import render

def trader(request):
    return render(request, 'trader/index.html')