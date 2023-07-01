from Application import views
from django.urls import path

urlpatterns = [
    path('', views.index, name ='index'),
    path('course_info/<name>', views.course_info, name = 'course_info'),
]
