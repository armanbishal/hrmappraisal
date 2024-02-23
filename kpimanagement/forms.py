from django import forms
from django.forms import ModelForm
from kpimanagement.models import *

class KPIPerformanceForm(ModelForm):
    class Meta:
        model = KPIPerformance
        fields = '__all__'

class EmployeeAssignForm(ModelForm):
    class Meta:
        model = KPIPerformance
        fields = ['sbu', 'employee', 'supervisor']

        widgets = {
            "sbu": forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            "employee": forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            "supervisor": forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }

class AssessmentDetailForm(ModelForm):
    class Meta:
        model = AssessmentDetail
        fields = '__all__'


