from django.core.management.base import BaseCommand, CommandError
from getpass import getpass
from django.conf import settings
from os import path
from json import dumps

class Command(BaseCommand):
    help = "a helper scripts that helps you rapidly configure your email information"

    def print_banner(self):
        print ("[Django-Email]: an email address that Django will use to send emails to both admins and clients")
        print ("[Django-Password]: the required password to login to gmail's smtp protocol")
        print ("[Admin-Emails: list]: the emails of admins, django will send report emails to these addresses")
        print (("-"*50)+"\n")

    def handle(self, *args, **options):
        self.print_banner()
        try:
            django_email = input("enter [Dajngo-Email]: ")
            django_password = getpass("enter [Django-Password]: ")
            admin_emails = []
            print ("now add as many emails as you want, enter `q` to end the prompt")
            while (admin_email:=input("enter [Admin-Emails]: ")) != "q":
                if admin_emails: # if not empty
                    admin_emails.append(admin_email)
            with open (path.join(settings.BASE_DIR, "email.config.json"), "w") as config_file:
                config_file.write(dumps({
                    "email": django_email,
                    "password": django_password,
                    "admin_emails": admin_emails
                }, indent=4))
            print ("configuration file has been written to the root directory")
        except KeyboardInterrupt:
            print ("operation cancled")
