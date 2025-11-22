from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from core import models
from django.utils import timezone
from .utils import cancel_all_plans, read_csv_file, chose_file,  get_file_name
from ...utils.auth import encode


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options):
        path = chose_file("create_mkt_users")
        file_name = get_file_name(path)

        confirm = input(f"confirma acao para o arquivo {file_name} [S/N]")
        if confirm == "s":
            data = read_csv_file(path)
            for item in data:
                client = self.create_client(item)
                self.assign_plan(client.id)

    def create_client(self, item):
        email = item['EMAIL']
        current = models.Client.objects.filter(
            email=email
        ).first()
        if current:
            print(f"USUARIO DE EMAIL {email} JA EXISTE")
            return current
        data = models.Client.objects.create(
            name=item['NOME'],
            cpf=item['CPF'],
            email=email,
            password=encode(item['CPF']),
            ibge=1194,
            active=1
        )
        print(f"USARIO DE EMAIL {email} CRIADO")
        return data

    def assign_plan(self, client_id):
        cancel_all_plans(client_id, 7)
        models.Subscription.objects.create(
            client_id=client_id,
            created_at=timezone.now(),
            payment_condition_id=4,  # Cortesia
            plan_id=16,  # Beleza Essencial
            subscription_status_id= 6,  # noqa Promocional
            external_payment_id="",
            value=0
        )
        print("PLANO PROMOCIONAL ATRIBUIDO")