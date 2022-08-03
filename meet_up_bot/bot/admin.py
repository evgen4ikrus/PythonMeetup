from django.contrib import admin

from .models import Block, Speaker, Presentation, Flow

@admin.register(Block)
class ComplaintAdmin(admin.ModelAdmin):
    pass


@admin.register(Speaker)
class ComplaintAdmin(admin.ModelAdmin):
    pass


@admin.register(Presentation)
class ComplaintAdmin(admin.ModelAdmin):
    pass


@admin.register(Flow)
class ComplaintAdmin(admin.ModelAdmin):
    pass

