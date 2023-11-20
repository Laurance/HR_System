from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'date_of_birth',
                    'industry', 'salary', 'years_of_experience']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'industry']
    list_filter = ['industry', 'years_of_experience']
    ordering = ['id']
