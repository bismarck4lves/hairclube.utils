
from core import models
from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.management.common_commands import CommonComands

SITUATION_CONFIRMED = 1
SITUATION_DONE = 2


class SyncSchedulesHandler(
    BaseCommand,
    CommonComands
):
    @transaction.atomic
    def exec_handle(self, *args, **options):
        self.log_info("INCIANDO SINCRONISMO DE AGENDAMENTOS")
        today = timezone.now().date()
        data = models.Schedule.objects.filter(
            situation=1,
            schedule__date__lt=today
        )
        for item in data:
            item.situation = SITUATION_DONE
            item.save()
