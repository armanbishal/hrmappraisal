from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, Group
from django.contrib.auth.models import Group
# Create your models here.


class User(AbstractUser):
    employee = models.IntegerField(blank=True, null=True )
    project = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    forget_password_token = models.CharField(max_length=100,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=255,null=True, blank=True)
    organization = models.CharField(max_length=255,null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    zipcode = models.CharField(max_length=255,null=True, blank=True)
    group = models.CharField(max_length=50,blank=True, null=True )
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField( blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-created_date', '-updated_date']

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['id']
        db_table = 'auth_user'

class Log(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    component = models.CharField(max_length=30)
    action = models.CharField(max_length=20)
    login_data = models.CharField(max_length=300,null=True, blank=True)
    logout_data = models.CharField(max_length=300,null=True, blank=True)
    date_time = models.DateTimeField()
    ip = models.GenericIPAddressField()

    class Meta:
        db_table = 'logger'


class Functionname(models.Model):
    module_type = models.CharField(max_length=300, null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.module_type

    class Meta:
        db_table = 'functionname'


class Modulename(models.Model):
    module_type = models.ForeignKey(Functionname, on_delete=models.CASCADE,null=True, blank=True)
    module_name = models.CharField(max_length=300, null=True, blank=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.module_name

    class Meta:
        db_table = 'modulename'


class Moduleurl(models.Model):
    module = models.ForeignKey(Modulename, on_delete=models.CASCADE)
    module_type = models.ForeignKey(Functionname, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return self.module_name
    def __str__(self):
        return self.url

    class Meta:
        db_table = 'moduleurl'


class Privileged(models.Model):
    module = models.ForeignKey(Modulename, on_delete=models.CASCADE)
    moduleurl = models.ForeignKey(Moduleurl, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="user_priv_group")
    module_type = models.ForeignKey(Functionname, on_delete=models.CASCADE,null=True, blank=True)
    user_role_type = models.IntegerField(null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'privileged'
