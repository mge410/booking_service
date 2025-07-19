from django.contrib import admin
from django.urls import path, include

import hotels.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(hotels.urls)),
]
