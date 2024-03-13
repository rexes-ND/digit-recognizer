import os
import zipfile

from django.conf import settings
from django.core.management.base import BaseCommand
from kaggle.api.kaggle_api_extended import KaggleApi


class Command(BaseCommand):
    help = "Downloads the digit-recognizer data from Kaggle"

    def handle(self, *args, **options):
        try:
            # https://www.kaggle.com/competitions/digit-recognizer
            competition = "digit-recognizer"
            data_path = f"{settings.BASE_DIR}/data"

            api = KaggleApi()
            api.authenticate()
            api.competition_download_files(
                competition=competition,
                path=data_path,
                force=False,
                quiet=False,
            )

            if os.path.exists(f"{data_path}/{competition}.zip"):
                with zipfile.ZipFile(f"{data_path}/{competition}.zip", "r") as zip_ref:
                    zip_ref.extractall(f"{data_path}")
                os.remove(f"{data_path}/{competition}.zip")

            self.stdout.write(self.style.SUCCESS("Successfully downloaded the data"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Something went wrong: {e}"))
