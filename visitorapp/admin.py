from django.contrib import admin

from django.contrib import admin

from .models import Wall, Visitor, Inscription

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ["wall", "moderation_status", "text", "signature"]
    ordering = ["wall", "moderation_status", "created_date"]


admin.site.register(Wall)
admin.site.register(Visitor)
admin.site.register(Inscription, InscriptionAdmin)


