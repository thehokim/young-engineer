from django.contrib import admin
from django.utils.html import format_html
from .models import Team, TeamMember, Project, BotSettings

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'institution', 'contact_info', 'video_link')  # ✅ Ссылка вместо видео
    inlines = [TeamMemberInline]
    readonly_fields = ('video_link',)  # ✅ Поле для ссылки на видео

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">🎥 Посмотреть видео</a>', obj.video.url)
        return "Нет видео"
    
    video_link.short_description = "Видео"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "bot_token")
