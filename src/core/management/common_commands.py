class CommonComands:

    def log_error(self, text):
        self.stdout.write(self.style.ERROR(text))

    def log_success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def log_warning(self, text):
        self.stdout.write(self.style.WARNING(text))

    def log_info(self, text):
        self.stdout.write(self.style.NOTICE(text))
