from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from uuid import uuid4

from .managers import UserManager

# Create your models here.
PACKAGES = [
('BASIC', 'Basic'),
('GOLD', 'Gold'),
]

NETWORKS = {
    ('twitter','Twitter'),
    ('facebook','Facebook'),
    ('googleplus','Google+'),
    ('instagram','Instagram'),
    ('whatsapp','WhatsApp'),
    ('linkedin','LinkedIn'),
    ('youtube','YouTube'),
    ('email','Email'),
}
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(max_length=255,unique=True)
    tel = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    package = models.CharField(max_length=255,choices=PACKAGES)
    referral_code = models.UUIDField(default=uuid4, editable=False, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','tel','first_name','last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.username},{self.first_name},{self.last_name},{self.tel}"
class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.FloatField()
    last_updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username},{self.balance},{self.last_updated_on}"
class Referral(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, to_field='username' ,related_name='+', on_delete=models.CASCADE)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL,editable=False, to_field='username' ,related_name='+', on_delete=models.CASCADE)
    fee_paid = models.BooleanField(default=False)
    date_confirmed = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=60000)
    timesent = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255,default='sent')

    objects = UserManager()

    def __str__(self):
        return self.subject
class Notification(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='username' ,related_name='+', on_delete=models.CASCADE)
    to = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='username' ,related_name='+', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=60000)
    timesent = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255,default='sent')

    objects = UserManager()

    def __str__(self):
        return self.message
class Feedback(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tel = models.CharField(max_length=255)
    can_be_contacted = models.BooleanField(default=False)
    message = models.TextField(max_length=300)

    objects = UserManager()
    def __str__(self):
        return self.message
class SocialNetwork(models.Model):
    network = models.CharField(max_length=30,unique=True,choices=NETWORKS)
    username = models.CharField(max_length=30)
    url = models.URLField()

    objects = UserManager()

    def __str__(self):
        return self.network

class Address(models.Model):
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=50)
    website = models.URLField()
    company_name = models.CharField(max_length=50)

    objects = UserManager()
    
    def __str__(self):
        return self.address_line_1
    
    class Meta:
        verbose_name_plural = 'Addresses'

class Objective(models.Model):
    heading = models.CharField(max_length=50)
    summary = models.TextField(max_length=10000)

    objects = UserManager()

    def __str__(self):
        return self.heading

class FactAtAGlance(models.Model):
    term = models.CharField(max_length=50)
    definition = models.CharField(max_length=20)
    fact_order = models.IntegerField(unique=True)

    objects = UserManager()

    def __str__(self):
        return self.term
    
    class Meta:
        verbose_name = 'Fact at a Glance'
        verbose_name_plural = 'Facts at a Glance'

class AboutParagraph(models.Model):
    paragraph_order = models.IntegerField(unique=True)
    paragraph_text = models.TextField(max_length=1500)

    objects = UserManager()

    def __str__(self):
        return str(self.paragraph_order)

class FAQ(models.Model):
    keyword = models.CharField(max_length=50)
    question = models.CharField(max_length=50)
    answer = models.TextField(max_length=10000)
    faq_order = models.IntegerField(unique=True)

    objects= UserManager()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Frequently asked Questions'
        verbose_name = 'Frequently asked Question'
class TermsAndCondition(models.Model):
    term = models.CharField(max_length=50)
    description = models.TextField(max_length=10000)
    term_order = models.IntegerField(unique=True)

    objects = UserManager()

    def __str__(self):
        return self.term
    class Meta:
        verbose_name = 'Term or Condition'
        verbose_name_plural = 'Terms and Conditions'
class PrivacyPolicy(models.Model):
    heading = models.CharField(max_length=50)
    description = models.TextField(max_length=10000)
    objects = UserManager()

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'
class Transaction(models.Model):
    transaction_code = models.CharField(max_length=255)
    amount = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timedone = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    objects = UserManager()

    def __str__(self):
        return self.transaction_code
        
class Statement(models.Model):
    statement_type = models.CharField(max_length=255)
    amount = models.FloatField()
    account = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username' ,related_name='+', on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    entry = models.CharField(max_length=255)

    objects = UserManager()

    def __str__(self):
        return self.amount