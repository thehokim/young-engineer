from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Team
from .serializers import TeamSerializer

# ✅ View for listing and creating teams (GET and POST)
class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]

# ✅ View for retrieving, updating, and deleting a specific team
class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]  # ✅ Requires authentication
