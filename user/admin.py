from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User,UserProfile,Hobby


# Register your models here.
class HobbyAdmin(admin.ModelAdmin):
    list_display=['id','name'] #리스트이거나 튜플이어야함
    # list_display=('id',)

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Hobby,HobbyAdmin) #Hobby라는 모델을 쓰고 HobbyAdmin 규칙 사용


# Unregister
admin.site.unregister(Group)