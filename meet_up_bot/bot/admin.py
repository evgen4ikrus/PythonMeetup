from django.contrib import admin
from .models import Block, Speaker, Presentation, Flow, Flow_group


@admin.register(Block)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time']
    list_editable = ['start_time', 'end_time']


@admin.register(Speaker)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_title']


@admin.register(Presentation)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'block']


@admin.register(Flow)
class ComplaintAdmin(admin.ModelAdmin):
    pass


@admin.register(Flow_group)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'flow', 'start_time', 'end_time']
    list_editable = ['start_time', 'end_time']
