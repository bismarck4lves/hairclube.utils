import os
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from .utils import get_docs_file_path
import mysql.connector
from mysql.connector import Error
from ...infra.smtp import AuthenticationSMTP


class EtlUtil:
    def __init__(self):
        self.mysql_conn = self.create_mysql_connection()

    def create_mysql_connection(self):
        try:
            conn = mysql.connector.connect(
                host="hair-club-server-mgr.mysql.database.azure.com",
                user="tuahhxuiua",
                password="Mzs3$yUMMzdHsKnt",
                database="hairclubbr"
            )
            print("Connected")
            return conn
        except Error as e:
            raise Error(f"❌ Erro ao conectar ao Mysql: {e}")

    def extract(self, operation):
        cursor = self.mysql_conn.cursor(dictionary=True)
        cursor.execute(operation)
        rows = cursor.fetchall()
        return rows


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.etl_process = EtlUtil()
        smtp = AuthenticationSMTP()
        folder_date = self.get_current_date_folder()
        data = [
            "relatorio_contas",
            "relatorio_cupons",
            "relatorio_planos",
            "relatorio_saloes",
            "relatorio_usuarios",
        ]
        paths = []
        for file in data:
            path = self._create_report_file(file, file, folder_date)
            paths.append(path)

        smtp.send_daily_report(
            to=[
                "isabele.gomes@hairclubbrasil.com.br",
                "ana.kelly@hairclubbrasil.com.br",
                "brigida.rodrigues@hairclubbrasil.com.br",
                "beatrice.rodrigues@hairclubbrasil.com.br",
            ],
            files=paths,
            message="Segue o relatório diário gerado automaticamente."
        )
        print("Emails enviados com sucesso")

    def _create_report_file(self, file_sql, file_name, folder_date):
        path = get_docs_file_path(f"/report_queries/{file_sql}.sql")
        query = self.get_query(path)
        data = self.etl_process.extract(query)
        return self.export_to_excel(
            data=data,
            output_path=get_docs_file_path(f"report_email/{folder_date}"),
            file_name=f"{file_name}_{folder_date}.xlsx"
        )

    def get_query(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception(f"Arquivo SQL não encontrado: {path}")
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo SQL ({path}): {e}")

    def export_to_excel(self, data, output_path: str, file_name: str):
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, file_name)
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine="openpyxl")
        print(file_name)
        return file_path

    def get_current_date_folder(self):
        return datetime.now().strftime("%d_%m_%Y")
