from django.contrib import admin
from django.urls import path
from .views import TeamListCreateView, TeamDetailView

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Admin panel
    path('teams/create/', TeamListCreateView.as_view(), name="team-list-create"),  # ✅ GET (list) & POST (create)
    path('teams/<int:pk>/', TeamDetailView.as_view(), name="team-detail"),  # ✅ GET, PUT, PATCH, DELETE
]
