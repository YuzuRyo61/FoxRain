def isAPRequest(request):
    if not (request.headers.get("accept", "").startswith("application/activity+json") or request.headers.get("accept", "").startswith("application/ld+json")):  # noqa: E501
        return False
    else:
        return True


def isAPRequestContent(request):
    if not (request.META.get("CONTENT_TYPE", "").startswith("application/activity+json") or request.META.get("CONTENT_TYPE", "").startswith("application/ld+json")):  # noqa: E501
        return False
    else:
        return True
