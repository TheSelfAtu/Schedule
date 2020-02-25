import datetime
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.
from . import mixins
from .forms import BS4ScheduleForm
from .models import Schedule 

class MyCalendar(mixins.MonthWithScheduleMixin,  generic.CreateView):
  
    template_name = 'Home/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):          
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day :
               day_aim=Schedule.objects.filter(date=datetime.date(year,month,day), owner=self.request.user).order_by('end_time')
        else:
               day_aim=Schedule.objects.filter(date=datetime.date.today(), owner=self.request.user).order_by('end_time')
        context = super().get_context_data(**kwargs)
        context['day_aim'] = day_aim 
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.owner = self.request.user
        schedule.save()
        return redirect('Home:mycalendar', year=date.year, month=date.month, day=date.day)
