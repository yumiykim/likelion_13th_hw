from django.shortcuts import render

# Create your views here.

def mainpage(request):
    return render(request, 'main/mainpage.html')

def secondpage(request):
    context = {
        'info' : {'name': 'Yumi Kim', 'major': 'Industrial Systems Engineering & Data Science Software', 'track' : 'BE'}
    }
    return render(request, 'main/secondpage.html', context)
    