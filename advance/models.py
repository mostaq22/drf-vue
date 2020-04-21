from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CommonInfoModel(models.Model):
    name = models.CharField(unique=True, max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Client(CommonInfoModel):
    pass


class Category(CommonInfoModel):
    pass


class Unit(CommonInfoModel):
    pass


class Department(CommonInfoModel):
    pass


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        Running = 'R'
        Completed = 'C'
        Upcoming = 'U'
        Postpont = 'P'

    name = models.CharField(max_length=200, unique=True)
    # generate automatically based on CLIENT_ID-DEPARTMENT_ID-
    code = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=False)
    requisition_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(
        max_length=2, choices=ProjectStatus.choices, default=ProjectStatus.Completed)

    description = models.TextField()

    def __str__(self):
        return self.name


class Site(models.Model):
    class SiteStatus(models.TextChoices):
        Running = 'R'
        Completed = 'C'
        Upcoming = 'U'
        Postpone = 'P'

    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(
        max_length=2, choices=SiteStatus.choices, default=SiteStatus.Completed)

    def __str__(self):
        return self.name

    def client(self):
        return self.project.client.name

    def department(self):
        return self.project.department.name


class Requisition(models.Model):
    site = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True, blank=False)
    submitted_for = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False, related_name='submitted_for')
    team = models.ManyToManyField(User, related_name='teams', blank=False)
    working_date = models.DateField(auto_now=False)
    payment_method = models.CharField(max_length=200)
    description = models.TextField()


class RequisitionDetail(models.Model):
    requistion = models.ForeignKey(
        Requisition, on_delete=models.SET_NULL, null=True, blank=False, related_name='detail')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=False)
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=200)


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline
