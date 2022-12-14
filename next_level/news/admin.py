from django.contrib import admin

from next_level.news.models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'subtitle', 'publication_date_and_time', 'updated_on',
                    'slug', 'author', 'image', 'link_to_video')

    search_fields = ('title', 'author__username')

    ordering = ('-id', '-publication_date_and_time', '-updated_on')

    list_filter = ('publication_date_and_time', 'updated_on', 'author')

    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Media files and urls', {
            'fields': ('image', 'link_to_video'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)
