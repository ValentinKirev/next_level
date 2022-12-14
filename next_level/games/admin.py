from django.contrib import admin
from next_level.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'developer', 'release_date', 'status', 'average_rating',
                    'publication_date_and_time', 'updated_on', 'slug', 'author', 'max_level', 'official_website',
                    'trailer', 'type')

    search_fields = ('title', 'author__username')

    ordering = ('-id', '-release_date', '-publication_date_and_time', '-updated_on', '-max_level', '-average_rating')

    list_filter = ('publication_date_and_time', 'updated_on', 'max_level', 'status', 'average_rating', 'author')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'developer', 'release_date', 'max_level',
                       'type', 'status')
        }),
        ('Media files and urls', {
            'fields': ('image', 'trailer', 'official_website'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)

