from django.contrib import admin
from .models import Team, TeamMember, Project

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'institution', 'contact_info')
    inlines = [TeamMemberInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
