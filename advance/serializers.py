from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

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
    category = CategorySerializer(many=False)
    unit = UnitSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = RequisitionDetail


class RequisitionDetailCreateSerializer(serializers.ModelSerializer):
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


class RequisitionCreateSerializer(serializers.ModelSerializer):
    detail = RequisitionDetailCreateSerializer(many=True)

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


class RequisitionDetailUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        fields = '__all__'
        model = RequisitionDetail


class RequisitionUpdateSerializer(serializers.ModelSerializer):
    detail = RequisitionDetailUpdateSerializer(many=True)

    class Meta:
        model = Requisition
        fields = ('id', 'site', 'team', 'working_date', 'payment_method', 'description', 'detail')

    def update(self, instance, validated_data):
        details = validated_data.pop('detail')
        team = validated_data.pop('team')
        for (k, v) in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        # Delete then Insert M2M
        instance.team.clear()
        instance.team.add(*team)
        # Update and create Child Model
        update = []
        create = []
        for detail in details:
            update.append(detail) if detail.get('id', None) else create.append(detail)
            obj, created = RequisitionDetail.objects.update_or_create(
                pk=detail.get('id'), requistion=instance, defaults={**detail}
            )
        return instance
