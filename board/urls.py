from django.urls import path
from board.views import BoardView

urlpatterns = [
    path("posts/", BoardView.as_view())
]
