# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User, Job, Application
from .forms import JobForm, ApplicationForm, UserRegistrationForm


def home(request):
    # You can either show the job list or a dedicated landing page
    # Option 1: Redirect to job list
    # return redirect('job_list')

    # Option 2: Show a dedicated landing page (create home.html)
    return render(request, "home.html")


# Authentication Views
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


# Dashboard
@login_required
def dashboard(request):
    if request.user.is_seeker():
        applications = Application.objects.filter(seeker=request.user)
        return render(request, "dashboard_seeker.html", {"applications": applications})
    else:
        jobs = Job.objects.filter(employer=request.user)
        return render(request, "dashboard_employer.html", {"jobs": jobs})


@login_required
@user_passes_test(lambda u: u.is_employer())
def dashboard_employer(request):
    jobs = Job.objects.filter(employer=request.user)
    total_applications = Application.objects.filter(job__employer=request.user).count()

    return render(
        request,
        "dashboard_employer.html",
        {"jobs": jobs, "total_applications": total_applications},
    )


# Job Views
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
    return render(request, "post_job.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    jobs = Job.objects.all()
    applications = Application.objects.all()
    employers = User.objects.filter(role="employer")

    return render(
        request,
        "admin_dashboard.html",
        {
            "users": users,
            "jobs": jobs,
            "applications": applications,
            "employers": employers,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_employer())
def manage_jobs(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, "manage_jobs.html", {"jobs": jobs})


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
        "job_list.html",
        {"jobs": jobs, "search": search, "applied_jobs": applied_jobs},
    )


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if already applied
    if Application.objects.filter(
        seeker=request.user, job=job
    ).exists():  # Changed from 'user' to 'seeker'
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_list")

    # Create application
    Application.objects.create(
        seeker=request.user,  # Changed from 'user' to 'seeker'
        job=job,
        status="applied",
    )

    messages.success(request, f"Successfully applied for {job.title} at {job.company}!")
    return redirect("job_list" + "?application=success")


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    if request.user.is_authenticated and request.user.is_seeker():
        has_applied = Application.objects.filter(job=job, seeker=request.user).exists()

    return render(request, "job_detail.html", {"job": job, "has_applied": has_applied})


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

    return render(request, "apply_job.html", {"form": form, "job": job})


@login_required
@user_passes_test(lambda u: u.is_employer())
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all()
    return render(
        request, "view_applications.html", {"job": job, "applications": applications}
    )


# Admin Views (simplified)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    jobs = Job.objects.all()
    applications = Application.objects.all()

    return render(
        request,
        "admin_dashboard.html",
        {"users": users, "jobs": jobs, "applications": applications},
    )
