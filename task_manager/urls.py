from django.urls import path

from .views import index, PositionListView


app_name = 'task_manager'

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
]