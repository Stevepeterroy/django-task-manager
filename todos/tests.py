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

class TaskWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="workflow")
        self.client.force_login(self.user)
    def test_priority_order(self):
        from datetime import date
        for priority in ["low", "high", "medium"]:
            Todo.objects.create(user=self.user, title=priority, priority=priority)
        Todo.objects.create(user=self.user, title="done", priority="high", completed=True)
        response = self.client.get(reverse("todo_list"))
        self.assertEqual([t.title for t in response.context["todos"]], ["high","medium","low","done"])
    def test_create_edit_delete_and_invalid_input(self):
        response=self.client.post(reverse("todo_create"), {"title":"", "priority":"invalid"})
        self.assertEqual(response.status_code,200)
        self.assertEqual(Todo.objects.count(),0)
        self.assertEqual(self.client.post(reverse("todo_create"), {"title":"First", "priority":"high"}).status_code,302)
        task=Todo.objects.get()
        self.assertEqual(task.user,self.user)
        self.assertEqual(self.client.post(reverse("todo_detail",args=[task.pk]), {"title":"Updated", "priority":"low"}).status_code,302)
        task.refresh_from_db(); self.assertEqual(task.title,"Updated")
        self.assertEqual(self.client.get(reverse("todo_delete",args=[task.pk])).status_code,200)
        self.assertTrue(Todo.objects.filter(pk=task.pk).exists())
        self.client.post(reverse("todo_delete",args=[task.pk]))
        self.assertFalse(Todo.objects.exists())
