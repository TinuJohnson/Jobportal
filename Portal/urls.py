# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Jobs
    path("jobs/", views.job_list, name="job_list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("jobs/post/", views.post_job, name="post_job"),
    path("jobs/manage/", views.manage_jobs, name="manage_jobs"),
    # Applications
    path("jobs/<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path(
        "jobs/<int:job_id>/applications/",
        views.view_applications,
        name="view_applications",
    ),
]
