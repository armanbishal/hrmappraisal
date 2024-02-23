from django.urls import path
from .views import *

app_name = 'kpimanagement'

urlpatterns = [

    path("random/", timmy, name='timmy'),

    # kpi-form
    path("EmployKPIPerformanceList/", EmployKPIPerformanceList, name='EmployKPIPerformanceList'),
    path("kpi_form/", kpiPerformanceSave, name='kpi_form'),
    path("kpiPerformanceList/", kpiPerformanceList, name='kpiPerformanceList'),
    path("IndividualKPIFrom/<id>/", IndividualKPIFrom, name='IndividualKPIFrom'),
    path("IndividualEmployeeDetails/<id>/", IndividualEmployeeDetails, name='IndividualEmployeeDetails'),

    # employee-assign
    path("employee_assign/", employeeAssign, name='employee_assign'),
    path("EmployeeAssignSupervisorUpdate/", EmployeeAssignSupervisorUpdate, name='EmployeeAssignSupervisorUpdate'),

    # assessment-details
    path("assessment_details_update/", assessmentDetailsUpdate, name='assessment_details_update'),
    path("assessment_details_update_single/<id>", assessmentDetailsUpdateSingle, name='assessment_details_update_single'),

    # assessment-report
    path("assessment_report/", assessmentReport, name='assessmentReport'),
    path("assessment_report/<id>", assessmentReportSingle, name='assessmentReportSingle'),

    # Assessment supervisor wise list
    path("assessment_supervisor/", assessmentSupervisorList, name='assessmentSupervisorList'),
    path("assessment_supervisor_single/<id>", assessmentSupervisorSingle,name='assessmentSupervisorSingle'),

    # Assessment supervisor wise list
    path("supervisorPerformanceList/", supervisorPerformanceList, name='supervisorPerformanceList'),
    path("supervisorPerformancSave/<id>", supervisorPerformancSave, name='supervisorPerformancSave'),
]
