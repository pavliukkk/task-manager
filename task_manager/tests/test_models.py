from datetime import date

from django.test import TestCase

from task_manager.models import TaskType, Position, Worker, Task


class TaskTypeModelTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug")

        self.assertEqual(str(task_type), "Bug")

    def test_task_type_ordering(self):
        TaskType.objects.create(name="Development")
        TaskType.objects.create(name="Bug")
        TaskType.objects.create(name="Testing")

        task_types = list(TaskType.objects.all())

        self.assertEqual(
            [task_type.name for task_type in task_types],
            ["Bug", "Development", "Testing"],
        )


class PositionModelTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Developer")

        self.assertEqual(str(position), "Developer")

    def test_position_ordering(self):
        Position.objects.create(name="Tester")
        Position.objects.create(name="Developer")
        Position.objects.create(name="Manager")

        positions = list(Position.objects.all())

        self.assertEqual(
            [position.name for position in positions],
            ["Developer", "Manager", "Tester"],
        )


class WorkerModelTests(TestCase):
    def test_worker_str(self):
        position = Position.objects.create(name="Developer")

        worker = Worker.objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Smith",
            position=position,
        )

        self.assertEqual(
            str(worker),
            "john: John Smith (Developer)",
        )

    def test_worker_can_have_no_position(self):
        worker = Worker.objects.create_user(
            username="john",
            password="test12345",
        )

        self.assertIsNone(worker.position)


class TaskModelTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_str(self):
        task = Task.objects.create(
            name="Fix login bug",
            description="Fix login problem",
            deadline=date.today(),
            task_type=self.task_type,
        )

        self.assertEqual(str(task), "Fix login bug")

    def test_task_default_values(self):
        task = Task.objects.create(
            name="New task",
            deadline=date.today(),
            task_type=self.task_type,
        )

        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_ordering(self):
        Task.objects.create(
            name="Task 2",
            deadline=date(2026, 8, 20),
            task_type=self.task_type,
        )

        Task.objects.create(
            name="Task 1",
            deadline=date(2026, 8, 10),
            task_type=self.task_type,
        )

        tasks = list(Task.objects.all())

        self.assertEqual(
            [task.name for task in tasks],
            ["Task 1", "Task 2"],
        )

    def test_task_assignees(self):
        position = Position.objects.create(name="Developer")

        worker = Worker.objects.create_user(
            username="john",
            password="test12345",
            position=position,
        )

        task = Task.objects.create(
            name="Fix bug",
            deadline=date.today(),
            task_type=self.task_type,
        )

        task.assignees.add(worker)

        self.assertIn(worker, task.assignees.all())
        self.assertIn(task, worker.assigned_tasks.all())