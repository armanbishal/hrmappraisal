from multiprocessing import context

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse
from datetime import date, datetime
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
from django.utils.decorators import method_decorator
from usermanagement.decorators import login_required, access_permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

year = date.today()
current_year = year.year
first_last_year = year.year - 1
second_last_year = year.year - 2
third_last_year = year.year - 3


@login_required("logged_in", 'usermanagement:login')
def timmy(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    todays_date = date.today()
    employee = Employee.objects.all()
    context = {
        'year': todays_date.year,
        'employee': employee,
        'data': userdata
    }
    return render(request, 'example/random.html', context)


@login_required("logged_in", 'usermanagement:login')
def IndividualEmployeeDetails(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    year = date.today().year
    prev_year = date.today().year - 1

    try:
        kpi_performance_obj = KPIPerformance.objects.get(
            Q(id=id) &
            Q(year=current_year)
        )
        prev_kpi_performance_obj = KPIPerformance.objects.get(employee_id=kpi_performance_obj.employee_id,
                                                              year=prev_year)
        print('employee id', kpi_performance_obj.employee_id)
        print('prev ----', prev_kpi_performance_obj)

    except ObjectDoesNotExist:
        prev_kpi_performance_obj =''

    form = KPIPerformanceForm(instance=kpi_performance_obj)


    context = {
        'data': userdata,
        'kpi_performance_obj': kpi_performance_obj,
        'prev_kpi_performance_obj': prev_kpi_performance_obj,
        'form': form,
        'year': year,
        'prev_year': prev_year

    }
    return render(request, 'kpimanagement/kpiperformance/individualemployeedetails.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def EmployKPIPerformanceList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    kpilist = KPIPerformance.objects.filter(
        employee_id=request.session['employee']).order_by('-id')
    context = {
        'data': userdata,
        'kpilist': kpilist
    }
    return render(request, 'kpimanagement/kpiperformance/KPI_performance_employee.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def kpiPerformanceList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    employee = Employee.objects.all()
    year = date.today().year

    employee = KPIPerformance.objects.filter(year=current_year)

    context = {
        'data': userdata,
        'employee': employee
    }
    return render(request, 'kpimanagement/kpiperformance/kpi_performance_list.html', context)


@login_required("logged_in", 'usermanagement:login')
def IndividualKPIFrom(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    year = date.today().year

    try:
        kpi_performance_obj = KPIPerformance.objects.get(
            Q(employee_id=id) &
            Q(year=current_year)
        )
    except:
        kpi_performance_obj = KPIPerformance.objects.create(
            employee=Employee.objects.get(id=id),
            year=current_year,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            created_by_id=request.session['id'],
            updated_by_id=request.session['id'],
        )
        kpi_performance_obj.save()

    kpi_performance_obj = KPIPerformance.objects.get(
        Q(employee_id=id) &
        Q(year=current_year)
    )
    form = KPIPerformanceForm(instance=kpi_performance_obj)

    context = {
        'data': userdata,
        'kpi_performance_obj': kpi_performance_obj,
        'form': form,
        'year': year

    }
    return render(request, 'kpimanagement/kpiperformance/individual_KPI_from.html', context)


@login_required("logged_in", 'usermanagement:login')
def kpi_form(request):
    todays_date = date.today()
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    context = {
        "year": todays_date.year,
        'data': userdata,
        "year": todays_date.year,
    }
    return render(request, 'kpimanagement/kpiperformance/kpi_performance.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def EmployKPIPerformanceList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    kpilist = KPIPerformance.objects.filter(employee_id=request.session['employee']).order_by('-year')
    print(kpilist)
    context = {
        'data': userdata,
        'kpilist': kpilist
    }
    return render(request, 'kpimanagement/kpiperformance/KPI_performance_employee.html', context)


@login_required("logged_in", 'usermanagement:login')
def kpiPerformanceSave(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    em = Employee.objects.get(employee_id=userdata['username'])
    year = date.today().year

    try:
        kpi_performance_obj = KPIPerformance.objects.get(
            Q(employee_id=em.id) &
            Q(year=current_year)
        )
    except:
        kpi_performance_obj = KPIPerformance.objects.create(
            employee=Employee.objects.get(id=em.id),
            year=current_year,
            sbu_id=em.sbu_id,
            supervisor_id=em.supervisor_id,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            created_by_id=request.session['id'],
            updated_by_id=request.session['id'],
        )
        kpi_performance_obj.save()

    kpi_performance_obj = KPIPerformance.objects.get(
        Q(employee_id=em.id) &
        Q(year=current_year)
    )
    form = KPIPerformanceForm(instance=kpi_performance_obj)

    if request.method == "POST":
        if 'draft_save' in request.POST:
            kpi_performance = KPIPerformance.objects.get(
                Q(employee_id=em.id) &
                Q(year=current_year)
            )
            if request.POST.get('production') is not "":
                kpi_performance.production = request.POST.get('production')
            if request.POST.get('production_rating') is not "":
                kpi_performance.production_rating = KPIObjective.objects.get(
                    id=request.POST.get('production_rating'))
            if request.POST.get('production_weightage') is not "":
                kpi_performance.production_weightage = request.POST.get(
                    'production_weightage')
            if request.POST.get('support') is not "":
                kpi_performance.support = request.POST.get('support')
            if request.POST.get('support_rating') is not "":
                kpi_performance.support_rating = KPIObjective.objects.get(
                    id=request.POST.get('support_rating'))
            if request.POST.get('support_weightage') is not "":
                kpi_performance.support_weightage = request.POST.get(
                    'support_weightage')
            if request.POST.get('innovation') is not "":
                kpi_performance.innovation = request.POST.get('innovation')
            if request.POST.get('innovation_rating') is not "":
                kpi_performance.innovation_rating = KPIObjective.objects.get(
                    id=request.POST.get('innovation_rating'))
            if request.POST.get('innovation_weightage') is not "":
                kpi_performance.innovation_weightage = request.POST.get(
                    'innovation_weightage')
            if request.POST.get('people') is not "":
                kpi_performance.people = request.POST.get('people')
            if request.POST.get('people_rating') is not "":
                kpi_performance.people_rating = KPIObjective.objects.get(
                    id=request.POST.get('people_rating'))
            if request.POST.get('people_weightage') is not "":
                kpi_performance.people_weightage = request.POST.get(
                    'people_weightage')
            if request.POST.get('other') is not "":
                kpi_performance.other = request.POST.get('other')
            if request.POST.get('other_rating') is not "":
                kpi_performance.other_rating = KPIObjective.objects.get(
                    id=request.POST.get('other_rating'))
            if request.POST.get('other_weightage') is not "":
                kpi_performance.other_weightage = request.POST.get(
                    'other_weightage')
            if request.POST.get('courageous') is not "":
                kpi_performance.courageous = request.POST.get('courageous')
            if request.POST.get('courageous_rating') is not "":
                kpi_performance.courageous_rating = KPIValue.objects.get(
                    id=request.POST.get('courageous_rating'))
            if request.POST.get('teamwork') is not "":
                kpi_performance.teamwork = request.POST.get('teamwork')
            if request.POST.get('teamwork_rating') is not "":
                kpi_performance.teamwork_rating = KPIValue.objects.get(
                    id=request.POST.get('teamwork_rating'))
            if request.POST.get('responsive') is not "":
                kpi_performance.responsive = request.POST.get('responsive')
            if request.POST.get('responsive_rating') is not "":
                kpi_performance.responsive_rating = KPIValue.objects.get(
                    id=request.POST.get('responsive_rating'))
            if request.POST.get('creative') is not "":
                kpi_performance.creative = request.POST.get('creative')
            if request.POST.get('creative_rating') is not "":
                kpi_performance.creative_rating = KPIValue.objects.get(
                    id=request.POST.get('creative_rating'))
            if request.POST.get('trustworthy') is not "":
                kpi_performance.trustworthy = request.POST.get('trustworthy')
            if request.POST.get('trustworthy_rating') is not "":
                kpi_performance.trustworthy_rating = KPIValue.objects.get(
                    id=request.POST.get('trustworthy_rating'))
            if request.POST.get('other_sustainable_achievement') is not "":
                kpi_performance.other_sustainable_achievement = request.POST.get(
                    'other_sustainable_achievement')
            if request.POST.get('significant_issue') is not "":
                kpi_performance.significant_issue = request.POST.get(
                    'significant_issue')
            if request.POST.get('individual_comment') is not "":
                kpi_performance.individual_comment = request.POST.get(
                    'individual_comment')
            if request.POST.get('manager_comment') is not "":
                kpi_performance.manager_comment = request.POST.get(
                    'manager_comment')
            if request.POST.get('senior_manager_functional_head_comment') is not "":
                kpi_performance.senior_manager_functional_head_comment = request.POST.get(
                    'senior_manager_functional_head_comment')
            if request.POST.get('director_chief_operating_officer_comment') is not "":
                kpi_performance.director_chief_operating_officer_comment = request.POST.get(
                    'director_chief_operating_officer_comment')
            if request.POST.get('overall_performance') is not "":
                kpi_performance.overall_performance = request.POST.get(
                    'overall_performance')
            kpi_performance.created_date = datetime.now()
            kpi_performance.updated_date = datetime.now()
            kpi_performance.created_by_id = request.session['id']
            kpi_performance.updated_by_id = request.session['id']
            kpi_performance.save()
            messages.success(request, 'Data Successfully Saved As Draft')
            return redirect('kpimanagement:kpi_form')

        if 'submit' in request.POST:
            kpi_performance = KPIPerformance.objects.get(
                Q(employee_id=em.id) &
                Q(year=current_year)
            )
            kpi_performance.flag = True
            if request.POST.get('production') is not "":
                kpi_performance.production = request.POST.get('production')
            if request.POST.get('production_rating') is not "":
                kpi_performance.production_rating = KPIObjective.objects.get(
                    id=request.POST.get('production_rating'))
            if request.POST.get('production_weightage') is not "":
                kpi_performance.production_weightage = request.POST.get(
                    'production_weightage')
            if request.POST.get('support') is not "":
                kpi_performance.support = request.POST.get('support')
            if request.POST.get('support_rating') is not "":
                kpi_performance.support_rating = KPIObjective.objects.get(
                    id=request.POST.get('support_rating'))
            if request.POST.get('support_weightage') is not "":
                kpi_performance.support_weightage = request.POST.get(
                    'support_weightage')
            if request.POST.get('innovation') is not "":
                kpi_performance.innovation = request.POST.get('innovation')
            if request.POST.get('innovation_rating') is not "":
                kpi_performance.innovation_rating = KPIObjective.objects.get(
                    id=request.POST.get('innovation_rating'))
            if request.POST.get('innovation_weightage') is not "":
                kpi_performance.innovation_weightage = request.POST.get(
                    'innovation_weightage')
            if request.POST.get('people') is not "":
                kpi_performance.people = request.POST.get('people')
            if request.POST.get('people_rating') is not "":
                kpi_performance.people_rating = KPIObjective.objects.get(
                    id=request.POST.get('people_rating'))
            if request.POST.get('people_weightage') is not "":
                kpi_performance.people_weightage = request.POST.get(
                    'people_weightage')
            if request.POST.get('other') is not "":
                kpi_performance.other = request.POST.get('other')
            if request.POST.get('other_rating') is not "":
                kpi_performance.other_rating = KPIObjective.objects.get(
                    id=request.POST.get('other_rating'))
            if request.POST.get('other_weightage') is not "":
                kpi_performance.other_weightage = request.POST.get(
                    'other_weightage')
            if request.POST.get('courageous') is not "":
                kpi_performance.courageous = request.POST.get('courageous')
            if request.POST.get('courageous_rating') is not "":
                kpi_performance.courageous_rating = KPIValue.objects.get(
                    id=request.POST.get('courageous_rating'))
            if request.POST.get('teamwork') is not "":
                kpi_performance.teamwork = request.POST.get('teamwork')
            if request.POST.get('teamwork_rating') is not "":
                kpi_performance.teamwork_rating = KPIValue.objects.get(
                    id=request.POST.get('teamwork_rating'))
            if request.POST.get('responsive') is not "":
                kpi_performance.responsive = request.POST.get('responsive')
            if request.POST.get('responsive_rating') is not "":
                kpi_performance.responsive_rating = KPIValue.objects.get(
                    id=request.POST.get('responsive_rating'))
            if request.POST.get('creative') is not "":
                kpi_performance.creative = request.POST.get('creative')
            if request.POST.get('creative_rating') is not "":
                kpi_performance.creative_rating = KPIValue.objects.get(
                    id=request.POST.get('creative_rating'))
            if request.POST.get('trustworthy') is not "":
                kpi_performance.trustworthy = request.POST.get('trustworthy')
            if request.POST.get('trustworthy_rating') is not "":
                kpi_performance.trustworthy_rating = KPIValue.objects.get(
                    id=request.POST.get('trustworthy_rating'))
            if request.POST.get('other_sustainable_achievement') is not "":
                kpi_performance.other_sustainable_achievement = request.POST.get(
                    'other_sustainable_achievement')
            if request.POST.get('significant_issue') is not "":
                kpi_performance.significant_issue = request.POST.get(
                    'significant_issue')
            if request.POST.get('individual_comment') is not "":
                kpi_performance.individual_comment = request.POST.get(
                    'individual_comment')
            if request.POST.get('manager_comment') is not "":
                kpi_performance.manager_comment = request.POST.get(
                    'manager_comment')
            if request.POST.get('senior_manager_functional_head_comment') is not "":
                kpi_performance.senior_manager_functional_head_comment = request.POST.get(
                    'senior_manager_functional_head_comment')
            if request.POST.get('director_chief_operating_officer_comment') is not "":
                kpi_performance.director_chief_operating_officer_comment = request.POST.get(
                    'director_chief_operating_officer_comment')
            if request.POST.get('overall_performance') is not "":
                kpi_performance.overall_performance = request.POST.get(
                    'overall_performance')
            kpi_performance.created_date = datetime.now()
            kpi_performance.updated_date = datetime.now()
            kpi_performance.created_by_id = request.session['id']
            kpi_performance.updated_by_id = request.session['id']
            kpi_performance.save()
            messages.success(request, 'Data Successfully Submitted')
            return redirect('kpimanagement:kpi_form')

    context = {'data': userdata,
               'kpi_performance_obj': kpi_performance_obj,
               'form': form,
               'year': year}
    return render(request, 'kpimanagement/kpiperformance/kpi_performance.html', context)


@login_required("logged_in", 'usermanagement:login')
def employeeAssign(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    form = EmployeeAssignForm
    sbu = SBU.objects.all()
    supervisor = Supervisor.objects.all()
    employee = Employee.objects.all()

    context = {'data': userdata,
               'sbu': sbu,
               'supervisor': supervisor,
               'employee': employee,
               'form': form}
    return render(request, 'kpimanagement/employeeassign/employee_assign.html', context)


def EmployeeAssignSupervisorUpdate(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    supervisor = request.POST.getlist('supervisor')
    print('supervisor',request.POST.getlist('supervisor'))
    print('employee',request.POST.getlist('employee'))
    sbu = request.POST['sbu']
    duration_startdate = request.POST['duration_startdate']
    duration_enddate = request.POST['duration_enddate']
    emp = Employee.objects.filter(sbu=request.POST['sbu'])
    # for assess in emp:
    #     emp_ass_sup = EmployeeAssignSupervisor.objects.create(supervisor_id=supervisor, sbu_id=sbu,
    #                                                           employee_id=assess.id, created_date=datetime.now(),
    #                                                           updated_date=datetime.now(),duration_startdate=duration_startdate,
    #                                                           duration_enddate=duration_enddate,
    #                                                           created_by_id=request.session['id'],
    #                                                           updated_by_id=request.session['id'])
    #     emp_ass_sup.save()
    sbu = SBU.objects.all()
    supervisor = Supervisor.objects.all()
    employee = Employee.objects.all()
    # messages.success(request, "Data Successfully Saved")
    # return redirect("kpimanagement:employeeAssign")

    context = {'data': userdata,
               'sbu': sbu,
               'supervisor': supervisor,
               'employee': employee,
               'messages': 'Data Successfully Saved'
               }
    return render(request, 'kpimanagement/employeeassign/employee_assign.html', context)


def assessmentDetailsUpdate(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()

    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    employee = Employee.objects.all()

    if 'sbu-search' in request.POST:
        sbu_flag = 1
        form = AssessmentDetailForm()
        sbu_list = SBU.objects.all()
        employee = Employee.objects.all()

        for em in employee:
            try:
                assessment_details_obj = AssessmentDetail.objects.get(
                    Q(employee_id=em.id) &
                    Q(year=current_year) &
                    Q(employee__date_of_joining__lt=date(current_year, 1, 1))
                )
            except:
                empall = Employee.objects.get(id=em.id)
                assessment_details_obj = AssessmentDetail.objects.create(
                    employee=Employee.objects.get(id=em.id),
                    sbu_id=empall.sbu.id,
                    supervisor_id=empall.supervisor.id,
                    total_salary_and_allowance=em.total_salary_and_allowance,
                    basic_salary=em.basic_salary,
                    house_rent=em.house_rent,
                    medical_allowance=em.medical_allowance,
                    conveyance_allowance=em.conveyance_allowance,
                    wppf=em.wppf,
                    special_bonus=em.special_bonus,
                    mobile_and_other_allowance=em.mobile_and_other_allowance,
                    project_expense=em.project_expense,
                    other_benefit=em.other_benefit,
                    gross_salary=em.gross_salary,
                    pf_com_contribution=em.pf_com_contribution,
                    year=date.today().year,
                    created_date=datetime.now(),
                    updated_date=datetime.now(),
                    created_by_id=request.session['id'],
                    updated_by_id=request.session['id'],
                )
                assessment_details_obj.save()

        sbu_search = request.POST.get('sbu')

        assessment_details = AssessmentDetail.objects.filter(
            Q(employee__sbu__name=sbu_search) &
            Q(year=current_year) &
            Q(employee__date_of_joining__lt=date(current_year, 1, 1))
        )

        emp = Employee.objects.all()
        for assess in assessment_details:
            if assess.employee not in emp:
                assess.delete()

        context = {'assessment_details': assessment_details,
                   'sbu_search': sbu_search,
                   'sbu_flag': sbu_flag,
                   'form': form,
                   'sbu_list': sbu_list,
                   'year': year,
                   'current_year': current_year,
                   'first_last_year': first_last_year,
                   'second_last_year': second_last_year,
                   'third_last_year': third_last_year,
                   'data': userdata,
                   'kpi_objective_obj': kpi_objective_obj,
                   'kpi_value_obj': kpi_value_obj,
                   'hr_rating_obj': hr_rating_obj,
                   'criticality_obj': criticality_obj,
                   'potential_for_improvement_obj': potential_for_improvement_obj,
                   'technical_implementation_operational_obj': technical_implementation_operational_obj,
                   'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
                   'best_performer_team_obj': best_performer_team_obj,
                   'best_innovator_team_obj': best_innovator_team_obj,
                   'employee': employee,
                   }
        return render(request, 'kpimanagement/assessmentdetails/assessment_details_update.html', context)

    if 'detail-save' in request.POST:
        em_id = request.POST.getlist('getEmID')
        kpi_objective = request.POST.getlist('kpi_objective')
        kpi_value = request.POST.getlist('kpi_value')
        kpi_overall = request.POST.getlist('kpi_overall')
        hr_rating = request.POST.getlist('hr_rating')
        criticality = request.POST.getlist('criticality')
        potential_for_improvement = request.POST.getlist(
            'potential_for_improvement')
        technical_implementation_operational = request.POST.getlist(
            'technical_implementation_operational')
        top_average_bottom_performer = request.POST.getlist(
            'top_average_bottom_performer')
        best_performer_team = request.POST.getlist('best_performer_team')
        best_innovator_team = request.POST.getlist('best_innovator_team')
        proposed_designation = request.POST.getlist('proposed_designation')
        remarks = request.POST.getlist('remarks')

        for i in range(0, len(em_id)):
            em = Employee.objects.get(employee_id=em_id[i])
            assessment_details_update = AssessmentDetail.objects.get(
                employee_id=em.id)
            assessment_details_update.kpi_objective = None
            assessment_details_update.kpi_value = None
            assessment_details_update.hr_rating = None
            if kpi_objective[i] is not "":
                assessment_details_update.kpi_objective = KPIObjective.objects.get(
                    id=kpi_objective[i])
            if kpi_value[i] is not "":
                assessment_details_update.kpi_value = KPIValue.objects.get(
                    id=kpi_value[i])
            if hr_rating[i] is not "":
                assessment_details_update.hr_rating = HRRating.objects.get(
                    id=hr_rating[i])
            if kpi_objective[i] is not "" and kpi_value[i] is not "" and hr_rating[i] is not "":
                assessment_details_update.kpi_overall = assessment_details_update.kpi_objective.grade + \
                                                        assessment_details_update.kpi_value.grade + \
                                                        assessment_details_update.hr_rating.grade
            if criticality[i] is not "":
                assessment_details_update.criticality = Criticality.objects.get(
                    id=criticality[i])
            if potential_for_improvement[i] is not "":
                assessment_details_update.potential_for_improvement = PotentialForImprovement.objects.get(
                    id=potential_for_improvement[i])
            if technical_implementation_operational[i] is not "":
                assessment_details_update.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                    id=technical_implementation_operational[i])
            if top_average_bottom_performer[i] is not "":
                assessment_details_update.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                    id=top_average_bottom_performer[i])
            if best_performer_team[i] is not "":
                assessment_details_update.best_performer_team = BestPerformerTeam.objects.get(
                    id=best_performer_team[i])
            if best_innovator_team[i] is not "":
                assessment_details_update.best_innovator_team = BestInnovatorTeam.objects.get(
                    id=best_innovator_team[i])
            if proposed_designation[i] is not "":
                assessment_details_update.proposed_designation = proposed_designation[i]
            if remarks[i] is not "":
                assessment_details_update.remarks = remarks[i]
            assessment_details_update.year = year.year
            assessment_details_update.created_date = datetime.now()
            assessment_details_update.updated_date = datetime.now()
            assessment_details_update.created_by_id = request.session['id']
            assessment_details_update.updated_by_id = request.session['id']
            assessment_details_update.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessment_details_update")

    context = {'year': year,
               'data': userdata,
               'kpi_objective_obj': kpi_objective_obj,
               'kpi_value_obj': kpi_value_obj,
               'hr_rating_obj': hr_rating_obj,
               'criticality_obj': criticality_obj,
               'potential_for_improvement_obj': potential_for_improvement_obj,
               'technical_implementation_operational_obj': technical_implementation_operational_obj,
               'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
               'best_performer_team_obj': best_performer_team_obj,
               'best_innovator_team_obj': best_innovator_team_obj,
               'sbu_list': sbu_list,
               'employee': employee,
               'form': form,
               'sbu_flag': sbu_flag, }
    return render(request, 'kpimanagement/assessmentdetails/assessment_details_update.html', context)


def assessmentDetailsUpdateSingle(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()
    best_performer_organization_obj = BestPerformerOrganization.objects.all()
    best_performer_pm_obj = BestPerformerPM.objects.all()
    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    get_assesment_data = AssessmentDetail.objects.get(id=id)
    # print(kpi_objective_obj)
    # print('best_performer_org',get_assesment_data.best_performer_org)
    # print('confirmation_increment_noincrement',get_assesment_data.confirmation_increment_noincrement)
    employee = Employee.objects.get(id=get_assesment_data.employee_id)

    if 'detail-save' in request.POST:
        # em_id = request.POST.getlist('getEmID')
        em_id = employee.id
        em_ds_id = employee.employee_id
        confirmation_increment_noincrement = request.POST['confirmation_increment_noincrement']
        kpi_objective = request.POST['kpi_objective']
        kpi_value = request.POST['kpi_value']
        # kpi_overall = request.POST['kpi_overall']
        hr_rating = request.POST['hr_rating']
        criticality = request.POST['criticality']
        potential_for_improvement = request.POST['potential_for_improvement']
        technical_implementation_operational = request.POST['technical_implementation_operational']
        top_average_bottom_performer = request.POST['top_average_bottom_performer']
        best_performer_team = request.POST['best_performer_team']
        best_performer_organization = request.POST['best_performer_org']
        best_performer_pm = request.POST['best_performer_pm']
        best_innovator_team = request.POST['best_innovator_team']
        proposed_designation = request.POST['proposed_designation']
        proposed_by_sbu_director_pm_self = request.POST['proposed_by_sbu_director_pm_self']
        remarks = request.POST['remarks']

        # for i in range(0, len(em_id)):
        em = Employee.objects.get(employee_id=em_ds_id)
        assessment_details_update = AssessmentDetail.objects.get(
            employee_id=em_id)
        assessment_details_update.kpi_objective = None
        assessment_details_update.kpi_value = None
        assessment_details_update.hr_rating = None
        if kpi_objective is not "":
            assessment_details_update.kpi_objective = KPIObjective.objects.get(
                id=kpi_objective)
        if kpi_value is not "":
            assessment_details_update.kpi_value = KPIValue.objects.get(
                id=kpi_value)
        if hr_rating is not "":
            assessment_details_update.hr_rating = HRRating.objects.get(
                id=hr_rating)
        if kpi_objective is not "" and kpi_value is not "" and hr_rating is not "":
            assessment_details_update.kpi_overall = assessment_details_update.kpi_objective.grade + \
                                                    assessment_details_update.kpi_value.grade + \
                                                    assessment_details_update.hr_rating.grade
        if criticality is not "":
            assessment_details_update.criticality = Criticality.objects.get(
                id=criticality)
        if potential_for_improvement is not "":
            assessment_details_update.potential_for_improvement = PotentialForImprovement.objects.get(
                id=potential_for_improvement)
        if technical_implementation_operational is not "":
            assessment_details_update.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                id=technical_implementation_operational)
        if top_average_bottom_performer is not "":
            assessment_details_update.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                id=top_average_bottom_performer)
        if best_performer_team is not "":
            assessment_details_update.best_performer_team = BestPerformerTeam.objects.get(
                id=best_performer_team)
        if best_performer_organization is not "":
            assessment_details_update.best_performer_org = BestPerformerOrganization.objects.get(
                id=best_performer_organization)
        if best_performer_pm is not "":
            assessment_details_update.best_performer_pm = BestPerformerPM.objects.get(
                id=best_performer_pm)
        if best_innovator_team is not "":
            assessment_details_update.best_innovator_team = BestInnovatorTeam.objects.get(
                id=best_innovator_team)
        if proposed_designation is not "":
            assessment_details_update.proposed_designation = proposed_designation
        if remarks is not "":
            assessment_details_update.remarks = remarks
        if confirmation_increment_noincrement is not "":
            assessment_details_update.confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.get(
                id=confirmation_increment_noincrement)
        if assessment_details_update.gross_salary is not None:
            if assessment_details_update.gross_salary >= 120000.0:
                assessment_details_update.gross_salary = (
                                                                 assessment_details_update.gross_salary * 2.75) / 100
                assessment_details_update.salary_grade = 'A'
            elif 100000.0 <= assessment_details_update.gross_salary < 120000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 3.25) / 100
                assessment_details_update.salary_grade = 'B'
            elif 90000.0 <= assessment_details_update.gross_salary < 100000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 4.00) / 100
                assessment_details_update.salary_grade = 'C'
            elif 80000.0 <= assessment_details_update.gross_salary < 90000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 5.50) / 100
                assessment_details_update.salary_grade = 'D'
            elif 60000.0 <= em.gross_salary < 70000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 6.50) / 100
                assessment_details_update.salary_grade = 'E'
            elif 40000.0 <= assessment_details_update.gross_salary < 50000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 8.50) / 100
                assessment_details_update.salary_grade = 'F'
            elif 30000.0 <= assessment_details_update.gross_salary < 40000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 11) / 100
                assessment_details_update.salary_grade = 'G'
            elif 20000.0 <= assessment_details_update.gross_salary < 30000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 15) / 100
                assessment_details_update.salary_grade = 'H'
            elif assessment_details_update.gross_salary < 20000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 17) / 100
                assessment_details_update.salary_grade = 'K'
        if assessment_details_update.gross_salary is not None and assessment_details_update.increment_amount_a is not None:
            assessment_details_update.hr_new_gross_salary_a = em.gross_salary + \
                                                              assessment_details_update.increment_amount_a
            assessment_details_update.percentage_hr_a = (
                                                                assessment_details_update.increment_amount_a / assessment_details_update.gross_salary) * 100
            assessment_details_update.fixed_increment_b = (
                                                                  assessment_details_update.gross_salary * 10) / 100
            assessment_details_update.fixed_increment_new_gross_salary_b = assessment_details_update.fixed_increment_b + \
                                                                           assessment_details_update.gross_salary

        total_salary_count_sbu = 0
        emp = Employee.objects.filter(sbu=em.sbu)
        for e in emp:
            if e.gross_salary is not None:
                total_salary_count_sbu = total_salary_count_sbu + e.gross_salary
        assessment_details_update.team_distribution_percentage_c = (
                                                                           total_salary_count_sbu * 10) / 100

        if assessment_details_update.fixed_increment_new_gross_salary_b is not None and assessment_details_update.fixed_increment_b is not None:
            assessment_details_update.difference_new_salary_a_new_salary_b = abs(
                assessment_details_update.fixed_increment_new_gross_salary_b - assessment_details_update.hr_new_gross_salary_a)

        if proposed_by_sbu_director_pm_self is not '':
            assessment_details_update.proposed_by_sbu_director_pm_self = proposed_by_sbu_director_pm_self

        if em.gross_salary is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.percentage_of_increment = round(
                ((float(assessment_details_update.proposed_by_sbu_director_pm_self) / em.gross_salary) * 100))

        if em.gross_salary is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.new_gross_salary_b = float(
                assessment_details_update.proposed_by_sbu_director_pm_self) + em.gross_salary

        assessment_details_report_last_year = None
        assessment_details_report_before_last_year = None

        try:
            assessment_details_report_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=first_last_year)
            )
        except:
            pass

        try:
            assessment_details_report_before_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=second_last_year)
            )
        except:
            pass

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.new_gross_salary_b is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None and assessment_details_report_last_year.proposed_by_sbu_director_pm_self and assessment_details_report_last_year.increment_amount_a:
                assessment_details_update.cagr_three_years = round((((
                                                                             assessment_details_update.new_gross_salary_b / (
                                                                             assessment_details_update.new_gross_salary_b - float(
                                                                         assessment_details_update.proposed_by_sbu_director_pm_self) - float(
                                                                         assessment_details_update.proposed_by_sbu_director_pm_self) - assessment_details_report_last_year.increment_amount_a)) ** (
                                                                             1 / 3)) - 1) * 100, 2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_update.average_three_years = round(
                    ((assessment_details_update.percentage_of_increment +
                      assessment_details_report_last_year.percentage_of_increment +
                      assessment_details_report_before_last_year.percentage_of_increment) / 3) * 100,
                    2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_update.average_actual = round((((
                        assessment_details_update.percentage_of_increment +
                        assessment_details_report_last_year.percentage_of_increment +
                        assessment_details_report_before_last_year.percentage_of_increment)) / 3) * 100, 2)

        if assessment_details_update.weighted_average_kpi is not None and em.gross_salary is not None:
            assessment_details_update.increment_with_kpi_percentage = round(
                ((assessment_details_update.weighted_average_kpi * em.gross_salary) / 100), 2)

        if assessment_details_update.increment_with_kpi_percentage is not None and em.gross_salary is not None:
            assessment_details_update.new_gross_salary_kpi_percentage = assessment_details_update.increment_with_kpi_percentage + em.gross_salary

        if assessment_details_update.increment_with_kpi_percentage is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.gap_manual_formula = abs(
                assessment_details_update.increment_with_kpi_percentage - float(
                    assessment_details_update.proposed_by_sbu_director_pm_self))

        if assessment_details_update.new_gross_salary_b is not None:
            em.gross_salary = assessment_details_update.new_gross_salary_b
            em.basic_salary = (assessment_details_update.new_gross_salary_b * 50) / 100
            em.house_rent = (assessment_details_update.new_gross_salary_b * 30) / 100
            em.medical_allowance = (assessment_details_update.new_gross_salary_b * 12.5) / 100
            em.conveyance_allowance = (assessment_details_update.new_gross_salary_b * 7.5) / 100
            em.save()
        assessment_details_update.year = year.year
        assessment_details_update.created_date = datetime.now()
        assessment_details_update.updated_date = datetime.now()
        assessment_details_update.created_by_id = request.session['id']
        assessment_details_update.updated_by_id = request.session['id']
        assessment_details_update.flag = 1
        assessment_details_update.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessmentSupervisorList")

    context = {
        'year': year,
        'data': userdata,
        'getdata': get_assesment_data,
        'kpi_objective_obj': kpi_objective_obj,
        'kpi_value_obj': kpi_value_obj,
        'hr_rating_obj': hr_rating_obj,
        'criticality_obj': criticality_obj,
        'potential_for_improvement_obj': potential_for_improvement_obj,
        'technical_implementation_operational_obj': technical_implementation_operational_obj,
        'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
        'best_performer_team_obj': best_performer_team_obj,
        'best_innovator_team_obj': best_innovator_team_obj,
        'best_performer_organization_obj': best_performer_organization_obj,
        'best_performer_pm_obj': best_performer_pm_obj,
        'confirmantion_increment_noincrement_obj': confirmation_increment_noincrement,
        'sbu_list': sbu_list,
        'employee': employee,
        'form': form,
        'sbu_flag': sbu_flag,
        'current_year': current_year}

    return render(request, 'kpimanagement/assessmentdetails/assessment_details_update_single.html', context)


@login_required("logged_in", 'usermanagement:login')
def assessmentReport(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    confirmantion_increment_noincrement_obj = ConfirmationIncrementNoincrement.objects.all()
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_performer_organization_obj = BestPerformerOrganization.objects.all()
    best_performer_pm_obj = BestPerformerPM.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()
    evaluation_obj = Evaluation.objects.all()

    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    employee = Employee.objects.all()

    if 'sbu-search' in request.POST:
        sbu_flag = 1
        form = AssessmentDetailForm()
        sbu_list = SBU.objects.all()
        employee = Employee.objects.all()

        year_com = str(current_year) + '-1-1'
        for em in employee:
            try:
                assessment_details_obj = AssessmentDetail.objects.get(
                    Q(employee_id=em.id) &
                    Q(year=current_year)
                    # Using Q(employee__date_of_joining__lt=year_com) makes the data tripled!
                )
            except:
                empall = Employee.objects.get(id=em.id)
                assessment_details_obj = AssessmentDetail.objects.create(
                    employee=Employee.objects.get(id=em.id),
                    sbu_id=empall.sbu,
                    supervisor_id=empall.supervisor,
                    total_salary_and_allowance=em.total_salary_and_allowance,
                    basic_salary=em.basic_salary,
                    house_rent=em.house_rent,
                    medical_allowance=em.medical_allowance,
                    conveyance_allowance=em.conveyance_allowance,
                    wppf=em.wppf,
                    special_bonus=em.special_bonus,
                    mobile_and_other_allowance=em.mobile_and_other_allowance,
                    project_expense=em.project_expense,
                    other_benefit=em.other_benefit,
                    gross_salary=em.gross_salary,
                    pf_com_contribution=em.pf_com_contribution,
                    year=current_year,
                    created_date=datetime.now(),
                    updated_date=datetime.now(),
                    created_by_id=request.session['id'],
                    updated_by_id=request.session['id'],
                )
                assessment_details_obj.save()

        sbu_search = request.POST.get('sbu')

        year_com = date(current_year, 1, 1)
        assessment_details = AssessmentDetail.objects.filter(
            Q(employee__sbu__name=sbu_search) &
            Q(year=current_year) &
            Q(employee__date_of_joining__lt=year_com)
        )

        emp = Employee.objects.all()
        for assess in assessment_details:
            if assess.employee not in emp:
                assess.delete()

        context = {'assessment_details': assessment_details,
                   'sbu_search': sbu_search,
                   'sbu_flag': sbu_flag,
                   'form': form,
                   'sbu_list': sbu_list,
                   'year': year,
                   'current_year': current_year,
                   'first_last_year': first_last_year,
                   'second_last_year': second_last_year,
                   'third_last_year': third_last_year,
                   'data': userdata,
                   'confirmantion_increment_noincrement_obj': confirmantion_increment_noincrement_obj,
                   'evaluation_obj': evaluation_obj,
                   'kpi_objective_obj': kpi_objective_obj,
                   'kpi_value_obj': kpi_value_obj,
                   'hr_rating_obj': hr_rating_obj,
                   'criticality_obj': criticality_obj,
                   'potential_for_improvement_obj': potential_for_improvement_obj,
                   'technical_implementation_operational_obj': technical_implementation_operational_obj,
                   'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
                   'best_performer_team_obj': best_performer_team_obj,
                   'best_performer_organization_obj': best_performer_organization_obj,
                   'best_performer_pm_obj': best_performer_pm_obj,
                   'best_innovator_team_obj': best_innovator_team_obj,
                   'employee': employee,
                   }
        return render(request, 'kpimanagement/assessmentreport/assessmentreport.html', context)

    if 'report-save' in request.POST:
        em_id = request.POST.getlist('getEmID')

        cofirmation_increment_noincrement = request.POST.getlist(
            'confirmation_increment_noincrement')
        # evaluation = request.POST.getlist('evaluation')
        kpi_objective = request.POST.getlist('kpi_objective')
        kpi_value = request.POST.getlist('kpi_value')
        hr_rating = request.POST.getlist('hr_rating')
        kpi_overall = request.POST.getlist('kpi_overall')
        criticality = request.POST.getlist('criticality')
        potential_for_improvement = request.POST.getlist(
            'potential_for_improvement')
        technical_implementation_operational = request.POST.getlist(
            'technical_implementation_operational')
        top_average_bottom_performer = request.POST.getlist(
            'top_average_bottom_performer')
        best_performer_team = request.POST.getlist('best_performer_team')
        best_performer_organization = request.POST.getlist(
            'best_performer_org')
        best_performer_pm = request.POST.getlist('best_performer_pm')
        best_innovator_team = request.POST.getlist('best_innovator_team')
        proposed_designation = request.POST.getlist('proposed_designation')
        proposed_by_sbu_director_pm_self = request.POST.getlist(
            'proposed_by_sbu_director_pm_self')
        remarks = request.POST.getlist('remarks')
        remarks_two = request.POST.getlist('remarks_two')

        for i in range(0, len(em_id)):
            em = Employee.objects.get(employee_id=em_id[i])
            assessment_details_report = AssessmentDetail.objects.get(
                employee_id=em.id, year=current_year)
            assessment_details_report.kpi_objective = None
            assessment_details_report.kpi_value = None
            assessment_details_report.hr_rating = None
            if cofirmation_increment_noincrement[i] is not "":
                assessment_details_report.confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.get(
                    id=cofirmation_increment_noincrement[i])
            if kpi_objective[i] is not "":
                assessment_details_report.kpi_objective = KPIObjective.objects.get(
                    id=kpi_objective[i])
                assessment_details_report.percentage_kpi_objective = assessment_details_report.kpi_objective.percentage
            if kpi_value[i] is not "":
                assessment_details_report.kpi_value = KPIValue.objects.get(
                    id=kpi_value[i])
                assessment_details_report.percentage_kpi_value = assessment_details_report.kpi_value.percentage
            if hr_rating[i] is not "":
                assessment_details_report.hr_rating = HRRating.objects.get(
                    id=hr_rating[i])
                assessment_details_report.percentage_kpi_hr = assessment_details_report.hr_rating.percentage
            if kpi_objective[i] is not "" and kpi_value[i] is not "" and hr_rating[i] is not "":
                assessment_details_report.kpi_overall = assessment_details_report.kpi_objective.grade + \
                                                        assessment_details_report.kpi_value.grade + \
                                                        assessment_details_report.hr_rating.grade
            if kpi_objective[i] is not "" and kpi_value[i] is not "" and hr_rating[i] is not "":
                assessment_details_report.weighted_average_kpi = round(((
                                                                                assessment_details_report.kpi_objective.percentage * 0.5) + (
                                                                                assessment_details_report.kpi_value.percentage * 0.3) + (
                                                                                assessment_details_report.hr_rating.percentage * 0.2)),
                                                                       2)
            if criticality[i] is not "":
                assessment_details_report.criticality = Criticality.objects.get(
                    id=criticality[i])
            if potential_for_improvement[i] is not "":
                assessment_details_report.potential_for_improvement = PotentialForImprovement.objects.get(
                    id=potential_for_improvement[i])
            if technical_implementation_operational[i] is not "":
                assessment_details_report.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                    id=technical_implementation_operational[i])
            if top_average_bottom_performer[i] is not "":
                assessment_details_report.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                    id=top_average_bottom_performer[i])
            if best_performer_team[i] is not "":
                assessment_details_report.best_performer_team = BestPerformerTeam.objects.get(
                    id=best_performer_team[i])
            if best_performer_organization[i] is not "":
                assessment_details_report.best_performer_org = BestPerformerOrganization.objects.get(
                    id=best_performer_organization[i])
            if best_performer_pm[i] is not "":
                assessment_details_report.best_performer_pm = BestPerformerPM.objects.get(
                    id=best_performer_pm[i])
            if best_innovator_team[i] is not "":
                assessment_details_report.best_innovator_team = BestInnovatorTeam.objects.get(
                    id=best_innovator_team[i])
            if proposed_designation[i] is not "":
                assessment_details_report.proposed_designation = proposed_designation[i]
            if remarks[i] is not "":
                assessment_details_report.remarks = remarks[i]
            if remarks_two[i] is not "":
                assessment_details_report.remarks_two = remarks_two[i]
            if assessment_details_report.gross_salary is not None:
                if assessment_details_report.gross_salary >= 120000.0:
                    assessment_details_report.gross_salary = (
                                                                     assessment_details_report.gross_salary * 2.75) / 100
                    assessment_details_report.salary_grade = 'A'
                elif 100000.0 <= assessment_details_report.gross_salary < 120000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 3.25) / 100
                    assessment_details_report.salary_grade = 'B'
                elif 90000.0 <= assessment_details_report.gross_salary < 100000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 4.00) / 100
                    assessment_details_report.salary_grade = 'C'
                elif 80000.0 <= assessment_details_report.gross_salary < 90000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 5.50) / 100
                    assessment_details_report.salary_grade = 'D'
                elif 60000.0 <= em.gross_salary < 70000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 6.50) / 100
                    assessment_details_report.salary_grade = 'E'
                elif 40000.0 <= assessment_details_report.gross_salary < 50000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 8.50) / 100
                    assessment_details_report.salary_grade = 'F'
                elif 30000.0 <= assessment_details_report.gross_salary < 40000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 11) / 100
                    assessment_details_report.salary_grade = 'G'
                elif 20000.0 <= assessment_details_report.gross_salary < 30000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 15) / 100
                    assessment_details_report.salary_grade = 'H'
                elif assessment_details_report.gross_salary < 20000.0:
                    assessment_details_report.increment_amount_a = (
                                                                           assessment_details_report.gross_salary * 17) / 100
                    assessment_details_report.salary_grade = 'K'
            if assessment_details_report.gross_salary is not None and assessment_details_report.increment_amount_a is not None:
                assessment_details_report.hr_new_gross_salary_a = em.gross_salary + \
                                                                  assessment_details_report.increment_amount_a
                assessment_details_report.percentage_hr_a = (
                                                                    assessment_details_report.increment_amount_a / assessment_details_report.gross_salary) * 100
                assessment_details_report.fixed_increment_b = (
                                                                      assessment_details_report.gross_salary * 10) / 100
                assessment_details_report.fixed_increment_new_gross_salary_b = assessment_details_report.fixed_increment_b + \
                                                                               assessment_details_report.gross_salary

            total_salary_count_sbu = 0
            emp = Employee.objects.filter(sbu=em.sbu)
            for e in emp:
                if e.gross_salary is not None:
                    total_salary_count_sbu = total_salary_count_sbu + e.gross_salary
            assessment_details_report.team_distribution_percentage_c = (
                                                                               total_salary_count_sbu * 10) / 100

            if assessment_details_report.fixed_increment_new_gross_salary_b is not None and assessment_details_report.fixed_increment_b is not None:
                assessment_details_report.difference_new_salary_a_new_salary_b = abs(
                    assessment_details_report.fixed_increment_new_gross_salary_b - assessment_details_report.hr_new_gross_salary_a)

            if proposed_by_sbu_director_pm_self[i] is not '':
                assessment_details_report.proposed_by_sbu_director_pm_self = proposed_by_sbu_director_pm_self[
                    i]

            if em.gross_salary is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
                assessment_details_report.percentage_of_increment = round(
                    ((float(assessment_details_report.proposed_by_sbu_director_pm_self) / em.gross_salary) * 100))

            if em.gross_salary is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
                assessment_details_report.new_gross_salary_b = float(
                    assessment_details_report.proposed_by_sbu_director_pm_self) + em.gross_salary

            assessment_details_report_last_year = None
            assessment_details_report_before_last_year = None

            try:
                assessment_details_report_last_year = AssessmentDetail.objects.get(
                    Q(employee_id=em.id) &
                    Q(year=first_last_year)
                )
            except:
                pass

            try:
                assessment_details_report_before_last_year = AssessmentDetail.objects.get(
                    Q(employee_id=em.id) &
                    Q(year=second_last_year)
                )
            except:
                pass

            if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
                if assessment_details_report.new_gross_salary_b is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None and assessment_details_report_last_year.proposed_by_sbu_director_pm_self and assessment_details_report_last_year.increment_amount_a:
                    assessment_details_report.cagr_three_years = round((((
                                                                                 assessment_details_report.new_gross_salary_b / (
                                                                                 assessment_details_report.new_gross_salary_b - float(
                                                                             assessment_details_report.proposed_by_sbu_director_pm_self) - float(
                                                                             assessment_details_report_last_year.proposed_by_sbu_director_pm_self) - assessment_details_report_last_year.increment_amount_a)) ** (
                                                                                 1 / 3)) - 1) * 100, 2)

            if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
                if assessment_details_report.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                    assessment_details_report.average_three_years = round(((
                                                                                   assessment_details_report.percentage_of_increment +
                                                                                   assessment_details_report_last_year.percentage_of_increment +
                                                                                   assessment_details_report_before_last_year.percentage_of_increment) / 3) * 100,
                                                                          2)

            if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
                if assessment_details_report.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                    assessment_details_report.average_actual = round((((
                            assessment_details_report.percentage_of_increment +
                            assessment_details_report_last_year.percentage_of_increment +
                            assessment_details_report_before_last_year.percentage_of_increment)) / 3) * 100, 2)

            if assessment_details_report.weighted_average_kpi is not None and em.gross_salary is not None:
                assessment_details_report.increment_with_kpi_percentage = round(
                    ((assessment_details_report.weighted_average_kpi * em.gross_salary) / 100), 2)

            if assessment_details_report.increment_with_kpi_percentage is not None and em.gross_salary is not None:
                assessment_details_report.new_gross_salary_kpi_percentage = assessment_details_report.increment_with_kpi_percentage + em.gross_salary

            if assessment_details_report.increment_with_kpi_percentage is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
                assessment_details_report.gap_manual_formula = abs(
                    assessment_details_report.increment_with_kpi_percentage - float(
                        assessment_details_report.proposed_by_sbu_director_pm_self))

            if assessment_details_report.new_gross_salary_b is not None:
                em.gross_salary = assessment_details_report.new_gross_salary_b
                em.basic_salary = (
                                          assessment_details_report.new_gross_salary_b * 50) / 100
                em.house_rent = (
                                        assessment_details_report.new_gross_salary_b * 30) / 100
                em.medical_allowance = (
                                               assessment_details_report.new_gross_salary_b * 12.5) / 100
                em.conveyance_allowance = (
                                                  assessment_details_report.new_gross_salary_b * 7.5) / 100
                em.save()

            assessment_details_report.year = year.year
            assessment_details_report.created_date = datetime.now()
            assessment_details_report.updated_date = datetime.now()
            assessment_details_report.created_by_id = request.session['id']
            assessment_details_report.updated_by_id = request.session['id']
            assessment_details_report.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessmentReport")

    context = {'year': year,
               'data': userdata,
               'confirmantion_increment_noincrement_obj': confirmantion_increment_noincrement_obj,
               'evaluation_obj': evaluation_obj,
               'kpi_objective_obj': kpi_objective_obj,
               'kpi_value_obj': kpi_value_obj,
               'hr_rating_obj': hr_rating_obj,
               'criticality_obj': criticality_obj,
               'potential_for_improvement_obj': potential_for_improvement_obj,
               'technical_implementation_operational_obj': technical_implementation_operational_obj,
               'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
               'best_performer_team_obj': best_performer_team_obj,
               'best_performer_organization_obj': best_performer_organization_obj,
               'best_performer_pm_obj': best_performer_pm_obj,
               'best_innovator_team_obj': best_innovator_team_obj,
               'sbu_list': sbu_list,
               'employee': employee,
               'form': form, }
    return render(request, 'kpimanagement/assessmentreport/assessmentreport.html', context)


