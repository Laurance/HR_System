from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from .models import Metric
from .serializers import PerIndustrySerializer, AverageExperienceSerializer
import pandas as pd


def _validate_parameter(parameter, error_message):
    """
    Validate if a parameter is provided, otherwise return a bad request response.
    """
    if not parameter:
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


class AverageAgePerIndustryView(generics.CreateAPIView):
    """
    Calculate and save the average age for a specified industry.

    Parameters:
    - industry (str): The industry for which to calculate the average age.

    Returns:
    - 201 Created: If the average age is successfully calculated and saved.
    - 400 Bad Request: If the 'industry' parameter is missing.
    - 404 Not Found: If the specified industry is not found in the data.

    Example:
    ```
    POST /api/metrics/average-age-per-industry/
    {
      "industry": "Technology"
    }
    """
    serializer_class = PerIndustrySerializer

    def create(self, request, *args, **kwargs):
        industry = request.data.get('industry')
        _validate_parameter(industry, "Industry parameter is required.")

        employees_data = Employee.objects.filter(industry=industry).values('date_of_birth')
        employees_df = pd.DataFrame.from_records(employees_data)

        if employees_df.empty:
            return Response(
                {"error": f"Industry '{industry}' not found in the data."},
                status=status.HTTP_404_NOT_FOUND
            )

        avg_age = pd.to_datetime('today').year - pd.to_datetime(employees_df['date_of_birth']).dt.year.mean()

        Metric.objects.update_or_create(
            industry=industry,
            defaults={'average_age': avg_age}
        )

        return Response(
            {"message": f"Average Age for {industry} calculated and saved successfully: {avg_age}."},
            status=status.HTTP_201_CREATED
        )


class AverageSalaryPerIndustryView(generics.CreateAPIView):
    """
    Calculate and save the average salary for a specified industry.

    Parameters:
    - industry (str): The industry for which to calculate the average salary.

    Returns:
    - 201 Created: If the average salary is successfully calculated and saved.
    - 400 Bad Request: If the 'industry' parameter is missing.
    - 404 Not Found: If the specified industry is not found in the data.

    Example:
    ```
    POST /api/metrics/average-salary-per-industry/
    {
      "industry": "Technology"
    }
    """
    serializer_class = PerIndustrySerializer

    def create(self, request, *args, **kwargs):
        industry = request.data.get('industry')
        _validate_parameter(industry, "Industry parameter is required.")

        employees_data = Employee.objects.filter(industry=industry).values('salary')
        employees_df = pd.DataFrame.from_records(employees_data)

        if employees_df.empty:
            return Response(
                {"error": f"Industry '{industry}' not found in the data."},
                status=status.HTTP_404_NOT_FOUND
            )

        avg_salary = employees_df['salary'].mean()

        Metric.objects.update_or_create(
            industry=industry,
            defaults={'average_salary': avg_salary}
        )

        return Response(
            {"message": f"Average Salary for {industry} calculated and saved successfully: {avg_salary}."},
            status=status.HTTP_201_CREATED
        )


class AverageSalaryPerExperienceView(generics.CreateAPIView):
    """
    Calculate and save the average salary for employees with a specified years of experience.

    Parameters:
    - years_of_experience (int): The years of experience for which to calculate the average salary.

    Returns:
    - 201 Created: If the average salary is successfully calculated and saved.
    - 400 Bad Request: If the 'years_of_experience' parameter is missing.
    - 404 Not Found: If employees with the specified years of experience are not found in the data.

    Example:
    ```
    POST /api/metrics/average-salary-per-experience/
    {
      "years_of_experience": 5
    }
    """
    serializer_class = AverageExperienceSerializer

    def create(self, request, *args, **kwargs):
        years_of_experience = request.data.get('years_of_experience')
        _validate_parameter(years_of_experience, "Years of Experience parameter is required.")

        employees_data = Employee.objects.filter(years_of_experience=years_of_experience).values('salary')
        employees_df = pd.DataFrame.from_records(employees_data)

        if employees_df.empty:
            return Response(
                {"error": f"Employees with '{years_of_experience}' Years of Experience not found in the data."},
                status=status.HTTP_404_NOT_FOUND
            )

        avg_salary = employees_df['salary'].mean()

        Metric.objects.update_or_create(
            industry=f"[ALL] {years_of_experience} Years of Experience",
            defaults={'average_salary': avg_salary}
        )

        return Response(
            {"message": f"Average Salary for {years_of_experience} Years of Experience calculated "
                        f"and saved successfully: {avg_salary}."},
            status=status.HTTP_201_CREATED
        )


class GenderDiversityIndexView(generics.CreateAPIView):
    """
    API view to calculate and save the Gender Diversity Index for a specified industry.

    Parameters:
    - industry (str): The industry for which to calculate the Gender Diversity Index.

    Returns:
    - HTTP 201 Created: Successfully calculated and saved the Gender Diversity Index.
        {
            "message": "Gender Diversity Index for {industry} calculated and saved successfully: {index}.",
            "gender_distribution": {
                "male_percentage": 60.0,
                "female_percentage": 40.0
            }
        }
    - HTTP 400 Bad Request: If the industry parameter is missing.
        {
            "error": "Industry parameter is required."
        }
    - HTTP 404 Not Found: If no employees are found for the specified industry.
        {
            "error": "No employees found in the data for the specified industry."
        }
    """
    serializer_class = PerIndustrySerializer

    def create(self, request, *args, **kwargs):
        industry = request.data.get('industry')
        _validate_parameter(industry, "Industry parameter is required.")

        employees_data = Employee.objects.filter(industry=industry).values('gender')
        employees_df = pd.DataFrame.from_records(employees_data)

        if employees_df.empty:
            return Response(
                {"error": f"No employees found in the data for the specified industry."},
                status=status.HTTP_404_NOT_FOUND
            )

        gender_distribution = employees_df['gender'].value_counts(normalize=True) * 100

        gender_diversity_index = 1 - ((gender_distribution/100)**2).sum()

        # Save the calculated metric to the Metric model
        Metric.objects.update_or_create(
            industry=industry,
            defaults={
                'gender_diversity_index': gender_diversity_index,
                'male_percentage': gender_distribution.get('M', 0),
                'female_percentage': gender_distribution.get('F', 0),
            }
        )

        response_data = {
            "message":
                f"Gender Diversity Index for {industry} calculated and saved successfully: {gender_diversity_index}.",
            "gender_distribution": {
                "male_percentage": gender_distribution.get('M', 0),
                "female_percentage": gender_distribution.get('F', 0),
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
