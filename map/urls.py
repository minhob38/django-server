from django.urls import path
from map.views import MapView

urlpatterns = [
    path("features/", MapView.as_view())
    # path("features?/", views.signup)
]
