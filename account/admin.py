from django.contrib import admin

from account.models import Profile, Department

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'contact_number', 'department')

    def user_name(self, obj):
        return obj
    user_name.short_description = 'Full Name'

admin.site.register(Profile, ProfileAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_count')

    def employee_count(self, obj):
        return '%s' % Profile.objects.filter(department=obj.id).count()
    employee_count.short_description = 'Employee Count'

admin.site.register(Department, DepartmentAdmin)
