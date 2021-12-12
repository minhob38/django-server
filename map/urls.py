from django.urls import path
from map.views import SggView, SggDetailView, SggBoundView, SggAreaView

urlpatterns = [
    path("sggs", SggBoundView.as_view()),
    path("sggs/", SggView.as_view()),
    path("sggs/areas/", SggAreaView.as_view()),
    path("sggs/<sgg_nm>/", SggDetailView.as_view()),
]
