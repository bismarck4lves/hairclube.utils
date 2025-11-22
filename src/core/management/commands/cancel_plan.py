import re
import math
import unicodedata

from django.utils import timezone
from django.db.transaction import atomic
from django.core.management.base import BaseCommand

from core import models

from .utils import (
    cancel_all_plans,
    read_csv_file,
    chose_file,
    get_file_name
)


class Command(BaseCommand):

    possible_status = {
        "active": 3,
        "canceled_by_client": 11,
        "canceled_by_non_payment": 12
    }

    @atomic
    def handle(self, *args, **options):
        path = chose_file("cancelamentos")
        file_name = get_file_name(path)
        confirm = input(f"confirma acao para o arquivo {file_name} [S/N]")

        if confirm.lower() == "s":
            data = read_csv_file(path)

            for item in data:
                email = item.get("EMAIL", None)
                if not email:
                    self.log_error(
                        "O formato do arquivo nao compativel (EMAIL)"
                    )
                    return
                if is_real_email(email):
                    reason = item.get('MOTIVO', None)
                    if not reason:
                        self.log_error(
                            "O formato do arquivo nao compativel (MOTIVO)"
                        )
                    case = set_case(str(item['MOTIVO']))
                    client = self.get_client_by_email(email)
                    if not client:
                        return
                    self.cancel_schedule(client.id)
                    self.update_current_plan(client.id, case)
                    self.set_basic_plan(client.id)

    def get_client_by_email(self, email):
        data = models.Client.objects.filter(
            email=email
        ).first()

        if not data:
            print("Usuário nao encontrado")
            return
        else:
            print("Usuário encontrado")
        return data

    def cancel_schedule(self, client_id):
        data = models.Schedule.objects.filter(
            client_id=client_id,
            situation=1
        )
        for item in data:
            item.cancel_origin = 1
            item.situation = 4
            item.save()

        print(f"{len(data)} Agendamentos cancelados")

    def update_current_plan(self, client_id, case):
        cancel_all_plans(
            client_id,
            self.possible_status.get(case)
        )

    def set_basic_plan(self, client_id):
        models.Subscription.objects.create(
            client_id=client_id,
            created_at=timezone.now(),
            payment_condition_id=4,  # Cortesia
            plan_id=7,  # promocao
            subscription_status_id=self.possible_status.get('active'),  # noqa Promocional
            external_payment_id="",
            value=0
        )
        print("Um plano basico associado")

    def log_error(self, text):
        self.stdout.write(self.style.ERROR(text))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def set_case(ref):
    txt = normalize(ref)

    if "cancelamento por inadimplencia" in txt:
        return "canceled_by_non_payment"

    if "solicitado pela cliente" in txt:
        return "canceled_by_client"

    return None


def is_real_email(email):
    try:
        if not email:
            return False
        if isinstance(email, float):
            if math.isnan(email):
                return False
        return True
    except Exception:
        return False
