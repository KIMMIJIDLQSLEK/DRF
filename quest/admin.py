from django.contrib import admin
from .models import User
from .models import UserProfile
from .models import Hobby

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Hobby)