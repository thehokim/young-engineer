from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название команды")
    city = models.CharField(max_length=255, verbose_name="Город/Регион")
    institution = models.CharField(max_length=255, verbose_name="Учебное заведение")
    contact_info = models.TextField(verbose_name="Контактная информация")

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    role = models.CharField(max_length=255, verbose_name="Роль в команде")

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Project(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="project")
    name = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Краткое описание проекта")
    technical_specs = models.TextField(verbose_name="Технические характеристики", blank=True, null=True)
    additional_info = models.TextField(verbose_name="Дополнительная информация", blank=True, null=True)

    def __str__(self):
        return self.name
