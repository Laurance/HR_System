from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    API View for listing and creating Employee instances.
    Provides filtering and sorting capabilities.

    Query Parameters:
    - 'first_name': Filters employees by first name.
    - 'last_name': Filters employees by last name.
    - 'industry': Filters employees by industry.
    - 'years_of_experience': Filters employees by years of experience.
      Can accept either a single value or a range (e.g., "1-5").

    Sorting:
    Supports ordering based on fields such as 'id', 'first_name', 'last_name',
    'date_of_birth', 'industry', 'salary', and 'years_of_experience'.

    Example API Requests:
    - GET /employees/ : Retrieve a list of all employees.
    - GET /employees/?first_name=Alex : Filter employees by first name.
    - GET /employees/?industry=IT : Filter employees by industry.
    - GET /employees/?years_of_experience=1-5 : Filter employees by experience range.
    - GET /employees/?ordering=first_name : Sort employees by first name.

    - POST /employees/ : Create one or more new employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'industry', 'salary', 'years_of_experience']

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            employees = []
            for employee_data in data:
                serializer = self.get_serializer(data=employee_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                employees.append(serializer.data)
            headers = self.get_success_headers(employees)
            return Response(employees, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Employee.objects.all()
        queryset = self.apply_first_name_filter(queryset)
        queryset = self.apply_last_name_filter(queryset)
        queryset = self.apply_industry_filter(queryset)
        queryset = self.apply_experience_filter(queryset)
        return queryset

    def apply_first_name_filter(self, queryset):
        first_name = self.request.query_params.get('first_name', None)
        if first_name:
            return queryset.filter(first_name__icontains=first_name)
        return queryset

    def apply_last_name_filter(self, queryset):
        last_name = self.request.query_params.get('last_name', None)
        if last_name:
            return queryset.filter(first_name__icontains=last_name)
        return queryset

    def apply_industry_filter(self, queryset):
        industry = self.request.query_params.get('industry', None)
        if industry:
            return queryset.filter(industry__icontains=industry)
        return queryset

    def apply_experience_filter(self, queryset):
        years_of_experience = self.request.query_params.get('years_of_experience', None)
        if years_of_experience:
            if '-' in years_of_experience:
                return self.apply_experience_range_filter(queryset, years_of_experience)
            else:
                return queryset.filter(years_of_experience=int(years_of_experience))
        return queryset

    @staticmethod
    def apply_experience_range_filter(queryset, years_of_experience):
        min_experience, max_experience = map(int, years_of_experience.split('-'))
        return queryset.filter(years_of_experience__range=(min_experience, max_experience))


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View for retrieving, updating, and deleting a single Employee instance.

    Supports CRUD operations for a specific Employee resource identified by its primary key (pk).
    GET request retrieves details for the specified employee.
    PUT or PATCH request updates the details of the specified employee.
    DELETE request deletes the specified employee.

    Query Parameters:
    None

    Request Methods:
    - GET /employees/<pk>/ : Retrieve details for the specified employee.
    - PUT /employees/<pk>/ : Update details for the specified employee.
    - PATCH /employees/<pk>/ : Partially update details for the specified employee.
    - DELETE /employees/<pk>/ : Delete the specified employee.

    Example API Requests:
    - GET /employees/1/ : Retrieve details for the employee with id=1.
    - PUT /employees/1/ : Update details for the employee with id=1.
    - PATCH /employees/1/ : Partially update details for the employee with id=1.
    - DELETE /employees/1/ : Delete the employee with id=1.

    Response:
    - For successful deletion, returns a 200 OK response with a custom message.
    - For other operations, returns a standard response based on the operation.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_200_OK)
