from django.urls import path

from .views import index, PositionListView, WorkerListView, TaskListView, TaskTypesListView, WorkerCreateView


app_name = 'task_manager'

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task-types/", TaskTypesListView.as_view(), name="task-types-list"),
]