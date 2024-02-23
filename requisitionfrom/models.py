from django.db import models

# Create your models here.
from configuration.models import Project, Employee
from usermanagement.models import User


class Certificaterequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='certificate_request_project')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='certificate_request_employee')
    remark = models.CharField(max_length=255)
    refno = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_request_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_request_updated_by')
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_request_approved_by', null=True)
    approved_by = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'certificate_request'

class Resourcerequisition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource_requisition_project')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='resource_requisition_employee')
    comment_unit_head = models.CharField(max_length=255)
    comment_sub_director = models.CharField(max_length=255)
    comment_director_finance = models.CharField(max_length=255)
    comment_chief_executive = models.CharField(max_length=255)
    comment_hr = models.CharField(max_length=255)
    requisition_raised_by = models.CharField(max_length=255)
    quantity_requisition = models.CharField(max_length=255)
    new_recruit = models.CharField(max_length=255)
    replacement = models.CharField(max_length=255)
    internal_fund = models.CharField(max_length=255)
    project_invoice= models.CharField(max_length=255)
    refno = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_requisition_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_requisition_updated_by')
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_requisition_approved_by', null=True)
    approved_by = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'resource_requisition'


class Noobjectioncertificaterequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='noobjectioncertificate_request_project')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='noobjectioncertificate_request_employee')
    remark = models.CharField(max_length=255)
    refno = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noobjectioncertificate_request_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noobjectioncertificate_request_updated_by')
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noobjectioncertificate_request_approved_by', null=True)
    approved_by = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'noobjectioncertificate_request'
