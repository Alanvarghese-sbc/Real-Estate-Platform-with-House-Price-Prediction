# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddProperty(models.Model):
    property_id = models.AutoField(primary_key=True)
    fk_reg_id = models.IntegerField()
    property_name = models.CharField(max_length=100)
    property_desc = models.TextField()
    property_image = models.CharField(max_length=35)
    property_loc = models.CharField(max_length=50)
    property_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    property_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    property_district = models.CharField(max_length=50)
    property_area = models.CharField(max_length=50, blank=True, null=True)
    no_of_bed_rooms = models.IntegerField()
    price_listed = models.DecimalField(max_digits=10, decimal_places=0)
    price_predicted = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    property_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'add_property'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    fk_property_id = models.IntegerField()
    fk_user_id = models.IntegerField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=0)
    bid_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'bid'


class Broker(models.Model):
    broker_id = models.AutoField(primary_key=True)
    broker_name = models.CharField(max_length=50)
    broker_email = models.CharField(max_length=100)
    broker_gender = models.CharField(max_length=15)
    broker_phone = models.CharField(max_length=15)
    broker_district = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'broker'


class BrokerTransaction(models.Model):
    broker_transaction_id = models.AutoField(primary_key=True)
    fk_property_id = models.IntegerField()
    fk_buyer_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    commission = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20)
    created_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'broker_transaction'


class ChatBox(models.Model):
    chat_box_id = models.AutoField(primary_key=True)
    fk_chat_sender_id = models.IntegerField()
    fk_chat_receiver_id = models.IntegerField()
    message = models.TextField()
    chat_time = models.DateTimeField()
    fk_bid_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chat_box'

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'contact'



class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'district'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Login(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    user_type = models.CharField(max_length=20)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'login'


class PropertyRequest(models.Model):
    property_req_id = models.AutoField(primary_key=True)
    fk_property_id = models.IntegerField()
    fk_user_id = models.IntegerField()
    property_req_status = models.CharField(max_length=20)
    request_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'property_request'


class Register(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=150)
    user_type = models.CharField(max_length=20)
    address = models.TextField()
    location = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register'


class ScheduleBroker(models.Model):
    sch_broker_id = models.AutoField(primary_key=True)
    fk_property_req_id = models.IntegerField()
    fk_broker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'schedule_broker'
