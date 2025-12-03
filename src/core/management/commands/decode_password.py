from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from core import models
from ...utils.auth import decode
import re


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options):

        username = "JANNA_S.R@HOTMAIL.COM" #input("Digite o nome de usuario: ").strip()

        usernames = [username]

        for username in usernames:
            context = 1

            type = self.username_type(username)
          
            # if type == "invalid":
            #     return "Tipo de usuario nao reconhecido"

            password = ""
            if context == 1:
                password = self.get_user_salon(username, type)
                if not password:
                    print("USUARIO NAO ENCONTRADO")
                    return
                print(password)
            # if context == 2:
            #     password = self.get_user_clint(username, type)
            #     if not password:
            #         print("USUARIO NAO ENCONTRADO")
            #         return

            print(f"username: {username}")
            print(f"username: {decode(password)}")
            # print("="* 20)

    def get_user_salon(self, username, type):
        user = None

        if type == "email":
            user = models.SalonUser.objects.filter(email=username).first()
            print(user)
        if type == "cpf":
            user = models.SalonUser.objects.filter(cpf=username)

        return user.password

    def get_user_clint(self, username, type):
        user = None

        if type == "email":
            user = models.Client.objects.filter(email=username).first()

        if type == "cpf":
            user = models.Client.objects.filter(cpf=username)
        return user.password

    def username_type(self, username: str) -> str:
        if not username:
            return "invalid"

        username = username.strip()

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(email_regex, username):
            return "email"

        numbers = re.sub(r"\D", "", username)

        if len(numbers) == 11:
            return "cpf"

        return "invalid"
