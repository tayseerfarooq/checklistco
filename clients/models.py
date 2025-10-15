from django.db import models
from django.contrib.auth.hashers import make_password

# class Client(models.Model):
#     reference_id = models.CharField(max_length=20, unique=True)  # Example: CHK123
#     name = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     password = models.CharField(max_length=255)  # stored hashed
#     active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         # Ensure password is hashed before saving
#         if not self.password.startswith("pbkdf2_"):
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.reference_id} - {self.name}"


# class Service(models.Model):
#     STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#     ]

#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='services')
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} ({self.client.reference_id})"


# class TimelineTask(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('done', 'Done'),
#     ]

#     service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='timeline_tasks')
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     due_date = models.DateField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     completed_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.title} - {self.service.title}"

#     @property
#     def is_completed(self):
#         return self.status == 'done'





class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    reference_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)   # ✅ add this line
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Service(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='In Progress')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def progress_percent(self):
        total = self.timeline_tasks.count()
        done = self.timeline_tasks.filter(completed=True).count()
        return int((done / total) * 100) if total > 0 else 0

    def __str__(self):
        return f"{self.title} ({self.client.name})"


class TimelineTask(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='timeline_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

# clients/models.py  (append this code)

import secrets
from django.utils import timezone

class ClientToken(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='tokens')
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            # generate a random hex token
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token {self.key[:8]}... for {self.client.reference_id}"