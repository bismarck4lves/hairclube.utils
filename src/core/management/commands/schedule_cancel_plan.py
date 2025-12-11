from dateutil.relativedelta import relativedelta
from django.db.transaction import atomic
from django.core.management.base import BaseCommand
from core import models
from ..common_commands import CommonComands
from core.constants.variables import (
    SUBSCRIPTION_STATUS_CANCELED_BY_CLIENT,
    SUBSCRIPTION_STATUS_CANCELED_BY_NON_PAYMENT,
)

from .utils import (
    read_csv_file,
    chose_file,
    get_file_name,
    is_real_email,
    is_nan,
    set_case,
)


class Command(BaseCommand, CommonComands):
    @atomic
    def handle(self, *args, **options):
        try:
            data = self.console_interations_and_load_file()
            if not data:
                self.log_error("Nenhum arquivo compativel")
            serializer_data = self.serialize_fiels(data)
            self.validate_fields(serializer_data)
            for item in serializer_data:
                email = item.get("EMAIL", None)
                case = set_case(str(item['MOTIVO']))
                client = self.get_client(email)
                if not client:
                    self.log_warning(
                        f"cliente de email: {email} nao encontrado"
                    )
                    return
                subscription = self.get_current_subscription(client.id)
                if not subscription:
                    self.log_warning("Assinatura nao encontrada ou inativada")
                self.create_subscription_schedule(subscription, case)
        except Exception as e:
            self.log_error(str(e))

    def serialize_fiels(self, data):
        to_return = []
        for item in data:
            email = item.get("EMAIL", None)
            if not is_nan(email):
                to_return.append(item)
        return to_return

    def validate_fields(self, data):
        for attrs in data:
            email = attrs.get("EMAIL", None)
            if not email:
                raise ValueError(
                    "O formato do arquivo nao compativel (EMAIL)"
                )
            if not is_real_email(email):
                raise ValueError(
                    f"O formato do arquivo nao compativel (EMAIL invalido) [{email}]" # noqa
                )
            if not attrs.get('MOTIVO', None):
                raise ValueError(
                    "O formato do arquivo nao compativel (MOTIVO)"
                )

    def console_interations_and_load_file(self):
        path = chose_file("cancelamentos")
        file_name = get_file_name(path)
        confirm = input(f"confirma acao para o arquivo {file_name} [S/N]")
        if confirm.lower() == "s":
            return read_csv_file(path)
        return None

    def get_current_subscription(self, client_id):
        return models.Subscription.objects.filter(
            client_id=client_id,
            cancellation_date__isnull=True
        ).first()

    def create_subscription_schedule(self, subscription, case):
        target_cancel_date = self.get_next_month_same_day(
            subscription.created_at
        )
        current = models.CancelPlansJob.objects.filter(
            subscription_id=subscription.id
        )
        if not current:
            models.CancelPlansJob.objects.create(
                subscription_id=subscription.id,
                target_cancel_date=target_cancel_date,
                reason=self.transalte_case_to_numeber(case),
                is_canceled=0
            )

    @staticmethod
    def get_next_month_same_day(dt):
        if not dt:
            return None
        return (dt + relativedelta(months=1) - relativedelta(days=1)).date()

    @staticmethod
    def get_client(email):
        return models.Client.objects.filter(
            email__icontains=email.strip()
        ).first()

    @staticmethod
    def transalte_case_to_numeber(case):
        if case == "canceled_by_non_payment":
            return SUBSCRIPTION_STATUS_CANCELED_BY_NON_PAYMENT
        if case == "canceled_by_client":
            return SUBSCRIPTION_STATUS_CANCELED_BY_CLIENT
        return SUBSCRIPTION_STATUS_CANCELED_BY_CLIENT
