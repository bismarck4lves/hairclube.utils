import os
from django.conf import settings
from django.core.mail import EmailMessage


class AuthenticationSMTP:
    def send_daily_report(
        self, to: str,
        files: list,
        message: str = "Segue o relatório diário"
    ):
        email = EmailMessage(
            subject="Relatório diário",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=to
        )
        for file_path in files:
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)

                with open(file_path, "rb") as f:
                    email.attach(file_name, f.read())
            else:
                print(f"⚠️ Arquivo não encontrado: {file_path}")
        return email.send()
