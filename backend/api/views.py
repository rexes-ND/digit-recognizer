from django.http import JsonResponse


def recognize(request):
    print(request.session)
    return JsonResponse(
        data={
            "status": True,
            "message": "Hello, World",
        }
    )
