from django.contrib import admin
from django.utils.safestring import mark_safe

from core.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'get_image')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'description')
    list_filter = ('date', )

    @admin.display(description='Обложка')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')