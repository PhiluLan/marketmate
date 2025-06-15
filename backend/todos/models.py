from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ToDo(models.Model):
    # Jeder ToDo gehört zu einem User
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todos"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({'✔' if self.is_completed else '✘'})"
