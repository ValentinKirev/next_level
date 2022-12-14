from django.contrib import admin

from next_level.common.models import Rating, Comment, Like


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'rating')

    search_fields = ('game__title', 'user__username')

    ordering = ('-id', '-rating')

    list_filter = ('rating', 'user')

    fieldsets = (
        (None, {
            'fields': ('game', 'rating')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user

        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_news_post', 'publication_date_and_time', 'updated_on', 'author', 'text')

    search_fields = ('to_news_post__title', 'author__username')

    ordering = ('-id', '-publication_date_and_time', '-updated_on')

    list_filter = ('publication_date_and_time', 'updated_on', 'author', 'to_news_post')

    fieldsets = (
        (None, {
            'fields': ('text', 'to_news_post')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_guide_post', 'to_news_post', 'author')

    search_fields = ('to_guide_post__title', 'to_news_post__title', 'author__username',)

    ordering = ('-id',)

    list_filter = ('to_guide_post', 'to_news_post', 'author')

    fieldsets = (
        (None, {
            'fields': ('to_guide_post', 'to_news_post')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)