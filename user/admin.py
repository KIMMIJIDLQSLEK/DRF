from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User,UserProfile,Hobby

# class UserProfileInline(admin.TabularInline): #가로
class UserProfileInline(admin.StackedInline): #세로
    model=UserProfile
    readonly_fields = ('birthday',)


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('id','username')
    list_display_links = ('username',)
    list_filter=('fullname',)
    search_fields=('username',)
    readonly_fields = ('username','password','join_date',)
    fieldsets = (
        ("info",{'fields':('username','email','password','fullname','join_date')}),
        ('permissions',{'fields':('is_active','is_admin')})
    )
    inlines = (
        UserProfileInline,
    )

class HobbyAdmin(admin.ModelAdmin):
    list_display=['id','name'] #리스트이거나 튜플이어야함
    # list_display=('id',)

admin.site.register(User,UserAdmin)
admin.site.register(Hobby,HobbyAdmin) #Hobby라는 모델을 쓰고 HobbyAdmin 규칙 사용


# Unregister
admin.site.unregister(Group)