from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('app.urls')),
#    path('register/', include('app.urls')),
#   path('login/', include('app.urls')),
#  path('dashboard/', include('app.urls')),
   # path('', include('app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
