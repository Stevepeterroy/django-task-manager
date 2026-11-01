from django.db import models
from django.contrib.auth.models import User

class TodoQuerySet(models.QuerySet):
    def by_priority(self):
        return self.order_by("completed", models.Case(
            models.When(priority="high", then=models.Value(0)),
            models.When(priority="medium", then=models.Value(1)),
            default=models.Value(2), output_field=models.IntegerField()),
            models.F("due_date").asc(nulls_last=True), "pk")

class Todo(models.Model):
    objects = TodoQuerySet.as_manager()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')

    class Meta:
        ordering = ['completed', '-priority', 'due_date']

    def __str__(self):
        return self.title
