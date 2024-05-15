import base64

from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from .tasks import classify


class RecognizeAPIView(APIView):
    def post(self, request):
        print(f"Session: {request.session}")
        session_id = request.session.get("id")

        img = request.data.get("img")
        if img is None:
            raise ParseError(
                code="invalid_img",
                detail="Invalid image",
            )

        img_str: str = base64.b64encode(img.read()).decode()
        async_result: AsyncResult = classify.delay(img_str, session_id)
        predicted_class = async_result.get()

        return Response(
            data={
                "digit": predicted_class,
            }
        )
