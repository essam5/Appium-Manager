from django.urls import path
from . import views

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
    path("app_list", views.app_list, name="app_list"),
    path("app/<int:app_id>/", views.app_detail, name="app_detail"),
    path("upload/", views.app_upload, name="app_upload"),
    path("app/<int:app_id>/update/", views.app_update, name="app_update"),
    path("app/<int:app_id>/delete/", views.app_delete, name="app_delete"),
    path("app/<int:app_id>/run_test/", views.run_test, name="run_test"),
    path(
        "toggle_high_contrast/", views.toggle_high_contrast, name="toggle_high_contrast"
    ),
    path("increase_font_size/", views.increase_font_size, name="increase_font_size"),
    path("decrease_font_size/", views.decrease_font_size, name="decrease_font_size"),
    path("set_language/<str:language_code>/", views.set_language, name="set_language"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
