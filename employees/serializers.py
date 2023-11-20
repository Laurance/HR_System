from rest_framework import serializers
from .models import Employee
from datetime import datetime


class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Employee
        fields = '__all__'

    def to_internal_value(self, data):
        if 'date_of_birth' in data:
            try:
                data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%d/%m/%Y').date()
            except ValueError:
                raise serializers.ValidationError({'date_of_birth': 'Date has wrong format. Use DD/MM/YYYY.'})

        return super().to_internal_value(data)
