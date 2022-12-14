from django.contrib import admin

from next_level.guides.models import GuidePost, GuideCategory


@admin.register(GuideCategory)
class GuideCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'publication_date_and_time', 'updated_on', 'to_game', 'slug', 'author')

    search_fields = ('title', 'to_game__title', 'author__username')

    ordering = ('-id', '-publication_date_and_time', '-updated_on')

    list_filter = ('publication_date_and_time', 'updated_on', 'to_game', 'author')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'to_game')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)


@admin.register(GuidePost)
class GuidePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'publication_date_and_time', 'updated_on',
                    'to_category', 'slug', 'author')

    search_fields = ('title', 'to_category__title', 'author__username')

    ordering = ('-id', '-publication_date_and_time', '-updated_on')

    list_filter = ('publication_date_and_time', 'updated_on', 'to_category', 'author')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'to_category')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)