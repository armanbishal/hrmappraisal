from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [

    # full-report-view
    path("fullreportview/", fullReportView, name='fullreportview'),

    # pivot-summary-all-employee
    path("pivotsummaryall/", pivotSummaryAll, name='pivotsummaryall'),

    # pivot-summary-increment/confirmation-employee-only
    path("pivotsummaryinc/", pivotSummaryInc, name='pivotsummaryinc'),

    # report-extraction
    path("reportextraction/", reportExtraction, name='reportpdf'),

   # assessment-Sbu-Wise-Report
    path("Assessment_Sbu_Wise_Report/", assessmentSbuWiseReport, name='assessmentSbuWiseReport'),
    path("Assessment_Sbu_Report/", assessmentSbuReport, name='assessmentSbuReport'),




]
