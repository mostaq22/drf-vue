# Generated by Django 3.0.5 on 2020-04-18 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advance', '0003_requisitiondetail_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisitiondetail',
            name='requistion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detail', to='advance.Requisition'),
        ),
    ]