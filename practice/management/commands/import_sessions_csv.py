import csv
from dateutil import parser
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from practice.models import Contract, Assessment, Session
from schedule.models import Event


class Command(BaseCommand):
    help = """
        Import a record of sessions for a given practice and practitioner.
        The CSV file should be in the format:
            client_alias,YYYY-MM-DD
    """

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('practice_id', type=int)
        parser.add_argument('practitioner_id', type=int)
        parser.add_argument('calendar_id', type=int)

        parser.add_argument(
            '--no-assessments',
            action='store_true',
            help='Treat session 1 as a session, not an assessment',
        )


    def handle(self, *args, **options):
        records_created = 0
        records_skipped = 0
        has_assessments = not options['no_assessments']

        with open(options['filename']) as csvfile:
            reader = csv.reader(csvfile)
            row_index = 1

            for row in reader:
                if row_index == 1:
                    # Ignore header line
                    row_index += 1
                    continue

                client_alias = row[0].strip()
                
                session_date = parser.parse('{} 00:00:00 UTC'.format(row[1]))
                session_date_start = session_date
                session_date_end = session_date.replace(hour=23, minute=59, second=59)

                session_number = int(row[2].strip())

                if session_number == 1 and has_assessments:
                    # Handle assessment
                    try:
                        client = Client.objects.get(alias=client_alias)

                        assessment, created = Assessment.objects.get_or_create(
                            assessment_practice__id=options['practice_id'],
                            assessment_practitioner__id=options['practitioner_id'],
                            assessment_client=client
                        )

                        if created:
                            event = Event.objects.create(
                                title='Assessment ({})'.format(client_alias),
                                start=session_date_start,
                                end=session_date_end,
                                calendar=options['calendar_id']
                            )

                            assessment.event = event
                            assessment.save()

                        session, created = Session.objects.create(
                            event=assessment.event,
                            title='Assessment ({})'.format(client_alias),
                            start=session_date.replace(hour=assessment.event.start.hour, minute=assessment.event.start.minute, second=0),
                            end=session_date.replace(hour=assessment.event.end.hour, minute=assessment.event.end.minute, second=0),
                            original_start=session_date.replace(hour=assessment.event.start.hour, minute=assessment.event.start.minute, second=0),
                            original_end=session_date.replace(hour=assessment.event.end.hour, minute=assessment.event.end.minute, second=0),
                            attendance='attended'
                        )

                        if created:
                            records_created += 1
                        else:
                            records_skipped += 1

                    except Client.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                'No client with alias {} on row {}'.format(
                                        client_alias,
                                        row_index
                                    )
                                )
                            )

                else:
                    # Handle session
                    try:
                        contract = Contract.objects.get(
                            Q(event__end_recurring_period__gte=session_date_start) | Q(event__end_recurring_period__isnull=True),
                            contract_practice__id=options['practice_id'],
                            contract_practitioner__id=options['practitioner_id'],
                            contract_client__alias=client_alias,
                            event__start__lte=session_date_end
                        )

                        session, created = Session.objects.get_or_create(
                            event=contract.event,
                            title='Session ({})'.format(client_alias),
                            start=session_date.replace(hour=contract.event.start.hour, minute=contract.event.start.minute, second=0),
                            end=session_date.replace(hour=contract.event.end.hour, minute=contract.event.end.minute, second=0),
                            original_start=session_date.replace(hour=contract.event.start.hour, minute=contract.event.start.minute, second=0),
                            original_end=session_date.replace(hour=contract.event.end.hour, minute=contract.event.end.minute, second=0),
                            attendance='attended'
                        )

                        if created:
                            records_created += 1
                        else:
                            records_skipped += 1

                    except Contract.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                'No contract found for client {} on row {}'.format(
                                        client_alias,
                                        row_index
                                    )
                                )
                            )

                row_index += 1
                
            self.stdout.write(self.style.SUCCESS('{} sessions created'.format(records_created)))

            if records_skipped > 0:
                self.stdout.write(self.style.WARNING('{} sessions skipped'.format(records_skipped)))

        self.stdout.write(self.style.SUCCESS('Done'))