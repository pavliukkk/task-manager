from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

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

def login_view(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return reverse("task_manager:index")

    return render(
        request,
        "accounts/login.html",
        {"error": "Invalid username and/or password."},
    )


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "task_manager/position_list.html"
    paginate_by = 5


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    paginate_by = 5