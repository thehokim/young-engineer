from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Admin panel
    path('api/', include('application_form.urls')),  # ✅ Includes API routes
]
