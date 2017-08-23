from django.conf.urls import url, include
from rest_framework import routers
from channels import views

router = routers.DefaultRouter()
router.register(r'^channels', views.ChannelViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^categories', views.CategoriesViewSet.as_view({'get': 'list'})),
    url(r'^relatives', views.RelativesViewSet.as_view()),
]
