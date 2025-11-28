from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from core import models
from tabulate import tabulate
from .utils import cancel_all_plans

CANCELED_STATUS = 10
UPGRADE_STATUS = 1


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options):
        email = str(input("Informe o email: "))
        client = models.Client.objects.filter(
            email=email
        ).first()
        self.upgrade_plan(client.id)

    def upgrade_plan(self, client_id):
        current = models.Subscription.objects.filter(
            client_id=client_id,
            cancellation_date__isnull=True
        ).first()
        plans = models.Plan.objects.filter(active=1)
        current_plan = plans.filter(id=current.plan_id).first()
        available_plans = plans.filter(cycles=current_plan.cycles)

        self.describe_plan(current_plan)
        self.show_plans_options(available_plans)

        plan_id = int(input("SELECT PLAN ID:  "))

        selected_plan = plans.filter(id=plan_id).first()

        if not selected_plan:
            self.stdout.write(
                self.style.ERROR("SELECTED PLAN NOT FOUND")
            )
            return

        cancel_all_plans(client_id, CANCELED_STATUS)

        self.create_new_plan(client_id, current, selected_plan)

    def create_new_plan(self, client_id, current, selected_plan):
        models.Subscription.objects.create(
            client_id=client_id,
            created_at=current.created_at,
            payment_condition_id=current.payment_condition_id,
            plan_id=selected_plan.id,
            subscription_status_id=UPGRADE_STATUS,
            external_payment_id="",
            value=selected_plan.value
        )
        self.stdout.write(
            self.style.SUCCESS("UPGRADE SUCCESSFUL")
        )

    def describe_plan(self, plan):
        desc = f"{plan.id} - {plan.name} ({plan.cycles}) price R${plan.value}"
        print(f"CURRENT PLAN: {desc}")
        print("\n")

    def show_plans_options(self, plans):
        self.stdout.write(self.style.NOTICE("AVAILABLE PLANS"))
        headers = ["ID", "Name", "Cycles", "Price"]
        data = []
        for plan in plans:
            data.append([
                plan.id,
                plan.name,
                plan.cycles,
                plan.value
            ])
        table = tabulate(data, headers, tablefmt="psql")
        self.stdout.write(table)
