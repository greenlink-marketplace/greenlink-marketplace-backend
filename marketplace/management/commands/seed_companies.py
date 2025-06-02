from django.core.management.base import BaseCommand
from accounts.models import User
from marketplace.models import Company
from faker import Faker
from validate_docbr import CNPJ
import secrets
import string

fake = Faker("pt_BR")
cnpj = CNPJ()

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

class Command(BaseCommand):
    help = 'Populates the database with dummy data for Company'

    def handle(self, *args, **kwargs):
        # Create fictitious companies
        for _ in range(10):
            username_company = fake.company()
            while User.objects.filter(username=username_company).exists():
                username_company = fake.user_name()
            email_company = fake.email()
            while User.objects.filter(email=email_company).exists():
                email_company = fake.email()

            user_obj = User.objects.create_user(
                username=username_company,
                email=email_company,
                password=generate_password(),
                role=User.UserRole.COMPANY
            )
            cnpj_company = cnpj.generate(mask=True)
            while Company.objects.filter(cnpj=cnpj_company).exists():
                cnpj_company = fake.email()
            
            Company.objects.create(
                user=user_obj,
                cnpj=cnpj_company,
                phone=fake.numerify('(##)9####-####'),
                address=fake.address()
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Database populated with fictitious companies."
            )
        )
