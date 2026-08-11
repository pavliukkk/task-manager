from datetime import date, timedelta

from django.test import TestCase

from task_manager.forms import (
    WorkerCreateForm,
    WorkerUpdateForm,
    PositionForm,
    TaskForm,
    TaskTypeForm,
    PositionNameSearchForm,
    TaskNameSearchForm,
    TaskTypeNameSearchForm,
    WorkerUsernameSearchForm,
    MyNotCompletedTasksSearchForm,
    MyCompletedTasksSearchForm,
)
from task_manager.models import Position, TaskType, Worker


class WorkerCreateFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_create_form_valid(self):
        form = WorkerCreateForm(
            data={
                "username": "john",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "first_name": "John",
                "last_name": "Smith",
                "email": "john@example.com",
                "position": self.position.id,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_worker_first_name_cannot_contain_digits(self):
        form = WorkerCreateForm(
            data={
                "username": "john",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "first_name": "John123",
                "last_name": "Smith",
                "email": "john@example.com",
                "position": self.position.id,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_worker_last_name_cannot_contain_digits(self):
        form = WorkerCreateForm(
            data={
                "username": "john",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "first_name": "John",
                "last_name": "Smith123",
                "email": "john@example.com",
                "position": self.position.id,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)


class WorkerUpdateFormTests(TestCase):
    def test_worker_update_form_valid(self):
        form = WorkerUpdateForm(
            data={
                "first_name": "John",
                "last_name": "Smith",
                "email": "john@example.com",
                "position": "",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_worker_update_form_invalid_first_name(self):
        form = WorkerUpdateForm(
            data={
                "first_name": "John123",
                "last_name": "Smith",
                "email": "john@example.com",
                "position": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)


class PositionFormTests(TestCase):
    def test_position_form_valid(self):
        form = PositionForm(
            data={
                "name": "Developer",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_position_form_invalid_name(self):
        form = PositionForm(
            data={
                "name": "Developer123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskTypeFormTests(TestCase):
    def test_task_type_form_valid(self):
        form = TaskTypeForm(
            data={
                "name": "Bug",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_task_type_form_invalid_name(self):
        form = TaskTypeForm(
            data={
                "name": "Bug123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = Worker.objects.create_user(
            username="john",
            password="test12345",
        )

    def get_valid_data(self, deadline=None):
        if deadline is None:
            deadline = date.today()

        return {
            "name": "Fix bug",
            "description": "Fix login bug",
            "deadline": deadline,
            "is_completed": False,
            "priority": "MEDIUM",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }

    def test_task_form_valid(self):
        form = TaskForm(data=self.get_valid_data())

        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_rejects_past_deadline(self):
        yesterday = date.today() - timedelta(days=1)

        form = TaskForm(
            data=self.get_valid_data(deadline=yesterday)
        )

        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_task_form_accepts_today_deadline(self):
        form = TaskForm(
            data=self.get_valid_data(deadline=date.today())
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_accepts_future_deadline(self):
        future_date = date.today() + timedelta(days=10)

        form = TaskForm(
            data=self.get_valid_data(deadline=future_date)
        )

        self.assertTrue(form.is_valid(), form.errors)


class SearchFormsTests(TestCase):
    def test_position_search_form_valid(self):
        form = PositionNameSearchForm(
            data={"name": "Developer"}
        )

        self.assertTrue(form.is_valid())

    def test_task_search_form_valid(self):
        form = TaskNameSearchForm(
            data={"name": "Fix bug"}
        )

        self.assertTrue(form.is_valid())

    def test_task_type_search_form_valid(self):
        form = TaskTypeNameSearchForm(
            data={"name": "Bug"}
        )

        self.assertTrue(form.is_valid())

    def test_worker_search_form_valid(self):
        form = WorkerUsernameSearchForm(
            data={"username": "john"}
        )

        self.assertTrue(form.is_valid())

    def test_not_completed_tasks_form(self):
        form = MyNotCompletedTasksSearchForm(
            data={"not_completed": "1"}
        )

        self.assertTrue(form.is_valid())

    def test_completed_tasks_form(self):
        form = MyCompletedTasksSearchForm(
            data={"completed": "1"}
        )

        self.assertTrue(form.is_valid())
