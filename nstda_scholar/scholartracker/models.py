from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, RegexValidator

from django_countries.fields import CountryField


class Student(models.Model):
    STUDENT_STATUS_CHOICES = (
        ('GR', 'Graduated'),
        ('CO', 'Continuing'),
        ('FL', 'Failed'),
        ('PR', 'Preparing'),
    )

    first_name          = models.CharField(max_length=255, blank=False)
    last_name           = models.CharField(max_length=255, blank=False)
    status              = models.CharField(max_length=2, blank=False, choices=STUDENT_STATUS_CHOICES, default='CO')
    awarded_year        = models.PositiveIntegerField(validators=[
                            MinValueValidator(1900), 
                            MaxValueValidator(datetime.now().year)],
                            help_text="Use the following format: YYYY", 
                            default=datetime.now().year)

    scholarship_type    = models.ForeignKey('ScholarshipType')
    country             = CountryField(default='TH')
    major               = models.TextField(blank=True)
    special_emphasis    = models.TextField(blank=True)
    division            = models.ForeignKey('Division')
    email               = models.EmailField(blank=True)
    degree_sought_bs    = models.BooleanField(verbose_name='Bachelor')
    degree_sought_ms    = models.BooleanField(verbose_name='Master')
    degree_sought_dr    = models.BooleanField(verbose_name='Doctoral')

    def __str__(self):
        return '[%d] %s %s' % (self.id,self.first_name,self.last_name)


class Education(models.Model):
    DEGREE_TYPE_CHOICES = (
        ('PH', 'Doctoral'),
        ('MS', 'Master'),
        ('BS', 'Bachelor'),
    )

    owner       = models.ForeignKey('Student')
    degree      = models.CharField(max_length=2, choices=DEGREE_TYPE_CHOICES, default='PH')
    university  = models.ForeignKey('University')

class ScholarshipType(models.Model):
    type_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.type_name


class Division(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

class Phone(models.Model):
    PHONE_TYPE_CHOICES = (
        ('M', 'Mobile'),
        ('H', 'Home'),
        ('W', 'Work'),
        ('F', 'Fax'),
    )

    owner       = models.ForeignKey('Student')
    phone_type  = models.CharField(max_length=1, choices=PHONE_TYPE_CHOICES, default='M')
    number      = models.CharField(max_length=15, blank=True, validators=[RegexValidator(regex=r'\d+'), ])

class University(models.Model):
    name      = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "universities"

    def __str__(self):
        return self.name
