# urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("jobs/", views.job_list, name="job_list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("jobs/<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path(
        "jobs/<int:job_id>/applications/",
        views.view_applications,
        name="view_applications",
    ),
    path("manage-jobs/", views.manage_jobs, name="manage_jobs"),
    path("post-job/", views.post_job, name="post_job"),
    path("edit-job/<int:job_id>/", views.edit_job, name="edit_job"),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete_job"),
    path(
        "view-applications/<int:job_id>/",
        views.view_applicants,
        name="view_applications",
    ),
    path(
        "application/<int:application_id>/update-status/<str:status>/",
        views.update_application_status,
        name="update_application_status",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
