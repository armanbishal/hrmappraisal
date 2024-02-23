from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from datetime import date
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from kpimanagement.forms import EmployeeAssignForm
from configuration.models import *
from configuration.forms import *
from kpimanagement.models import *
from kpimanagement.forms import *
from kpimanagement.views import year
from report.models import *
from django.utils.decorators import method_decorator
from usermanagement.decorators import login_required, access_permission_required
import requests
import xlwt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from reportlab.lib.enums import TA_CENTER
import reportlab.lib.pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab import rl_config
from io import BytesIO
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

year = date.today()
current_year = year.year
first_last_year = year.year - 1
second_last_year = year.year - 2
third_last_year = year.year - 3

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % (doc.page))
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % (doc.page))
    canvas.restoreState()


def myLandscapePage(canvas, doc):
    canvas.saveState()
    canvas.setPageSize(landscape(letter))
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, ""))
    canvas.restoreState()


def fullReportView(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    sbu_flag = 0
    sbu_list = SBU.objects.all()
    employee = Employee.objects.all()

    if 'sbu-search' in request.POST:
        sbu_flag = 1
        form = AssessmentDetailForm()
        sbu_list = SBU.objects.all()
        employee = Employee.objects.all()

        sbu_search = request.POST.get('sbu')

        assessment_details = AssessmentDetail.objects.filter(year__in=[second_last_year, first_last_year, current_year],
                                                             employee__sbu__name=sbu_search).order_by('employee',
                                                                                                      'year')

        dict = {}
        assessment_details_temp = assessment_details

        for i in assessment_details_temp:
            count_num = AssessmentDetail.objects.filter(year__in=[second_last_year, first_last_year, current_year],
                                                        employee_id=i.employee_id).count()
            if count_num >= 3 and i.employee_id not in dict:
                dict[i.employee_id] = []
                dict[i.employee_id].append(i.employee.name)
                dict[i.employee_id].append(i.employee.name)
                dict[i.employee_id].append(i.employee.employee_id)
                dict[i.employee_id].append(i.employee.date_of_joining)
                dict[i.employee_id].append(i.employee.timesince)
                dict[i.employee_id].append(i.employee.sbu)
                dict[i.employee_id].append(i.employee.sub_sbu)
                dict[i.employee_id].append(i.employee.supervisor)
                dict[i.employee_id].append(None)

            elif count_num == 2 and i.employee_id not in dict:
                dict[i.employee_id] = []
                dict[i.employee_id].append(i.employee.name)
                dict[i.employee_id].append(i.employee.designation)
                dict[i.employee_id].append(i.employee.employee_id)
                dict[i.employee_id].append(i.employee.date_of_joining)
                dict[i.employee_id].append(i.employee.timesince)
                dict[i.employee_id].append(i.employee.sbu)
                dict[i.employee_id].append(i.employee.sub_sbu)
                dict[i.employee_id].append(i.employee.supervisor)
                dict[i.employee_id].append(None)

                dict[i.employee_id].append('1 Jan, ' + str(first_last_year))
                for x in range(0, 52):
                    dict[i.employee_id].append('No Data Available')

            elif count_num == 1 and i.employee_id not in dict:
                dict[i.employee_id] = []
                dict[i.employee_id].append(i.employee.name)
                dict[i.employee_id].append(i.employee.designation)
                dict[i.employee_id].append(i.employee.employee_id)
                dict[i.employee_id].append(i.employee.date_of_joining)
                dict[i.employee_id].append(i.employee.timesince)
                dict[i.employee_id].append(i.employee.sbu)
                dict[i.employee_id].append(i.employee.sub_sbu)
                dict[i.employee_id].append(i.employee.supervisor)
                dict[i.employee_id].append(None)

                dict[i.employee_id].append('1 Jan, ' + str(second_last_year))
                for x in range(0, 52):
                    dict[i.employee_id].append('No Data Available')

                dict[i.employee_id].append('1 Jan, ' + str(first_last_year))
                for x in range(0, 52):
                    dict[i.employee_id].append('No Data Available')

            # elif count_num == 0:
            #     dict[i.employee_id] = []
            #
            #     dict[i.employee_id].append('1 Jan, ' + str(second_last_year))
            #     for x in range(0, 52):
            #         dict[i.employee_id].append('No Data Available')
            #
            #     dict[i.employee_id].append('1 Jan, ' + str(first_last_year))
            #     for x in range(0, 52):
            #         dict[i.employee_id].append('No Data Available')
            #
            #     dict[i.employee_id].append('1 Jan, ' + str(current_year))
            #     for x in range(0, 52):
            #         dict[i.employee_id].append('No Data Available')

        for i in assessment_details:
            dict[i.employee_id].append('1 Jan, ' + str(current_year))
            dict[i.employee_id].append(
                i.confirmation_increment_noincrement if i.confirmation_increment_noincrement is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.total_salary_and_allowance if i.total_salary_and_allowance is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.basic_salary if i.basic_salary is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.house_rent if i.house_rent is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.medical_allowance if i.medical_allowance is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.conveyance_allowance if i.conveyance_allowance is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.wppf if i.wppf is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.special_bonus if i.special_bonus is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.mobile_and_other_allowance if i.mobile_and_other_allowance is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.project_expense if i.project_expense is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.other_benefit if i.other_benefit is not None else 'No Data Available')
            dict[i.employee_id].append(i.employee.gross_salary if i.gross_salary is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.pf_com_contribution if i.pf_com_contribution is not None else 'No Data Available')
            dict[i.employee_id].append(i.salary_grade if i.salary_grade is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.employee.assessmentDuration() if i.employee.assessmentDuration() is not None else 'No Data Available')
            dict[i.employee_id].append(i.kpi_objective if i.kpi_objective is not None else 'No Data Available')
            dict[i.employee_id].append(i.kpi_value if i.kpi_objective is not None else 'No Data Available')
            dict[i.employee_id].append(i.hr_rating if i.kpi_objective is not None else 'No Data Available')
            dict[i.employee_id].append(i.kpi_overall if i.kpi_overall is not None else 'No Data Available')
            dict[i.employee_id].append(i.percentage_kpi_objective if i.percentage_kpi_objective is not None else None)
            dict[i.employee_id].append(i.percentage_kpi_value if i.percentage_kpi_value is not None else None)
            dict[i.employee_id].append(i.percentage_kpi_hr if i.percentage_kpi_hr is not None else None)
            dict[i.employee_id].append(
                i.weighted_average_kpi if i.weighted_average_kpi is not None else 'No Data Available')
            dict[i.employee_id].append(i.criticality if i.criticality is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.potential_for_improvement if i.potential_for_improvement is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.technical_implementation_operational if i.technical_implementation_operational is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.top_average_bottom_performer if i.top_average_bottom_performer is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.best_performer_team if i.best_performer_team is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.best_innovator_team if i.best_innovator_team is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.best_performer_org if i.best_performer_org is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.proposed_designation if i.proposed_designation is not None else 'No Data Available')
            dict[i.employee_id].append(i.best_performer_pm if i.best_performer_pm is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.increment_amount_a if i.increment_amount_a is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.hr_new_gross_salary_a if i.hr_new_gross_salary_a is not None else 'No Data Available')
            dict[i.employee_id].append(i.percentage_hr_a if i.percentage_hr_a is not None else 'No Data Available')
            dict[i.employee_id].append(i.fixed_increment_b if i.fixed_increment_b is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.fixed_increment_new_gross_salary_b if i.fixed_increment_new_gross_salary_b is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.team_distribution_percentage_c if i.team_distribution_percentage_c is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.difference_new_salary_a_new_salary_b if i.difference_new_salary_a_new_salary_b is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.proposed_by_sbu_director_pm_self if i.proposed_by_sbu_director_pm_self is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.percentage_of_increment if i.percentage_of_increment is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.new_gross_salary_b if i.new_gross_salary_b is not None else 'No Data Available')
            dict[i.employee_id].append(i.cagr_three_years if i.cagr_three_years is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.average_three_years if i.average_three_years is not None else 'No Data Available')
            dict[i.employee_id].append(i.average_actual if i.average_actual is not None else 'No Data Available')
            dict[i.employee_id].append(i.kpi_overall if i.kpi_overall is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.weighted_average_kpi if i.weighted_average_kpi is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.increment_with_kpi_percentage if i.increment_with_kpi_percentage is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.new_gross_salary_kpi_percentage if i.new_gross_salary_kpi_percentage is not None else 'No Data Available')
            dict[i.employee_id].append(
                i.gap_manual_formula if i.gap_manual_formula is not None else 'No Data Available')
            dict[i.employee_id].append(i.remarks if i.remarks is not None else 'No Data Available')
            dict[i.employee_id].append(i.remarks_two if i.remarks_two is not None else 'No Data Available')

        context = {'dict': dict,
                   'assessment_details': assessment_details,
                   'sbu_search': sbu_search,
                   'sbu_flag': sbu_flag,
                   'sbu_list': sbu_list,
                   'year': year,
                   'current_year': current_year,
                   'first_last_year': first_last_year,
                   'second_last_year': second_last_year,
                   'third_last_year': third_last_year,
                   'data': userdata,
                   'employee': employee,
                   }
        return render(request, 'report/assessmentfullreport/assessmentfullreport.html', context)

    context = {'data': userdata,
               'year': year,
               'data': userdata,
               'sbu_list': sbu_list,
               'employee': employee,
               }

    return render(request, 'report/assessmentfullreport/assessmentfullreport.html', context)


def pivotSummaryAll(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    year_flag = 0
    year_list = []
    for i in range(2020, date.today().year + 1):
        year_list.append(i)

    if 'year-search' in request.POST:
        year_flag = 1

        year_exact = request.POST.get('year')
        last_year_exact = int(year_exact) - 1

        dict = {}
        sbu_list = SBU.objects.all()
        employee_total = 0
        emp_gross_monthly_salary_current_year_total = 0
        emp_gross_monthly_salary_last_year_total = 0
        yoy_total = 0
        yoy_total_percenatage = 0
        emp_gross_monthly_salary_current_year_percentage_total = 0
        emp_gross_monthly_salary_last_year_percentage_total = 0
        emp_percentage_total = 0

        for i in sbu_list:

            assess = AssessmentDetail.objects.filter(
                Q(employee__sbu__name=i.name) &
                Q(year=year_exact)
            )
            # print(assess)
            for j in assess:
                assess_exact = AssessmentDetail.objects.get(employee_id=j.employee.id, year__in=[year_exact])
                if assess_exact.gross_salary is not None:
                    emp_gross_monthly_salary_last_year_total = emp_gross_monthly_salary_last_year_total + assess_exact.gross_salary
                if assess_exact.new_gross_salary_b is not None:
                    emp_gross_monthly_salary_current_year_total = emp_gross_monthly_salary_current_year_total + assess_exact.new_gross_salary_b
                employee_total = employee_total + 1

        for i in sbu_list:
            emp_gross_monthly_salary_current_year = 0
            emp_gross_monthly_salary_last_year = 0
            emp_gross_monthly_salary_current_year_percentage = 0
            emp_gross_monthly_salary_last_year_percentage = 0
            emp_percentage = 0
            emp_count = 0

            assess = AssessmentDetail.objects.filter(
                Q(employee__sbu__name=i.name) &
                Q(year=year_exact)
            )
            for j in assess:
                assess_exact = AssessmentDetail.objects.get(employee_id=j.employee.id, year__in=[year_exact])
                if assess_exact.gross_salary is not None and emp_gross_monthly_salary_last_year_total is not 0:
                    emp_gross_monthly_salary_last_year = emp_gross_monthly_salary_last_year + assess_exact.gross_salary
                    emp_gross_monthly_salary_last_year_percentage = round(
                        ((emp_gross_monthly_salary_last_year / emp_gross_monthly_salary_last_year_total) * 100), 2)
                if assess_exact.new_gross_salary_b is not None and emp_gross_monthly_salary_current_year_total is not 0:
                    emp_gross_monthly_salary_current_year = emp_gross_monthly_salary_current_year + assess_exact.new_gross_salary_b
                    emp_gross_monthly_salary_current_year_percentage = round(
                        ((emp_gross_monthly_salary_current_year / emp_gross_monthly_salary_current_year_total) * 100),
                        2)
                emp_count = emp_count + 1

            yoy = 0
            if emp_gross_monthly_salary_current_year is not 0 or None and emp_gross_monthly_salary_last_year is not 0 or None:
                yoy = round(emp_gross_monthly_salary_current_year - emp_gross_monthly_salary_last_year)
            if yoy is not 0 and emp_gross_monthly_salary_last_year is not 0:
                yoy_percentage = str(round(((yoy / emp_gross_monthly_salary_last_year) * 100), 2)) + '%'
            else:
                yoy_percentage = 'N/A'

            emp_gross_monthly_salary_last_year_percentage_total = round(
                (emp_gross_monthly_salary_last_year_percentage_total + emp_gross_monthly_salary_last_year_percentage),
                2)
            emp_gross_monthly_salary_current_year_percentage_total = round((
                    emp_gross_monthly_salary_current_year_percentage_total + emp_gross_monthly_salary_current_year_percentage),
                2)
            if emp_count is not 0 and employee_total is not 0:
                emp_percentage = round((emp_count / employee_total) * 100)
                emp_percentage_total = emp_percentage_total + emp_percentage

            dict[i.name] = []
            dict[i.name].append(i.name)
            dict[i.name].append(emp_count)
            dict[i.name].append(str(emp_percentage) + '%')
            dict[i.name].append(emp_gross_monthly_salary_last_year)
            dict[i.name].append(str(emp_gross_monthly_salary_last_year_percentage) + '%')
            dict[i.name].append(emp_gross_monthly_salary_current_year)
            dict[i.name].append(str(emp_gross_monthly_salary_current_year_percentage) + '%')
            dict[i.name].append(yoy)
            dict[i.name].append(yoy_percentage)

        yoy_total = round(emp_gross_monthly_salary_current_year_total - emp_gross_monthly_salary_last_year_total)
        if yoy_total is not 0 and emp_gross_monthly_salary_last_year_total is not 0:
            yoy_total_percenatage = str(round(((yoy_total / emp_gross_monthly_salary_last_year_total) * 100), 2)) + '%'
        else:
            yoy_total_percenatage = 'N/A'

        dict['total'] = []
        dict['total'].append('Grand Total')
        dict['total'].append(employee_total)
        dict['total'].append(str(emp_percentage_total) + '%')
        dict['total'].append(emp_gross_monthly_salary_last_year_total)
        dict['total'].append(str(emp_gross_monthly_salary_last_year_percentage_total) + '%')
        dict['total'].append(emp_gross_monthly_salary_current_year_total)
        dict['total'].append(str(emp_gross_monthly_salary_current_year_percentage_total) + '%')
        dict['total'].append(yoy_total)
        dict['total'].append(yoy_total_percenatage)

        context = {'data': userdata,
                   'dict': dict,
                   'year': year,
                   'year_list': year_list,
                   'year_flag': year_flag,
                   'year_exact': year_exact,
                   'last_year_exact': last_year_exact,
                   'current_year': current_year,
                   'first_last_year': first_last_year,
                   'second_last_year': second_last_year,
                   'third_last_year': third_last_year
                   }
        return render(request, 'report/pivotsummary/pivotsummaryall.html', context)

    context = {'data': userdata,
               'year_list': year_list,
               'year_flag': year_flag,
               }
    return render(request, 'report/pivotsummary/pivotsummaryall.html', context)


def pivotSummaryInc(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    year_flag = 0
    year_list = []
    for i in range(2020, date.today().year + 1):
        year_list.append(i)

    if 'year-search' in request.POST:
        year_flag = 1

        year_exact = request.POST.get('year')
        last_year_exact = int(year_exact) - 1

        dict = {}
        sbu_list = SBU.objects.all()
        employee_total = 0
        gross_salary_new_gross_salary_diff_total = 0
        gross_salary_new_gross_salary_diff_percentage_total = 0
        emp_percentage_total = 0

        for i in sbu_list:

            assess = AssessmentDetail.objects.filter(
                Q(employee__sbu__name=i.name) &
                Q(year=year_exact)
            )

            for j in assess:
                assess_exact = AssessmentDetail.objects.get(employee_id=j.employee.id, year__in=[year_exact])
                if assess_exact.gross_salary != assess_exact.new_gross_salary_b and assess_exact.new_gross_salary_b is not None:
                    if assess_exact.gross_salary is not None and assess_exact.new_gross_salary_b is not None:
                        gross_salary_new_gross_salary_diff_total = gross_salary_new_gross_salary_diff_total + (
                                assess_exact.new_gross_salary_b - assess_exact.gross_salary)
                    employee_total = employee_total + 1

        for i in sbu_list:
            gross_salary_new_gross_salary_diff = 0
            gross_salary_new_gross_salary_diff_percentage = 0
            emp_percentage = 0
            emp_count = 0

            assess = AssessmentDetail.objects.filter(
                Q(employee__sbu__name=i.name) &
                Q(year=year_exact)
            )

            for j in assess:
                assess_exact = AssessmentDetail.objects.get(employee_id=j.employee.id, year__in=[year_exact])
                if assess_exact.gross_salary != assess_exact.new_gross_salary_b and assess_exact.new_gross_salary_b is not None:
                    if assess_exact.gross_salary is not None and assess_exact.new_gross_salary_b is not None:
                        gross_salary_new_gross_salary_diff = gross_salary_new_gross_salary_diff + (
                                assess_exact.new_gross_salary_b - assess_exact.gross_salary)
                        gross_salary_new_gross_salary_diff_percentage = round(
                            ((gross_salary_new_gross_salary_diff / gross_salary_new_gross_salary_diff_total) * 100), 2)
                    emp_count = emp_count + 1

            gross_salary_new_gross_salary_diff_percentage_total = gross_salary_new_gross_salary_diff_percentage_total + gross_salary_new_gross_salary_diff_percentage
            if emp_count is not 0 and employee_total is not 0:
                emp_percentage = round((emp_count / employee_total) * 100)
                emp_percentage_total = emp_percentage_total + emp_percentage

            dict[i.name] = []
            dict[i.name].append(i.name)
            dict[i.name].append(emp_count)
            dict[i.name].append(str(emp_percentage) + '%')
            dict[i.name].append(gross_salary_new_gross_salary_diff)
            dict[i.name].append(str(gross_salary_new_gross_salary_diff_percentage) + '%')

        dict['total'] = []
        dict['total'].append('Grand Total')
        dict['total'].append(employee_total)
        dict['total'].append(str(emp_percentage_total) + '%')
        dict['total'].append(gross_salary_new_gross_salary_diff_total)
        dict['total'].append(str(gross_salary_new_gross_salary_diff_percentage_total) + '%')

        context = {'data': userdata,
                   'dict': dict,
                   'year': year,
                   'year_list': year_list,
                   'year_flag': year_flag,
                   'year_exact': year_exact,
                   'last_year_exact': last_year_exact,
                   'current_year': current_year,
                   'first_last_year': first_last_year,
                   'second_last_year': second_last_year,
                   'third_last_year': third_last_year
                   }
        return render(request, 'report/pivotsummary/pivotsummaryinc.html', context)

    context = {'data': userdata,
               'year_list': year_list,
               'year_flag': year_flag,
               }
    return render(request, 'report/pivotsummary/pivotsummaryinc.html', context)


def reportExtraction(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    context = {'data': userdata}
    return render(request, 'report/reportpdf/reportpdf.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def assessmentSbuWiseReport(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    year_list = []
    for i in range(2020, date.today().year + 1):
        year_list.append(i)
    sbu_list = SBU.objects.all()
    context = {'data': userdata, 'sbu_list': sbu_list,'year_list':year_list}

    return render(request, 'report/assessmentfullreport/assessmentSbuWiseReport.html', context)





@login_required("logged_in", 'usermanagement:login')
def assessmentSbuReport(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
        }
        if request.method == 'POST':
            sbu = request.POST['sbu']
            current_year=request.POST['year']
            datasets = AssessmentDetail.objects.filter(sbu_id=sbu,year=current_year)
            if not datasets.exists():
                messages.error(request, 'Data Not Found')
                return redirect('report:assessmentSbuWiseReport')
            if 'xls_export' in request.POST:

                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="Assessment Report.xls"'
                timedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
                ws = wb.add_sheet('Assessment_Report-'+str(current_year))

                row_num = 3
                # year = date.today()
                # current_year = year.year
                font_style = xlwt.XFStyle()
                # font_style.font.bold = True
                common = "font:name Calibri,colour_index blue, bold on, height 220; align: horiz center, vert center ;"
                columns = ['SL', 'Employee Name', 'Designation', 'ID No', 'DOJ', 'Confirmation/Increment/No Increment',
                           'Duration', 'SBU', 'Sub SBU', 'PM Name','SBU Director Name', ' Effective Date', ' Total Salary and Allowance-'+str(current_year), 'Basic-'+str(current_year),
                           'House Rent-'+str(current_year), 'Medical Allowance-'+str(current_year),
                           'Conveyance Allowance-'+str(current_year), 'WPPF-'+str(current_year), 'Special Bonus-'+str(current_year), 'Mobile and Other Allowance-'+str(current_year),
                           'Project Expense-'+str(current_year), 'Other Benefits-'+str(current_year),
                           'Gross Salary-'+str(current_year), 'PF Com Contribution-'+str(current_year), 'Grade Salary-'+str(current_year), 'Year of Assessment Duation-'+str(current_year),
                           'KPI Objective-'+str(current_year), 'KPI-Value-'+str(current_year),
                           'KPI-HR-'+str(current_year), 'KPI-Overall-'+str(current_year), '% of KPI-Objective-'+str(current_year), '% of KPI-Value-'+str(current_year), '% of KPI-HR-'+str(current_year),
                           'Weighted Average of KPI-'+str(current_year),
                           'Criticality-'+str(current_year), 'Potential for Improvement-'+str(current_year), 'Technical/Implementation/Operational-'+str(current_year),
                           'Top/Average/Bottom Performer-'+str(current_year),
                           'Best performer inside team-'+str(current_year), 'Best innovator inside team-'+str(current_year),
                           'Best Performer in the organization-'+str(current_year), 'Proposed Designation-'+str(current_year),
                           'Best Performer among all PM-'+str(current_year), 'Salary Grade-'+str(current_year), 'Increment Amount (HR)-'+str(current_year),
                           'HR New Gross Salary(A)-'+str(current_year), 'HR %-'+str(current_year), 'Fixed Increment %-'+str(current_year),
                           'Fixed Increment New Gross Salary(B)-'+str(current_year), 'Team Distribution (%) (C)-'+str(current_year),
                           'Difference = New salary A- New salary B-'+str(current_year), 'Proposed By SBU Director/PM/Self-'+str(current_year),
                           '% of Increment-'+str(current_year), 'New Gross Salary B-'+str(current_year), 'CAGR 3 years-'+str(current_year), 'Avarage 3 Years-'+str(current_year), 'Average Actual-'+str(current_year),
                           'KPI-Overall-'+str(current_year),
                           'Weighted Average of KPI %-'+str(current_year), 'Increment with KPI %-'+str(current_year), 'New Gross Salary KPI %-'+str(current_year),
                           'Gap Manual vs Formula-'+str(current_year),
                           'Remarks', 'Remarks']

                ws.write_merge(0, 1, 0, 5, 'Assessment Report', xlwt.easyxf(common))

                for col in range(len(columns)):
                    ws.write(row_num, col, columns[col], xlwt.easyxf(common))
                row_num += 1
                datamounth = '1-Jan-'
                for count, data in enumerate((datasets)):
                    common1 = "font:name Calibri;"
                    font_style = xlwt.easyxf(common1)
                    dateformat = xlwt.easyxf(common1, num_format_str='dd/mm/yyyy')
                    print(str(data.employee.assessmentDuration))
                    ws.write(row_num, 0, count + 1, font_style)
                    ws.write(row_num, 1, data.employee.name, font_style)
                    ws.write(row_num, 2, data.employee.designation, font_style)
                    ws.write(row_num, 3, data.employee.employee_id, font_style)
                    ws.write(row_num, 4, data.employee.date_of_joining, dateformat)
                    if data.confirmation_increment_noincrement is not None:
                        ws.write(row_num, 5, data.confirmation_increment_noincrement.name, font_style)
                    else:
                        ''
                    ws.write(row_num, 6, '', font_style)
                    ws.write(row_num, 7, data.sbu.name, font_style)
                    ws.write(row_num, 8, data.employee.sub_sbu.name, font_style)
                    ws.write(row_num, 9, data.employee.supervisor.name, font_style)
                    ws.write(row_num, 10, '')
                    ws.write(row_num, 11, datamounth + data.year, dateformat)
                    ws.write(row_num, 12, data.total_salary_and_allowance, font_style)
                    ws.write(row_num, 13, data.basic_salary, font_style)
                    ws.write(row_num, 14, data.house_rent, font_style)
                    ws.write(row_num, 15, data.medical_allowance, font_style)
                    ws.write(row_num, 16, data.conveyance_allowance, font_style)
                    ws.write(row_num, 17, data.wppf, font_style)
                    ws.write(row_num, 18, data.special_bonus, font_style)
                    ws.write(row_num, 19, data.mobile_and_other_allowance, font_style)
                    ws.write(row_num, 20, data.project_expense, font_style)
                    ws.write(row_num, 21, data.other_benefit, font_style)
                    ws.write(row_num, 22, data.gross_salary, font_style)
                    ws.write(row_num, 23, data.pf_com_contribution, font_style)
                    ws.write(row_num, 24, '', font_style)
                    ws.write(row_num, 25, '', font_style)
                    ws.write(row_num, 26, data.kpi_objective.name, font_style)
                    ws.write(row_num, 27, data.kpi_value.name, font_style)
                    ws.write(row_num, 28, data.hr_rating.name, font_style)
                    ws.write(row_num, 29, data.kpi_overall, font_style)
                    ws.write(row_num, 30, data.percentage_kpi_objective, font_style)
                    ws.write(row_num, 31, data.percentage_kpi_value, font_style)
                    ws.write(row_num, 32, data.percentage_kpi_hr, font_style)
                    ws.write(row_num, 33, data.weighted_average_kpi, font_style)

                    if data.criticality is not None:
                        ws.write(row_num, 34, data.criticality.name, font_style)
                    else:
                        ''
                    if data.potential_for_improvement_id is not None:
                       ws.write(row_num, 35, data.potential_for_improvement.name, font_style)
                    else:
                        ''
                    if data.technical_implementation_operational is not None:
                        ws.write(row_num, 36, data.technical_implementation_operational.name, font_style)
                    else:
                        ''
                    if data.top_average_bottom_performer is not None:
                        ws.write(row_num, 37, data.top_average_bottom_performer.name, font_style)
                    else:
                        ''
                    if data.best_performer_team is not None:
                        ws.write(row_num, 38, data.best_performer_team.name, font_style)
                    else:
                        ''
                    if data.best_innovator_team is not None:
                        ws.write(row_num, 39, data.best_innovator_team.name, font_style)
                    else:
                        ''
                    if data.best_performer_org is not None:
                        ws.write(row_num, 40, data.best_performer_org.name, font_style)
                    else:
                        ''
                    ws.write(row_num, 41, data.proposed_designation, font_style)
                    if data.best_performer_pm is not None:
                       ws.write(row_num, 42, data.best_performer_pm.name, font_style)
                    else:
                        ''
                    ws.write(row_num, 43, data.salary_grade, font_style)
                    ws.write(row_num, 44, data.increment_amount_a, font_style)
                    ws.write(row_num, 45, data.hr_new_gross_salary_a, font_style)
                    ws.write(row_num, 46, data.percentage_hr_a, font_style)
                    ws.write(row_num, 47, data.fixed_increment_b, font_style)
                    ws.write(row_num, 48, data.fixed_increment_new_gross_salary_b, font_style)
                    ws.write(row_num, 49, data.team_distribution_percentage_c, font_style)
                    ws.write(row_num, 50, data.difference_new_salary_a_new_salary_b, font_style)
                    ws.write(row_num, 51, data.proposed_by_sbu_director_pm_self, font_style)
                    ws.write(row_num, 52, data.percentage_of_increment, font_style)
                    ws.write(row_num, 53, data.new_gross_salary_b, font_style)
                    ws.write(row_num, 54, data.cagr_three_years, font_style)
                    ws.write(row_num, 55, data.average_three_years, font_style)
                    ws.write(row_num, 56, data.average_actual, font_style)
                    ws.write(row_num, 57, data.kpi_overall, font_style)
                    ws.write(row_num, 58, data.weighted_average_kpi, font_style)
                    ws.write(row_num, 59, data.increment_with_kpi_percentage, font_style)
                    ws.write(row_num, 60, data.new_gross_salary_kpi_percentage, font_style)
                    ws.write(row_num, 61, data.gap_manual_formula, font_style)
                    ws.write(row_num, 62, data.remarks, font_style)
                    ws.write(row_num, 63, data.remarks_two, font_style)

                    row_num += 1

                wb.save(response)
                return response
            elif 'pdf_export' in request.POST:
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate("static/assets/pdf_files/Assessment Report.pdf",
                                        pagesize=reportlab.lib.pagesizes.letter)
                story = []
                elements = []
                columns = []
                parastyles = ParagraphStyle(
                    'header',
                    parent=styles['Normal'],
                    fontName='Helvetica-Bold',
                    fontSize=6,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                    leading=5
                )
                columns.insert(0,
                           [Paragraph('SL', parastyles),Paragraph('Employee Name', parastyles),Paragraph('Designation', parastyles),Paragraph('ID No', parastyles),Paragraph('DOJ', parastyles),Paragraph('Confirmation/Increment/No Increment', parastyles),
                           Paragraph('Duration', parastyles),Paragraph('SBU', parastyles),Paragraph('Sub SBU', parastyles),Paragraph('PM Name', parastyles),Paragraph('SBU Director Name', parastyles),Paragraph(' Effective Date', parastyles),Paragraph(' Total Salary and Allowance-'+str(current_year),parastyles),Paragraph('Basic-'+str(current_year),parastyles),
                           Paragraph('House Rent-'+str(current_year),parastyles),Paragraph('Medical Allowance-'+str(current_year),parastyles),

                           ])

                texstyles = ParagraphStyle(
                    'text',
                    parent=styles['Normal'],
                    fontSize=6,
                    alignment=TA_CENTER,
                    textColor=colors.black,
                    leading=5
                )
                j = 1

                for count, data in enumerate(datasets):
                    columns.insert(j, [Paragraph(str(j), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),
                                       Paragraph(str(data.employee.name), texstyles),

                                       ])
                    j = j + 1

                t = Table(columns, repeatRows=1, splitByRow=1)
                t.setStyle(TableStyle(
                    [
                        ('FONTSIZE', (0, 0), (-1, -1), 1),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))

                story.append(Paragraph("Assessment Report(" + str(datasets) + ")", parastyles))
                story.append(Spacer(1, 0.7 * inch))
                elements.append(t)
                story.append(t)
                doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
                fs = FileSystemStorage()
                with fs.open("static/assets/pdf_files/Assessment Report.pdf") as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Assessment Report.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
                return response
    except Exception as ex:
        messages.error(request, 'Data Not Found'+str(ex))
        return redirect('report:assessmentSbuWiseReport')
