from core import models
from django.db.transaction import atomic
from django.utils import timezone
from core.management.common_commands import CommonComands
from core.constants.variables import (
    SCHEDULE_SITUATION_CANCEL,
    SCHEDULE_SITUATION_SCHEDULED,
    SCHEDULE_ORIGIN_CANCEL,
    PAYMENT_CONDITION_COURTESY,
    PLAN_PROMO,
    SUBSCRIPTION_STATUS_ACTIVE,
)
from django.core.management.base import BaseCommand


class CancelPlanHandler(
    BaseCommand,
    CommonComands
):
    @atomic
    def exec_handle(self):
        self.log_info("INCIANDO CANCELAMENTOS")
        job = models.CancelPlansJob.objects.filter(
            target_cancel_date__lte=timezone.now().date(),
            is_canceled=0
        )
        if not job:
            self.log_warning("NENHUM CANCELAMENTO DE PLANO AGENDADO PARA HOJE OU DATAS PASSADAS") # noqa

        for item in job:
            subs = models.Subscription.objects.filter(
                id=item.subscription_id
            ).first()
            if not subs:
                return
            self.cancel_schedule(subs.client_id)
            self.cancel_all_plans(subs.client_id, item.reason)
            self.set_basic_plan(subs.client_id)
            item.is_canceled = 1
            item.save()

    def cancel_all_plans(self, client_id, subscription_status_id):
        data = models.Subscription.objects.filter(
            client_id=client_id,
            cancellation_date__isnull=True
        )
        for item in data:
            item.cancellation_date = timezone.now()
            item.subscription_status_id = subscription_status_id
            item.save()
        self.log_success(f"{len(data)} planos cancelados")

    def set_basic_plan(self, client_id):
        models.Subscription.objects.create(
            client_id=client_id,
            created_at=timezone.now(),
            payment_condition_id=PAYMENT_CONDITION_COURTESY,
            plan_id=PLAN_PROMO,
            subscription_status_id=SUBSCRIPTION_STATUS_ACTIVE,
            external_payment_id="",
            value=0
        )
        self.log_success("Um plano básico associado")

    def cancel_schedule(self, client_id):
        data = models.Schedule.objects.filter(
            client_id=client_id,
            situation=SCHEDULE_SITUATION_SCHEDULED
        ).update(
            cancel_origin=SCHEDULE_ORIGIN_CANCEL,
            situation=SCHEDULE_SITUATION_CANCEL
        )
        self.log_success(f"{data} agendamentos cancelados")
