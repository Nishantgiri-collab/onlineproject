
from django.contrib import admin
from .models import RegistrationUser,ClassSlot
# Register your models here.
@admin.register(RegistrationUser)
class RegistrationUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone_number', 'age', 'previous_qualification', 'previous_qualification_percentage', 'created_at','password','confirm_password')
    search_fields = ('fullname', 'email', 'phone_number')
    list_filter = ('previous_qualification', 'age')
    ordering = ('-created_at',)


# ClassSlot Admin
@admin.register(ClassSlot)
class ClassSlotAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'get_email', 'slot', 'booked_on')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
