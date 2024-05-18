import base64
from io import BytesIO
from time import sleep

import torch
import numpy as np
from PIL import Image
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from .cnn import cnn_model


@shared_task(bind=True)
def classify(self, img_str: str, session_id: int):
    task_id: str = str(self.request.id)

    channel_layer = get_channel_layer()
    task_group_name = f"group_{task_id}"

    sleep(1)
    async_to_sync(channel_layer.group_send)(
        task_group_name,
        {
            "type": "digit.progress",
            "code": "STARTED",
            "data": None,
        },
    )

    img = Image.open(BytesIO(base64.b64decode(img_str)))
    img = img.resize((28, 28)).convert("L")
    img = Image.fromarray(255 - np.array(img))

    sleep(1)
    async_to_sync(channel_layer.group_send)(
        task_group_name,
        {
            "type": "digit.progress",
            "code": "IMAGE_PROCESSED",
            "data": None,
        },
    )

    img_features = np.array(img, dtype=np.float32) / 255
    img_features = torch.from_numpy(img_features)
    img_features = img_features.unsqueeze(0).unsqueeze(0)

    sleep(1)
    async_to_sync(channel_layer.group_send)(
        task_group_name,
        {
            "type": "digit.progress",
            "code": "IMAGE_FEATURE_EXTRACTED",
            "data": None,
        },
    )

    with torch.no_grad():
        outputs = cnn_model(img_features)

    sleep(1)
    # Get the predicted class
    predicted_class = torch.argmax(outputs, dim=1).item()
    async_to_sync(channel_layer.group_send)(
        task_group_name,
        {
            "type": "digit.progress",
            "code": "FINISHED",
            "data": predicted_class,
        },
    )
    return int(predicted_class)
