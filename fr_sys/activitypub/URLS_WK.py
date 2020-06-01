"""
 for ActivityPub router (well-known)
"""

from django.urls import path

from .well_known import webfinger

urlpatterns = [
    path('webfinger', webfinger, name="WebFinger")
]
