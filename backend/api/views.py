from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
import numpy as np


@csrf_exempt
def recognize(request):
    print(request.session)
    original_img = request.FILES.get("img")
    if original_img is None:
        return JsonResponse(
            status=400,
            data={
                "message": "Please send FILE at key `img`",
            },
        )
    img = Image.open(BytesIO(original_img.read()))
    img = img.resize((28, 28)).convert("L")
    img = Image.fromarray(255 - np.array(img))
    img.save("output.png")

    return JsonResponse(
        status=200,
        data={
            "message": "Hello, World",
        },
    )
