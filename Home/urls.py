from django.urls import include, path
from django.views.generic import TemplateView
from . import views


app_name = 'Home'

urlpatterns = [
        path('', views.MyCalendar.as_view(), name='mycalendar'),
        path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),
]
