from django.conf import settings


def endpoint(request):
    return {"FR_ENDPOINT": settings.FR_ENDPOINT}
