from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
import numpy as np
import torch

from .cnn import cnn_model


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

    img_features = np.array(img, dtype=np.float32) / 255
    img_features = torch.from_numpy(img_features)
    img_features = img_features.unsqueeze(0).unsqueeze(0)

    # print(img_features)
    # print(img_features.shape)
    with torch.no_grad():
        outputs = cnn_model(img_features)

    # Get the predicted class
    predicted_class = torch.argmax(outputs, dim=1).item()

    # Print the predicted class
    print("Predicted class:", predicted_class)

    return JsonResponse(
        status=200,
        data={
            "message": "Hello, World",
        },
    )
