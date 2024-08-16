import json

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed Database with starting data using fixture file"

    def add_arguments(self, parser):
        # Optional arquments
        parser.add_argument(
            "-m",
            "--model",
            type=str,
            help="Model to populate: '<app_name>.<model_name>'",
        )
        parser.add_argument("-f", "--file", type=str, help="Fixture file path")

    def handle(self, *args, **kwargs):
        self.stdout.write("running...")
        model = kwargs.get("model")
        file = kwargs.get("file")

        if model and file:
            Model = apps.get_model(model)
            # model_name = Model.__name__
            failed_count = 0
            with open(file, "r", encoding="utf8") as f:
                data = json.loads(f.read())
                for item in data:
                    try:
                        Model.objects.create(**item)
                    except Exception:
                        failed_count += 1

            succesful_count = len(data) - failed_count
            self.stdout.write(
                f"{Model.__name__} updated with {succesful_count} records. {failed_count} Failed"
            )

        else:
            self.stdout.write(self.style.WARNING("Please provide model and file path"))
