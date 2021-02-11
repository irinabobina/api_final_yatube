from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'),
        name='redoc'),
    #  Логин и логаут для более удобной работы с browsable API
    path('api-auth/', include('rest_framework.urls'))
]
