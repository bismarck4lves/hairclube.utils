import os
import pandas as pd
from datetime import datetime
from django.db import connection
from core.management.commands.utils import get_docs_file_path
from core.management.common_commands import CommonComands
from core.infra.smtp import AuthenticationSMTP
from django.core.management.base import BaseCommand


class EmailReportHandler(
    BaseCommand,
    CommonComands
):

    def exec_handle(self):
        self.log_info("EMAIL STEP(1/3) INCIANDO Envio de email")
        folder_date = self.get_current_date_folder()
        data = [
            "relatorio_contas",
            "relatorio_cupons",
            "relatorio_planos",
            "relatorio_saloes",
            "relatorio_usuarios",
            "relatorio_cancelamentos_agendados"
        ]
        paths = []
        self.log_info("EMAIL STEP(2/3) AQUIVOS PROCESSADOS")
        for file in data:
            path = self._create_report_file(file, file, folder_date)
            paths.append(path)

        AuthenticationSMTP().send_daily_report(
            to=[
                "bismarckalvess@gmail.com",
                "isabele.gomes@hairclubbrasil.com.br",
                "ana.kelly@hairclubbrasil.com.br",
                "brigida.rodrigues@hairclubbrasil.com.br",
                "beatrice.rodrigues@hairclubbrasil.com.br",
            ],
            files=paths,
            message="Segue o relatório diário gerado automaticamente."
        )
        self.log_info("EMAIL STEP(3/3) EMAILS ENVIADOS COM SUCESSO")

    def _create_report_file(self, file_sql, file_name, folder_date):
        path = get_docs_file_path(f"/report_queries/{file_sql}.sql")
        query = self.load_query_on_sql_file(path)
        data = self.extract_db_data_from_query(query)
        return self.export_to_excel(
            data=data,
            output_path=get_docs_file_path(f"report_email/{folder_date}"),
            file_name=f"{file_name}_{folder_date}.xlsx"
        )

    def load_query_on_sql_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo SQL não encontrado: {path}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(f"Erro ao ler arquivo SQL ({path}): {e}")

    def extract_db_data_from_query(self, query):

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def export_to_excel(self, data, output_path: str, file_name: str):
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, file_name)
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine="openpyxl")
        print(file_name)
        return file_path

    def get_current_date_folder(self):
        return datetime.now().strftime("%d_%m_%Y")
