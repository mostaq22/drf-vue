from .models import Client, Category, Department, Unit, Project, Site, Requisition, RequisitionDetail
from django.contrib.auth.models import User
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'username']
        model = User


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Client


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Category


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Department


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Unit


class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    department = DepartmentSerializer(many=False)

    class Meta:
        fields = ['id', 'name', 'client', 'department']
        model = Project


class SiteSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False)

    class Meta:
        fields = ['id', 'name', 'project']
        model = Site


class RequisitionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = RequisitionDetail


class RequisitionSerializer(serializers.ModelSerializer):
    site = SiteSerializer(many=False)
    detail = RequisitionDetailSerializer(many=True)
    team = TeamSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'site', 'team', 'detail', 'working_date', 'payment_method', 'description']
        model = Requisition


class RequisitionTeamAddEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id']


class RequisitionCreateUpdateSerializer(serializers.ModelSerializer):
    detail = RequisitionDetailSerializer(many=True)
    # team = RequisitionTeamAddEditSerializer(many=True)

    class Meta:
        model = Requisition
        fields = ('id', 'site', 'team', 'working_date', 'payment_method', 'description', 'detail')

    def create(self, validated_data):
        details = validated_data.pop('detail')
        team = validated_data.pop('team')
        requisition = Requisition.objects.create(**validated_data)
        requisition.team.add(*team)
        details_list = []
        for detail in details:
            details_list.append(RequisitionDetail(requistion=requisition, **detail))
        RequisitionDetail.objects.bulk_create(details_list)
        return requisition
