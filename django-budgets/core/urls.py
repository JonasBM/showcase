from django.urls import path, include

from core.helpers.admin import user_admin_site

urlpatterns = [
    path('doc/', include('django.contrib.admindocs.urls')),
    path('', user_admin_site.urls),
]
