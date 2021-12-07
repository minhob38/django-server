from django.urls import path
from map.views import MapView

urlpatterns = [
    path("sggs/", MapView.as_view())
]
