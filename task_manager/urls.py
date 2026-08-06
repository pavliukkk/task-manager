from django.urls import path

from .views import index, PositionListView, WorkerListView, TaskListView


app_name = 'task_manager'

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]