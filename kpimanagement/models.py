from django.db import models
from configuration.models import *
from usermanagement.models import *


class KPIPerformance(models.Model):
    flag = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='kpiperformance_employee')
    sbu = models.ForeignKey(SBU, on_delete=models.CASCADE, null=True, blank=True, related_name='kpiperformance_subsbu')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True, related_name='kpiperformance_supervisor')
    year = models.CharField(max_length=255, null=True, blank=True)
    production = models.TextField(null=True, blank=True)
    production_rating = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True, related_name='production_rating')
    production_weightage = models.CharField(max_length=255, null=True, blank=True)
    support = models.TextField(null=True, blank=True)
    support_rating = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True, related_name='support_rating')
    support_weightage = models.CharField(max_length=255, null=True, blank=True)
    innovation = models.TextField(null=True, blank=True)
    innovation_rating = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True, related_name='innovation_rating')
    innovation_weightage = models.CharField(max_length=255, null=True, blank=True)
    people = models.TextField(null=True, blank=True)
    people_rating = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True, related_name='people_rating')
    people_weightage = models.CharField(max_length=255, null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    other_rating = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True, related_name='other_rating')
    other_weightage = models.CharField(max_length=255, null=True, blank=True)
    courageous = models.TextField(null=True, blank=True)
    courageous_rating = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True, related_name='courageous_rating')
    teamwork = models.TextField(null=True, blank=True)
    teamwork_rating = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True, related_name='teamwork_rating')
    responsive = models.TextField(null=True, blank=True)
    responsive_rating = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True, related_name='responsive_rating')
    creative = models.TextField(null=True, blank=True)
    creative_rating = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True, related_name='creative_rating')
    trustworthy = models.TextField(null=True, blank=True)
    trustworthy_rating = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True, related_name='trustworthy_rating')
    other_sustainable_achievement = models.TextField(null=True, blank=True)
    significant_issue = models.TextField(null=True, blank=True)
    individual_comment = models.TextField(null=True, blank=True)
    manager_comment = models.TextField(null=True, blank=True)
    senior_manager_functional_head_comment = models.TextField(null=True, blank=True)
    director_chief_operating_officer_comment = models.TextField(null=True, blank=True)
    overall_performance = models.TextField(null=True, blank=True)
    # overall_performance_rating = models.ForeignKey(ReviewRating, on_delete=models.CASCADE, null=True, blank=True, related_name='overall_performance_rating')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpiperformace_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpiperformace_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        db_table = 'kpi_performance'
        ordering = ('-id',)

class AssessmentDetail(models.Model):
    flag = models.IntegerField(default=0,null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    sbu = models.ForeignKey(SBU, on_delete=models.CASCADE, null=True, blank=True)
    supervisor= models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True)
    total_salary_and_allowance = models.FloatField(null=True, blank=True)
    basic_salary = models.FloatField(null=True, blank=True)
    house_rent = models.FloatField(null=True, blank=True)
    medical_allowance = models.FloatField(null=True, blank=True)
    conveyance_allowance = models.FloatField(null=True, blank=True)
    wppf = models.FloatField(null=True, blank=True)
    special_bonus = models.FloatField(null=True, blank=True)
    mobile_and_other_allowance = models.FloatField(null=True, blank=True)
    project_expense = models.FloatField(null=True, blank=True)
    other_benefit = models.FloatField(null=True, blank=True)
    gross_salary = models.FloatField(null=True, blank=True)
    pf_com_contribution = models.FloatField(null=True, blank=True)
    confirmation_increment_noincrement = models.ForeignKey(ConfirmationIncrementNoincrement, on_delete=models.CASCADE, null=True, blank=True)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=True, blank=True)
    kpi_objective = models.ForeignKey(KPIObjective, on_delete=models.CASCADE, null=True, blank=True)
    kpi_value = models.ForeignKey(KPIValue, on_delete=models.CASCADE, null=True, blank=True)
    hr_rating = models.ForeignKey(HRRating, on_delete=models.CASCADE, null=True, blank=True)
    kpi_overall = models.CharField(max_length=255, null=True, blank=True)
    percentage_kpi_objective = models.FloatField(default=None, null=True, blank=True)
    percentage_kpi_value = models.FloatField(default=None, null=True, blank=True)
    percentage_kpi_hr = models.FloatField(default=None, null=True, blank=True)
    weighted_average_kpi = models.FloatField(default=None, null=True, blank=True)
    criticality = models.ForeignKey(Criticality, on_delete=models.CASCADE, null=True, blank=True)
    potential_for_improvement = models.ForeignKey(PotentialForImprovement, on_delete=models.CASCADE, null=True, blank=True)
    technical_implementation_operational = models.ForeignKey(TechnicalImplementationOperational, on_delete=models.CASCADE, null=True, blank=True)
    top_average_bottom_performer = models.ForeignKey(TopAverageBottomPerformer, on_delete=models.CASCADE, null=True, blank=True)
    best_performer_team = models.ForeignKey(BestPerformerTeam, on_delete=models.CASCADE, null=True, blank=True)
    best_performer_org = models.ForeignKey(BestPerformerOrganization, on_delete=models.CASCADE, null=True, blank=True)
    best_innovator_team = models.ForeignKey(BestInnovatorTeam, on_delete=models.CASCADE, null=True, blank=True)
    proposed_designation = models.CharField(max_length=255, null=True, blank=True)
    best_performer_pm = models.ForeignKey(BestPerformerPM, on_delete=models.CASCADE, null=True, blank=True)
    salary_grade = models.CharField(max_length=1, null=True, blank=True)
    increment_amount_a = models.FloatField(default=None, null=True, blank=True)
    hr_new_gross_salary_a = models.FloatField(default=None, null=True, blank=True)
    percentage_hr_a = models.FloatField(default=None, null=True, blank=True)
    fixed_increment_b = models.FloatField(default=None, null=True, blank=True)
    fixed_increment_new_gross_salary_b = models.FloatField(default=None, null=True, blank=True)
    team_distribution_percentage_c = models.FloatField(default=None, null=True, blank=True)
    difference_new_salary_a_new_salary_b = models.FloatField(default=None, null=True, blank=True)
    increment = models.FloatField(default=None, null=True, blank=True)
    proposed_by_sbu_director_pm_self = models.FloatField(default=None, null=True, blank=True)
    percentage_of_increment = models.FloatField(default=None, null=True, blank=True)
    cagr_three_years = models.FloatField(default=None, null=True, blank=True)
    average_three_years = models.FloatField(default=None, null=True, blank=True)
    average_actual = models.FloatField(default=None, null=True, blank=True)
    new_gross_salary_b = models.FloatField(default=None, null=True, blank=True)
    increment_with_kpi_percentage = models.FloatField(default=None, null=True, blank=True)
    new_gross_salary_kpi_percentage = models.FloatField(default=None, null=True, blank=True)
    gap_manual_formula = models.FloatField(default=None, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    remarks_two = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_details_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_details_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    flag = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        db_table = 'assessment_detail'
        ordering = ['employee']




class  EmployeeAssignSupervisor(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='employee_assign_employee')
    sbu = models.ForeignKey(SBU, on_delete=models.CASCADE, null=True, blank=True, related_name='employee_assign_subsbu')
    supervisor_id = models.CharField(max_length=20,null=True, blank=True)
    status=models.IntegerField(null=True, blank=True)
    remark=models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_assign_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_assign_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    duration_startdate = models.DateTimeField()
    duration_enddate = models.DateTimeField()
    def __str__(self):
        return f"{self.employee}"

    class Meta:
        db_table = 'employee_assign_supervisor'
        ordering = ['employee']

