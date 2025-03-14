from rest_framework import serializers
from .models import Team, TeamMember, Project
from .telegram import send_telegram_message, upload_file_to_telegram
import json

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['full_name', 'birth_date', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'technical_specs', 'additional_info']

class TeamSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=False)
    members = serializers.CharField(write_only=True)
    project = serializers.CharField(write_only=True)

    class Meta:
        model = Team
        fields = "__all__"

    def create(self, validated_data):
        members_data = json.loads(validated_data.pop("members"))
        project_data = json.loads(validated_data.pop("project"))
        video_file = validated_data.pop("video", None)

        # Create team instance
        team = Team.objects.create(**validated_data)

        # Create team members
        for member in members_data:
            TeamMember.objects.create(team=team, **member)

        # Create project
        Project.objects.create(team=team, **project_data)

        # Upload video to Telegram and get file_id
        file_id = None
        if video_file:
            file_id = upload_file_to_telegram(video_file)
            if file_id:
                team.video = file_id  # Store file_id if field exists
                team.save()

        # Send team info to Telegram
        try:
            send_telegram_message({
                "name": team.name,
                "city": team.city,
                "institution": team.institution,
                "contact_info": team.contact_info,
                "members": members_data,
                "project": project_data
            })
        except Exception as e:
            print(f"⚠️ Error sending to Telegram: {e}")

        return team