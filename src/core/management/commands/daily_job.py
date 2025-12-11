from django.core.management.base import BaseCommand
from core.handlers.cancel_plan_handler import CancelPlanHandler
from core.handlers.email_report_handler import EmailReportHandler
from core.handlers.sync_sheduldes_handler import SyncSchedulesHandler


class Command(BaseCommand):

    def handle(self, *args, **options):
        SyncSchedulesHandler().exec_handle()
        CancelPlanHandler().exec_handle()
        EmailReportHandler().exec_handle()
