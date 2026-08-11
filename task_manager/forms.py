import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms

from task_manager.models import Worker, Task, Position, TaskType


class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "position",)

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("First name must have only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("First name must have only letters")
        return last_name


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("first_name", "last_name", "email", "position",)

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("First name must have only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("First name must have only letters")
        return last_name


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not all(char.isalpha() or char.isspace() for char in name):
            raise forms.ValidationError("Position name must have only letters")
        return name


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        today = datetime.date.today()
        if deadline < today:
            raise forms.ValidationError(f"Ensure that value is >={today}")
        return deadline


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not all(char.isalpha() or char.isspace() for char in name):
            raise forms.ValidationError("Task type name must have only letters")
        return name


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class MyNotCompletedTasksSearchForm(forms.Form):
    not_completed = forms.CharField(widget=forms.HiddenInput(), required=False, initial=True)


class MyCompletedTasksSearchForm(forms.Form):
    completed = forms.CharField(widget=forms.HiddenInput(), required=False, initial=True)


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )
