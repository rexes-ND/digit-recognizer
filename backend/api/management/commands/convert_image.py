from django.core.management.base import BaseCommand

from PIL import Image
import numpy as np


class Command(BaseCommand):
    help = "Convert image from frontend to correct format"

    def handle(self, *args, **options):
        try:
            image = Image.open("test.png")
            resized_image = image.resize((28, 28))
            grayscale_image = resized_image.convert("L")
            inverted_image = Image.fromarray(255 - np.array(grayscale_image))
            inverted_image.save("inverted_image.png")
            self.stdout.write(self.style.SUCCESS("Successfully transformed the image"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Something went wrong: {e}"))
