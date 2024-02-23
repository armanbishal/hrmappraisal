from datetime import date

from django.utils import timesince

from usermanagement.models import *


class Employee(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(null=True, blank=True)
    employee_id = models.CharField(max_length=255, unique=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.CASCADE, null=True, blank=True)
    sbu = models.ForeignKey('SBU', on_delete=models.CASCADE, null=True, blank=True)
    sub_sbu = models.ForeignKey('SubSBU', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    class Meta:
        db_table = 'employee'
        ordering = ['employee_id']

    def __str__(self):
        return self.name

    @property
    def timesince(self):
        return timesince.timesince(self.date_of_joining)

    def assessmentDuration(self):
        d1 = date.today()
        d2 = self.date_of_joining
        month_diff = d1.month - d2.month + 12 * (d1.year - d2.year)
        if month_diff <= 7:
            return f'{0} Month'
        elif month_diff > 7 and month_diff - 7 > 12:
            return f'{12} Months'
        elif month_diff > 7:
            if d1.month - d2.month + 12 * (d1.year - d2.year) - 7 == 1:
                return f'{1} Month'
            else:
                return f'{d1.month - d2.month + 12 * (d1.year - d2.year) - 7} Months'


class ConfirmationIncrementNoincrement(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='confirmation_increment_noincrement_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='confirmation_increment_noincrement_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'confirmation_increment_noincrement'


class SBU(models.Model):
    name = models.CharField(max_length=255)
    director_name = models.ForeignKey('SBUDirectorName', on_delete=models.CASCADE, related_name='SBU_Director_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sbu_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sbu_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sbu'


class SubSBU(models.Model):
    name = models.CharField(max_length=255)
    sbu = models.ForeignKey(SBU, on_delete=models.CASCADE, related_name='SBU_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sub_sbu_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sub_sbu_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_sbu'


class SBUDirectorName(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='sbu_director_name_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='sbu_director_name_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sbu_director_name'


class Supervisor(models.Model):
    name = models.CharField(max_length=255)
    sbu = models.ForeignKey('SBU', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'supervisor'


class Project(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project'


class ReviewRating(models.Model):
    name = models.CharField(max_length=255, null=True)
    rating = models.IntegerField(null=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_rating_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_rating_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'review_rating'


class KPIConfig(models.Model):
    name = models.CharField(max_length=255)
    shortlist = models.IntegerField(null=True)
    year = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_config_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_config_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kpi_config'


class Evaluation(models.Model):
    name = models.CharField(max_length=255)
    shortlist = models.IntegerField(null=True)
    grade = models.CharField(max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluation_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluation_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'evaluation'


class KPIObjective(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.FloatField(default=None, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    grade = models.CharField(max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_objective_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_objective_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kpiobjective'


class KPIValue(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    percentage = models.FloatField(default=None, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    grade = models.CharField(max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_value_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_value_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kpi_value'


class HRRating(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    percentage = models.FloatField(default=None, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    grade = models.CharField(max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hr_rating_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hr_rating_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'hr_rating'


class KPIOverall(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    percentage = models.FloatField(default=None, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_overall_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_overall_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kpi_overall'


class Criticality(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criticality_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criticality_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'criticality'


class PotentialForImprovement(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='potential_for_improvement_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='potential_for_improvement_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'potential_for_improvement'


class TechnicalImplementationOperational(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='technical_implementation_operational_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='technical_implementation_operational_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'technical_implementation_operational'


class TopAverageBottomPerformer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='top_average_bottom_performer_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='top_average_bottom_performer_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'top_average_bottom_performer'


class BestPerformerTeam(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_performer_team_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_performer_team_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'best_performer_team'


class BestPerformerOrganization(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='best_performer_organization_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='best_performer_organization_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'best_performer_organization'


class BestPerformerPM(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_performer_pm_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_performer_pm_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'best_performer_pm'


class BestInnovatorTeam(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    shortlist = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_innovator_team_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='best_innovator_team_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'best_innovator_team'
