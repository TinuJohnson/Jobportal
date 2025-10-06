from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Job, Application


# Register your models
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Application)
