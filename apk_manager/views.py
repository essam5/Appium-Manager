import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import App, TestRun
from .forms import UserRegistrationForm, AppForm
from .appium_test import run_appium_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect


# User registration view
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            login(request, user)
            return redirect("app_list")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


@login_required
def app_list(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, "app_list.html", {"apps": apps})


@login_required
def app_detail(request, app_id):
    app = get_object_or_404(App, pk=app_id, uploaded_by=request.user)
    test_runs = TestRun.objects.filter(app=app)
    return render(request, "app_detail.html", {"app": app, "test_runs": test_runs})


@login_required
def app_upload(request):
    if request.method == "POST":
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()
            messages.success(request, _("App uploaded successfully!"))
            return redirect("app_list")
        else:
            messages.error(
                request, _("Failed to upload app. Please correct the errors below.")
            )
    else:
        form = AppForm()

    return render(request, "app_form.html", {"form": form})


@login_required
def app_update(request, app_id):
    app = get_object_or_404(App, pk=app_id, uploaded_by=request.user)

    if request.method == "POST":
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, _("App updated successfully!"))
            return redirect("app_detail", app_id=app.id)
        else:
            messages.error(
                request, _("Failed to update app. Please correct the errors below.")
            )
    else:
        form = AppForm(instance=app)

    return render(request, "app_form.html", {"form": form, "app": app})


@login_required
def app_delete(request, app_id):
    app = get_object_or_404(App, pk=app_id, uploaded_by=request.user)
    if request.method == "POST":
        app.delete()
        messages.success(request, _("App deleted successfully!"))
        return redirect("app_list")

    return render(request, "app_confirm_delete.html", {"app": app})


@login_required
def run_test(request, app_id):
    app = get_object_or_404(App, pk=app_id, uploaded_by=request.user)

    # Define paths for screenshots, video, and logs
    first_screenshot_path = os.path.join(
        settings.MEDIA_ROOT, "screenshots", f"{app.id}_first.png"
    )
    second_screenshot_path = os.path.join(
        settings.MEDIA_ROOT, "screenshots", f"{app.id}_second.png"
    )
    video_path = os.path.join(settings.MEDIA_ROOT, "videos", f"{app.id}.mp4")
    logs_path = os.path.join(settings.MEDIA_ROOT, "logs", f"{app.id}.log")

    try:
        # Call the Appium script and run the test
        ui_hierarchy, screen_changed = run_appium_test(
            apk_path=app.apk_file_path.path,
            first_screenshot_path=first_screenshot_path,
            second_screenshot_path=second_screenshot_path,
            video_path=video_path,
        )

        # Update the app model with test results
        app.first_screen_screenshot_path = first_screenshot_path
        app.second_screen_screenshot_path = second_screenshot_path
        app.video_recording_path = video_path
        app.ui_hierarchy = ui_hierarchy
        app.screen_changed = screen_changed
        app.save()

        TestRun.objects.create(
            app=app,
            result="Success",
            logs_path=logs_path,
        )

        messages.success(request, _("Test completed successfully!"))

    except Exception as e:
        TestRun.objects.create(
            app=app,
            result="Failed",
            logs_path=logs_path,
        )
        messages.error(request, _("Test failed: %s") % str(e))

    return redirect("app_detail", app_id=app.id)


@login_required
def toggle_high_contrast(request):
    if "high_contrast" in request.session:
        del request.session["high_contrast"]
    else:
        request.session["high_contrast"] = True
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def increase_font_size(request):
    request.session["font_size"] = "large"
    print("font_sizewwwwwwww")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def decrease_font_size(request):
    request.session["font_size"] = "small"
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def set_language(request, language_code):
    from django.utils import translation

    translation.activate(language_code)
    request.session["django_language"] = language_code  # Store the language in session

    # Reload the current page
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class CustomLoginView(LoginView):
    template_name = "login.html"


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
