from django.core.management.base import BaseCommand
from core import models
from django.db import transaction
from django.utils import timezone

SITUATION_CONFIRMED = 1
SITUATION_DONE = 2


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().date()
        data = models.Schedule.objects.filter(
            situation=1,
            schedule__date__lt=today
        )
        for item in data:
            item.situation = SITUATION_DONE
            item.save()
