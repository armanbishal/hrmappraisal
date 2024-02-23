import uuid
from django.db import models
from configuration.models import Employee,Project
from usermanagement.models import *
# Create your models here.

class Invoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invoice_project')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='invoice_employee')
    invoice_date = models.DateField()
    invoice_code = models.CharField(max_length=255)
    valid = models.BooleanField(null=True)
    remark = models.TextField(null=True)
    approved_status = models.IntegerField(null=True, blank=True, default=0)
    totalamount = models.DecimalField(decimal_places=2, max_digits=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_approved_by', null=True)
    approved_at = models.DateTimeField(null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='invoice_status')

    def __str__(self):
        return str(self.id)

    def total_items(self):
        total = 0
        items = self.invoiceitem_set.all()

        for item in items:
            total += item.cost * item.qty

        return total

    def total(self):
        items = self.total_items()
        return items

    class Meta:
        db_table = 'invoice'

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    qty = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name

    def total(self):
        return self.cost * self.qty

    class Meta:
            db_table = 'invoice_item'

class Conveyance(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='conveyance_project')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='conveyance_employee')
    conveyance_date = models.DateField()
    invoice_code = models.CharField(max_length=255)
    valid = models.BooleanField(default=True)
    remark = models.TextField(null=True)
    approved_status = models.IntegerField(null=True, blank=True, default=0)
    totalamount = models.DecimalField(decimal_places=2, max_digits=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conveyance_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conveyance_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conveyance_approved_by', null=True)
    approved_by = models.DateTimeField(null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='conveyance_status')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'conveyance'

class ConveyanceItem(models.Model):
    conveyance = models.ForeignKey(Conveyance, on_delete=models.CASCADE)
    date = models.DateField()
    purposefrom = models.TextField(default=None, null=True, blank=True)
    purposeto = models.TextField(default=None, null=True, blank=True)
    purposevisit = models.CharField(max_length=100,default=None, null=True, blank=True)
    modetransport = models.CharField(max_length=100,default=None, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.id
    class Meta:
        db_table = 'conveyance_item'

class Status(models.Model):
    name = models.CharField(max_length=255,default=None, null=True, blank=True)
    value = models.IntegerField(default=None, null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'status'


class FileUpload (models.Model):
    title = models.TextField()
    main_img = models.ImageField(upload_to='invoice_images/')
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='status_invoice_created_by')
    conveyance=models.ForeignKey(Conveyance, on_delete=models.CASCADE, related_name='status_Conveyance_created_by')
    status=models.IntegerField(null=True, blank=True,default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fileupload_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fileupload_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()


    def __str__(self):
        return str(self.id)


    class Meta:
        db_table = 'file_upload'