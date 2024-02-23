import string
import random
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from usermanagement.decorators import *
from .forms import *
from configuration.forms import *
from django.contrib import *
from datetime import datetime, date
from num2words import num2words
current_day = date.today().day
current_month = date.today().month
current_year = date.today().year

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def billList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    bill_list = Invoice.objects.all()
    files = FileUpload.objects.all()

    context = {
        'data': userdata,
        'bill_list': bill_list,
        'files': files,
    }

    return render(request, 'billmanagement/bill/billlist.html', context)

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def billFormPage(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    invoice_item = InvoiceItem.objects.all()
    project_list = Project.objects.all()
    employee_list = Employee.objects.all()
    invoice_form = InvoiceItemForm()

    if 'billform-save' in request.POST:
        project_id = request.POST.get('project')
        employee_id = request.POST.get('employee_id')
        total_amount = request.POST.get('total_amount')
        date = request.POST.getlist('date[]')
        particulars = request.POST.getlist('particulars[]')
        unit = request.POST.getlist('unit[]')
        unit_price = request.POST.getlist('unitPrice[]')
        letters = string.ascii_lowercase
        dateformat = datetime.now()
        invoice_code = dateformat.strftime("%d%m%Y") + str(random.randint(100000, 999999))
        invoice_date = request.POST.get('invoice_date')

        files = request.FILES.getlist('files[]')
        print('file name',request.FILES.getlist('files[]'))

        emp = Employee.objects.get(employee_id__exact=employee_id)
        # print(request.FILES.getlist('files[]'))
        # file_form = FileUploadForm(request.FILES.getlist('files[]'))
        # if file_form.is_valid():
        #     file_save = file_form.save(commit=False)
        #     file_save.save()

        inv = Invoice.objects.create(
            project=Project.objects.get(id=project_id),
            employee=emp,
            status=Status.objects.get(value=1),
            totalamount=total_amount,
            invoice_code=invoice_code,
            invoice_date=invoice_date,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            created_by_id=request.session['id'],
            updated_by_id=request.session['id'],
            valid=1
        )

        for file in files:
            FileUpload.objects.create(main_img=file,
                                      invoice=Invoice.objects.latest('id'),
                                      created_by_id=request.session['id'])
            print(file)

        for i in range(0, len(particulars)):

            InvoiceItem.objects.create(
                name=emp.name,
                description=particulars[i],
                qty=int(unit[i]),
                cost=int(unit_price[i]),
                date=date[i],
                invoice=inv
            )


        messages.success(request, "Data Successfully Saved")
        return redirect("billmanagement:billlist")

    context = {
        'data': userdata,
        'invoice_item': invoice_item,
        'invoice_form': invoice_form,
        'project_list': project_list,
        'employee_list': employee_list,
    }

    return render(request, 'billmanagement/bill/billform.html', context)

def BillInvoice(request,pk):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    billlist = Invoice.objects.get(id=pk)
    # print(billlist)
    invoiceite=InvoiceItem.objects.filter(invoice_id=pk)
    # print(invoiceite)
    word=num2words(billlist.totalamount)

    context = {
        'data': userdata,
        'billlist': billlist,
        'invoiceite': invoiceite,
        'word': word,
    }

    return render(request, 'billmanagement/bill/invoice.html', context)

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def billApprove(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    bill_list = Invoice.objects.all()

    context = {
        'data': userdata,
        'bill_list': bill_list,
    }

    return render(request, 'billmanagement/bill/billapprove.html', context)

def BillStatus(request,pk):
    try:
        Invoice.objects.filter(id=pk).update(status_id=2)
        # if request.POST:
        #     Invoice.objects.filter(id=pk).update(status_id=2)
        #     print(request.POST,pk)
        messages.success(request, 'Data Successfully Approved')
        return redirect('billmanagement:billApprove')
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('billmanagement:billApprove')

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def conveyanceList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    conveyance_list = Conveyance.objects.all()

    context = {
        'data': userdata,
        'conveyance_list': conveyance_list
    }

    return render(request, 'billmanagement/conveyance/conveyancelist.html', context)

def conveyanceFormPage(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    conveyance_form = ConveyanceItem.objects.all()
    project_list = Project.objects.all()
    employee_list = Employee.objects.all()
    invoice_item = InvoiceItem.objects.all()
    project_list = Project.objects.all()
    employee_list = Employee.objects.all()
    invoice_form = InvoiceItemForm()

    if 'conveyanceform-save' in request.POST:

        project_id = request.POST.get('project')
        employee_id = request.POST.get('employee_id')
        total_amount = request.POST.get('total_amount')
        date = request.POST.getlist('date[]')
        purpose_from = request.POST.getlist('purposefrom[]')
        purpose_to = request.POST.getlist('purposeto[]')
        purpose_visit = request.POST.getlist('purposevisit[]')
        mode_of_transport = request.POST.getlist('modetransport[]')
        amount = request.POST.getlist('amount[]')
        letters = string.ascii_lowercase
        dateformat = datetime.now()
        invoice_code = dateformat.strftime("%d%m%Y") + str(random.randint(100000, 999999))
        emp = Employee.objects.get(employee_id__exact=employee_id)

        conv = Conveyance.objects.create(
            project=Project.objects.get(id=project_id),
            employee=emp,
            status=Status.objects.get(value=1),
            totalamount=total_amount,
            invoice_code=invoice_code,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            created_by_id=request.session['id'],
            updated_by_id=request.session['id']
        )

        for i in range(0, len(purpose_from)):
            conv_item = ConveyanceItem.objects.create(
                date=date[i],
                purposefrom=purpose_from[i],
                purposeto=purpose_to[i],
                purposevisit=purpose_visit[i],
                modetransport=mode_of_transport[i],
                amount=amount[i],
                conveyance=conv
            )

        messages.success(request, "Data Successfully Saved")
        return redirect("billmanagement:conveyancelist")

    context = {
        'data': userdata,
        'conveyance_form': conveyance_form,
        'project_list': project_list,
        'employee_list': employee_list,
    }

    return render(request, 'billmanagement/conveyance/conveyanceform.html', context)

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def conveyanceApprove(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    conveyance_list = Conveyance.objects.all()

    context = {
        'data': userdata,
        'conveyance_list': conveyance_list
    }

    return render(request, 'billmanagement/conveyance/conveyanceapprove.html', context)