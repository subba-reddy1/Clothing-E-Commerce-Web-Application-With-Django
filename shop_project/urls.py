from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Manager/Admin Routes (Go to adminApp)
    path('manager/', include('adminApp.urls')),

    # 2. Customer Routes (Go to usersApp)
    path('', include('usersApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)