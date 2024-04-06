from io import BytesIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from PIL import Image
import numpy as np
import torch

from .cnn import cnn_model


class RecognizeAPIView(APIView):
    def post(self, request):
        original_img = request.data.get("img")
        if original_img is None:
            raise ParseError(
                code="invalid_img",
                detail="Invalid image",
            )
        img = Image.open(BytesIO(original_img.read()))
        img = img.resize((28, 28)).convert("L")
        img = Image.fromarray(255 - np.array(img))

        img_features = np.array(img, dtype=np.float32) / 255
        img_features = torch.from_numpy(img_features)
        img_features = img_features.unsqueeze(0).unsqueeze(0)

        with torch.no_grad():
            outputs = cnn_model(img_features)

        # Get the predicted class
        predicted_class = torch.argmax(outputs, dim=1).item()

        return Response(
            data={
                "digit": predicted_class,
            }
        )
