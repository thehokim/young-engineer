from rest_framework import serializers
from .models import Team, TeamMember, Project
from .telegram import send_telegram_message, upload_video_to_telegram

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['full_name', 'birth_date', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'technical_specs', 'additional_info']

class TeamSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=False)  # ✅ Видео как файл (но сохранять будем ссылку)
    members = TeamMemberSerializer(many=True)
    project = ProjectSerializer()

    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        project_data = validated_data.pop('project')
        video_file = validated_data.pop('video', None)  # ✅ Получаем видео

        team = Team.objects.create(**validated_data)

        for member in members_data:
            TeamMember.objects.create(team=team, **member)

        project = Project.objects.create(team=team, **project_data)

        # ✅ Загружаем видео в Telegram и получаем ссылку
        video_url = None
        if video_file:
            video_url = upload_video_to_telegram(video_file)

        # ✅ Отправляем сообщение в Telegram
        try:
            send_telegram_message({
                "name": team.name,
                "city": team.city,
                "institution": team.institution,
                "contact_info": team.contact_info,
                "members": members_data,
                "project": project_data
            }, video_url)
        except Exception as e:
            print(f"⚠️ Ошибка при отправке в Telegram: {e}")

        # ✅ Сохраняем в базе не сам файл, а ссылку на видео
        if video_url:
            team.video = video_url
            team.save()

        return team
