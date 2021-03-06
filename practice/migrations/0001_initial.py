# Generated by Django 3.1.7 on 2021-03-12 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0012_auto_20191025_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimestampedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('alias', models.CharField(max_length=16)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('non_binary', 'Non-binary'), ('fluid', 'Gender fluid'), ('unknown', 'Unknown'), ('other', 'Other')], max_length=16)),
            ],
            bases=('practice.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('name', models.CharField(max_length=64)),
                ('sessions_per_week', models.FloatField(default=1)),
                ('missed_sessions_payable', models.BooleanField(default=True)),
                ('holiday_allowance_per_year', models.IntegerField(default=4)),
                ('typical_contact_method', models.CharField(choices=[('in_person', 'In person'), ('video_call', 'Video call'), ('telephone', 'Telephone'), ('ad_hoc', 'Ad-hoc')], max_length=32)),
            ],
            bases=('practice.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('name', models.CharField(max_length=64)),
            ],
            bases=('practice.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('practice', models.ManyToManyField(to='practice.Practice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('practice.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('fee_per_session', models.FloatField(blank=True, null=True)),
                ('date_started', models.DateField()),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('ended', 'Ended')], max_length=16)),
                ('contract_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.client')),
                ('contract_practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.practice')),
                ('contract_practitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.practitioner')),
                ('contract_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.contracttype')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.event')),
            ],
            bases=('practice.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='practice.timestampedmodel')),
                ('assessment_date', models.DateTimeField()),
                ('assessment_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.client')),
                ('assessment_practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.practice')),
                ('assessment_practitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practice.practitioner')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.event')),
            ],
            bases=('practice.timestampedmodel',),
        ),
    ]
