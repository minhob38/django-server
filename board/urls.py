from django.urls import path
from map.views import MapView

urlpatterns = [
    path("posts/", MapView.as_view())
]
