from django.urls import path
from .views import (
    AverageAgePerIndustryView,
    AverageSalaryPerIndustryView,
    AverageSalaryPerExperienceView,
    GenderDiversityIndexView
)

urlpatterns = [
    path(
        'average-age-per-industry/',
        AverageAgePerIndustryView.as_view(),
        name='average-age-per-industry'
    ),
    path(
        'average-salary-per-industry/',
        AverageSalaryPerIndustryView.as_view(),
        name='average-salary-per-industry'
    ),
    path(
        'average-salary-per-experience/',
        AverageSalaryPerExperienceView.as_view(),
        name='average-salary-per-experience'
    ),
    path(
        'gender-diversity-index/',
        GenderDiversityIndexView.as_view(),
        name='gender-diversity-index'
    )
]
