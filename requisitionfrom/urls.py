from django.urls import path
from .views import *

app_name = 'requisitionfrom'

urlpatterns = [

    path('certificateRequest/', CertificateRequestList, name='certificateRequestList'),
    path('SalaryCertificateadd/', SalaryCertificateadd, name='SalaryCertificateadd'),
    path('CertificateRequestForm/', CertificateRequestForm, name='CertificateRequestForm'),
    path('CertificateRequestApprove/', CertificateRequestApprove, name='CertificateRequestApprove'),
    path('CertificaterequestStatus/<id>/', CertificaterequestStatus, name='CertificaterequestStatus'),
    path('SalaryCertificateview/<employee_id>/', SalaryCertificateview, name='SalaryCertificateview'),
    path('ResourceRequisitionList/', ResourceRequisitionList, name='ResourceRequisitionList'),
    path('NoObjectionCertificateList/', NoObjectionCertificateList, name='NoObjectionCertificateList'),
    path('NoObjectionCertificateForm/', NoObjectionCertificateForm, name='NoObjectionCertificateForm'),
    path('NoObjectionCertificateSave/', NoObjectionCertificateSave, name='NoObjectionCertificateSave'),

]
