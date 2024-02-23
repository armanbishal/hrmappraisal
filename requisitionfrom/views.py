from django.contrib import messages
from django.utils import timezone, dateformat
from django.shortcuts import render, redirect
from django.utils import dateformat
from usermanagement.models import User
# Create your views here.
import usermanagement.decorators
from requisitionfrom.models import *
from configuration.models import Employee
from usermanagement.decorators import login_required, access_permission_required


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def CertificateRequestList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    user = User.objects.get(id=request.session['id'])
    employee = Employee.objects.get(id=user.employee)
    formatted_date = dateformat.format(timezone.now(), 'YmdHis')
    certificaterequest = Certificaterequest.objects.filter(created_by_id=user.id)

    context = {
        'formatted_date': formatted_date,
        'employee': employee,
        'data': userdata,
        'certificaterequest': certificaterequest
    }

    return render(request, 'requisitionfrom/salarycertificate/salarycertificaterequest.html', context)


def CertificateRequestForm(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    if request.POST:
        user = User.objects.get(id=request.session['id'])
        createdate = dateformat.format(timezone.now(), 'Y-m-d')
        Certificaterequest.objects.create(date=createdate, remark=request.POST['remark'],
                                          refno='DS/HR/ Salary/' + request.POST['formatted_date'],
                                          employee_id=user.employee,
                                          project_id=user.project, created_by_id=user.id, created_date=timezone.now())
        messages.success(request, "Data Successfully Saved")
        return redirect("requisitionfrom:certificateRequestList")

    context = {
        'data': userdata,
    }


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def CertificateRequestApprove(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    certificaterequest = Certificaterequest.objects.all()

    context = {
        'data': userdata,
        'certificaterequest': certificaterequest
    }

    return render(request, 'requisitionfrom/salarycertificate/salarycertificateapprove.html', context)


def CertificaterequestStatus(request, id):
    try:

        Certificaterequest.objects.filter(id=id).update(status=1)
        messages.success(request, 'Data Successfully Approved')
        return redirect('requisitionfrom:CertificateRequestApprove')
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('requisitionfrom:CertificateRequestApprove')


def SalaryCertificateview(request, employee_id):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    certificaterequest = Certificaterequest.objects.all()

    context = {
        'data': userdata,
        'certificaterequest': certificaterequest
    }

    return render(request, 'requisitionfrom/salarycertificate/salarycertificateview.html', context)


def SalaryCertificateadd(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    user = User.objects.get(id=request.session['id'])
    employee = Employee.objects.get(id=user.employee)
    formatted_date = dateformat.format(timezone.now(), 'YmdHis')
    certificaterequest = Certificaterequest.objects.filter(created_by_id=user.id)

    context = {
        'formatted_date': formatted_date,
        'employee': employee,
        'data': userdata,
        'certificaterequest': certificaterequest
    }

    return render(request, 'requisitionfrom/salarycertificate/salarycertificateadd.html', context)


def ResourceRequisitionList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    user = User.objects.get(id=request.session['id'])
    employee = Employee.objects.get(id=user.employee)
    formatted_date = dateformat.format(timezone.now(), 'YmdHis')
    resourcerequisition = Resourcerequisition.objects.filter(created_by_id=user.id)

    context = {
        'formatted_date': formatted_date,
        'employee': employee,
        'data': userdata,
        'resourcerequisition': resourcerequisition
    }

    return render(request, 'requisitionfrom/resourcerequisition/resourcerequisitionlist.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def NoObjectionCertificateList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    user = User.objects.get(id=request.session['id'])
    employee = Employee.objects.get(id=user.employee)
    formatted_date = dateformat.format(timezone.now(), 'YmdHis')
    noobjectioncertificate = Noobjectioncertificaterequest.objects.filter(created_by_id=user.id)
    print(noobjectioncertificate)
    context = {
        'formatted_date': formatted_date,
        'employee': employee,
        'data': userdata,
        'noobjectioncertificate': noobjectioncertificate
    }

    return render(request, 'requisitionfrom/noobjectioncertificate/noobjectioncertificatelist.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def NoObjectionCertificateForm(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }

    user = User.objects.get(id=request.session['id'])
    employee = Employee.objects.get(id=user.employee)

    context = {
        'data': userdata,
        'employee': employee
    }

    return render(request, 'requisitionfrom/noobjectioncertificate/noobjectioncertificaterequest.html', context)


def NoObjectionCertificateSave(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    if request.POST:
        user = User.objects.get(id=request.session['id'])
        createdate = dateformat.format(timezone.now(), 'Y-m-d')
        refdate = dateformat.format(timezone.now(), 'Ymdhis')
        Noobjectioncertificaterequest.objects.create(date=createdate, remark=request.POST['remark'],
                                                     refno=refdate,
                                                     employee_id=user.employee,
                                                     project_id=user.project, created_by_id=user.id,
                                                     created_date=timezone.now())
        messages.success(request, "Data Successfully Saved")
        return redirect("requisitionfrom:NoObjectionCertificateList")

    context = {
        'data': userdata,
    }
