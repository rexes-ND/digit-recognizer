from io import BytesIO
import base64

import torch
import numpy as np
from PIL import Image
from celery import shared_task
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


from .cnn import cnn_model


@shared_task
def classify(img_str: str, session_id: int):
    # channel_layer = get_channel_layer()
    img = Image.open(BytesIO(base64.b64decode(img_str)))
    img = img.resize((28, 28)).convert("L")
    img = Image.fromarray(255 - np.array(img))

    img_features = np.array(img, dtype=np.float32) / 255
    img_features = torch.from_numpy(img_features)
    img_features = img_features.unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        outputs = cnn_model(img_features)

    # Get the predicted class
    predicted_class = torch.argmax(outputs, dim=1).item()
    # async_to_sync(channel_layer.group_send)(
    #     session_id,
    #     {
    #         "type": "recognize.progress",
    #         "message": "done",
    #     },
    # )
    return int(predicted_class)
