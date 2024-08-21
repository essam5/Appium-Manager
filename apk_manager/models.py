# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class App(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file_path = models.FileField(upload_to="apks/")
    first_screen_screenshot_path = models.ImageField(upload_to="screenshots/")
    second_screen_screenshot_path = models.ImageField(upload_to="screenshots/")
    video_recording_path = models.FileField(upload_to="videos/")
    ui_hierarchy = models.TextField()
    screen_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestRun(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="test_runs")
    run_date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)
    logs_path = models.FileField(upload_to="logs/")

    def __str__(self):
        return f"Test Run for {self.app.name} on {self.run_date}"
