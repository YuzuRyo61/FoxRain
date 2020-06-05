from rest_framework import routers

from api import views

router = routers.DefaultRouter()

router.register('user', views.UserViewSet)
router.register('post', views.PostViewSet)

urlpatterns = router.urls
