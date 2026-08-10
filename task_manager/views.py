from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from task_manager.forms import WorkerCreateForm, TaskForm, WorkerUpdateForm, PositionNameSearchForm, TaskNameSearchForm, \
    TaskTypeNameSearchForm, WorkerUsernameSearchForm, MyNotCompletedTasksSearchForm, MyCompletedTasksSearchForm
from task_manager.models import Worker, Position, Task, TaskType


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


def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.is_completed = not task.is_completed
    task.save()

    return redirect("task_manager:task-list")


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

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        queryset = Position.objects.all()
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerUsernameSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        username = self.request.GET.get("username", "")
        queryset = Worker.objects.all()
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        context["not_completed_tasks_form"] = MyNotCompletedTasksSearchForm()
        context["completed_tasks_form"] = MyCompletedTasksSearchForm()
        return context

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        not_completed = self.request.GET.get("not_completed", "")
        completed = self.request.GET.get("completed")
        user = self.request.user.username

        queryset = Task.objects.prefetch_related("assignees")
        if name:
            return queryset.filter(name__icontains=name)
        if not_completed:
            return queryset.filter(is_completed=False, assignees__username=user)
        if completed:
            return queryset.filter(is_completed=True, assignees__username=user)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        queryset = TaskType.objects.all()
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
