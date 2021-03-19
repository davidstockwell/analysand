from django.contrib import admin

from .models import *

admin.site.register(Practice)
admin.site.register(Practitioner)
admin.site.register(Client)
admin.site.register(Assessment)
admin.site.register(ContractType)
admin.site.register(Contract)
admin.site.register(ClientHolidayPeriod)
admin.site.register(PractitionerHolidayPeriod)
admin.site.register(Session)