@login_required("logged_in", 'usermanagement:login')
def assessmentReportSingle(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    confirmantion_increment_noincrement_obj = ConfirmationIncrementNoincrement.objects.all()
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_performer_organization_obj = BestPerformerOrganization.objects.all()
    best_performer_pm_obj = BestPerformerPM.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()
    evaluation_obj = Evaluation.objects.all()

    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    get_assesment_data = AssessmentDetail.objects.get(id=id)
    employee = Employee.objects.get(id=get_assesment_data.employee_id)

    print(get_assesment_data.employee.id)

    if 'report-save' in request.POST:
        # em_id = request.POST.getlist('getEmID')
        em_id = employee.id
        em_ds_id = employee.employee_id
        cofirmation_increment_noincrement = request.POST['confirmation_increment_noincrement']
        # evaluation = request.POST['evaluation']
        kpi_objective = request.POST['kpi_objective']
        kpi_value = request.POST['kpi_value']
        hr_rating = request.POST['hr_rating']
        # kpi_overall = request.POST['kpi_overall']
        criticality = request.POST['criticality']
        potential_for_improvement = request.POST['potential_for_improvement']
        technical_implementation_operational = request.POST['technical_implementation_operational']
        top_average_bottom_performer = request.POST['top_average_bottom_performer']
        best_performer_team = request.POST['best_performer_team']
        best_performer_organization = request.POST['best_performer_org']
        best_performer_pm = request.POST['best_performer_pm']
        best_innovator_team = request.POST['best_innovator_team']
        proposed_designation = request.POST['proposed_designation']
        proposed_by_sbu_director_pm_self = request.POST['proposed_by_sbu_director_pm_self']
        remarks = request.POST['remarks']
        remarks_two = request.POST['remarks_two']

        # for i in range(0, len(em_id)):

        # em = Employee.objects.get(employee_id=em_id)
        em = Employee.objects.get(employee_id=em_ds_id)
        assessment_details_report = AssessmentDetail.objects.get(
            employee_id=em_id, year=current_year)
        assessment_details_report.kpi_objective = None
        assessment_details_report.kpi_value = None
        assessment_details_report.hr_rating = None
        if cofirmation_increment_noincrement is not "":
            assessment_details_report.confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.get(
                id=cofirmation_increment_noincrement)
        if kpi_objective is not "":
            assessment_details_report.kpi_objective = KPIObjective.objects.get(
                id=kpi_objective)
            assessment_details_report.percentage_kpi_objective = assessment_details_report.kpi_objective.percentage
        if kpi_value is not "":
            assessment_details_report.kpi_value = KPIValue.objects.get(
                id=kpi_value)
            assessment_details_report.percentage_kpi_value = assessment_details_report.kpi_value.percentage
        if hr_rating is not "":
            assessment_details_report.hr_rating = HRRating.objects.get(
                id=hr_rating)
            assessment_details_report.percentage_kpi_hr = assessment_details_report.hr_rating.percentage
        if kpi_objective is not "" and kpi_value is not "" and hr_rating is not "":
            assessment_details_report.kpi_overall = assessment_details_report.kpi_objective.grade + \
                                                    assessment_details_report.kpi_value.grade + \
                                                    assessment_details_report.hr_rating.grade
        if kpi_objective is not "" and kpi_value is not "" and hr_rating is not "":
            assessment_details_report.weighted_average_kpi = round(((
                                                                            assessment_details_report.kpi_objective.percentage * 0.5) + (
                                                                            assessment_details_report.kpi_value.percentage * 0.3) + (
                                                                            assessment_details_report.hr_rating.percentage * 0.2)),
                                                                   2)
        if criticality is not "":
            assessment_details_report.criticality = Criticality.objects.get(
                id=criticality)
        if potential_for_improvement is not "":
            assessment_details_report.potential_for_improvement = PotentialForImprovement.objects.get(
                id=potential_for_improvement)
        if technical_implementation_operational is not "":
            assessment_details_report.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                id=technical_implementation_operational)
        if top_average_bottom_performer is not "":
            assessment_details_report.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                id=top_average_bottom_performer)
        if best_performer_team is not "":
            assessment_details_report.best_performer_team = BestPerformerTeam.objects.get(
                id=best_performer_team)
        if best_performer_organization is not "":
            assessment_details_report.best_performer_org = BestPerformerOrganization.objects.get(
                id=best_performer_organization)
        if best_performer_pm is not "":
            assessment_details_report.best_performer_pm = BestPerformerPM.objects.get(
                id=best_performer_pm)
        if best_innovator_team is not "":
            assessment_details_report.best_innovator_team = BestInnovatorTeam.objects.get(
                id=best_innovator_team)
        if proposed_designation is not "":
            assessment_details_report.proposed_designation = proposed_designation
        if remarks is not "":
            assessment_details_report.remarks = remarks
        if remarks_two is not "":
            assessment_details_report.remarks_two = remarks_two
        if assessment_details_report.gross_salary is not None:
            if assessment_details_report.gross_salary >= 120000.0:
                assessment_details_report.gross_salary = (
                                                                 assessment_details_report.gross_salary * 2.75) / 100
                assessment_details_report.salary_grade = 'A'
            elif 100000.0 <= assessment_details_report.gross_salary < 120000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 3.25) / 100
                assessment_details_report.salary_grade = 'B'
            elif 90000.0 <= assessment_details_report.gross_salary < 100000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 4.00) / 100
                assessment_details_report.salary_grade = 'C'
            elif 80000.0 <= assessment_details_report.gross_salary < 90000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 5.50) / 100
                assessment_details_report.salary_grade = 'D'
            elif 60000.0 <= em.gross_salary < 70000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 6.50) / 100
                assessment_details_report.salary_grade = 'E'
            elif 40000.0 <= assessment_details_report.gross_salary < 50000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 8.50) / 100
                assessment_details_report.salary_grade = 'F'
            elif 30000.0 <= assessment_details_report.gross_salary < 40000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 11) / 100
                assessment_details_report.salary_grade = 'G'
            elif 20000.0 <= assessment_details_report.gross_salary < 30000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 15) / 100
                assessment_details_report.salary_grade = 'H'
            elif assessment_details_report.gross_salary < 20000.0:
                assessment_details_report.increment_amount_a = (
                                                                       assessment_details_report.gross_salary * 17) / 100
                assessment_details_report.salary_grade = 'K'
        if assessment_details_report.gross_salary is not None and assessment_details_report.increment_amount_a is not None:
            assessment_details_report.hr_new_gross_salary_a = em.gross_salary + \
                                                              assessment_details_report.increment_amount_a
            assessment_details_report.percentage_hr_a = (
                                                                assessment_details_report.increment_amount_a / assessment_details_report.gross_salary) * 100
            assessment_details_report.fixed_increment_b = (
                                                                  assessment_details_report.gross_salary * 10) / 100
            assessment_details_report.fixed_increment_new_gross_salary_b = assessment_details_report.fixed_increment_b + \
                                                                           assessment_details_report.gross_salary

        total_salary_count_sbu = 0
        emp = Employee.objects.filter(sbu=em.sbu)
        for e in emp:
            if e.gross_salary is not None:
                total_salary_count_sbu = total_salary_count_sbu + e.gross_salary
        assessment_details_report.team_distribution_percentage_c = (
                                                                           total_salary_count_sbu * 10) / 100

        if assessment_details_report.fixed_increment_new_gross_salary_b is not None and assessment_details_report.fixed_increment_b is not None:
            assessment_details_report.difference_new_salary_a_new_salary_b = abs(
                assessment_details_report.fixed_increment_new_gross_salary_b - assessment_details_report.hr_new_gross_salary_a)

        if proposed_by_sbu_director_pm_self is not '':
            assessment_details_report.proposed_by_sbu_director_pm_self = proposed_by_sbu_director_pm_self

        if em.gross_salary is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
            assessment_details_report.percentage_of_increment = round(
                ((float(assessment_details_report.proposed_by_sbu_director_pm_self) / em.gross_salary) * 100))

        if em.gross_salary is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
            assessment_details_report.new_gross_salary_b = float(
                assessment_details_report.proposed_by_sbu_director_pm_self) + em.gross_salary

        assessment_details_report_last_year = None
        assessment_details_report_before_last_year = None

        try:
            assessment_details_report_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=first_last_year)
            )
        except:
            pass

        try:
            assessment_details_report_before_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=second_last_year)
            )
        except:
            pass

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_report.new_gross_salary_b is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None and assessment_details_report_last_year.proposed_by_sbu_director_pm_self and assessment_details_report_last_year.increment_amount_a:
                assessment_details_report.cagr_three_years = round((((
                                                                             assessment_details_report.new_gross_salary_b / (
                                                                             assessment_details_report.new_gross_salary_b - float(
                                                                         assessment_details_report.proposed_by_sbu_director_pm_self) - float(
                                                                         assessment_details_report_last_year.proposed_by_sbu_director_pm_self) - assessment_details_report_last_year.increment_amount_a)) ** (
                                                                             1 / 3)) - 1) * 100, 2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_report.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_report.average_three_years = round(((
                                                                               assessment_details_report.percentage_of_increment +
                                                                               assessment_details_report_last_year.percentage_of_increment +
                                                                               assessment_details_report_before_last_year.percentage_of_increment) / 3) * 100,
                                                                      2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_report.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_report.average_actual = round((((
                        assessment_details_report.percentage_of_increment +
                        assessment_details_report_last_year.percentage_of_increment +
                        assessment_details_report_before_last_year.percentage_of_increment)) / 3) * 100, 2)

        if assessment_details_report.weighted_average_kpi is not None and em.gross_salary is not None:
            assessment_details_report.increment_with_kpi_percentage = round(
                ((assessment_details_report.weighted_average_kpi * em.gross_salary) / 100), 2)

        if assessment_details_report.increment_with_kpi_percentage is not None and em.gross_salary is not None:
            assessment_details_report.new_gross_salary_kpi_percentage = assessment_details_report.increment_with_kpi_percentage + em.gross_salary

        if assessment_details_report.increment_with_kpi_percentage is not None and assessment_details_report.proposed_by_sbu_director_pm_self is not None:
            assessment_details_report.gap_manual_formula = abs(
                assessment_details_report.increment_with_kpi_percentage - float(
                    assessment_details_report.proposed_by_sbu_director_pm_self))

        if assessment_details_report.new_gross_salary_b is not None:
            em.gross_salary = assessment_details_report.new_gross_salary_b
            em.basic_salary = (
                                      assessment_details_report.new_gross_salary_b * 50) / 100
            em.house_rent = (
                                    assessment_details_report.new_gross_salary_b * 30) / 100
            em.medical_allowance = (
                                           assessment_details_report.new_gross_salary_b * 12.5) / 100
            em.conveyance_allowance = (
                                              assessment_details_report.new_gross_salary_b * 7.5) / 100
            em.save()

        assessment_details_report.year = year.year
        assessment_details_report.created_date = datetime.now()
        assessment_details_report.updated_date = datetime.now()
        assessment_details_report.created_by_id = request.session['id']
        assessment_details_report.updated_by_id = request.session['id']
        assessment_details_report.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessmentReport")

    context = {'year': year,
               'data': userdata,
               'data2': get_assesment_data,
               'confirmantion_increment_noincrement_obj': confirmantion_increment_noincrement_obj,
               'evaluation_obj': evaluation_obj,
               'kpi_objective_obj': kpi_objective_obj,
               'kpi_value_obj': kpi_value_obj,
               'hr_rating_obj': hr_rating_obj,
               'criticality_obj': criticality_obj,
               'potential_for_improvement_obj': potential_for_improvement_obj,
               'technical_implementation_operational_obj': technical_implementation_operational_obj,
               'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
               'best_performer_team_obj': best_performer_team_obj,
               'best_performer_organization_obj': best_performer_organization_obj,
               'best_performer_pm_obj': best_performer_pm_obj,
               'best_innovator_team_obj': best_innovator_team_obj,
               'sbu_list': sbu_list,
               'employee': employee,
               'form': form,
               'current_year': current_year}

    return render(request, 'kpimanagement/assessmentreport/assessment_report_single.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def assessmentSupervisorList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    emp = Employee.objects.get(id=request.session['employee'])
    # print(emp.id)
    # print(emp.supervisor_id)
    sup = Supervisor.objects.get(id=emp.supervisor_id)
    # print('sup',sup)
    assessmentsuper = AssessmentDetail.objects.filter(supervisor_id=sup.id)
    # print('asss',assessmentsuper)
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()

    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    employee = Employee.objects.all()

    if 'detail-save' in request.POST:
        em_id = request.POST.getlist('getEmID')
        kpi_objective = request.POST.getlist('kpi_objective')
        kpi_value = request.POST.getlist('kpi_value')
        kpi_overall = request.POST.getlist('kpi_overall')
        hr_rating = request.POST.getlist('hr_rating')
        criticality = request.POST.getlist('criticality')
        potential_for_improvement = request.POST.getlist(
            'potential_for_improvement')
        technical_implementation_operational = request.POST.getlist(
            'technical_implementation_operational')
        top_average_bottom_performer = request.POST.getlist(
            'top_average_bottom_performer')
        best_performer_team = request.POST.getlist('best_performer_team')
        best_innovator_team = request.POST.getlist('best_innovator_team')
        proposed_designation = request.POST.getlist('proposed_designation')
        remarks = request.POST.getlist('remarks')

        for i in range(0, len(em_id)):
            em = Employee.objects.get(employee_id=em_id[i])
            assessment_details_update = AssessmentDetail.objects.get(
                employee_id=em.id)
            assessment_details_update.kpi_objective = None
            assessment_details_update.kpi_value = None
            assessment_details_update.hr_rating = None
            if kpi_objective[i] is not "":
                assessment_details_update.kpi_objective = KPIObjective.objects.get(
                    id=kpi_objective[i])
            if kpi_value[i] is not "":
                assessment_details_update.kpi_value = KPIValue.objects.get(
                    id=kpi_value[i])
            if hr_rating[i] is not "":
                assessment_details_update.hr_rating = HRRating.objects.get(
                    id=hr_rating[i])
            if kpi_objective[i] is not "" and kpi_value[i] is not "" and hr_rating[i] is not "":
                assessment_details_update.kpi_overall = assessment_details_update.kpi_objective.grade + \
                                                        assessment_details_update.kpi_value.grade + \
                                                        assessment_details_update.hr_rating.grade
            if criticality[i] is not "":
                assessment_details_update.criticality = Criticality.objects.get(
                    id=criticality[i])
            if potential_for_improvement[i] is not "":
                assessment_details_update.potential_for_improvement = PotentialForImprovement.objects.get(
                    id=potential_for_improvement[i])
            if technical_implementation_operational[i] is not "":
                assessment_details_update.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                    id=technical_implementation_operational[i])
            if top_average_bottom_performer[i] is not "":
                assessment_details_update.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                    id=top_average_bottom_performer[i])
            if best_performer_team[i] is not "":
                assessment_details_update.best_performer_team = BestPerformerTeam.objects.get(
                    id=best_performer_team[i])
            if best_innovator_team[i] is not "":
                assessment_details_update.best_innovator_team = BestInnovatorTeam.objects.get(
                    id=best_innovator_team[i])
            if proposed_designation[i] is not "":
                assessment_details_update.proposed_designation = proposed_designation[i]
            if remarks[i] is not "":
                assessment_details_update.remarks = remarks[i]
            assessment_details_update.year = year.year
            assessment_details_update.created_date = datetime.now()
            assessment_details_update.updated_date = datetime.now()
            assessment_details_update.created_by_id = request.session['id']
            assessment_details_update.updated_by_id = request.session['id']
            assessment_details_update.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessmentSupervisorList")

    context = {'year': year,
               'data': userdata,
               'kpi_objective_obj': kpi_objective_obj,
               'kpi_value_obj': kpi_value_obj,
               'hr_rating_obj': hr_rating_obj,
               'criticality_obj': criticality_obj,
               'potential_for_improvement_obj': potential_for_improvement_obj,
               'technical_implementation_operational_obj': technical_implementation_operational_obj,
               'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
               'best_performer_team_obj': best_performer_team_obj,
               'best_innovator_team_obj': best_innovator_team_obj,
               'sbu_list': sbu_list,
               'employee': employee,
               'form': form,
               'sbu_flag': sbu_flag, 'assessmentsuper': assessmentsuper}
    return render(request, 'kpimanagement/kpiperformance/assessment_supervisor_list.html', context)


def assessmentSupervisorSingle(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    kpi_objective_obj = KPIObjective.objects.all()
    kpi_value_obj = KPIValue.objects.all()
    hr_rating_obj = HRRating.objects.all()
    criticality_obj = Criticality.objects.all()
    confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.all()
    potential_for_improvement_obj = PotentialForImprovement.objects.all()
    technical_implementation_operational_obj = TechnicalImplementationOperational.objects.all()
    top_average_bottom_performer_obj = TopAverageBottomPerformer.objects.all()
    best_performer_team_obj = BestPerformerTeam.objects.all()
    best_innovator_team_obj = BestInnovatorTeam.objects.all()
    best_performer_organization_obj = BestPerformerOrganization.objects.all()
    best_performer_pm_obj = BestPerformerPM.objects.all()
    sbu_flag = 0
    form = AssessmentDetailForm()
    sbu_list = SBU.objects.all()
    get_assesment_data = AssessmentDetail.objects.get(id=id)
    # print(kpi_objective_obj)
    # print('best_performer_org',get_assesment_data.best_performer_org)
    # print('confirmation_increment_noincrement',get_assesment_data.confirmation_increment_noincrement)
    employee = Employee.objects.get(id=get_assesment_data.employee_id)

    if 'detail-save' in request.POST:
        # em_id = request.POST.getlist('getEmID')
        em_id = employee.id
        em_ds_id = employee.employee_id
        confirmation_increment_noincrement = request.POST['confirmation_increment_noincrement']
        kpi_objective = request.POST['kpi_objective']
        kpi_value = request.POST['kpi_value']
        # kpi_overall = request.POST['kpi_overall']
        hr_rating = request.POST['hr_rating']
        criticality = request.POST['criticality']
        potential_for_improvement = request.POST['potential_for_improvement']
        technical_implementation_operational = request.POST['technical_implementation_operational']
        top_average_bottom_performer = request.POST['top_average_bottom_performer']
        best_performer_team = request.POST['best_performer_team']
        best_performer_organization = request.POST['best_performer_org']
        best_performer_pm = request.POST['best_performer_pm']
        best_innovator_team = request.POST['best_innovator_team']
        proposed_designation = request.POST['proposed_designation']
        proposed_by_sbu_director_pm_self = request.POST['proposed_by_sbu_director_pm_self']
        remarks = request.POST['remarks']

        # for i in range(0, len(em_id)):
        em = Employee.objects.get(employee_id=em_ds_id)
        assessment_details_update = AssessmentDetail.objects.get(
            employee_id=em_id)
        assessment_details_update.kpi_objective = None
        assessment_details_update.kpi_value = None
        assessment_details_update.hr_rating = None
        if kpi_objective is not "":
            assessment_details_update.kpi_objective = KPIObjective.objects.get(
                id=kpi_objective)
        if kpi_value is not "":
            assessment_details_update.kpi_value = KPIValue.objects.get(
                id=kpi_value)
        if hr_rating is not "":
            assessment_details_update.hr_rating = HRRating.objects.get(
                id=hr_rating)
        if kpi_objective is not "" and kpi_value is not "" and hr_rating is not "":
            assessment_details_update.kpi_overall = assessment_details_update.kpi_objective.grade + \
                                                    assessment_details_update.kpi_value.grade + \
                                                    assessment_details_update.hr_rating.grade
        if criticality is not "":
            assessment_details_update.criticality = Criticality.objects.get(
                id=criticality)
        if potential_for_improvement is not "":
            assessment_details_update.potential_for_improvement = PotentialForImprovement.objects.get(
                id=potential_for_improvement)
        if technical_implementation_operational is not "":
            assessment_details_update.technical_implementation_operational = TechnicalImplementationOperational.objects.get(
                id=technical_implementation_operational)
        if top_average_bottom_performer is not "":
            assessment_details_update.top_average_bottom_performer = TopAverageBottomPerformer.objects.get(
                id=top_average_bottom_performer)
        if best_performer_team is not "":
            assessment_details_update.best_performer_team = BestPerformerTeam.objects.get(
                id=best_performer_team)
        if best_performer_organization is not "":
            assessment_details_update.best_performer_org = BestPerformerOrganization.objects.get(
                id=best_performer_organization)
        if best_performer_pm is not "":
            assessment_details_update.best_performer_pm = BestPerformerPM.objects.get(
                id=best_performer_pm)
        if best_innovator_team is not "":
            assessment_details_update.best_innovator_team = BestInnovatorTeam.objects.get(
                id=best_innovator_team)
        if proposed_designation is not "":
            assessment_details_update.proposed_designation = proposed_designation
        if remarks is not "":
            assessment_details_update.remarks = remarks
        if confirmation_increment_noincrement is not "":
            assessment_details_update.confirmation_increment_noincrement = ConfirmationIncrementNoincrement.objects.get(
                id=confirmation_increment_noincrement)
        if assessment_details_update.gross_salary is not None:
            if assessment_details_update.gross_salary >= 120000.0:
                assessment_details_update.gross_salary = (
                                                                 assessment_details_update.gross_salary * 2.75) / 100
                assessment_details_update.salary_grade = 'A'
            elif 100000.0 <= assessment_details_update.gross_salary < 120000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 3.25) / 100
                assessment_details_update.salary_grade = 'B'
            elif 90000.0 <= assessment_details_update.gross_salary < 100000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 4.00) / 100
                assessment_details_update.salary_grade = 'C'
            elif 80000.0 <= assessment_details_update.gross_salary < 90000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 5.50) / 100
                assessment_details_update.salary_grade = 'D'
            elif 60000.0 <= em.gross_salary < 70000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 6.50) / 100
                assessment_details_update.salary_grade = 'E'
            elif 40000.0 <= assessment_details_update.gross_salary < 50000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 8.50) / 100
                assessment_details_update.salary_grade = 'F'
            elif 30000.0 <= assessment_details_update.gross_salary < 40000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 11) / 100
                assessment_details_update.salary_grade = 'G'
            elif 20000.0 <= assessment_details_update.gross_salary < 30000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 15) / 100
                assessment_details_update.salary_grade = 'H'
            elif assessment_details_update.gross_salary < 20000.0:
                assessment_details_update.increment_amount_a = (
                                                                       assessment_details_update.gross_salary * 17) / 100
                assessment_details_update.salary_grade = 'K'
        if assessment_details_update.gross_salary is not None and assessment_details_update.increment_amount_a is not None:
            assessment_details_update.hr_new_gross_salary_a = em.gross_salary + \
                                                              assessment_details_update.increment_amount_a
            assessment_details_update.percentage_hr_a = (
                                                                assessment_details_update.increment_amount_a / assessment_details_update.gross_salary) * 100
            assessment_details_update.fixed_increment_b = (
                                                                  assessment_details_update.gross_salary * 10) / 100
            assessment_details_update.fixed_increment_new_gross_salary_b = assessment_details_update.fixed_increment_b + \
                                                                           assessment_details_update.gross_salary

        total_salary_count_sbu = 0
        emp = Employee.objects.filter(sbu=em.sbu)
        for e in emp:
            if e.gross_salary is not None:
                total_salary_count_sbu = total_salary_count_sbu + e.gross_salary
        assessment_details_update.team_distribution_percentage_c = (
                                                                           total_salary_count_sbu * 10) / 100

        if assessment_details_update.fixed_increment_new_gross_salary_b is not None and assessment_details_update.fixed_increment_b is not None:
            assessment_details_update.difference_new_salary_a_new_salary_b = abs(
                assessment_details_update.fixed_increment_new_gross_salary_b - assessment_details_update.hr_new_gross_salary_a)

        if proposed_by_sbu_director_pm_self is not '':
            assessment_details_update.proposed_by_sbu_director_pm_self = proposed_by_sbu_director_pm_self

        if em.gross_salary is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.percentage_of_increment = round(
                ((float(assessment_details_update.proposed_by_sbu_director_pm_self) / em.gross_salary) * 100))

        if em.gross_salary is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.new_gross_salary_b = float(
                assessment_details_update.proposed_by_sbu_director_pm_self) + em.gross_salary

        assessment_details_report_last_year = None
        assessment_details_report_before_last_year = None

        try:
            assessment_details_report_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=first_last_year)
            )
        except:
            pass

        try:
            assessment_details_report_before_last_year = AssessmentDetail.objects.get(
                Q(employee_id=em.id) &
                Q(year=second_last_year)
            )
        except:
            pass

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.new_gross_salary_b is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None and assessment_details_report_last_year.proposed_by_sbu_director_pm_self and assessment_details_report_last_year.increment_amount_a:
                assessment_details_update.cagr_three_years = round((((
                                                                             assessment_details_update.new_gross_salary_b / (
                                                                             assessment_details_update.new_gross_salary_b - float(
                                                                         assessment_details_update.proposed_by_sbu_director_pm_self) - float(
                                                                         assessment_details_update.proposed_by_sbu_director_pm_self) - assessment_details_report_last_year.increment_amount_a)) ** (
                                                                             1 / 3)) - 1) * 100, 2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_update.average_three_years = round(((assessment_details_update.percentage_of_increment +
                                                                               assessment_details_report_last_year.percentage_of_increment +
                                                                               assessment_details_report_before_last_year.percentage_of_increment) / 3) * 100,
                                                                      2)

        if assessment_details_report_last_year is not None and assessment_details_report_before_last_year is not None:
            if assessment_details_update.percentage_of_increment is not None and assessment_details_report_last_year.percentage_of_increment is not None and assessment_details_report_before_last_year.percentage_of_increment:
                assessment_details_update.average_actual = round((((
                        assessment_details_update.percentage_of_increment +
                        assessment_details_report_last_year.percentage_of_increment +
                        assessment_details_report_before_last_year.percentage_of_increment)) / 3) * 100, 2)

        if assessment_details_update.weighted_average_kpi is not None and em.gross_salary is not None:
            assessment_details_update.increment_with_kpi_percentage = round(
                ((assessment_details_update.weighted_average_kpi * em.gross_salary) / 100), 2)

        if assessment_details_update.increment_with_kpi_percentage is not None and em.gross_salary is not None:
            assessment_details_update.new_gross_salary_kpi_percentage = assessment_details_update.increment_with_kpi_percentage + em.gross_salary

        if assessment_details_update.increment_with_kpi_percentage is not None and assessment_details_update.proposed_by_sbu_director_pm_self is not None:
            assessment_details_update.gap_manual_formula = abs(
                assessment_details_update.increment_with_kpi_percentage - float(
                    assessment_details_update.proposed_by_sbu_director_pm_self))

        if assessment_details_update.new_gross_salary_b is not None:
            em.gross_salary = assessment_details_update.new_gross_salary_b
            em.basic_salary = (assessment_details_update.new_gross_salary_b * 50) / 100
            em.house_rent = (assessment_details_update.new_gross_salary_b * 30) / 100
            em.medical_allowance = (assessment_details_update.new_gross_salary_b * 12.5) / 100
            em.conveyance_allowance = (assessment_details_update.new_gross_salary_b * 7.5) / 100
            em.save()
        assessment_details_update.year = year.year
        assessment_details_update.created_date = datetime.now()
        assessment_details_update.updated_date = datetime.now()
        assessment_details_update.created_by_id = request.session['id']
        assessment_details_update.updated_by_id = request.session['id']
        assessment_details_update.flag = 1
        assessment_details_update.save()
        messages.success(request, "Data Successfully Saved")
        return redirect("kpimanagement:assessmentSupervisorList")

    context = {
        'year': year,
        'data': userdata,
        'getdata': get_assesment_data,
        'kpi_objective_obj': kpi_objective_obj,
        'kpi_value_obj': kpi_value_obj,
        'hr_rating_obj': hr_rating_obj,
        'criticality_obj': criticality_obj,
        'potential_for_improvement_obj': potential_for_improvement_obj,
        'technical_implementation_operational_obj': technical_implementation_operational_obj,
        'top_average_bottom_performer_obj': top_average_bottom_performer_obj,
        'best_performer_team_obj': best_performer_team_obj,
        'best_innovator_team_obj': best_innovator_team_obj,
        'best_performer_organization_obj': best_performer_organization_obj,
        'best_performer_pm_obj': best_performer_pm_obj,
        'confirmantion_increment_noincrement_obj': confirmation_increment_noincrement,
        'sbu_list': sbu_list,
        'employee': employee,
        'form': form,
        'sbu_flag': sbu_flag,
        'current_year': current_year}

    return render(request, 'kpimanagement/kpiperformance/assessment_supervisor_single.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def supervisorPerformanceList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    year = date.today().year
    emp = Employee.objects.get(id=request.session['employee'])
    # print(emp.id)
    # print(emp.supervisor_id)
    sup = Supervisor.objects.get(id=emp.supervisor_id)
    performancesuper = KPIPerformance.objects.filter(supervisor_id=sup.id,year=year)
    # print('performancesuper',performancesuper)

    context = {'data': userdata,
               'performancesuper': performancesuper,
               }

    return render(request, 'kpimanagement/kpiperformance/supervisor_performance.html', context)


@login_required("logged_in", 'usermanagement:login')
def supervisorPerformancSave(request, id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    em = Employee.objects.get(employee_id=userdata['username'])
    year = date.today().year

    try:
        kpi_performance_obj = KPIPerformance.objects.get(id=id)
    except:
        kpi_performance_obj = KPIPerformance.objects.create(
            employee=Employee.objects.get(id=em.id),
            year=current_year,
            sbu_id=em.sbu_id,
            supervisor_id=em.supervisor_id,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            created_by_id=request.session['id'],
            updated_by_id=request.session['id'],
        )
        kpi_performance_obj.save()

    kpi_performance_obj = KPIPerformance.objects.get(id=id)
    form = KPIPerformanceForm(instance=kpi_performance_obj)

    if request.method == "POST":
        if 'draft_save' in request.POST:
            kpi_performance = KPIPerformance.objects.get(
                Q(id=id))
            if request.POST.get('production') is not "":
                kpi_performance.production = request.POST.get('production')
            if request.POST.get('production_rating') is not "":
                kpi_performance.production_rating = KPIObjective.objects.get(
                    id=request.POST.get('production_rating'))
            if request.POST.get('production_weightage') is not "":
                kpi_performance.production_weightage = request.POST.get(
                    'production_weightage')
            if request.POST.get('support') is not "":
                kpi_performance.support = request.POST.get('support')
            if request.POST.get('support_rating') is not "":
                kpi_performance.support_rating = KPIObjective.objects.get(
                    id=request.POST.get('support_rating'))
            if request.POST.get('support_weightage') is not "":
                kpi_performance.support_weightage = request.POST.get(
                    'support_weightage')
            if request.POST.get('innovation') is not "":
                kpi_performance.innovation = request.POST.get('innovation')
            if request.POST.get('innovation_rating') is not "":
                kpi_performance.innovation_rating = KPIObjective.objects.get(
                    id=request.POST.get('innovation_rating'))
            if request.POST.get('innovation_weightage') is not "":
                kpi_performance.innovation_weightage = request.POST.get(
                    'innovation_weightage')
            if request.POST.get('people') is not "":
                kpi_performance.people = request.POST.get('people')
            if request.POST.get('people_rating') is not "":
                kpi_performance.people_rating = KPIObjective.objects.get(
                    id=request.POST.get('people_rating'))
            if request.POST.get('people_weightage') is not "":
                kpi_performance.people_weightage = request.POST.get(
                    'people_weightage')
            if request.POST.get('other') is not "":
                kpi_performance.other = request.POST.get('other')
            if request.POST.get('other_rating') is not "":
                kpi_performance.other_rating = KPIObjective.objects.get(
                    id=request.POST.get('other_rating'))
            if request.POST.get('other_weightage') is not "":
                kpi_performance.other_weightage = request.POST.get(
                    'other_weightage')
            if request.POST.get('courageous') is not "":
                kpi_performance.courageous = request.POST.get('courageous')
            if request.POST.get('courageous_rating') is not "":
                kpi_performance.courageous_rating = KPIValue.objects.get(
                    id=request.POST.get('courageous_rating'))
            if request.POST.get('teamwork') is not "":
                kpi_performance.teamwork = request.POST.get('teamwork')
            if request.POST.get('teamwork_rating') is not "":
                kpi_performance.teamwork_rating = KPIValue.objects.get(
                    id=request.POST.get('teamwork_rating'))
            if request.POST.get('responsive') is not "":
                kpi_performance.responsive = request.POST.get('responsive')
            if request.POST.get('responsive_rating') is not "":
                kpi_performance.responsive_rating = KPIValue.objects.get(
                    id=request.POST.get('responsive_rating'))
            if request.POST.get('creative') is not "":
                kpi_performance.creative = request.POST.get('creative')
            if request.POST.get('creative_rating') is not "":
                kpi_performance.creative_rating = KPIValue.objects.get(
                    id=request.POST.get('creative_rating'))
            if request.POST.get('trustworthy') is not "":
                kpi_performance.trustworthy = request.POST.get('trustworthy')
            if request.POST.get('trustworthy_rating') is not "":
                kpi_performance.trustworthy_rating = KPIValue.objects.get(
                    id=request.POST.get('trustworthy_rating'))
            if request.POST.get('other_sustainable_achievement') is not "":
                kpi_performance.other_sustainable_achievement = request.POST.get(
                    'other_sustainable_achievement')
            if request.POST.get('significant_issue') is not "":
                kpi_performance.significant_issue = request.POST.get(
                    'significant_issue')
            if request.POST.get('individual_comment') is not "":
                kpi_performance.individual_comment = request.POST.get(
                    'individual_comment')
            if request.POST.get('manager_comment') is not "":
                kpi_performance.manager_comment = request.POST.get(
                    'manager_comment')
            if request.POST.get('senior_manager_functional_head_comment') is not "":
                kpi_performance.senior_manager_functional_head_comment = request.POST.get(
                    'senior_manager_functional_head_comment')
            if request.POST.get('director_chief_operating_officer_comment') is not "":
                kpi_performance.director_chief_operating_officer_comment = request.POST.get(
                    'director_chief_operating_officer_comment')
            if request.POST.get('overall_performance') is not "":
                kpi_performance.overall_performance = request.POST.get(
                    'overall_performance')
            kpi_performance.created_date = datetime.now()
            kpi_performance.updated_date = datetime.now()
            kpi_performance.created_by_id = request.session['id']
            kpi_performance.updated_by_id = request.session['id']
            kpi_performance.save()
            messages.success(request, 'Data Successfully Saved As Draft')
            return redirect('kpimanagement:supervisorPerformanceList')

        if 'submit' in request.POST:
            kpi_performance = KPIPerformance.objects.get(id=id)
            kpi_performance.flag = True
            if request.POST.get('production') is not "":
                kpi_performance.production = request.POST.get('production')
            if request.POST.get('production_rating') is not "":
                kpi_performance.production_rating = KPIObjective.objects.get(
                    id=request.POST.get('production_rating'))
            if request.POST.get('production_weightage') is not "":
                kpi_performance.production_weightage = request.POST.get(
                    'production_weightage')
            if request.POST.get('support') is not "":
                kpi_performance.support = request.POST.get('support')
            if request.POST.get('support_rating') is not "":
                kpi_performance.support_rating = KPIObjective.objects.get(
                    id=request.POST.get('support_rating'))
            if request.POST.get('support_weightage') is not "":
                kpi_performance.support_weightage = request.POST.get(
                    'support_weightage')
            if request.POST.get('innovation') is not "":
                kpi_performance.innovation = request.POST.get('innovation')
            if request.POST.get('innovation_rating') is not "":
                kpi_performance.innovation_rating = KPIObjective.objects.get(
                    id=request.POST.get('innovation_rating'))
            if request.POST.get('innovation_weightage') is not "":
                kpi_performance.innovation_weightage = request.POST.get(
                    'innovation_weightage')
            if request.POST.get('people') is not "":
                kpi_performance.people = request.POST.get('people')
            if request.POST.get('people_rating') is not "":
                kpi_performance.people_rating = KPIObjective.objects.get(
                    id=request.POST.get('people_rating'))
            if request.POST.get('people_weightage') is not "":
                kpi_performance.people_weightage = request.POST.get(
                    'people_weightage')
            if request.POST.get('other') is not "":
                kpi_performance.other = request.POST.get('other')
            if request.POST.get('other_rating') is not "":
                kpi_performance.other_rating = KPIObjective.objects.get(
                    id=request.POST.get('other_rating'))
            if request.POST.get('other_weightage') is not "":
                kpi_performance.other_weightage = request.POST.get(
                    'other_weightage')
            if request.POST.get('courageous') is not "":
                kpi_performance.courageous = request.POST.get('courageous')
            if request.POST.get('courageous_rating') is not "":
                kpi_performance.courageous_rating = KPIValue.objects.get(
                    id=request.POST.get('courageous_rating'))
            if request.POST.get('teamwork') is not "":
                kpi_performance.teamwork = request.POST.get('teamwork')
            if request.POST.get('teamwork_rating') is not "":
                kpi_performance.teamwork_rating = KPIValue.objects.get(
                    id=request.POST.get('teamwork_rating'))
            if request.POST.get('responsive') is not "":
                kpi_performance.responsive = request.POST.get('responsive')
            if request.POST.get('responsive_rating') is not "":
                kpi_performance.responsive_rating = KPIValue.objects.get(
                    id=request.POST.get('responsive_rating'))
            if request.POST.get('creative') is not "":
                kpi_performance.creative = request.POST.get('creative')
            if request.POST.get('creative_rating') is not "":
                kpi_performance.creative_rating = KPIValue.objects.get(
                    id=request.POST.get('creative_rating'))
            if request.POST.get('trustworthy') is not "":
                kpi_performance.trustworthy = request.POST.get('trustworthy')
            if request.POST.get('trustworthy_rating') is not "":
                kpi_performance.trustworthy_rating = KPIValue.objects.get(
                    id=request.POST.get('trustworthy_rating'))
            if request.POST.get('other_sustainable_achievement') is not "":
                kpi_performance.other_sustainable_achievement = request.POST.get(
                    'other_sustainable_achievement')
            if request.POST.get('significant_issue') is not "":
                kpi_performance.significant_issue = request.POST.get(
                    'significant_issue')
            if request.POST.get('individual_comment') is not "":
                kpi_performance.individual_comment = request.POST.get(
                    'individual_comment')
            if request.POST.get('manager_comment') is not "":
                kpi_performance.manager_comment = request.POST.get(
                    'manager_comment')
            if request.POST.get('senior_manager_functional_head_comment') is not "":
                kpi_performance.senior_manager_functional_head_comment = request.POST.get(
                    'senior_manager_functional_head_comment')
            if request.POST.get('director_chief_operating_officer_comment') is not "":
                kpi_performance.director_chief_operating_officer_comment = request.POST.get(
                    'director_chief_operating_officer_comment')
            if request.POST.get('overall_performance') is not "":
                kpi_performance.overall_performance = request.POST.get(
                    'overall_performance')
            kpi_performance.created_date = datetime.now()
            kpi_performance.updated_date = datetime.now()
            kpi_performance.created_by_id = request.session['id']
            kpi_performance.updated_by_id = request.session['id']
            kpi_performance.save()
            messages.success(request, 'Data Successfully Submitted')
            return redirect('kpimanagement:supervisorPerformanceList')

    context = {'data': userdata,
               'kpi_performance_obj': kpi_performance_obj,
               'form': form,
               'year': year}

    return render(request, 'kpimanagement/kpiperformance/supervisor_performance_save.html', context)
