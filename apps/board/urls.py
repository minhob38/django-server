from django.urls import path
from .views import BoardView, PostView

urlpatterns = [
    path("posts/", BoardView.as_view()),
    path("posts/<int:post_id>/", PostView.as_view()),
]
