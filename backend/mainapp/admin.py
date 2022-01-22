from django.contrib import admin
from .models import Page, Video, Audio, Text

# admin.site.register(Page)
# admin.site.register(Video)
# admin.site.register(Audio)
# admin.site.register(Text)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    pass

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass
