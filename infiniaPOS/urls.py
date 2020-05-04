from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('api_v1/', include('api_v1.database_api.urls')),
    path('api_v1/', include('api_v1.sale_api.urls')),
    path('api_v1/', include('api_v1.employee_api.urls')),
    path('api_v1/', include('api_v1.payment_api.urls')),
    path('api_v1/', include('api_v1.inventory_api.urls')),
    path('api_v1/', include('api_v1.analytics_api.urls')),
    path('api_v1/', include('sale.urls'))



]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

