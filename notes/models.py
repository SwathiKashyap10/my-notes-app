from django.db import models

PRIORITY_CHOICES = [
    ('L', 'Low'),
    ('M', 'Medium'),
    ('H', 'High'),
]

class Note(models.Model):
    heading = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    created_at = models.DateTimeField(auto_now_add=True)
    task_date = models.DateField(null=True, blank=True)  # New field adde

    def __str__(self):
        return f"{self.heading} ({self.get_priority_display()})"
