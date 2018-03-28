from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('tasks.urls'))
] + static_url + media_url
