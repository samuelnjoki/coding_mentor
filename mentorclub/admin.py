from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm

from mentorclub.models import Course, Event, Member, Schedule, User

# Register your models here

class CustomUserAdmin(admin.ModelAdmin):
    add_form =RegistrationForm
    model = User
    
    list_display = ("username","firstname", "lastname","gender","email", "is_admin", "last_login","date_joined",)
    
    readonly_fields=('id','date_joined','last_login',)
   
admin.site.register(User,CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Schedule)

