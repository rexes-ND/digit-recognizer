from django.core.management.base import BaseCommand, CommandParser

import pandas as pd
import numpy as np
from PIL import Image


class Command(BaseCommand):
    help = "Convert csv row to image"

    def add_arguments(self, parser: CommandParser):
        (
            parser.add_argument(
                "--csv_file_path",
                type=str,
                help="Path to CSV file",
                required=True,
            ),
        )
        parser.add_argument(
            "--row_number",
            type=int,
            help="Row number in the CSV file",
            required=True,
        )

    def handle(self, *args, **options):
        try:
            csv_file_path = options["csv_file_path"]
            row_number = options["row_number"]
            df = pd.read_csv(csv_file_path)
            row = df.iloc[row_number - 1]
            print(f"digit: {row['label']}")
            row_pixels = np.array([row[f"pixel{i}"] for i in range(784)])
            image = Image.new("L", size=(28, 28))
            image.putdata(row_pixels)
            image.save("output.png")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully convert row number {row_number} to PNG image"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Something went wrong: {e}"))
