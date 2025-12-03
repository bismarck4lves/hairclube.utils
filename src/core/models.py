from django.db import models


class Client(models.Model):
    id = models.AutoField(
        db_column="Id",
        primary_key=True
    )
    name = models.TextField(
        db_column="Nome"
    )
    cpf = models.TextField(
        db_column="Cpf"
    )
    phone = models.TextField(
        db_column="Telefone"
    )
    email = models.TextField(
        db_column="Email"
    )
    password = models.TextField(
        db_column="Senha"
    )
    ibge = models.IntegerField(
        db_column="Fk_CidadesIBGE"
    )
    active = models.IntegerField(
        db_column="Ativo"
    )

    class Meta:
        db_table = "cadclientes"
        managed = False


class Schedule(models.Model):

    id = models.AutoField(
        primary_key=True,
        db_column="Id"
    )
    client_id = models.IntegerField(
        db_column="Fk_CadClientes",
    )
    plan = models.IntegerField(
        db_column="Fk_CadPlanos"
    )
    salon_service_user_id = models.IntegerField(
        db_column="Fk_CadEstabelecimentoServicosUsuarios",
    )
    date_hour = models.DateTimeField(
        db_column="DataHora"
    )
    re_schedule = models.DateTimeField(
        db_column="DataReagendamento"
    )
    schedule = models.DateTimeField(
        db_column="DataAgendamento"
    )
    cancel_origin = models.IntegerField(
        db_column="OrigemCancelamento"
    )
    situation = models.IntegerField(
        db_column="Situacao"
    )

    class Meta:
        db_table = "MovCadClientesConsumo"
        managed = False


class Subscription(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="Id"
    )

    client_id = models.IntegerField(
        db_column="Fk_CadClientes"
    )

    plan_id = models.IntegerField(
        db_column="Fk_CadPlanos"
    )

    payment_condition_id = models.IntegerField(
        db_column="Fk_CadCondPagto"
    )

    subscription_status_id = models.IntegerField(
        null=True,
        blank=True,
        db_column="Fk_CadSituacaoAssinaturas"
    )

    created_at = models.DateTimeField(
        null=True,
        blank=True,
        db_column="DataHora"
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        db_column="Valor"
    )

    external_payment_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="IdPagamentoExterno"
    )

    subscription_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="SubscriptionId"
    )

    cancellation_date = models.DateTimeField(
        null=True,
        blank=True,
        db_column="DataCancelamento"
    )

    class Meta:
        db_table = "MovCadClientesAssinaturas"
        managed = False


class SalonUser(models.Model):

    id = models.AutoField(
        primary_key=True,
        db_column="Id"
    )
    email = models.TextField(
        db_column="Email"
    )
    password = models.TextField(
        db_column="Senha"
    )
    cpf = models.TextField(
        db_column="Cpf"
    )

    class Meta:
        db_table = "CadEstabelecimentoUsuarios"
        managed = False


class Plan(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column="Id"
    )
    active = models.IntegerField(
        db_column="Ativo"
    )
    name = models.TextField(
        db_column="Nome"
    )
    cycles = models.IntegerField(
        db_column="Ciclo"
    )
    value = models.DecimalField(
        db_column="Valor",
        decimal_places=2,
        max_digits=10
    )

    class Meta:
        db_table = "cadplanos"
        managed = False
