from rest_framework import serializers
from .models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('industry', 'average_age', 'average_salary', 'gender_diversity_index')


class PerIndustrySerializer(serializers.Serializer):
    industry = serializers.CharField(max_length=255)


class AverageExperienceSerializer(serializers.Serializer):
    years_of_experience = serializers.IntegerField()
