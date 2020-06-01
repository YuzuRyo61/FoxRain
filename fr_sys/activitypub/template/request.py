def isAPRequest(request):
    if not (request.headers.get("accept", "").startswith("application/activity+json") or request.headers.get("accept", "").startswith("application/ld+json")):
        return False
    else:
        return True
