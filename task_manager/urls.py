from django.urls import path

from .views import (
    index,
    PositionListView,
    WorkerListView,
    TaskListView,
    TaskTypesListView,
    WorkerCreateView,
    PositionCreateView,
    TaskCreateView
)

app_name = 'task_manager'

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("task-types/", TaskTypesListView.as_view(), name="task-types-list"),
]
