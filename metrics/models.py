from django.db import models


class Metric(models.Model):
    industry = models.CharField(max_length=255)
    average_age = models.FloatField(null=True, blank=True)
    average_salary = models.FloatField(null=True, blank=True)
    gender_diversity_index = models.FloatField(null=True, blank=True)
    male_percentage = models.FloatField(null=True, blank=True)
    female_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.industry} Metrics"
