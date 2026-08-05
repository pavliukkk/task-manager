from django.shortcuts import render

from task_manager.models import Worker, Position, Task, TaskType


# Create your views here.
def index(request):
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    context = {
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
    }
    return render(request, "task_manager/index.html", context=context)