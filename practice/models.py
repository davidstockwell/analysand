from django.db import models
from django.contrib.auth.models import User
from schedule.models import Event, Occurrence

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-binary'),
    ('fluid', 'Gender fluid'),
    ('unknown', 'Unknown'),
    ('other', 'Other'),
)

CONTACT_METHOD_CHOICES = (
    ('in_person', 'In person'),
    ('video_call', 'Video call'),
    ('telephone', 'Telephone'),
    ('ad_hoc', 'Ad-hoc'),
)

CONTRACT_STATUS_CHOICES = (
    ('active', 'Active'),
    ('paused', 'Paused'),
    ('ended', 'Ended'),
)

SESSION_ATTENDANCE_CHOICES = (
    ('attended', 'Attended'),
    ('cancelled', 'Cancelled'),
    ('missed', 'Missed')
)

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Practice(TimestampedModel):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name


class Practitioner(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ManyToManyField(Practice)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Client(TimestampedModel):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField(null=True, blank=True)
    alias = models.CharField(max_length=16,  unique=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES)

    def __str__(self):
        return self.alias


    class Meta:
        ordering = ['alias']


class Assessment(TimestampedModel):
    assessment_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    assessment_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    assessment_practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.event)


class ContractType(TimestampedModel):
    name = models.CharField(max_length=64)
    sessions_per_week = models.FloatField(default=1)
    missed_sessions_payable = models.BooleanField(default=True)
    holiday_allowance_per_year = models.IntegerField(default=4)
    typical_contact_method = models.CharField(max_length=32, choices=CONTACT_METHOD_CHOICES)

    class Meta:
        verbose_name = 'Contract type'
        verbose_name_plural = 'Contract types'

    def __str__(self):
        return self.name

class Contract(TimestampedModel):
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    contract_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    contract_practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    fee_per_session = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=CONTRACT_STATUS_CHOICES)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} - {} [{}]'.format(self.contract_client, self.contract_type, self.status)


class ClientHolidayPeriod(TimestampedModel):
    holiday_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '{} - {} to {}'.format(self.holiday_client, self.start_date, self.end_date)


class PractitionerHolidayPeriod(TimestampedModel):
    holiday_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '{} - {} to {}'.format(self.holiday_practitioner, self.start_date, self.end_date)


class Session(Occurrence):
    attendance = models.CharField(max_length=16, choices=SESSION_ATTENDANCE_CHOICES)

    def __str__(self):
        return '{} ({}) [{}]'.format(
                self.title,
                self.start.strftime('%Y-%m-%d %H:%M'),
                self.attendance
            )
