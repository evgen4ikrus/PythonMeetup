from django.contrib import admin

from .models import Block, Speaker, Presentation, Flow, Flow_group

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


@admin.register(Flow_group)
class ComplaintAdmin(admin.ModelAdmin):
    pass
