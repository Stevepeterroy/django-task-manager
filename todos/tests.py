from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TaskAccessTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owner", password="local-test-only")
        self.other = get_user_model().objects.create_user(username="other", password="local-test-only")
        self.task = Todo.objects.create(user=self.owner, title="Private task")

    def test_anonymous_user_must_sign_in(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 302)

    def test_another_user_cannot_read_or_mutate_task(self):
        self.client.force_login(self.other)
        for name in ["todo_detail", "todo_delete", "todo_toggle_complete"]:
            response = self.client.post(reverse(name, args=[self.task.pk]))
            self.assertEqual(response.status_code, 404)
        self.assertTrue(Todo.objects.filter(pk=self.task.pk).exists())
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)

    def test_toggle_requires_post(self):
        self.client.force_login(self.owner)
        url = reverse("todo_toggle_complete", args=[self.task.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_task_list_excludes_other_users(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Private task")
