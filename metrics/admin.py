from django.contrib import admin
from .models import Metric


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('industry', 'average_age', 'average_salary', 'gender_diversity_index')
    search_fields = ('industry',)
    readonly_fields = ('average_age', 'average_salary', 'gender_diversity_index',
                       'male_percentage', 'female_percentage')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
