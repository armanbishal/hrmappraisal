from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from configuration.forms import *
from kpimanagement.models import *
from django.utils.decorators import method_decorator
from usermanagement.decorators import *
import logging.config
import hrmapprisal.settings
log = hrmapprisal.settings.log_setting()
logging.config.dictConfig(log)
mylog = logging.getLogger('configuration')

@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EmployeeListView(ListView):
    model = Employee
    template_name = 'configuration/employee/employee_list.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'configuration/employee/employee_add.html'
    success_url = reverse_lazy('configuration:EmployeeListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            employee = form.save(commit=False)
            employee.created_date = datetime.now()
            employee.updated_date = datetime.now()
            employee.created_by_id = self.request.session['id']
            employee.updated_by_id = self.request.session['id']
            employee.save()
            # assessment_details = AssessmentDetail.objects.create(
            #     employee = employee,
            #     total_salary_and_allowance=employee.total_salary_and_allowance,
            #     basic_salary=employee.basic_salary,
            #     house_rent=employee.house_rent,
            #     medical_allowance=employee.medical_allowance,
            #     conveyance_allowance=employee.conveyance_allowance,
            #     wppf=employee.wppf,
            #     special_bonus=employee.special_bonus,
            #     mobile_and_other_allowance=employee.mobile_and_other_allowance,
            #     project_expense=employee.project_expense,
            #     other_benefit=employee.other_benefit,
            #     gross_salary=employee.gross_salary,
            #     pf_com_contribution=employee.pf_com_contribution,
            #     year=date.today().year,
            #     created_date=datetime.now(),
            #     updated_date=datetime.now(),
            #     created_by_id=self.request.session['id'],
            #     updated_by_id=self.request.session['id'],
            # )
            # assessment_details.save()
            # kpi_performance = KPIPerformance.objects.create(
            #     employee=employee,
            #     year=date.today().year,
            #     created_date=datetime.now(),
            #     updated_date=datetime.now(),
            #     created_by_id=self.request.session['id'],
            #     updated_by_id=self.request.session['id'],
            # )
            # kpi_performance.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(EmployeeCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(EmployeeCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'configuration/employee/employee_update.html'
    success_url = reverse_lazy('configuration:EmployeeListView')
    context_object_name = 'employeeedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.updated_by_id = self.request.session['id']
                employee.updated_date = datetime.now()
                employee.save()
                # assessment_details = AssessmentDetail.objects.get(employee=employee)
                # assessment_details.total_salary_and_allowance = employee.total_salary_and_allowance
                # assessment_details.basic_salary = employee.basic_salary
                # assessment_details.house_rent = employee.house_rent
                # assessment_details.medical_allowance = employee.medical_allowance
                # assessment_details.conveyance_allowance = employee.conveyance_allowance
                # assessment_details.wppf = employee.wppf
                # assessment_details.special_bonus = employee.special_bonus
                # assessment_details.mobile_and_other_allowance = employee.mobile_and_other_allowance
                # assessment_details.project_expense = employee.project_expense
                # assessment_details.other_benefit = employee.other_benefit
                # assessment_details.gross_salary = employee.gross_salary
                # assessment_details.pf_com_contribution = employee.pf_com_contribution
                # assessment_details.updated_date = datetime.now()
                # assessment_details.updated_by_id = self.request.session['id']
                # assessment_details.save()
            except ValueError as e:
                print(e)
            messages.success(self.request, 'Data Successfully Updated')
            return super(EmployeeUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(EmployeeUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'configuration/employee/employee_list.html'
    success_url = reverse_lazy('configuration:EmployeeListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EmployeeDeleteView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context

    def get_success_url(self):
        messages.success(self.request, 'Data Successfully Deleted')
        return reverse_lazy('configuration:EmployeeListView')


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ConfirmationIncrementNoincrementListView(ListView):
    model = ConfirmationIncrementNoincrement
    template_name = 'configuration/confirmationincrementnoincrement/confirmationincrementnoincrement_list.html'
    context_object_name = 'confirmationincrementnoincrements'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ConfirmationIncrementNoincrementListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ConfirmationIncrementNoincrementCreateView(CreateView):
    model = ConfirmationIncrementNoincrement
    form_class = ConfirmationIncrementNoincrementForm
    template_name = 'configuration/confirmationincrementnoincrement/confirmationincrementnoincrement_add.html'
    success_url = reverse_lazy('configuration:ConfirmationIncrementNoincrementListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ConfirmationIncrementNoincrementCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            confirmation_increment_noincrement = form.save(commit=False)
            confirmation_increment_noincrement.created_date = datetime.now()
            confirmation_increment_noincrement.updated_date = datetime.now()
            confirmation_increment_noincrement.created_by_id = self.request.session['id']
            confirmation_increment_noincrement.updated_by_id = self.request.session['id']
            confirmation_increment_noincrement.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(ConfirmationIncrementNoincrementCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ConfirmationIncrementNoincrementCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ConfirmationIncrementNoincrementUpdateView(UpdateView):
    model = ConfirmationIncrementNoincrement
    form_class = ConfirmationIncrementNoincrementForm
    template_name = 'configuration/confirmationincrementnoincrement/confirmationincrementnoincrement_update.html'
    success_url = reverse_lazy('configuration:ConfirmationIncrementNoincrementListView')
    context_object_name = 'confirmationincrementnoincrementsedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ConfirmationIncrementNoincrementUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            confirmation_increment_noincrement = form.save(commit=False)
            confirmation_increment_noincrement.updated_by_id = self.request.session['id']
            confirmation_increment_noincrement.updated_date = datetime.now()
            confirmation_increment_noincrement.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(ConfirmationIncrementNoincrementUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ConfirmationIncrementNoincrementUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUListView(ListView):
    model = SBU
    template_name = 'configuration/sbu/sbu_list.html'
    context_object_name = 'sbus'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUCreateView(CreateView):
    model = SBU
    form_class = SBUForm
    template_name = 'configuration/sbu/sbu_add.html'
    success_url = reverse_lazy('configuration:SBUListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            sbu = form.save(commit=False)
            sbu.created_date = datetime.now()
            sbu.updated_date = datetime.now()
            sbu.created_by_id = self.request.session['id']
            sbu.updated_by_id = self.request.session['id']
            sbu.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(SBUCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SBUCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUUpdateView(UpdateView):
    model = SBU
    form_class = SBUForm
    template_name = 'configuration/sbu/sbu_update.html'
    success_url = reverse_lazy('configuration:SBUListView')
    context_object_name = 'sbus'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            sbu = form.save(commit=False)
            sbu.updated_by_id = self.request.session['id']
            sbu.updated_date = datetime.now()
            sbu.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(SBUUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SBUUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SubSBUListView(ListView):
    model = SubSBU
    template_name = 'configuration/subsbu/subsbu_list.html'
    context_object_name = 'subsbus'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SubSBUListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SubSBUCreateView(CreateView):
    model = SubSBU
    form_class = SubSBUForm
    template_name = 'configuration/subsbu/subsbu_add.html'
    success_url = reverse_lazy('configuration:SubSBUListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SubSBUCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            sbusbu = form.save(commit=False)
            sbusbu.created_date = datetime.now()
            sbusbu.updated_date = datetime.now()
            sbusbu.created_by_id = self.request.session['id']
            sbusbu.updated_by_id = self.request.session['id']
            sbusbu.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(SubSBUCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SubSBUCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SubSBUUpdateView(UpdateView):
    model = SubSBU
    form_class = SubSBUForm
    template_name = 'configuration/subsbu/subsbu_update.html'
    success_url = reverse_lazy('configuration:SubSBUListView')
    context_object_name = 'subsbus'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SubSBUUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            subsbu = form.save(commit=False)
            subsbu.updated_by_id = self.request.session['id']
            subsbu.updated_date = datetime.now()
            subsbu.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(SubSBUUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SubSBUUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUDirectorNameListView(ListView):
    model = SBUDirectorName
    template_name = 'configuration/sbudirectorname/sbudirectorname_list.html'
    context_object_name = 'sbudirectornames'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUDirectorNameListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUDirectorNameCreateView(CreateView):
    model = SBUDirectorName
    form_class = SBUDirectorNameForm
    template_name = 'configuration/sbudirectorname/sbudirectorname_add.html'
    success_url = reverse_lazy('configuration:SBUDirectorNameListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUDirectorNameCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            sbu_director_name = form.save(commit=False)
            sbu_director_name.created_date = datetime.now()
            sbu_director_name.updated_date = datetime.now()
            sbu_director_name.created_by_id = self.request.session['id']
            sbu_director_name.updated_by_id = self.request.session['id']
            sbu_director_name.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(SBUDirectorNameCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SBUDirectorNameCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SBUDirectorNameUpdateView(UpdateView):
    model = SBUDirectorName
    form_class = SBUDirectorNameForm
    template_name = 'configuration/sbudirectorname/sbudirectorname_update.html'
    success_url = reverse_lazy('configuration:SBUDirectorNameListView')
    context_object_name = 'sbudirectornames'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SBUDirectorNameUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            sbu_director_name = form.save(commit=False)
            sbu_director_name.updated_by_id = self.request.session['id']
            sbu_director_name.updated_date = datetime.now()
            sbu_director_name.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(SBUDirectorNameUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SBUDirectorNameUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SupervisorListView(ListView):
    model = Supervisor
    template_name = 'configuration/supervisor/supervisor_list.html'
    context_object_name = 'supervisors'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SupervisorListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SupervisorCreateView(CreateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = 'configuration/supervisor/supervisor_add.html'
    success_url = reverse_lazy('configuration:SupervisorListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SupervisorCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            supervisor = form.save(commit=False)
            supervisor.created_date = datetime.now()
            supervisor.updated_date = datetime.now()
            supervisor.created_by_id = self.request.session['id']
            supervisor.updated_by_id = self.request.session['id']
            supervisor.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(SupervisorCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SupervisorCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class SupervisorUpdateView(UpdateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = 'configuration/supervisor/supervisor_update.html'
    success_url = reverse_lazy('configuration:SupervisorListView')
    context_object_name = 'supervisors'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(SupervisorUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            supervisor = form.save(commit=False)
            supervisor.updated_by_id = self.request.session['id']
            supervisor.updated_date = datetime.now()
            supervisor.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(SupervisorUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(SupervisorUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'configuration/project/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'configuration/project/project_add.html'
    success_url = reverse_lazy('configuration:ProjectListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            project = form.save(commit=False)
            project.created_date = datetime.now()
            project.updated_date = datetime.now()
            project.created_by_id = self.request.session['id']
            project.updated_by_id = self.request.session['id']
            project.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(ProjectCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ProjectCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'configuration/project/project_update.html'
    success_url = reverse_lazy('configuration:ProjectListView')
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            project = form.save(commit=False)
            project.updated_by_id = self.request.session['id']
            project.updated_date = datetime.now()
            project.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(ProjectUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ProjectUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ReviewRatingListView(ListView):
    model = ReviewRating
    template_name = 'configuration/reviewrating/reviewrating_list.html'
    context_object_name = 'reviewratings'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ReviewRatingListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ReviewRatingCreateView(CreateView):
    model = ReviewRating
    form_class = ReviewRatingForm
    template_name = 'configuration/reviewrating/reviewrating_add.html'
    success_url = reverse_lazy('configuration:ReviewRatingListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ReviewRatingCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            reviewrating = form.save(commit=False)
            reviewrating.created_date = datetime.now()
            reviewrating.updated_date = datetime.now()
            reviewrating.created_by_id = self.request.session['id']
            reviewrating.updated_by_id = self.request.session['id']
            reviewrating.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(ReviewRatingCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ReviewRatingCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ReviewRatingUpdateView(UpdateView):
    model = ReviewRating
    form_class = ReviewRatingForm
    template_name = 'configuration/reviewrating/reviewrating_update.html'
    success_url = reverse_lazy('configuration:ReviewRatingListView')
    context_object_name = 'reviewratings'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(ReviewRatingUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            reviewrating = form.save(commit=False)
            reviewrating.updated_by_id = self.request.session['id']
            reviewrating.updated_date = datetime.now()
            reviewrating.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(ReviewRatingUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ReviewRatingUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIConfigListView(ListView):
    model = KPIConfig
    template_name = 'configuration/kpiconfiguration/kpiconfiguration_list.html'
    context_object_name = 'kpiconfigs'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIConfigListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIConfigCreateView(CreateView):
    model = KPIConfig
    form_class = KPIConfigForm
    template_name = 'configuration/kpiconfiguration/kpiconfiguration_add.html'
    success_url = reverse_lazy('configuration:KPIConfigListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIConfigCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            kpiconfig = form.save(commit=False)
            kpiconfig.created_date = datetime.now()
            kpiconfig.updated_date = datetime.now()
            kpiconfig.created_by_id = self.request.session['id']
            kpiconfig.updated_by_id = self.request.session['id']
            kpiconfig.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(KPIConfigCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIConfigCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIConfigUpdateView(UpdateView):
    model = KPIConfig
    form_class = KPIConfigForm
    template_name = 'configuration/kpiconfiguration/kpiconfiguration_update.html'
    success_url = reverse_lazy('configuration:KPIConfigListView')
    context_object_name = 'kpiconfigedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIConfigUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            kpiconfig = form.save(commit=False)
            kpiconfig.updated_by_id = self.request.session['id']
            kpiconfig.updated_date = datetime.now()
            kpiconfig.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(KPIConfigUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIConfigUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EvaluationListView(ListView):
    model = Evaluation
    template_name = 'configuration/evaluation/evaluation_list.html'
    context_object_name = 'evaluation'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EvaluationListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EvaluationCreateView(CreateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'configuration/evaluation/evaluation_add.html'
    success_url = reverse_lazy('configuration:EvaluationListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EvaluationCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            evaluation = form.save(commit=False)
            evaluation.created_date = datetime.now()
            evaluation.updated_date = datetime.now()
            evaluation.created_by_id = self.request.session['id']
            evaluation.updated_by_id = self.request.session['id']
            evaluation.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(EvaluationCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(EvaluationCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class EvaluationUpdateView(UpdateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'configuration/evaluation/evaluation_update.html'
    success_url = reverse_lazy('configuration:EvaluationListView')
    context_object_name = 'evaluationedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(EvaluationUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            evaluation = form.save(commit=False)
            evaluation.updated_by_id = self.request.session['id']
            evaluation.updated_date = datetime.now()
            evaluation.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(EvaluationUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(EvaluationUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIObjectiveListView(ListView):
    model = KPIObjective
    template_name = 'configuration/kpiobjective/kpiobjective_list.html'
    context_object_name = 'kpiobjectives'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIObjectiveListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIObjectiveCreateView(CreateView):
    model = KPIObjective
    form_class = KPIObjectiveForm
    template_name = 'configuration/kpiobjective/kpiobjective_add.html'
    success_url = reverse_lazy('configuration:KPIObjectiveListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIObjectiveCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            kpiobjective = form.save(commit=False)
            kpiobjective.created_date = datetime.now()
            kpiobjective.updated_date = datetime.now()
            kpiobjective.created_by_id = self.request.session['id']
            kpiobjective.updated_by_id = self.request.session['id']
            kpiobjective.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(KPIObjectiveCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIObjectiveCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIObjectiveUpdateView(UpdateView):
    model = KPIObjective
    form_class = KPIObjectiveForm
    template_name = 'configuration/kpiobjective/kpiobjective_update.html'
    success_url = reverse_lazy('configuration:KPIObjectiveListView')
    context_object_name = 'kpiobjectiveedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIObjectiveUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            kpiobjective = form.save(commit=False)
            kpiobjective.updated_by_id = self.request.session['id']
            kpiobjective.updated_date = datetime.now()
            kpiobjective.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(KPIObjectiveUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIObjectiveUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIValueListView(ListView):
    model = KPIValue
    template_name = 'configuration/kpivalue/kpivalue_list.html'
    context_object_name = 'kpivalues'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIValueListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIValueCreateView(CreateView):
    model = KPIValue
    form_class = KPIValueForm
    template_name = 'configuration/kpivalue/kpivalue_add.html'
    success_url = reverse_lazy('configuration:KPIValueListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIValueCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            kpivalue = form.save(commit=False)
            kpivalue.created_date = datetime.now()
            kpivalue.updated_date = datetime.now()
            kpivalue.created_by_id = self.request.session['id']
            kpivalue.updated_by_id = self.request.session['id']
            kpivalue.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(KPIValueCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIValueCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class KPIValueUpdateView(UpdateView):
    model = KPIValue
    form_class = KPIValueForm
    template_name = 'configuration/kpivalue/kpivalue_update.html'
    success_url = reverse_lazy('configuration:KPIValueListView')
    context_object_name = 'kpivalueedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(KPIValueUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            kpivalue = form.save(commit=False)
            kpivalue.updated_by_id = self.request.session['id']
            kpivalue.updated_date = datetime.now()
            kpivalue.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(KPIValueUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(KPIValueUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class HRRatingListView(ListView):
    model = HRRating
    template_name = 'configuration/hrrating/hrrating_list.html'
    context_object_name = 'hrrating'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(HRRatingListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class HRRatingCreateView(CreateView):
    model = HRRating
    form_class = HRRatingForm
    template_name = 'configuration/hrrating/hrrating_add.html'
    success_url = reverse_lazy('configuration:HRRatingListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(HRRatingCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            hrrating = form.save(commit=False)
            hrrating.created_date = datetime.now()
            hrrating.updated_date = datetime.now()
            hrrating.created_by_id = self.request.session['id']
            hrrating.updated_by_id = self.request.session['id']
            hrrating.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(HRRatingCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(HRRatingCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class HRRatingUpdateView(UpdateView):
    model = HRRating
    form_class = HRRatingForm
    template_name = 'configuration/hrrating/hrrating_update.html'
    success_url = reverse_lazy('configuration:HRRatingListView')
    context_object_name = 'hrratingedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(HRRatingUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            hrrating = form.save(commit=False)
            hrrating.updated_by_id = self.request.session['id']
            hrrating.updated_date = datetime.now()
            hrrating.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(HRRatingUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(HRRatingUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CriticalityListView(ListView):
    model = Criticality
    template_name = 'configuration/criticality/criticality_list.html'
    context_object_name = 'criticality'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(CriticalityListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CriticalityCreateView(CreateView):
    model = Criticality
    form_class = CriticalityForm
    template_name = 'configuration/criticality/criticality_add.html'
    success_url = reverse_lazy('configuration:CriticalityListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(CriticalityCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            criticality = form.save(commit=False)
            criticality.created_date = datetime.now()
            criticality.updated_date = datetime.now()
            criticality.created_by_id = self.request.session['id']
            criticality.updated_by_id = self.request.session['id']
            criticality.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(CriticalityCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(CriticalityCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CriticalityUpdateView(UpdateView):
    model = Criticality
    form_class = CriticalityForm
    template_name = 'configuration/criticality/criticality_update.html'
    success_url = reverse_lazy('configuration:CriticalityListView')
    context_object_name = 'criticalityedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(CriticalityUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            criticality = form.save(commit=False)
            criticality.updated_by_id = self.request.session['id']
            criticality.updated_date = datetime.now()
            criticality.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(CriticalityUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(CriticalityUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class PotentialForImprovementListView(ListView):
    model = PotentialForImprovement
    template_name = 'configuration/potentialforimprovement/potentialforimprovement_list.html'
    context_object_name = 'potentialforimprovement'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(PotentialForImprovementListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class PotentialForImprovementCreateView(CreateView):
    model = PotentialForImprovement
    form_class = PotentialForImprovementForm
    template_name = 'configuration/potentialforimprovement/potentialforimprovement_add.html'
    success_url = reverse_lazy('configuration:PotentialForImprovementListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(PotentialForImprovementCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            potentialforimprovement = form.save(commit=False)
            potentialforimprovement.created_date = datetime.now()
            potentialforimprovement.updated_date = datetime.now()
            potentialforimprovement.created_by_id = self.request.session['id']
            potentialforimprovement.updated_by_id = self.request.session['id']
            potentialforimprovement.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(PotentialForImprovementCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(PotentialForImprovementCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class PotentialForImprovementUpdateView(UpdateView):
    model = PotentialForImprovement
    form_class = PotentialForImprovementForm
    template_name = 'configuration/potentialforimprovement/potentialforimprovement_update.html'
    success_url = reverse_lazy('configuration:PotentialForImprovementListView')
    context_object_name = 'potentialforimprovementedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(PotentialForImprovementUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            potentialforimprovement = form.save(commit=False)
            potentialforimprovement.updated_by_id = self.request.session['id']
            potentialforimprovement.updated_date = datetime.now()
            potentialforimprovement.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(PotentialForImprovementUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(PotentialForImprovementUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TechnicalImplementationOperationalListView(ListView):
    model = TechnicalImplementationOperational
    template_name = 'configuration/technicalimplementationoperational/technicalimplementationoperational_list.html'
    context_object_name = 'technicalimplementationoperational'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TechnicalImplementationOperationalListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TechnicalImplementationOperationalCreateView(CreateView):
    model = TechnicalImplementationOperational
    form_class = TechnicalImplementationOperationalForm
    template_name = 'configuration/technicalimplementationoperational/technicalimplementationoperational_add.html'
    success_url = reverse_lazy('configuration:TechnicalImplementationOperationalListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TechnicalImplementationOperationalCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            technicalimplementationoperational = form.save(commit=False)
            technicalimplementationoperational.created_date = datetime.now()
            technicalimplementationoperational.updated_date = datetime.now()
            technicalimplementationoperational.created_by_id = self.request.session['id']
            technicalimplementationoperational.updated_by_id = self.request.session['id']
            technicalimplementationoperational.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(TechnicalImplementationOperationalCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(TechnicalImplementationOperationalCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TechnicalImplementationOperationalUpdateView(UpdateView):
    model = TechnicalImplementationOperational
    form_class = TechnicalImplementationOperationalForm
    template_name = 'configuration/technicalimplementationoperational/technicalimplementationoperational_update.html'
    success_url = reverse_lazy('configuration:TechnicalImplementationOperationalListView')
    context_object_name = 'technicalimplementationoperationaledit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TechnicalImplementationOperationalUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            technicalimplementationoperational = form.save(commit=False)
            technicalimplementationoperational.updated_by_id = self.request.session['id']
            technicalimplementationoperational.updated_date = datetime.now()
            technicalimplementationoperational.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(TechnicalImplementationOperationalUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(TechnicalImplementationOperationalUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TopAverageBottomPerformerListView(ListView):
    model = TopAverageBottomPerformer
    template_name = 'configuration/topaveragebottomperformer/topaveragebottomperformer_list.html'
    context_object_name = 'topaveragebottomperformer'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TopAverageBottomPerformerListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TopAverageBottomPerformerCreateView(CreateView):
    model = TopAverageBottomPerformer
    form_class = TopAverageBottomPerformerForm
    template_name = 'configuration/topaveragebottomperformer/topaveragebottomperformer_add.html'
    success_url = reverse_lazy('configuration:TopAverageBottomPerformerListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TopAverageBottomPerformerCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            topaveragebottomperformer = form.save(commit=False)
            topaveragebottomperformer.created_date = datetime.now()
            topaveragebottomperformer.updated_date = datetime.now()
            topaveragebottomperformer.created_by_id = self.request.session['id']
            topaveragebottomperformer.updated_by_id = self.request.session['id']
            topaveragebottomperformer.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(TopAverageBottomPerformerCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(TopAverageBottomPerformerCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class TopAverageBottomPerformerUpdateView(UpdateView):
    model = TopAverageBottomPerformer
    form_class = TopAverageBottomPerformerForm
    template_name = 'configuration/topaveragebottomperformer/topaveragebottomperformer_update.html'
    success_url = reverse_lazy('configuration:TopAverageBottomPerformerListView')
    context_object_name = 'topaveragebottomperformeredit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(TopAverageBottomPerformerUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            topaveragebottomperformer = form.save(commit=False)
            topaveragebottomperformer.updated_by_id = self.request.session['id']
            topaveragebottomperformer.updated_date = datetime.now()
            topaveragebottomperformer.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(TopAverageBottomPerformerUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(TopAverageBottomPerformerUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerTeamListView(ListView):
    model = BestPerformerTeam
    template_name = 'configuration/bestperformerteam/bestperformerteam_list.html'
    context_object_name = 'bestperformerteam'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerTeamListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerTeamCreateView(CreateView):
    model = BestPerformerTeam
    form_class = BestPerformerTeamForm
    template_name = 'configuration/bestperformerteam/bestperformerteam_add.html'
    success_url = reverse_lazy('configuration:BestPerformerTeamListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerTeamCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            best_performer_team = form.save(commit=False)
            best_performer_team.created_date = datetime.now()
            best_performer_team.updated_date = datetime.now()
            best_performer_team.created_by_id = self.request.session['id']
            best_performer_team.updated_by_id = self.request.session['id']
            best_performer_team.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(BestPerformerTeamCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerTeamCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerTeamUpdateView(UpdateView):
    model = BestPerformerTeam
    form_class = BestInnovatorTeamForm
    template_name = 'configuration/bestperformerteam/bestperformerteam_update.html'
    success_url = reverse_lazy('configuration:BestPerformerTeamListView')
    context_object_name = 'bestperformerteamedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerTeamUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            best_performer_team = form.save(commit=False)
            best_performer_team.updated_by_id = self.request.session['id']
            best_performer_team.updated_date = datetime.now()
            best_performer_team.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(BestPerformerTeamUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerTeamUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerOrganizationListView(ListView):
    model = BestPerformerOrganization
    template_name = 'configuration/bestperformerorganization/bestperformerorganization_list.html'
    context_object_name = 'bestperformerorganization'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerOrganizationListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerOrganizationCreateView(CreateView):
    model = BestPerformerOrganization
    form_class = BestPerformerOrganizationForm
    template_name = 'configuration/bestperformerorganization/bestperformerorganization_add.html'
    success_url = reverse_lazy('configuration:BestPerformerOrganizationListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerOrganizationCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            best_performer_org = form.save(commit=False)
            best_performer_org.created_date = datetime.now()
            best_performer_org.updated_date = datetime.now()
            best_performer_org.created_by_id = self.request.session['id']
            best_performer_org.updated_by_id = self.request.session['id']
            best_performer_org.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(BestPerformerOrganizationCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerOrganizationCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerOrganizationUpdateView(UpdateView):
    model = BestPerformerOrganization
    form_class = BestPerformerOrganizationForm
    template_name = 'configuration/bestperformerorganization/bestperformerorganization_update.html'
    success_url = reverse_lazy('configuration:BestPerformerOrganizationListView')
    context_object_name = 'bestperformerorganizationedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerOrganizationUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            best_performer_org = form.save(commit=False)
            best_performer_org.updated_by_id = self.request.session['id']
            best_performer_org.updated_date = datetime.now()
            best_performer_org.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(BestPerformerOrganizationUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerOrganizationUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerPMListView(ListView):
    model = BestPerformerPM
    template_name = 'configuration/bestperformerpm/bestperformerpm_list.html'
    context_object_name = 'bestperformerpm'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerPMListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerPMCreateView(CreateView):
    model = BestPerformerPM
    form_class = BestPerformerPMForm
    template_name = 'configuration/bestperformerpm/bestperformerpm_add.html'
    success_url = reverse_lazy('configuration:BestPerformerPMListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerPMCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            best_performer_pm = form.save(commit=False)
            best_performer_pm.created_date = datetime.now()
            best_performer_pm.updated_date = datetime.now()
            best_performer_pm.created_by_id = self.request.session['id']
            best_performer_pm.updated_by_id = self.request.session['id']
            best_performer_pm.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(BestPerformerPMCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerPMCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestPerformerPMUpdateView(UpdateView):
    model = BestPerformerPM
    form_class = BestPerformerPMForm
    template_name = 'configuration/bestperformerpm/bestperformerpm_update.html'
    success_url = reverse_lazy('configuration:BestPerformerPMListView')
    context_object_name = 'bestperformerpmedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestPerformerPMUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            best_performer_pm = form.save(commit=False)
            best_performer_pm.updated_by_id = self.request.session['id']
            best_performer_pm.updated_date = datetime.now()
            best_performer_pm.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(BestPerformerPMUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestPerformerPMUpdateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestInnovatorTeamListView(ListView):
    model = BestInnovatorTeam
    template_name = 'configuration/bestinnovatorteam/bestinnovatorteam_list.html'
    context_object_name = 'bestinnovatorteam'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestInnovatorTeamListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['employee'] = self.model.objects.all()
        return context


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestInnovatorTeamCreateView(CreateView):
    model = BestInnovatorTeam
    form_class = BestInnovatorTeamForm
    template_name = 'configuration/bestinnovatorteam/bestinnovatorteam_add.html'
    success_url = reverse_lazy('configuration:BestInnovatorTeamListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestInnovatorTeamCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            best_innovator_team = form.save(commit=False)
            best_innovator_team.created_date = datetime.now()
            best_innovator_team.updated_date = datetime.now()
            best_innovator_team.created_by_id = self.request.session['id']
            best_innovator_team.updated_by_id = self.request.session['id']
            best_innovator_team.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(BestInnovatorTeamCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestInnovatorTeamCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'usermanagement:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class BestInnovatorTeamUpdateView(UpdateView):
    model = BestInnovatorTeam
    form_class = BestInnovatorTeamForm
    template_name = 'configuration/bestinnovatorteam/bestinnovatorteam_update.html'
    success_url = reverse_lazy('configuration:BestInnovatorTeamListView')
    context_object_name = 'bestinnovatorteamedit'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(BestInnovatorTeamUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        # context['form'] = self.form_class
        return context

    def form_valid(self, form):

        if form.is_valid:
            best_innovator_team = form.save(commit=False)
            best_innovator_team.updated_by_id = self.request.session['id']
            best_innovator_team.updated_date = datetime.now()
            best_innovator_team.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(BestInnovatorTeamUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(BestInnovatorTeamUpdateView, self).form_invalid(form)
