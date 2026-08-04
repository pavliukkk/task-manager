from django.contrib import admin
from .models import Worker, Task, TaskType, Position


admin.site.register(Worker)
admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Position)
