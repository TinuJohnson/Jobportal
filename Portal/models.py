from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ("seeker", "Job Seeker"),
        ("employer", "Employer"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_seeker(self):
        return self.role == "seeker"

    def is_employer(self):
        return self.role == "employer"


class Job(models.Model):
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs",
        limit_choices_to={"role": "employer"},
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    salary = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.company}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        limit_choices_to={"role": "seeker"},
    )
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(["pdf", "doc", "docx"])],
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "seeker")  # one application per seeker per job
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.seeker.username} → {self.job.title}"
