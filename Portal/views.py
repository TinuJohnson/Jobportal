# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User, Job, Application
from .forms import JobForm, ApplicationForm, UserRegistrationForm


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    if request.user.is_seeker():
        applications = Application.objects.filter(seeker=request.user)
        return render(
            request, "seeker/dashboard_seeker.html", {"applications": applications}
        )
    else:
        jobs = Job.objects.filter(employer=request.user)
        return render(request, "employer/dashboard_employer.html", {"jobs": jobs})


@login_required
@user_passes_test(lambda u: u.is_employer())
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("dashboard")
    else:
        form = JobForm()
    return render(request, "employer/post_job.html", {"form": form})


@login_required
def manage_jobs(request):
    # Only show jobs posted by the current user
    jobs = Job.objects.filter(employer=request.user).order_by("-created_at")
    return render(request, "employer/manage_jobs.html", {"jobs": jobs})


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = Application.objects.filter(job=job).select_related("seeker")

    return render(
        request,
        "employer/view_applicants.html",
        {"job": job, "applications": applications},
    )


@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)

    # Ensure the current user owns the job
    if application.job.employer != request.user:
        raise Http404("Application not found")

    valid_statuses = ["pending", "reviewed", "shortlisted", "accepted", "rejected"]
    if status in valid_statuses:
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}.")
    else:
        messages.error(request, "Invalid status.")

    return redirect("seeker/view_applications", job_id=application.job.id)


@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)

    # Ensure the current user owns the job
    if application.job.employer != request.user:
        raise Http404("Application not found")

    valid_statuses = ["pending", "reviewed", "accepted", "rejected"]
    if status in valid_statuses:
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}.")
    else:
        messages.error(request, "Invalid status.")

    return redirect("seeker/view_applications", job_id=application.job.id)


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("manage_jobs")
    else:
        form = JobForm(instance=job)

    return render(request, "employer/edit_job.html", {"form": form, "job": job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" has been deleted successfully.')
        return redirect("manage_jobs")

    # If not POST, redirect to manage jobs
    return redirect("manage_jobs")


def job_list(request):
    search = request.GET.get("search", "")
    jobs = Job.objects.all()

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(company__icontains=search)
            | Q(description__icontains=search)
        )

    applied_jobs = []
    if request.user.is_authenticated:
        applied_jobs = Application.objects.filter(
            seeker=request.user  # Changed from 'user' to 'seeker'
        ).values_list("job_id", flat=True)

    return render(
        request,
        "seeker/job_list.html",
        {"jobs": jobs, "search": search, "applied_jobs": applied_jobs},
    )


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    if request.user.is_authenticated and request.user.is_seeker():
        has_applied = Application.objects.filter(job=job, seeker=request.user).exists()

    return render(
        request, "seeker/job_detail.html", {"job": job, "has_applied": has_applied}
    )


# Application Views
@login_required
@user_passes_test(lambda u: u.is_seeker())
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if already applied
    if Application.objects.filter(job=job, seeker=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_detail", job_id=job_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("dashboard")
    else:
        form = ApplicationForm()

    return render(request, "seeker/apply_job.html", {"form": form, "job": job})


@login_required
@user_passes_test(lambda u: u.is_employer())
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all()

    return render(
        request,
        "seeker/view_applications.html",
        {
            "job": job,
            "applications": applications,
        },
    )
