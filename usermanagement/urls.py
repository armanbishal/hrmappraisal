from django.urls import path
from .views import *

app_name = 'usermanagement'

urlpatterns = [
    path('', login, name='login'),
    path('validate', login_validate, name='login_validate'),
    path('logout/', logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    # user-management
    path('authuserlist/', authUserList, name='authuserlist'),
    path('authuserrole/', authUserRole, name='authuserrole'),
    path('authuserpriviledge/<id>/', authUserPriviledge, name='authuserpriviledge'),
    path('PrIv3Yll22gE/', add_role_with_permission, name='add_role_with_permission'),
]
