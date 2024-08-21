from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import App, TestRun
from .forms import UserRegistrationForm


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.app = App.objects.create(
            name="Test App", apk_file_path="apks/", uploaded_by=self.user
        )

    def test_register_view(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_list"))

    def test_app_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("app_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_list.html")

    def test_app_detail_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("app_detail", args=[self.app.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_detail.html")

    def test_app_upload_view(self):
        self.client.login(username="testuser", password="testpass")
        with open("apks/test.apk", "rb") as apk_file:
            response = self.client.post(
                reverse("app_upload"),
                {
                    "name": "Test App",
                    "apk_file_path": apk_file,
                },
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_list"))

    def test_app_delete_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("app_delete", args=[self.app.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_list"))
        self.assertFalse(App.objects.filter(id=self.app.id).exists())

    def test_run_test_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("run_test", args=[self.app.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_detail", args=[self.app.id]))
