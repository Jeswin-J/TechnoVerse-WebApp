from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')

def course_info(request, name):
    context = {
        'name' : name,
    }
    return render(request, 'course_info.html', context)
