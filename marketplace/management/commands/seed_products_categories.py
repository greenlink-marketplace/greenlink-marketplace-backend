from django.core.management.base import BaseCommand
from marketplace.models import ProductCategory
from faker import Faker

faker = Faker("pt_BR")

class Command(BaseCommand):
    help = 'Populates the database with dummy data for ProductCategory'

    def handle(self, *args, **kwargs):
        # Create categories with descriptions
        names_categories = [
            "Móveis", "Eletrônicos",
            "Roupas", "Livros",
            "Plásticos"
        ]

        for name_category in names_categories:
            if ProductCategory.objects.filter(
                        name=name_category
                    ).exists():
                continue
            ProductCategory.objects.create(
                name=name_category,
                description=faker.sentence(nb_words=8)
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Database populated with fictitious products categories."
            )
        )
