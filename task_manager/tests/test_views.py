from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Task, TaskType


Worker = get_user_model()


class ViewTestMixin:
    def create_test_data(self):
        self.position = Position.objects.create(
            name="Developer"
        )

        self.task_type = TaskType.objects.create(
            name="Bug"
        )

        self.worker = Worker.objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Smith",
            position=self.position,
        )

        self.other_worker = Worker.objects.create_user(
            username="mike",
            password="test12345",
        )

        self.task = Task.objects.create(
            name="Fix login",
            description="Fix login problem",
            deadline=date.today(),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
        )

        self.task.assignees.add(self.worker)


class IndexViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_index_view(self):
        response = self.client.get(
            reverse("task_manager:index")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_workers"], 2)
        self.assertEqual(response.context["num_positions"], 1)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_task_types"], 1)


class LoginViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()

    def test_login_page(self):
        response = self.client.get(
            reverse("task_manager:login")
        )

        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(
            reverse("task_manager:login"),
            {
                "username": "john",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Invalid username and/or password.",
        )


class PositionListViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_position_list(self):
        response = self.client.get(
            reverse("task_manager:position-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Developer")

    def test_position_search(self):
        Position.objects.create(name="Tester")

        response = self.client.get(
            reverse("task_manager:position-list"),
            {"name": "Dev"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Developer")
        self.assertNotContains(response, "Tester")


class PositionCreateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_position_create(self):
        response = self.client.post(
            reverse("task_manager:position-create"),
            {
                "name": "Tester",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Position.objects.filter(name="Tester").exists()
        )


class PositionUpdateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_position_update(self):
        response = self.client.post(
            reverse(
                "task_manager:position-update",
                args=[self.position.pk],
            ),
            {
                "name": "Senior Developer",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.position.refresh_from_db()

        self.assertEqual(
            self.position.name,
            "Senior Developer",
        )


class PositionDeleteViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_position_delete(self):
        # Position has CASCADE relation to Worker.
        # Therefore create a separate position without workers.
        position = Position.objects.create(name="Tester")

        response = self.client.post(
            reverse(
                "task_manager:position-delete",
                args=[position.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Position.objects.filter(pk=position.pk).exists()
        )


class WorkerListViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_worker_list(self):
        response = self.client.get(
            reverse("task_manager:worker-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")

    def test_worker_search(self):
        response = self.client.get(
            reverse("task_manager:worker-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")


class WorkerCreateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_worker_create(self):
        response = self.client.post(
            reverse("task_manager:worker-create"),
            {
                "username": "alice",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "first_name": "Alice",
                "last_name": "Brown",
                "email": "alice@example.com",
                "position": self.position.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Worker.objects.filter(username="alice").exists()
        )


class WorkerUpdateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_worker_update(self):
        response = self.client.post(
            reverse(
                "task_manager:worker-update",
                args=[self.worker.pk],
            ),
            {
                "first_name": "Johnny",
                "last_name": "Smith",
                "email": "john@example.com",
                "position": self.position.pk,
            },
        )

        self.assertEqual(response.status_code, 302)

        self.worker.refresh_from_db()

        self.assertEqual(
            self.worker.first_name,
            "Johnny",
        )


class WorkerDeleteViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_worker_delete(self):
        worker = Worker.objects.create_user(
            username="delete_me",
            password="test12345",
        )

        response = self.client.post(
            reverse(
                "task_manager:worker-delete",
                args=[worker.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Worker.objects.filter(pk=worker.pk).exists()
        )


class TaskListViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_list(self):
        response = self.client.get(
            reverse("task_manager:task-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login")

    def test_task_search(self):
        Task.objects.create(
            name="Implement registration",
            deadline=date.today(),
            task_type=self.task_type,
        )

        response = self.client.get(
            reverse("task_manager:task-list"),
            {"name": "login"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login")
        self.assertNotContains(
            response,
            "Implement registration",
        )

    def test_my_not_completed_tasks(self):
        self.task.is_completed = False
        self.task.save()

        response = self.client.get(
            reverse("task_manager:task-list"),
            {"not_completed": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login")

    def test_my_completed_tasks(self):
        self.task.is_completed = True
        self.task.save()

        response = self.client.get(
            reverse("task_manager:task-list"),
            {"completed": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login")

    def test_other_worker_task_not_in_my_completed_tasks(self):
        self.task.assignees.clear()
        self.task.assignees.add(self.other_worker)
        self.task.is_completed = True
        self.task.save()

        response = self.client.get(
            reverse("task_manager:task-list"),
            {"completed": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Fix login")


class CompleteTaskViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_complete_task(self):
        self.assertFalse(self.task.is_completed)

        response = self.client.get(
            reverse(
                "task_manager:complete-task",
                args=[self.task.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertTrue(self.task.is_completed)

    def test_uncomplete_task(self):
        self.task.is_completed = True
        self.task.save()

        response = self.client.get(
            reverse(
                "task_manager:complete-task",
                args=[self.task.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertFalse(self.task.is_completed)


class TaskCreateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_create(self):
        response = self.client.post(
            reverse("task_manager:task-create"),
            {
                "name": "New task",
                "description": "Some description",
                "deadline": date.today(),
                "is_completed": False,
                "priority": "HIGH",
                "task_type": self.task_type.pk,
                "assignees": [self.worker.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.filter(name="New task").exists()
        )


class TaskUpdateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_update(self):
        response = self.client.post(
            reverse(
                "task_manager:task-update",
                args=[self.task.pk],
            ),
            {
                "name": "Updated task",
                "description": "Updated description",
                "deadline": date.today(),
                "is_completed": False,
                "priority": "HIGH",
                "task_type": self.task_type.pk,
                "assignees": [self.worker.pk],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.name,
            "Updated task",
        )
        self.assertEqual(
            self.task.priority,
            Task.Priority.HIGH,
        )


class TaskDeleteViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_delete(self):
        response = self.client.post(
            reverse(
                "task_manager:task-delete",
                args=[self.task.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Task.objects.filter(pk=self.task.pk).exists()
        )


class TaskTypeListViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_type_list(self):
        response = self.client.get(
            reverse("task_manager:task-type-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_task_type_search(self):
        TaskType.objects.create(name="Feature")

        response = self.client.get(
            reverse("task_manager:task-type-list"),
            {"name": "Bug"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")
        self.assertNotContains(response, "Feature")


class TaskTypeCreateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_type_create(self):
        response = self.client.post(
            reverse("task_manager:task-type-create"),
            {
                "name": "Feature",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            TaskType.objects.filter(name="Feature").exists()
        )


class TaskTypeUpdateViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_type_update(self):
        response = self.client.post(
            reverse(
                "task_manager:task-type-update",
                args=[self.task_type.pk],
            ),
            {
                "name": "Feature",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.task_type.refresh_from_db()

        self.assertEqual(
            self.task_type.name,
            "Feature",
        )


class TaskTypeDeleteViewTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()
        self.client.force_login(self.worker)

    def test_task_type_delete(self):
        task_type = TaskType.objects.create(
            name="Temporary"
        )

        response = self.client.post(
            reverse(
                "task_manager:task-type-delete",
                args=[task_type.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            TaskType.objects.filter(pk=task_type.pk).exists()
        )


class AuthenticationTests(ViewTestMixin, TestCase):
    def setUp(self):
        self.create_test_data()

    def test_anonymous_user_redirected_from_protected_view(self):
        response = self.client.get(
            reverse("task_manager:task-list")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("login"),
            response.url,
        )