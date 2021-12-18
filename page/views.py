from django.shortcuts import render
from django.views import View
from datetime import datetime


class HomeView(View):
    def get(self, request):
        current_datetime = datetime.now()
        cur_year = current_datetime.year
        cur_month = current_datetime.month
        cur_day = current_datetime.day
        cur_hour = current_datetime.hour
        cur_minute = current_datetime.minute
        cur_second = current_datetime.second

        context = {
            "current_date_time": {
                "year": cur_year,
                "month": cur_month,
                "day": cur_day,
                "hour": cur_hour,
                "minute": cur_minute,
                "second": cur_second,
            }
        }

        return render(request, "home/home.html", context)
