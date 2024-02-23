from django import forms
from django.forms import ModelForm
from configuration.models import *
from kpimanagement.models import *


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ['status','created_by','updated_by','updated_date','id']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Name', 'required': 'required'}),
            "employee_id": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Employee ID', 'required': 'required'}),
            "designation": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Designation', 'required': 'required'}),
            "basic_salary": forms.NumberInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter a number. Ex: 35000'}),
            "date_of_joining": forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id':'html5-date-input'}),
            "sbu": forms.Select(attrs={'class': 'form-control'}),
            "sub_sbu": forms.Select(attrs={'class': 'form-control'}),
            "supervisor": forms.Select(attrs={'class': 'form-control'}),
            "project": forms.Select(attrs={'class': 'form-control'}),
            "total_salary_and_allowance": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "basic": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "house_rent": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "medical_allowance": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "conveyance_allowance": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "wppf": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "special_bonus": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
            "mobile_and_other_allowance": forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Enter a number. Ex: 35000'}),
            "project_expense": forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Enter a number. Ex: 35000'}),
            "other_benefit": forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Enter a number. Ex: 35000'}),
            "gross_salary": forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Enter a number. Ex: 35000', 'required': 'required'}),
            "pf_com_contribution": forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter a number. Ex: 35000'}),
        }

class ConfirmationIncrementNoincrementForm(ModelForm):
    class Meta:
        model = ConfirmationIncrementNoincrement
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class SBUForm(ModelForm):
    class Meta:
        model = SBU
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "director_name": forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }

class SubSBUForm(ModelForm):
    class Meta:
        model = SubSBU
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "sub": forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }

class SBUDirectorNameForm(ModelForm):
    class Meta:
        model = SBUDirectorName
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class SupervisorForm(ModelForm):
    class Meta:
        model = Supervisor
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class ReviewRatingForm(ModelForm):
    class Meta:
        model = ReviewRating
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "rating": forms.NumberInput(attrs={'class': 'form-control',
                                           'placeholder': 'Rating', 'required': 'required'}),
        }

class KPIConfigForm(ModelForm):
    class Meta:
        model = KPIConfig
        exclude = ['created_by','updated_by','updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Name', 'required': 'required'}),
            "year": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Year', 'required': 'required'}),
        }

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "grade": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Grade', 'required': 'required'}),
        }

class KPIObjectiveForm(ModelForm):
    class Meta:
        model = KPIObjective
        fields = '__all__'
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "percentage": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Percentage', 'required': 'required'}),
            "grade": forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Grade', 'required': 'required'}),
        }

class KPIValueForm(ModelForm):
    class Meta:
        model = KPIValue
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "percentage": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Percentage', 'required': 'required'}),
            "grade": forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Grade', 'required': 'required'}),
        }

class HRRatingForm(ModelForm):
    class Meta:
        model = HRRating
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
            "percentage": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Percentage', 'required': 'required'}),
            "grade": forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Grade', 'required': 'required'}),
        }

class CriticalityForm(ModelForm):
    class Meta:
        model = Criticality
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class PotentialForImprovementForm(ModelForm):
    class Meta:
        model = PotentialForImprovement
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class TechnicalImplementationOperationalForm(ModelForm):
    class Meta:
        model = TechnicalImplementationOperational
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class TopAverageBottomPerformerForm(ModelForm):
    class Meta:
        model = TopAverageBottomPerformer
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class BestPerformerTeamForm(ModelForm):
    class Meta:
        model = BestPerformerTeam
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class BestPerformerOrganizationForm(ModelForm):
    class Meta:
        model = BestPerformerOrganization
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class BestPerformerPMForm(ModelForm):
    class Meta:
        model = BestPerformerPM
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }

class BestInnovatorTeamForm(ModelForm):
    class Meta:
        model = BestInnovatorTeam
        exclude = ['created_by', 'updated_by', 'updated_date']

        widgets = {
            "shortlist": forms.NumberInput(attrs={'class': 'form-control',
                                                'placeholder': 'Shortlist', 'required': 'required'}),
            "name": forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name', 'required': 'required'}),
        }





