from django.contrib import admin
from schedule.models import Event
from .models import *


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment_practitioner', 'assessment_client', 'event')
    list_filter = ('assessment_practitioner', 'assessment_client')


class ContractInline(admin.StackedInline):
    model = Contract
    fk_name = 'contract_client'
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    inlines = [ContractInline]


class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_practitioner', 'contract_client', 'contract_type', 'status')
    list_filter = ('contract_practitioner', 'contract_type', 'status')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('client', 'start', 'attendance')


admin.site.register(Practice)
admin.site.register(Practitioner)
admin.site.register(Client, ClientAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(ContractType)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ClientHolidayPeriod)
admin.site.register(PractitionerHolidayPeriod)
admin.site.register(Session, SessionAdmin)
